import os
import pandas as pd
import requests
from datetime import datetime, timedelta
import calendar
from flask import Flask, render_template, request, send_file, jsonify
import tempfile
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def get_hebrew_holidays(year):
    """Fetch Hebrew holidays from hebcal.com API"""
    try:
        url = f"https://www.hebcal.com/hebcal"
        params = {
            'v': 1,
            'cfg': 'json',
            'maj': 'on',
            'mod': 'on',
            'nh': 'on',
            'd': 'on',
            'lg': 's',
            'year': year,
            'start': f"{year}-01-01",
            'end': f"{year}-12-31"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        holidays = set()
        
        for item in data.get('items', []):
            if item.get('category') in ['holiday', 'roshchodesh']:
                date_str = item.get('date')
                if date_str:
                    # Convert from YYYY-MM-DD format
                    holiday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    holidays.add(holiday_date)
        
        return holidays
    except Exception as e:
        print(f"Error fetching Hebrew holidays: {e}")
        return set()

def is_working_day(date, holidays):
    """Check if a date is a working day (Sunday-Thursday, not a holiday)"""
    # Sunday = 6, Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3
    # Friday = 4, Saturday = 5
    weekday = date.weekday()
    
    # Friday (4) and Saturday (5) are non-working days
    if weekday in [4, 5]:
        return False
    
    # Check if it's a holiday
    if date in holidays:
        return False
    
    return True

def get_next_working_day(date, holidays):
    """Get the next working day from a given date"""
    current_date = date
    while not is_working_day(current_date, holidays):
        current_date += timedelta(days=1)
    return current_date

def calculate_schedule(syllabus_df, start_date, add_break, break_days, consider_holidays):
    """Calculate the course schedule based on the syllabus"""
    
    # Get holidays if needed
    holidays = set()
    if consider_holidays:
        # Get holidays for current year and next year
        current_year = start_date.year
        holidays = get_hebrew_holidays(current_year)
        holidays.update(get_hebrew_holidays(current_year + 1))
    
    schedule_data = []
    current_date = start_date
    
    # Group by Main Topic
    for main_topic, group in syllabus_df.groupby('Main Topic'):
        topic_start_date = None
        
        for _, row in group.iterrows():
            subtopic = row['Subtopic']
            # Handle NaN values and convert to integer
            days_value = row['Days']
            if pd.isna(days_value):
                raise ValueError(f"Invalid value in 'Days' column for subtopic '{subtopic}'. Please ensure all days values are numbers.")
            days_needed = int(days_value)
            
            # Find the next working day to start
            if topic_start_date is None:
                current_date = get_next_working_day(current_date, holidays)
                topic_start_date = current_date
            
            start_date_for_subtopic = current_date
            days_allocated = 0
            end_date = start_date_for_subtopic
            
            # Allocate working days for this subtopic
            while days_allocated < days_needed:
                if is_working_day(current_date, holidays):
                    days_allocated += 1
                end_date = current_date
                current_date += timedelta(days=1)
            
            schedule_data.append({
                'Main Topic': main_topic,
                'Subtopic': subtopic,
                'Start Date': start_date_for_subtopic.strftime('%Y-%m-%d'),
                'End Date': end_date.strftime('%Y-%m-%d'),
                'Duration (Days)': days_needed
            })
        
        # Add break after each main topic if enabled
        if add_break and break_days > 0:
            current_date = get_next_working_day(current_date, holidays)
            break_start = current_date
            
            # Skip break_days working days
            break_days_allocated = 0
            while break_days_allocated < break_days:
                if is_working_day(current_date, holidays):
                    break_days_allocated += 1
                current_date += timedelta(days=1)
            
            break_end = current_date - timedelta(days=1)
            
            schedule_data.append({
                'Main Topic': f"{main_topic} - Break",
                'Subtopic': 'Break Period',
                'Start Date': break_start.strftime('%Y-%m-%d'),
                'End Date': break_end.strftime('%Y-%m-%d'),
                'Duration (Days)': break_days
            })
    
    return pd.DataFrame(schedule_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Read the CSV file
        syllabus_df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Main Topic', 'Subtopic', 'Days']
        missing_columns = [col for col in required_columns if col not in syllabus_df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing required columns: {", ".join(missing_columns)}'}), 400
        
        # Validate data
        if syllabus_df.empty:
            return jsonify({'error': 'The uploaded CSV file is empty'}), 400
        
        # Get form data for empty value handling
        handle_empty_days = request.form.get('handle_empty_days') == 'true'
        default_days = int(request.form.get('default_days', 1))
        
        # Check for non-numeric values in Days column
        try:
            syllabus_df['Days'] = pd.to_numeric(syllabus_df['Days'], errors='coerce')
        except Exception as e:
            return jsonify({'error': f'Error processing Days column: {str(e)}'}), 400
        
        # Handle empty values based on user preference
        if syllabus_df['Days'].isna().any():
            if handle_empty_days:
                # Fill empty values with default
                empty_count = syllabus_df['Days'].isna().sum()
                syllabus_df['Days'] = syllabus_df['Days'].fillna(default_days)
                print(f"Info: Filled {empty_count} empty values in Days column with {default_days} day(s) each.")
            else:
                return jsonify({'error': 'Found empty values in the Days column. Please enable empty value handling or fill the values manually'}), 400
        
        # Get form data
        start_date_str = request.form.get('start_date')
        add_break = request.form.get('add_break') == 'true'
        break_days = int(request.form.get('break_days', 0))
        consider_holidays = request.form.get('consider_holidays') == 'true'
        
        if not start_date_str:
            return jsonify({'error': 'Start date is required'}), 400
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        
        # Calculate schedule
        schedule_df = calculate_schedule(syllabus_df, start_date, add_break, break_days, consider_holidays)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            schedule_df.to_csv(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name
        
        return jsonify({
            'success': True,
            'message': 'Schedule generated successfully',
            'file_path': tmp_file_path
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download/<path:file_path>')
def download_file(file_path):
    try:
        return send_file(file_path, as_attachment=True, download_name='course_schedule.csv')
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 