from flask import Flask, render_template, request, send_file, jsonify, session
from werkzeug.utils import secure_filename
import pandas as pd
import io
import os
import uuid
import traceback
from utils.data_cleaner import DataCleaner, clean_data  # Custom data-cleaning logic

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions

# Store data cleaners in session (in production, use Redis or database)
data_cleaners = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    """Handle CSV upload and return initial dataset summary"""
    try:
        if 'csv_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['csv_file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400
        
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Create a unique session ID for this dataset
        session_id = str(uuid.uuid4())
        
        # Create data cleaner instance
        cleaner = DataCleaner(df)
        data_cleaners[session_id] = cleaner
        
        # Store session ID in Flask session
        session['session_id'] = session_id
        
        # Get initial dataset summary
        summary = cleaner.get_dataset_summary()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'summary': summary
        })
        
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Failed to read CSV file: {str(e)}'}), 500

@app.route('/clean', methods=['POST'])
def clean_csv():
    """Legacy endpoint for backward compatibility"""
    file = request.files.get('csv_file')

    # Validate uploaded file
    if not file or not file.filename.endswith('.csv'):
        return "Invalid file format. Please upload a CSV file.", 400

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return f"Failed to read CSV file: {str(e)}", 500

    # Read form options safely
    options = {
        'remove_duplicates': bool(request.form.get('remove_duplicates')),
        'fill_missing': bool(request.form.get('fill_missing')),
        'detect_outliers': bool(request.form.get('detect_outliers')),
    }

    try:
        cleaned_df = clean_data(df, options)
    except Exception as e:
        return f"Error during data cleaning: {str(e)}", 500

    output = io.BytesIO()
    cleaned_df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        download_name='cleaned.csv',
        as_attachment=True
    )

@app.route('/api/clean', methods=['POST'])
def api_clean():
    """API endpoint for cleaning operations"""
    try:
        data = request.get_json()
        operation = data.get('operation')
        session_id = session.get('session_id')
        
        if not session_id or session_id not in data_cleaners:
            return jsonify({'error': 'No active dataset. Please upload a CSV file first.'}), 400
        
        cleaner = data_cleaners[session_id]
        
        if operation == 'remove_duplicates':
            result = cleaner.remove_duplicates()
        elif operation == 'fill_missing':
            method = data.get('method', 'mean')
            result = cleaner.fill_missing_values(method)
        elif operation == 'drop_high_missing':
            threshold = data.get('threshold', 0.5)
            result = cleaner.drop_high_missing_columns(threshold)
        elif operation == 'remove_special_chars':
            result = cleaner.remove_special_characters()
        elif operation == 'convert_types':
            result = cleaner.convert_data_types()
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        app.logger.error(f"Cleaning error: {str(e)}")
        app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Error during cleaning: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def download_cleaned():
    """Download the cleaned CSV file"""
    try:
        session_id = session.get('session_id')
        
        if not session_id or session_id not in data_cleaners:
            return jsonify({'error': 'No active dataset. Please upload a CSV file first.'}), 400
        
        cleaner = data_cleaners[session_id]
        cleaned_df = cleaner.get_cleaned_dataframe()
        
        output = io.BytesIO()
        cleaned_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            download_name='cleaned_dataset.csv',
            as_attachment=True
        )
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get current dataset summary"""
    try:
        session_id = session.get('session_id')
        
        if not session_id or session_id not in data_cleaners:
            return jsonify({'error': 'No active dataset'}), 400
        
        cleaner = data_cleaners[session_id]
        summary = cleaner.get_dataset_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        app.logger.error(f"Summary error: {str(e)}")
        return jsonify({'error': f'Failed to get summary: {str(e)}'}), 500

@app.route('/api/reset', methods=['POST'])
def reset_dataset():
    """Reset dataset to original state"""
    try:
        session_id = session.get('session_id')
        
        if not session_id or session_id not in data_cleaners:
            return jsonify({'error': 'No active dataset'}), 400
        
        cleaner = data_cleaners[session_id]
        cleaner.reset_to_original()
        
        summary = cleaner.get_dataset_summary()
        
        return jsonify({
            'success': True,
            'summary': summary,
            'message': 'Dataset reset to original state'
        })
    except Exception as e:
        app.logger.error(f"Reset error: {str(e)}")
        return jsonify({'error': f'Failed to reset dataset: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)