import io
import json
import uuid
import hashlib
import asyncio

import pandas as pd
import pdfplumber
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from normalizer import normalize_dataframe
from column_profiler import profile_columns
from filter_engine import apply_filters

app = FastAPI()

# ── In-memory store (keyed by session id) ──
store: dict = {}          # sid → {"df": DataFrame, "filename": str}
share_store: dict = {}    # share id → share data

MAX_PREVIEW_ROWS = 500
MAX_SHEET_NAME   = 31


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ext(filename: str) -> str:
    return ("." + filename.rsplit(".", 1)[-1].lower()) if "." in filename else ""


def _read_file(content: bytes, filename: str) -> pd.DataFrame:
    ext = _ext(filename)
    if ext == ".csv":
        return pd.read_csv(io.BytesIO(content))
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(io.BytesIO(content))
    if ext == ".pdf":
        rows, headers = [], None
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    if headers is None:
                        headers = table[0]
                        rows.extend(table[1:])
                    else:
                        rows.extend(table[1:])
        if not rows:
            raise ValueError("No tables found in PDF.")
        return pd.DataFrame(rows, columns=headers)
    raise ValueError(f"Unsupported file type: {ext}")


def _serialize(df: pd.DataFrame) -> pd.DataFrame:
    """Convert non-JSON-serializable types to strings."""
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")
        else:
            df[col] = df[col].apply(
                lambda x: x.strftime("%Y-%m-%d") if hasattr(x, "strftime") else x
            )
    return df


def _export_cols(df: pd.DataFrame) -> list:
    """Return only original (non-normalized) columns."""
    return [c for c in df.columns if not c.startswith("_norm_")]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html") as f:
        return f.read()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file, normalize it, profile its columns.
    Returns a session id + column profiles.
    """
    try:
        content = await file.read()
        df = await asyncio.to_thread(_read_file, content, file.filename or "")
        df.columns = [str(c).strip() for c in df.columns]
        df = await asyncio.to_thread(normalize_dataframe, df)

        sid = str(uuid.uuid4())[:12]
        store[sid] = {"df": df, "filename": file.filename or "upload"}

        profile = await asyncio.to_thread(profile_columns, df)

        return JSONResponse({
            "sid": sid,
            "filename": file.filename,
            "total_rows": len(df),
            "total_cols": len([c for c in df.columns if not c.startswith("_norm_")]),
            "columns": profile,
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/columns")
async def get_columns(file: UploadFile = File(...)):
    """Get column names from uploaded file."""
    try:
        content = await file.read()
        df = await asyncio.to_thread(_read_file, content, file.filename or "")
        df.columns = [str(c).strip() for c in df.columns]
        cols = [c for c in df.columns if not c.startswith("_norm_")]
        return JSONResponse({"columns": cols})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/summary")
async def get_summary(file: UploadFile = File(...)):
    """Get file summary with column statistics."""
    try:
        content = await file.read()
        df = await asyncio.to_thread(_read_file, content, file.filename or "")
        df.columns = [str(c).strip() for c in df.columns]
        df = await asyncio.to_thread(normalize_dataframe, df)
        
        cols_info = []
        for col in df.columns:
            if col.startswith("_norm_"):
                continue
            series = df[col].dropna()
            top_vals = series.value_counts().head(3).index.tolist() if len(series) > 0 else []
            cols_info.append({
                "name": col,
                "type": str(df[col].dtype),
                "unique": int(series.nunique()),
                "nulls": int(df[col].isna().sum()),
                "top_values": [str(v) for v in top_vals]
            })
        
        return JSONResponse({
            "total_rows": len(df),
            "total_cols": len([c for c in df.columns if not c.startswith("_norm_")]),
            "columns": cols_info
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/filter")
async def filter_data(
    file: UploadFile = File(...),
    query: str = Form(...),
    clean: str = Form("false"),
    download: str = Form("0"),
    export_format: str = Form("csv")
):
    """
    Apply natural language filter to an uploaded file.
    Accepts FormData with file + query string.
    """
    try:
        from query_parser import parse_query
        
        # Read and normalize file
        content = await file.read()
        df = await asyncio.to_thread(_read_file, content, file.filename or "")
        df.columns = [str(c).strip() for c in df.columns]
        df = await asyncio.to_thread(normalize_dataframe, df)
        
        # Parse query into structured rules
        all_cols = list(df.columns)
        rules, logic = await asyncio.to_thread(parse_query, query, all_cols)
        
        # Apply filters
        result = await asyncio.to_thread(apply_filters, df, rules, logic)
        
        # Clean data if requested
        if clean.lower() == "true":
            result = result.drop_duplicates()
            for col in result.select_dtypes(include="object").columns:
                if not col.startswith("_norm_"):
                    result[col] = result[col].astype(str).str.strip()
        
        # Strip internal norm columns for output
        out_cols = _export_cols(result)
        result_out = _serialize(result[out_cols].copy())
        
        # Export if requested
        if download == "1":
            if export_format == "xlsx":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    result_out.to_excel(writer, index=False, sheet_name="Filtered")
                    ws = writer.sheets["Filtered"]
                    hdr_fmt = writer.book.add_format({
                        "bold": True, "bg_color": "#111118",
                        "font_color": "#c8ff57", "border": 1,
                    })
                    for i, col in enumerate(result_out.columns):
                        ws.write(0, i, col, hdr_fmt)
                        w = max(len(str(col)),
                                result_out[col].astype(str).str.len().max() if len(result_out) else len(col)) + 2
                        ws.set_column(i, i, min(w, 45))
                output.seek(0)
                return StreamingResponse(output,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment; filename=filtered_results.xlsx"})
            else:  # CSV
                output = io.StringIO()
                result_out.to_csv(output, index=False)
                return StreamingResponse(iter([output.getvalue()]),
                    media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=filtered_results.csv"})
        
        # Return preview
        return JSONResponse({
            "total": len(result_out),
            "columns": list(result_out.columns),
            "rows": result_out.head(MAX_PREVIEW_ROWS).fillna("").to_dict(orient="records"),
        })
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/share")
async def share_result(request: Request):
    """Store filtered result for sharing."""
    try:
        body     = await request.json()
        sid      = body.get("sid", "")
        rules    = body.get("rules", [])
        logic    = body.get("logic", "AND")
        password = body.get("password", "")

        entry = store.get(sid)
        if not entry:
            return JSONResponse({"error": "Session not found."}, status_code=404)

        df     = entry["df"]
        result = await asyncio.to_thread(apply_filters, df, rules, logic)
        out_cols = _export_cols(result)
        result_out = _serialize(result[out_cols].copy())

        share_id = str(uuid.uuid4())[:8]
        pwd_hash = hashlib.sha256(password.encode()).hexdigest() if password else ""
        share_store[share_id] = {
            "columns":  list(result_out.columns),
            "rows":     result_out.head(MAX_PREVIEW_ROWS).fillna("").values.tolist(),
            "total":    len(result_out),
            "filename": entry["filename"],
            "pwd_hash": pwd_hash,
        }
        return JSONResponse({"id": share_id, "url": f"/share/{share_id}"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/share-data")
async def share_data_direct(request: Request):
    """Store already-filtered data for sharing (used by frontend)."""
    try:
        body = await request.json()
        query = body.get("query", "")
        filename = body.get("filename", "unknown")
        password = body.get("password", "")
        columns = body.get("columns", [])
        rows = body.get("rows", [])
        total = body.get("total", 0)
        
        share_id = str(uuid.uuid4())[:8]
        pwd_hash = hashlib.sha256(password.encode()).hexdigest() if password else ""
        
        # Convert rows (list of dicts) to list of lists for storage
        rows_list = [[row.get(col, "") for col in columns] for row in rows]
        
        share_store[share_id] = {
            "columns": columns,
            "rows": rows_list,
            "total": total,
            "filename": filename,
            "pwd_hash": pwd_hash,
        }
        return JSONResponse({"id": share_id, "url": f"/share/{share_id}"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.get("/share/{share_id}", response_class=HTMLResponse)
def view_share(share_id: str, pwd: str = ""):
    from html import escape
    data = share_store.get(share_id)
    if not data:
        return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px'>Link expired or not found.</h2>", 404)

    if data.get("pwd_hash"):
        if hashlib.sha256(pwd.encode()).hexdigest() != data["pwd_hash"]:
            return HTMLResponse("""<!DOCTYPE html><html><head><meta charset="UTF-8"/>
<title>FilterIQ — Protected</title>
<style>body{font-family:sans-serif;background:#0b0b0f;color:#f0f0f5;display:flex;align-items:center;justify-content:center;min-height:100vh}
.box{background:#111118;border:1px solid #222230;border-radius:12px;padding:40px;text-align:center;max-width:360px}
input{width:100%;padding:10px;border-radius:8px;border:1px solid #2e2e40;background:#18181f;color:#f0f0f5;font-size:1rem;margin-bottom:12px}
button{background:#c8ff57;color:#0b0b0f;border:none;padding:10px 24px;border-radius:8px;font-weight:700;cursor:pointer;width:100%}
</style></head><body><div class="box"><h2>🔒 Password protected</h2>
<form method="get"><input type="password" name="pwd" placeholder="Enter password" autofocus/>
<button type="submit">Unlock</button></form></div></body></html>""")

    cols_html = "".join(f"<th>{escape(str(c))}</th>" for c in data["columns"])
    rows_html = "".join(
        "<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>"
        for row in data["rows"]
    )
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"/><title>FilterIQ Shared</title>
<style>body{{font-family:sans-serif;background:#0b0b0f;color:#f0f0f5;padding:32px}}
.wrap{{overflow-x:auto;border:1px solid #222230;border-radius:10px}}
table{{width:100%;border-collapse:collapse;font-size:.84rem}}
th{{background:#18181f;padding:10px 14px;text-align:left;color:#6b6b88;font-size:.72rem;text-transform:uppercase;border-bottom:1px solid #222230}}
td{{padding:9px 14px;border-bottom:1px solid #1a1a28;color:#9898b8}}
tr:hover td{{background:#13131f}}
</style></head><body>
<h2 style="margin-bottom:6px">FilterIQ — Shared Results</h2>
<p style="color:#6b6b88;margin-bottom:20px">{data['total']} rows · {escape(data['filename'])}</p>
<div class="wrap"><table><thead><tr>{cols_html}</tr></thead><tbody>{rows_html}</tbody></table></div>
</body></html>"""


app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Presets ──
presets_store: dict = {}  # session_id → list of presets


@app.get("/presets/{session_id}")
async def get_presets(session_id: str):
    """Get saved presets for a session."""
    presets = presets_store.get(session_id, [])
    return JSONResponse({"presets": presets})


@app.post("/presets/save")
async def save_preset(
    session_id: str = Form(...),
    name: str = Form(...),
    query: str = Form(...)
):
    """Save a filter preset."""
    if session_id not in presets_store:
        presets_store[session_id] = []
    
    # Remove existing preset with same name
    presets_store[session_id] = [p for p in presets_store[session_id] if p["name"] != name]
    
    # Add new preset
    presets_store[session_id].append({"name": name, "query": query})
    
    return JSONResponse({"presets": presets_store[session_id]})


@app.delete("/presets/{session_id}/{name}")
async def delete_preset(session_id: str, name: str):
    """Delete a preset."""
    if session_id in presets_store:
        presets_store[session_id] = [p for p in presets_store[session_id] if p["name"] != name]
    return JSONResponse({"success": True})


@app.post("/bulk-filter")
async def bulk_filter(
    file: UploadFile = File(...),
    filters: str = Form(...),
    clean: str = Form("false")
):
    """
    Apply multiple filters and export as Excel with multiple sheets.
    """
    try:
        from query_parser import parse_query
        import json
        
        # Read and normalize file
        content = await file.read()
        df = await asyncio.to_thread(_read_file, content, file.filename or "")
        df.columns = [str(c).strip() for c in df.columns]
        df = await asyncio.to_thread(normalize_dataframe, df)
        
        # Parse filters JSON
        filters_list = json.loads(filters)
        
        # Create Excel with multiple sheets
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            workbook = writer.book
            hdr_fmt = workbook.add_format({
                "bold": True, "bg_color": "#111118",
                "font_color": "#c8ff57", "border": 1,
            })
            
            # Summary sheet
            summary_data = []
            
            for filter_def in filters_list:
                sheet_name = filter_def.get("name", "Sheet")[:31]  # Excel limit
                query = filter_def.get("query", "")
                
                # Parse and apply filter
                all_cols = list(df.columns)
                rules, logic = await asyncio.to_thread(parse_query, query, all_cols)
                result = await asyncio.to_thread(apply_filters, df, rules, logic)
                
                # Clean if requested
                if clean.lower() == "true":
                    result = result.drop_duplicates()
                    for col in result.select_dtypes(include="object").columns:
                        if not col.startswith("_norm_"):
                            result[col] = result[col].astype(str).str.strip()
                
                # Export columns (no norm columns)
                out_cols = _export_cols(result)
                result_out = _serialize(result[out_cols].copy())
                
                # Write to sheet
                result_out.to_excel(writer, index=False, sheet_name=sheet_name)
                ws = writer.sheets[sheet_name]
                
                # Format header
                for i, col in enumerate(result_out.columns):
                    ws.write(0, i, col, hdr_fmt)
                    w = max(len(str(col)),
                            result_out[col].astype(str).str.len().max() if len(result_out) else len(col)) + 2
                    ws.set_column(i, i, min(w, 45))
                
                # Add to summary
                summary_data.append({
                    "Sheet": sheet_name,
                    "Query": query,
                    "Rows": len(result_out)
                })
            
            # Add summary sheet
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, index=False, sheet_name="Summary")
                ws = writer.sheets["Summary"]
                for i, col in enumerate(summary_df.columns):
                    ws.write(0, i, col, hdr_fmt)
                    ws.set_column(i, i, max(len(str(col)), 20))
        
        output.seek(0)
        return StreamingResponse(output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=bulk_filtered.xlsx"})
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return JSONResponse({"error": str(e)}, status_code=400)
 