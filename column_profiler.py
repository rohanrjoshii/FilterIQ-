import re
import pandas as pd
from normalizer import parse_height_to_cm, parse_salary_to_annual_inr


# Column name hints for smart type detection
HEIGHT_HINTS   = {"height", "hight", "ht", "tall"}
AGE_HINTS      = {"age", "yrs", "years"}
SALARY_HINTS   = {"salary", "income", "ctc", "package", "pay", "earning", "sal"}
DOB_HINTS      = {"dob", "birth", "born", "date"}
GENDER_HINTS   = {"gender", "bride", "bridegroom", "sex", "role"}
CITY_HINTS     = {"city", "location", "place", "area", "district", "address", "state", "region"}
CASTE_HINTS    = {"caste", "cast", "community", "jati", "kula"}
RELIGION_HINTS = {"religion", "denomination", "faith", "church"}
MARITAL_HINTS  = {"marital", "status", "married"}
EDUCATION_HINTS= {"education", "qualification", "degree", "study"}
OCCUPATION_HINTS={"occupation", "job", "profession", "work", "employed"}
NAME_HINTS     = {"name", "applicant", "person", "candidate"}


def _col_lower(col: str) -> str:
    return col.lower().replace(" ", "").replace("_", "").replace("-", "").replace("/", "")


def infer_column_type(col_name: str, series: pd.Series) -> str:
    cl = _col_lower(col_name)

    # Explicit name-based detection first
    if any(h in cl for h in HEIGHT_HINTS):
        return "height"
    if any(h in cl for h in AGE_HINTS):
        return "age"
    if any(h in cl for h in DOB_HINTS):
        return "date"
    if any(h in cl for h in SALARY_HINTS):
        return "salary"
    if any(h in cl for h in GENDER_HINTS):
        return "categorical"
    if any(h in cl for h in CITY_HINTS):
        return "categorical"
    if any(h in cl for h in CASTE_HINTS):
        return "categorical"
    if any(h in cl for h in RELIGION_HINTS):
        return "categorical"
    if any(h in cl for h in MARITAL_HINTS):
        return "categorical"
    if any(h in cl for h in EDUCATION_HINTS):
        return "categorical"
    if any(h in cl for h in OCCUPATION_HINTS):
        return "categorical"
    if any(h in cl for h in NAME_HINTS):
        return "text"

    # Data-driven detection
    non_null = series.dropna()
    if len(non_null) == 0:
        return "text"

    # Try numeric
    numeric = pd.to_numeric(non_null, errors="coerce")
    numeric_ratio = numeric.notna().mean()
    if numeric_ratio > 0.85:
        mn, mx = float(numeric.min()), float(numeric.max())
        # Looks like age
        if 0 < mn and mx <= 120:
            return "age"
        return "numeric"

    # Categorical if low cardinality
    if non_null.nunique() <= 60:
        return "categorical"

    return "text"


def profile_columns(df: pd.DataFrame) -> list:
    """
    Returns a list of column profiles, each with:
    - col: column name
    - type: height | age | salary | numeric | categorical | date | text
    - null_count, unique_count
    - For categorical: values (sorted list)
    - For numeric/age/height/salary: min, max
    - norm_col: name of the normalized column (if any)
    - ui: suggested UI control
    """
    profiles = []
    for col in df.columns:
        if col.startswith("_norm_"):
            continue
        series = df[col].dropna()
        dtype = infer_column_type(col, series)

        p = {
            "col": col,
            "type": dtype,
            "null_count": int(df[col].isna().sum()),
            "unique_count": int(series.nunique()),
            "norm_col": None,
            "ui": _suggest_ui(dtype, series),
        }

        if dtype == "categorical":
            vals = sorted(series.astype(str).str.strip().unique().tolist())
            # Remove empty/nan strings
            vals = [v for v in vals if v and v.lower() not in ("nan", "none", "")]
            p["values"] = vals

        elif dtype == "height":
            norm_col = f"_norm_{col}_cm"
            if norm_col in df.columns:
                cms = df[norm_col].dropna()
                if len(cms):
                    p["min"] = round(float(cms.min()), 1)
                    p["max"] = round(float(cms.max()), 1)
                    p["norm_col"] = norm_col
            # Also expose raw values for display
            p["values"] = sorted(series.astype(str).str.strip().unique().tolist())

        elif dtype == "salary":
            norm_col = f"_norm_{col}_salary"
            if norm_col in df.columns:
                nums = df[norm_col].dropna()
                if len(nums):
                    p["min"] = round(float(nums.min()), 0)
                    p["max"] = round(float(nums.max()), 0)
                    p["norm_col"] = norm_col
            p["values"] = sorted(series.astype(str).str.strip().unique().tolist())

        elif dtype in ("age", "numeric"):
            norm_col = f"_norm_{col}_num"
            nums = pd.to_numeric(series, errors="coerce").dropna()
            if len(nums):
                p["min"] = round(float(nums.min()), 1)
                p["max"] = round(float(nums.max()), 1)
                p["norm_col"] = norm_col

        profiles.append(p)

    return profiles


def _suggest_ui(dtype: str, series: pd.Series) -> str:
    if dtype == "categorical":
        n = series.nunique()
        if n <= 2:
            return "toggle"
        if n <= 10:
            return "checkbox"
        return "multiselect"
    if dtype in ("age", "numeric", "height", "salary"):
        return "range"
    if dtype == "date":
        return "daterange"
    return "text"
