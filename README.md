# FilterIQ - Smart Data Filtering Application

<div align="center">

![FilterIQ Logo](https://img.shields.io/badge/FilterIQ-Smart_Filtering-7c6dff?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

**Filter and analyze your data using plain English queries. No SQL or programming required.**

[Features](#features) • [Demo](#demo) • [Quick Start](#quick-start) • [Tech Stack](#tech-stack) • [Documentation](#documentation)

</div>

---

## 🎯 Overview

FilterIQ is a powerful web-based application that allows users to filter and analyze large datasets using natural language queries. Simply upload your Excel, CSV, or PDF file and describe what you want in plain English!

### Why FilterIQ?

- 🚀 **Fast**: Process 10,000+ rows in under 2 seconds
- 🎯 **Simple**: No SQL or programming knowledge needed
- 🔄 **Smart**: Automatically normalizes diverse data formats
- 📊 **Visual**: Interactive charts and real-time preview
- 💼 **Professional**: Export to Excel with multiple sheets

---

## ✨ Features

### Core Functionality
- **Natural Language Filtering**: Write queries like "Age > 25 AND City contains Mumbai"
- **Multiple File Formats**: Support for Excel (.xlsx), CSV (.csv), and PDF files
- **Smart Normalization**: Automatically handles height (5ft 8in → cm), salary (10 LPA → INR), age formats
- **Real-Time Preview**: See filtered results instantly with row count

### Advanced Features
- 📦 **Bulk Export**: Apply multiple filters and get one Excel file with separate sheets
- 🔒 **Password-Protected Sharing**: Share filtered results with optional password protection
- 📈 **Interactive Charts**: Visualize data with bar, line, pie, and doughnut charts
- 💾 **Filter Presets**: Save and reuse frequently used filters
- 📜 **Filter History**: Access and rerun previous filters
- 🎨 **Dark/Light Theme**: Comfortable viewing in any environment

### Supported Filter Operators
- **Equality**: `is`, `is not`, `=`, `!=`
- **Text**: `contains`, `not contains`, `starts with`, `ends with`
- **Numeric**: `>`, `<`, `>=`, `<=`, `between`
- **Logic**: `AND`, `OR` combinations
- **Empty checks**: `is empty`, `is not empty`

---

## 🎬 Demo

### Example Queries

```
Gender is Female
Age between 25 and 35
Salary > 50000
City contains Mumbai OR City contains Delhi
Department is Engineering AND Status is Active
Occupation contains Software OR Occupation contains IT
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Option 1: Using Python directly

```bash
# Clone the repository
git clone https://github.com/rohanrjoshii/FilterIQ-.git
cd FilterIQ-

# Install dependencies
pip install -r requirements.txt

# Start the server
./start.sh
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using Docker

```bash
# Clone the repository
git clone https://github.com/rohanrjoshii/FilterIQ-.git
cd FilterIQ-

# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

---

## 📚 Usage Guide

### Basic Workflow

1. **Upload Your File**
   - Drag & drop or click to upload
   - Supports Excel, CSV, and PDF files
   - Files are processed in-memory (never stored permanently)

2. **Review Detected Columns**
   - System automatically detects column types
   - View data summary and statistics

3. **Write Your Filter Query**
   ```
   Gender is Female AND Age between 25 and 35 AND City contains Hyderabad
   ```

4. **View Results**
   - Preview filtered data in table view
   - Switch to chart view for visualizations
   - See total row count

5. **Export or Share**
   - Download as Excel or CSV
   - Share with password protection
   - Use bulk export for multiple filters

### Filter Query Examples

**Simple Filters:**
```
Age > 25
Salary >= 50000
Department is Engineering
Status is Active
```

**Combined Filters (AND):**
```
Gender is Female AND Age > 25
City contains Mumbai AND Salary > 50000
Department is Engineering AND Status is Active
```

**Multiple Options (OR):**
```
City contains Mumbai OR City contains Delhi
Department is Engineering OR Department is IT
Age < 25 OR Age > 60
```

**Complex Queries:**
```
Gender is Female AND Age between 25 and 35 AND City contains Mumbai
Occupation contains Software OR Occupation contains IT OR Occupation contains Developer
Salary > 50000 AND Department is Engineering AND Status is Active
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pandas**: Powerful data manipulation and analysis
- **pdfplumber**: PDF table extraction
- **xlsxwriter**: Excel file generation with formatting
- **openpyxl**: Excel file reading

### Frontend
- **Vanilla JavaScript**: No framework overhead
- **Chart.js**: Beautiful, responsive charts
- **Custom CSS**: Dark/Light theme support

### Architecture
- RESTful API design
- Async/await patterns for performance
- In-memory data processing (no database)
- Session-based file management

---

## 📖 Documentation

### Project Structure

```
FilterIQ/
├── main.py                 # FastAPI application and routes
├── filter_engine.py        # Filter rule processing
├── normalizer.py          # Data normalization functions
├── column_profiler.py     # Column type detection
├── query_parser.py        # Natural language query parser
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── start.sh             # Quick start script
├── static/
│   └── index.html       # Frontend UI
└── docs/
    ├── QUICK_START.md   # Quick start guide
    ├── FILTER_FIXED.md  # Filter examples
    └── CURRENT_STATUS.md # Technical overview
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve frontend UI |
| `/upload` | POST | Upload and profile file |
| `/columns` | POST | Get column names |
| `/summary` | POST | Get file statistics |
| `/filter` | POST | Apply filter and get results |
| `/share-data` | POST | Create shareable link |
| `/share/{id}` | GET | View shared results |
| `/bulk-filter` | POST | Bulk export multiple sheets |
| `/presets/*` | GET/POST/DELETE | Manage filter presets |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000

# Data Processing
MAX_PREVIEW_ROWS=500
MAX_FILE_SIZE_MB=50

# Session
SESSION_TIMEOUT_MINUTES=60
```

### Customization

**Modify UI Colors** (in `static/index.html`):
```css
:root {
  --accent: #7c6dff;  /* Primary accent color */
  --bg: #0a0a0f;      /* Background color */
}
```

**Change Processing Limits** (in `main.py`):
```python
MAX_PREVIEW_ROWS = 500
MAX_SHEET_NAME = 31
```

---

## 🚢 Deployment

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create filteriq-app

# Push code
git push heroku main

# Open app
heroku open
```

### Deploy to Railway

1. Fork this repository
2. Connect Railway to your GitHub
3. Deploy from the dashboard
4. Railway will auto-detect the Dockerfile

### Deploy to Render

1. Create a new Web Service
2. Connect your repository: `https://github.com/rohanrjoshii/FilterIQ-`
3. Use Docker environment
4. Deploy!

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/rohanrjoshii/FilterIQ-.git
cd FilterIQ-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
uvicorn main:app --reload
```

---

## 📝 Roadmap

- [ ] Add SQLite for persistent storage
- [ ] Implement user authentication
- [ ] Add more export formats (JSON, Parquet)
- [ ] Create filter builder UI (drag-and-drop)
- [ ] Add data validation rules
- [ ] Implement API rate limiting
- [ ] Add support for JOIN operations across files
- [ ] Mobile app (React Native)

---

## 🐛 Known Issues

- Large files (>50MB) may cause timeout
- PDF parsing depends on table structure
- In-memory storage clears on server restart

See [Issues](https://github.com/rohanrjoshii/FilterIQ-/issues) for full list.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing web framework
- [Pandas](https://pandas.pydata.org/) - Powerful data analysis
- [Chart.js](https://www.chartjs.org/) - Beautiful charts
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF extraction

---

## 📧 Contact

**Rohan Joshi** - [GitHub](https://github.com/rohanrjoshii)

Project Link: [https://github.com/rohanrjoshii/FilterIQ-](https://github.com/rohanrjoshii/FilterIQ-)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ by Rohan Joshi**

[Report Bug](https://github.com/rohanrjoshii/FilterIQ-/issues) • [Request Feature](https://github.com/rohanrjoshii/FilterIQ-/issues)

</div>
