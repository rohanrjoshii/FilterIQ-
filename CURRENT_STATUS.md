# FilterIQ - Current Status

## ✅ What's Working

The application is now running with a **clean, structured filter architecture** - no NLP, no natural language parsing, just intelligent data normalization and structured filtering.

### Server Status
- **Running on:** http://localhost:8000
- **Status:** ✅ Active and ready

### Architecture Overview

```
Upload (CSV/Excel/PDF)
         ↓
Schema Detection & Normalization
         ↓
Structured Filter Engine
         ↓
Result Preview
         ↓
Export (.xlsx / .csv)
```

## 🎯 Key Features

### 1. **Smart Normalization** (`normalizer.py`)
Automatically normalizes data on upload:
- **Height:** Converts "5ft 8in", "5'8", "175cm" → standardized cm
- **Salary:** Handles "10 LPA", "5 lakhs", "50k" → annual INR
- **Age:** Validates and normalizes age values
- **Text:** Lowercase, trimmed for consistent matching

### 2. **Column Profiler** (`column_profiler.py`)
Detects column types intelligently:
- Recognizes height, age, salary, gender, location, education, occupation
- Provides min/max ranges for numeric fields
- Lists unique values for categorical fields
- Suggests appropriate UI controls (range slider, dropdown, etc.)

### 3. **Filter Engine** (`filter_engine.py`)
Supports structured filtering with operators:
- **Equality:** equals, not_equals
- **Membership:** in, not_in
- **Text:** contains, not_contains, starts_with, ends_with
- **Numeric:** between, gte, lte, gt, lt
- **Null checks:** is_empty, is_not_empty
- **Logic:** AND / OR combinations

### 4. **Frontend** (`static/index.html`)
Clean, modern UI with:
- Drag-and-drop file upload
- Column detection display
- Filter input (structured format)
- Results preview with table/chart views
- Export to Excel/CSV
- Share functionality
- Bulk filter (multiple sheets in one Excel)

## 📊 How Filtering Works

### Example Filter Request
```json
{
  "sid": "session-id",
  "rules": [
    {
      "column": "Bride/Bridegroom",
      "operator": "equals",
      "value": "Bride"
    },
    {
      "column": "Age",
      "operator": "between",
      "norm_column": "_norm_Age_num",
      "value": [25, 30]
    },
    {
      "column": "Occupation",
      "operator": "contains",
      "value": "Software"
    },
    {
      "column": "Address",
      "operator": "contains",
      "value": "Telangana"
    }
  ],
  "logic": "AND"
}
```

## 🔧 Technical Stack

- **Backend:** FastAPI (Python)
- **Data Processing:** Pandas
- **PDF Parsing:** pdfplumber
- **Excel Export:** xlsxwriter
- **Frontend:** Vanilla JavaScript + Chart.js
- **Styling:** Custom CSS with dark/light theme

## 📁 File Structure

```
.
├── main.py              # FastAPI routes & session management
├── filter_engine.py     # Structured filter logic
├── normalizer.py        # Data normalization functions
├── column_profiler.py   # Column type detection
├── requirements.txt     # Python dependencies
├── static/
│   └── index.html      # Frontend UI
├── start.sh            # Server startup script
└── Dockerfile          # Container configuration
```

## 🚀 Usage

### Start Server
```bash
./start.sh
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access Application
Open http://localhost:8000 in your browser

### Workflow
1. **Upload** your Excel/CSV/PDF file
2. **Review** detected columns and data summary
3. **Apply filters** using the structured format
4. **Preview** results in table or chart view
5. **Export** to Excel or CSV

## 🎨 Frontend Features

- **Dark/Light Theme Toggle**
- **Drag & Drop Upload**
- **Column Chips** - Click to see column details
- **Smart Suggestions** - Auto-generated filter examples
- **Filter History** - Rerun previous filters
- **Bulk Export** - Multiple filtered sheets in one Excel
- **Share Links** - Password-protected result sharing
- **Charts** - Bar, Line, Pie, Doughnut visualizations

## 🔒 Data Privacy

- All processing happens in-memory
- No data is stored permanently
- Files are processed and discarded
- Session-based storage (cleared on restart)

## 📝 Notes

- The old NLP-based approach has been removed
- Current implementation uses structured filters only
- Frontend is the same as backup (both files are identical)
- Normalization happens once on upload for performance
- Supports AND/OR logic with proper precedence

## 🐛 Known Limitations

- In-memory storage (sessions lost on restart)
- Preview limited to 500 rows
- No persistent database
- Single-user sessions (no multi-tenancy)

## 🔄 Next Steps (If Needed)

1. Add SQLite for persistent storage
2. Implement user authentication
3. Add more export formats (JSON, Parquet)
4. Create filter builder UI (no typing needed)
5. Add data validation rules
6. Implement scheduled exports

---

**Status:** ✅ Ready for use
**Last Updated:** April 20, 2026
