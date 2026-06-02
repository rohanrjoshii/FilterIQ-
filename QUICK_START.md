# FilterIQ - Quick Start Guide

## 🚀 Your Application is Ready!

The server is **already running** at: **http://localhost:8000**

Just open your browser and start filtering!

---

## 📋 What Changed

✅ **Removed NLP/Natural Language Processing** - No more spaCy dependency  
✅ **Using structured filters** - Clean, predictable, fast  
✅ **Smart normalization** - Handles height, salary, age automatically  
✅ **Old frontend restored** - Simple, clean interface  

---

## 🎯 How to Use

### 1. Upload Your File
- Drag & drop or click to upload
- Supports: Excel (.xlsx), CSV (.csv), PDF (.pdf)

### 2. View Detected Columns
- System automatically detects column types
- Shows data summary and statistics

### 3. Apply Filters
The system uses **structured filtering** - here's how to write filters:

#### Basic Examples:
```
Bride/Bridegroom is Bride
Age >= 25
Age between 25 and 30
Occupation contains Software
Address contains Telangana
Cast in Mala, Mala (SC), B.C.C-Mala
```

#### Combined Filters (AND logic):
```
Bride/Bridegroom is Bride
AND Age between 25 and 30
AND Occupation contains Software
AND Address contains Telangana
```

#### Multiple Options (OR logic):
```
Occupation contains Software
OR Occupation contains IT
OR Occupation contains Developer
```

### 4. Export Results
- **Preview** - See first 500 rows in browser
- **CSV** - Download as CSV file
- **Excel** - Download as formatted Excel file
- **Share** - Generate shareable link (optional password)

---

## 🔍 Smart Features

### Automatic Normalization
The system automatically handles:

- **Height:** "5ft 8in", "5'8", "175cm" → all converted to cm
- **Salary:** "10 LPA", "5 lakhs", "50k" → all converted to annual INR
- **Age:** Validates and normalizes
- **Text:** Case-insensitive matching

### Example: Finding Software Professionals
```
Occupation contains Software
OR Occupation contains IT
OR Occupation contains Developer
OR Occupation contains Engineer
```

This will match:
- "Software Engineer"
- "IT Professional"
- "Developer"
- "Computer Engineer"
- "Software Developer"
- etc.

---

## 🎨 Advanced Features

### Bulk Export
1. Click "Advanced Tools"
2. Add multiple filters with sheet names
3. Export all as one Excel file with multiple sheets

### Filter History
- All your filters are saved
- Click "Rerun" to apply again

### Charts
- Switch to "Chart" tab after filtering
- Visualize data with bar, line, pie, or doughnut charts

---

## 🛠️ Server Management

### Start Server
```bash
./start.sh
```

### Stop Server
Press `Ctrl+C` in the terminal

### Restart Server
```bash
# Stop with Ctrl+C, then:
./start.sh
```

---

## 📊 Filter Operators Reference

| Operator | Example | Description |
|----------|---------|-------------|
| `is` | `Gender is Female` | Exact match |
| `contains` | `City contains Hyderabad` | Contains text |
| `>=` | `Age >= 25` | Greater than or equal |
| `<=` | `Age <= 30` | Less than or equal |
| `between` | `Age between 25 and 30` | Range (inclusive) |
| `in` | `Cast in Mala, Reddy` | Match any in list |
| `AND` | `Gender is Female AND Age >= 25` | Both conditions |
| `OR` | `City contains Hyderabad OR City contains Bangalore` | Either condition |

---

## 💡 Tips

1. **Use contains for partial matches**
   - `Occupation contains Software` matches "Software Engineer", "Software Developer", etc.

2. **Combine multiple conditions**
   - Use AND for strict filtering
   - Use OR for broader results

3. **Check the preview first**
   - See how many rows match before exporting

4. **Use bulk export for multiple segments**
   - Create different sheets for different criteria in one Excel file

5. **Height and Salary are normalized**
   - No need to worry about different formats
   - System handles "5ft 8in" and "175cm" equally

---

## 🐛 Troubleshooting

### No results found?
- Check column names match exactly
- Use "contains" instead of "is" for partial matches
- Try OR logic for broader matching

### Server not responding?
- Check if server is running: http://localhost:8000
- Restart with `./start.sh`

### File upload fails?
- Ensure file is .xlsx, .csv, or .pdf
- Check file isn't corrupted
- Try a smaller file first

---

## 📞 Need Help?

The application is designed to be intuitive, but if you need help:

1. Check the **Smart Suggestions** after uploading a file
2. Look at **Filter History** for examples
3. Use the **Filter Builder** (in Advanced Tools) for no-typing filtering

---

**Enjoy filtering! 🎉**
