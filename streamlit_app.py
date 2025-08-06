import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import calendar
import tempfile
import json
import io

# Page configuration
st.set_page_config(
    page_title="📚 Syllabus Calculator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3a8bfe 0%, #00d4fe 100%);
    }
</style>
""", unsafe_allow_html=True)

def get_hebrew_holidays(year):
    """Fetch Hebrew holidays from hebcal.com API"""
    try:
        url = "https://www.hebcal.com/hebcal"
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
                    holiday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    holidays.add(holiday_date)
        
        return holidays
    except Exception as e:
        st.warning(f"Warning: Could not fetch Hebrew holidays: {e}")
        return set()

def is_working_day(date, holidays):
    """Check if a date is a working day (Sunday-Thursday, not a holiday)"""
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

def calculate_schedule(syllabus_df, start_date, add_break, break_days, consider_holidays, handle_empty_days=True, default_days=1):
    """Calculate the course schedule based on the syllabus"""
    
    # Validate data before processing
    if syllabus_df.empty:
        st.error("❌ The uploaded CSV file is empty.")
        return pd.DataFrame()
    
    # Check for non-numeric values in Days column
    try:
        syllabus_df['Days'] = pd.to_numeric(syllabus_df['Days'], errors='coerce')
    except Exception as e:
        st.error(f"❌ Error processing 'Days' column: {str(e)}")
        return pd.DataFrame()
    
    # Handle empty values based on user preference
    if syllabus_df['Days'].isna().any():
        if handle_empty_days:
            # Fill empty values with default
            empty_count = syllabus_df['Days'].isna().sum()
            syllabus_df['Days'] = syllabus_df['Days'].fillna(default_days)
            st.info(f"ℹ️ Filled {empty_count} empty values in 'Days' column with {default_days} day(s) each.")
        else:
            st.error("❌ Found empty values in the 'Days' column. Please enable 'Handle empty values' option or fill the values manually.")
            return pd.DataFrame()
    
    # Get holidays if needed
    holidays = set()
    if consider_holidays:
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
                st.error(f"❌ Invalid value in 'Days' column for subtopic '{subtopic}'. Please ensure all days values are numbers.")
                return pd.DataFrame()
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

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 Syllabus Calculator</h1>
        <p>Generate course schedules with Hebrew calendar integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Info box
    with st.container():
        st.markdown("""
        <div class="info-box">
            <h3>📋 Instructions</h3>
            <ul>
                <li>Upload a CSV file with columns: <strong>Main Topic</strong>, <strong>Subtopic</strong>, <strong>Days</strong></li>
                <li>Working days: Sunday - Thursday (Friday and Saturday are weekends)</li>
                <li>Empty values in 'Days' column can be handled automatically</li>
                <li>Hebrew holidays are automatically excluded when enabled</li>
                <li>Breaks can be added after each main topic completion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # File upload
        uploaded_file = st.file_uploader(
            "📁 Upload Syllabus CSV File",
            type=['csv'],
            help="Upload a CSV file with Main Topic, Subtopic, and Days columns"
        )
        
        # Start date
        start_date = st.date_input(
            "📅 Course Start Date",
            value=datetime.now().date(),
            help="Select when your course begins"
        )
        
        # Break settings
        st.subheader("🔄 Break Settings")
        add_break = st.checkbox(
            "Add break after each main topic?",
            help="Enable to add breaks after completing each main topic"
        )
        
        break_days = st.number_input(
            "⏰ Break Duration (working days)",
            min_value=1,
            max_value=30,
            value=2,
            help="Number of working days for each break period"
        )
        
        # Data processing settings
        st.subheader("📊 Data Processing")
        handle_empty_days = st.checkbox(
            "Handle empty values in 'Days' column?",
            value=True,
            help="Automatically fill empty days with default value"
        )
        
        if handle_empty_days:
            default_days = st.number_input(
                "Default days for empty values",
                min_value=1,
                max_value=30,
                value=1,
                help="Number of days to assign when 'Days' column is empty"
            )
        
        # Holiday settings
        st.subheader("📅 Holiday Settings")
        consider_holidays = st.checkbox(
            "Consider Hebrew holidays and weekends?",
            value=True,
            help="Automatically exclude Hebrew holidays and weekends"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Syllabus Preview")
        
        if uploaded_file is not None:
            try:
                # Read and display the uploaded CSV
                syllabus_df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_columns = ['Main Topic', 'Subtopic', 'Days']
                missing_columns = [col for col in required_columns if col not in syllabus_df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                    st.info("Please ensure your CSV file contains: Main Topic, Subtopic, and Days columns")
                else:
                    st.success("✅ CSV file loaded successfully!")
                    
                    # Display preview
                    st.subheader("📋 Syllabus Structure")
                    st.dataframe(syllabus_df, use_container_width=True)
                    
                    # Check for empty values and show info
                    empty_days = syllabus_df['Days'].isna().sum()
                    if empty_days > 0:
                        st.warning(f"⚠️ Found {empty_days} empty value(s) in 'Days' column. Enable 'Handle empty values' option to process them automatically.")
                    
                    # Summary statistics
                    st.subheader("📈 Summary")
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        st.metric("Main Topics", len(syllabus_df['Main Topic'].unique()))
                    
                    with col_b:
                        st.metric("Total Subtopics", len(syllabus_df))
                    
                    with col_c:
                        # Calculate total days excluding NaN values
                        total_days = syllabus_df['Days'].sum(skipna=True)
                        st.metric("Total Days", total_days)
                    
                    with col_d:
                        st.metric("Empty Values", empty_days)
                    
                    # Generate schedule button
                    if st.button("🚀 Generate Schedule", type="primary"):
                        with st.spinner("Generating your course schedule..."):
                            try:
                                # Calculate schedule
                                schedule_df = calculate_schedule(
                                    syllabus_df, start_date, add_break, break_days, consider_holidays, 
                                    handle_empty_days, default_days if handle_empty_days else 1
                                )
                                
                                # Check if schedule was generated successfully
                                if schedule_df.empty:
                                    st.error("❌ Failed to generate schedule. Please check your data and try again.")
                                    return
                                
                                # Display results
                                st.success("✅ Schedule generated successfully!")
                                
                                # Show schedule
                                st.subheader("📅 Generated Schedule")
                                st.dataframe(schedule_df, use_container_width=True)
                                
                                # Download button
                                csv_buffer = io.StringIO()
                                schedule_df.to_csv(csv_buffer, index=False)
                                csv_str = csv_buffer.getvalue()
                                
                                st.download_button(
                                    label="📥 Download course_schedule.csv",
                                    data=csv_str,
                                    file_name="course_schedule.csv",
                                    mime="text/csv",
                                    type="primary"
                                )
                                
                                # Schedule summary
                                st.subheader("📊 Schedule Summary")
                                col_x, col_y, col_z = st.columns(3)
                                
                                with col_x:
                                    st.metric("Total Schedule Items", len(schedule_df))
                                
                                with col_y:
                                    start_date_schedule = datetime.strptime(schedule_df.iloc[0]['Start Date'], '%Y-%m-%d').date()
                                    end_date_schedule = datetime.strptime(schedule_df.iloc[-1]['End Date'], '%Y-%m-%d').date()
                                    total_days = (end_date_schedule - start_date_schedule).days + 1
                                    st.metric("Total Calendar Days", total_days)
                                
                                with col_z:
                                    working_days = schedule_df[~schedule_df['Main Topic'].str.contains('Break')]['Duration (Days)'].sum()
                                    st.metric("Total Working Days", working_days)
                                
                            except Exception as e:
                                st.error(f"❌ Error generating schedule: {str(e)}")
                
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
                st.info("Please ensure your file is a valid CSV format")
        else:
            st.info("👆 Please upload a CSV file to get started")
    
    with col2:
        st.header("📝 Sample Format")
        st.markdown("""
        Your CSV should look like this:
        
        ```csv
        Main Topic,Subtopic,Days
        Introduction to Programming,Basic Concepts,3
        Introduction to Programming,Variables and Data Types,2
        Object-Oriented Programming,Classes and Objects,3
        ```
        
        **Note**: Empty values in 'Days' column are supported and can be filled automatically.
        """)
        
        # Show sample data
        sample_data = {
            'Main Topic': ['Introduction to Programming', 'Introduction to Programming', 'OOP'],
            'Subtopic': ['Basic Concepts', 'Variables', 'Classes'],
            'Days': [3, '', 3]  # Show empty value example
        }
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
        
        # Download sample
        sample_csv = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=sample_csv,
            file_name="sample_syllabus.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 