# Cleaner CSV App

A professional, modern web application for cleaning and preprocessing CSV datasets with an intuitive dark-themed interface.

## Features

### 🚀 **Core Functionality**
- **CSV Upload & Analysis**: Upload CSV files and get instant dataset summaries
- **Professional Data Cleaning**: Multiple cleaning operations with before/after comparisons
- **Real-time Processing**: AJAX-based operations without page refreshes
- **Session Management**: Maintain dataset state across operations

### 🧹 **Cleaning Operations**
- **Remove Duplicates**: Eliminate duplicate rows from your dataset
- **Fill Missing Values**: Choose from mean, median, or mode strategies
- **Drop High Missing Columns**: Remove columns with excessive missing data (30%, 50%, 70% thresholds)
- **Remove Special Characters**: Clean text data while preserving readability
- **Convert Data Types**: Automatic data type optimization for better performance

### 🎨 **User Interface**
- **Dark Theme**: Modern, professional dark interface
- **Responsive Design**: Works seamlessly on all device sizes
- **Bootstrap 5**: Built with the latest Bootstrap framework
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Real-time Feedback**: Loading indicators and success/error messages

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd cleaner_csv_app

# Or simply download and extract the files
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access the App
Open your browser and navigate to: `http://localhost:5000`

## Usage Guide

### Step 1: Upload CSV File
1. Click "Choose File" and select your CSV file
2. Click "Upload & Analyze" to process the file
3. View the initial dataset summary (rows, columns, missing values, etc.)

### Step 2: Perform Cleaning Operations
- **Remove Duplicates**: Click the button to eliminate duplicate rows
- **Fill Missing Values**: Choose from dropdown options (mean, median, mode)
- **Drop High Missing Columns**: Select threshold and remove problematic columns
- **Remove Special Characters**: Clean text data automatically
- **Convert Data Types**: Optimize data types for better performance

### Step 3: Monitor Progress
- Each operation shows detailed before/after comparisons
- Dataset summary updates in real-time
- View cleaning history and results

### Step 4: Download Results
- Click "Download Cleaned CSV" to get your processed dataset
- Use "Reset" button to return to the original dataset

## Technical Architecture

### Backend (Flask)
- **Flask Framework**: Lightweight, flexible web framework
- **Pandas Integration**: Powerful data manipulation and analysis
- **Session Management**: Maintain dataset state across requests
- **RESTful API**: Clean, organized endpoint structure

### Frontend (HTML/CSS/JavaScript)
- **Bootstrap 5**: Modern, responsive CSS framework
- **Vanilla JavaScript**: ES6+ features with async/await
- **AJAX Communication**: Seamless backend integration
- **Responsive Design**: Mobile-first approach

### Data Processing
- **DataCleaner Class**: Modular, extensible cleaning operations
- **Memory Optimization**: Efficient data handling for large datasets
- **Error Handling**: Robust error management and user feedback

## File Structure

```
cleaner_csv_app/
│── app.py                 # Main Flask application
│── requirements.txt       # Python dependencies
│── README.md             # This file
│── utils/
│   └── data_cleaner.py  # Data cleaning logic
│── templates/
│   └── index.html        # Main HTML template
│── static/
│   ├── css/
│   │   └── style.css     # Custom dark theme styles
│   ├── js/
│   │   └── script.js     # Frontend JavaScript logic
│   └── images/           # Application images
│── uploads/              # Temporary file storage
└── cleaned/              # Processed file storage
```

## API Endpoints

### File Operations
- `POST /upload` - Upload and analyze CSV file
- `POST /api/download` - Download cleaned CSV file

### Data Cleaning
- `POST /api/clean` - Perform cleaning operations
- `GET /api/summary` - Get current dataset summary
- `POST /api/reset` - Reset to original dataset

### Legacy Support
- `POST /clean` - Original cleaning endpoint (backward compatibility)

## Customization

### Adding New Cleaning Operations
1. Extend the `DataCleaner` class in `utils/data_cleaner.py`
2. Add corresponding API endpoint in `app.py`
3. Update frontend JavaScript in `static/js/script.js`
4. Add UI elements in `templates/index.html`

### Styling Changes
- Modify `static/css/style.css` for custom themes
- Update Bootstrap classes in HTML for layout changes
- Customize color variables in CSS `:root` section

## Browser Support

- **Chrome**: 90+ (Recommended)
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## Performance Considerations

- **Large Files**: Optimized for datasets up to 100MB
- **Memory Usage**: Efficient pandas operations with minimal memory overhead
- **Session Storage**: In-memory storage (consider Redis for production)

## Security Features

- **File Validation**: Strict CSV file type checking
- **Session Management**: Secure session handling
- **Input Sanitization**: Safe data processing

## Troubleshooting

### Common Issues

**File Upload Fails**
- Ensure file is valid CSV format
- Check file size (recommended < 100MB)
- Verify file encoding (UTF-8 recommended)

**Cleaning Operations Not Working**
- Refresh page and re-upload file
- Check browser console for JavaScript errors
- Verify all dependencies are installed

**Performance Issues**
- Close other browser tabs
- Use smaller datasets for testing
- Check available system memory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section above

---

**Built with ❤️ using Flask, Pandas, and Bootstrap**
