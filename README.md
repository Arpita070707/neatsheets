# 🧹📊 NeatSheets  

**Clean data, better results** — Transform messy spreadsheets into clean, analysis-ready datasets with this simple, fast, and effective web application.  

---

## 🚀 What is NeatSheets?  

NeatSheets is a web-based **data cleaning tool** that helps you transform messy CSV files into clean, analysis-ready datasets.  
Built with **Flask** and **Python**, it provides an intuitive interface for common data cleaning operations — without requiring coding knowledge.  

---

## ✨ Features  

### 🔍 Smart Data Analysis  
- **Dataset Overview** → Get instant insights into your data structure  
- **Missing Value Detection** → Identify columns with missing data  
- **Data Type Analysis** → Understand your column types automatically  
- **Memory Usage Tracking** → Monitor dataset size and optimization  

### 🧹 Cleaning Operations  
- **Remove Duplicates** → Eliminate duplicate rows  
- **Fill Missing Values** → Choose from strategies:  
  - Mean (numeric columns)  
  - Median (numeric columns)  
  - Mode (categorical columns)  
- **Drop High Missing Columns** → Remove columns with excessive missing data 
- **Remove Special Characters** → Clean text while preserving readability  
- **Convert Data Types** → Automatically optimize data types for performance  

### 💾 Session Management  
- **Persistent Sessions** → Work with data across multiple operations  
- **Operation History** → Track all cleaning steps applied  
- **Reset Functionality** → Revert to original dataset anytime  
- **Download Cleaned Data** → Export cleaned dataset as CSV  

---

## 🛠️ Technology Stack  

- **Backend**: Flask (Python web framework)  
- **Data Processing**: Pandas, NumPy  
- **Frontend**: HTML5, CSS3, JavaScript  
- **File Handling**: Secure file upload utilities  

---

## 📋 Requirements  

- Python 3.7+  
- Flask 2.3.3  
- Pandas 2.1.1  
- NumPy 1.24.3

---

## ⚡ Installation  

```bash
# 1. Clone the repository
git clone https://github.com/Arpita070707/neatsheets.git
cd neatsheets

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Access in browser
# Open http://localhost:5000
```

---

## 📖 Usage Guide

### Step 1: Upload CSV File

```text
1. Click "Choose File" and select your CSV  
2. Click "Upload & Analyze"  
3. View dataset summary (rows, columns, missing values, etc.)  
```

### Step 2: Review Dataset Summary

```text
- View rows, columns, and data types  
- Check missing values and duplicates  
- Monitor memory usage  
```

### Step 3: Apply Cleaning Operations

```text
- Remove Duplicates  
- Fill Missing Values (Mean / Median / Mode)  
- Drop High Missing Columns  
- Remove Special Characters  
- Convert Data Types  
```

### Step 4: Download Cleaned Data

```text
- Click "Download" to get cleaned CSV  
- All cleaning steps are preserved  
```

---

## 🔧 API Endpoints

```http
POST   /upload       → Upload CSV + get dataset summary  
POST   /api/clean    → Perform cleaning operations  
GET    /api/summary  → Get dataset summary  
POST   /api/download → Download cleaned dataset  
POST   /api/reset    → Reset to original dataset  
```

---

## 📂 Project Structure

```text
neatsheets/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── start_app.bat         # Windows startup script
├── static/               # Static assets (CSS, JS, Images)
├── templates/            # HTML templates
│   └── index.html        # Main interface
├── utils/                # Utility modules
│   └── data_cleaner.py   # Core data cleaning logic
└── uploads/              # File upload directory
```

---

## 🎯 Use Cases

* **Data Scientists** → Quick preprocessing before analysis
* **Business Analysts** → Clean messy Excel/CSV exports
* **Researchers** → Prepare datasets for statistics
* **Students** → Learn data cleaning hands-on
* **Anyone** → Transform messy spreadsheets into clean data

---

## 🔒 Security Notes

* Runs locally on your machine
* No data sent to external servers
* Session data stored in memory (cleared on restart)
* For production: use Redis or a database for session storage

---

## 🔧 Configuration

- **SECRET_KEY**: In `app.py`, replace `app.secret_key` with a strong random value before deploying.

---

## 🚧 Limitations

* Supports **CSV only**
* File size depends on available memory
* Session data lost when app restarts
* Designed for moderate-sized datasets

---

## 🤝 Contributing

Contributions are welcome! You can:

* Report bugs
* Suggest new features
* Improve UI/UX
* Add new cleaning operations
* Optimize performance

---

## 🆘 Support

If you face issues:

```text
1. Check console/logs for errors  
2. Ensure dependencies are installed  
3. Verify CSV format is correct  
4. Check required ports are available  
```

---
