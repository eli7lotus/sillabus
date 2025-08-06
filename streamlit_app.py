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

# Custom CSS for modern and beautiful styling
st.markdown("""
<style>
    /* Modern color palette and variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --bg-color: #f8fafc;
        --card-bg: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Global styles */
    .main {
        background: var(--bg-color);
        padding: 2rem 0;
    }

    /* Modern header with clean and compact design */
    .main-header {
        background: var(--primary-gradient);
        padding: 2rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 2;
        letter-spacing: -0.01em;
    }

    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        position: relative;
        z-index: 2;
        font-weight: 400;
        letter-spacing: 0.01em;
        margin-bottom: 0;
    }

    /* Responsive header */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
            border-radius: 12px;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
    }

    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main-header p {
            font-size: 0.9rem;
        }
    }

    /* Modern card styling */
    .stExpander {
        background: var(--card-bg);
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
        overflow: hidden;
    }

    .stExpander > div[data-testid="stExpander"] {
        border: none;
        background: transparent;
    }

    /* Modern button styling */
    .stButton > button {
        background: var(--accent-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #3a8bfe 0%, #00d4fe 100%);
    }

    /* Modern metric cards */
    .stMetric {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        transition: transform 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    /* Modern file uploader */
    .stFileUploader {
        background: var(--card-bg);
        border-radius: 12px;
        border: 2px dashed var(--border-color);
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }

    /* Modern sidebar */
    .css-1d391kg {
        background: var(--card-bg);
        border-right: 1px solid var(--border-color);
    }

    .css-1d391kg .stSidebar {
        background: var(--card-bg);
        padding: 2rem 1rem;
    }

    /* Modern dataframe */
    .stDataFrame {
        background: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        overflow: hidden;
    }

    /* Modern info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: var(--shadow);
    }

    /* Success message styling */
    .stAlert[data-testid="stAlert"]:has(div[data-testid="stAlert"]:contains("✅")) {
        background: var(--success-gradient);
        color: white;
    }

    /* Error message styling */
    .stAlert[data-testid="stAlert"]:has(div[data-testid="stAlert"]:contains("❌")) {
        background: var(--warning-gradient);
        color: white;
    }

    /* Modern code blocks */
    .stCodeBlock {
        background: #1e293b;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: var(--shadow);
    }

    /* Modern download button */
    .stDownloadButton > button {
        background: var(--success-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    /* Modern date input */
    .stDateInput > div > div {
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }

    /* Modern number input */
    .stNumberInput > div > div {
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }

    /* Modern checkbox */
    .stCheckbox > div {
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }

    .stCheckbox > div:hover {
        background: rgba(102, 126, 234, 0.05);
    }

    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 600;
    }

    p, li {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-color);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }

    /* Animation for page load */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main-header, .stExpander, .stMetric {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
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

def calculate_schedule(syllabus_df, start_date, add_break, break_days, consider_holidays, handle_empty_days=True):
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
            syllabus_df['Days'] = syllabus_df['Days'].fillna(0) # Changed to 0
            st.info(f"ℹ️ Filled {empty_count} empty values in 'Days' column with 0 day(s) each.")
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
    
    # Info box with expandable instructions
    with st.container():
        with st.expander("📋 Instructions", expanded=False):
            st.markdown("""
            **Required CSV Format:**
            - Upload a CSV file with columns: **Main Topic**, **Subtopic**, **Days**
            - Working days: Sunday - Thursday (Friday and Saturday are weekends)
            - Empty values in 'Days' column are automatically filled with 0
            - Hebrew holidays are automatically excluded when enabled
            - Breaks can be added after each main topic completion
            """)
        
        # Sample Format expander in instructions section
        with st.expander("📝 Sample Format", expanded=False):
            st.markdown("### Required Columns:")
            st.markdown("""
            - **Main Topic**: The main subject or module name
            - **Subtopic**: Specific topics within the main topic  
            - **Days**: Number of working days needed for each subtopic
            """)
            
            st.markdown("### Example CSV Content:")
            st.code("""
Main Topic,Subtopic,Days
Introduction to Programming,Basic Concepts,3
Introduction to Programming,Variables and Data Types,2
Introduction to Programming,Control Structures,4
Object-Oriented Programming,Classes and Objects,3
Object-Oriented Programming,Inheritance,2
Object-Oriented Programming,Polymorphism,3
            """, language="csv")
            
            st.markdown("### 💡 Tips:")
            st.markdown("""
            - Empty values in 'Days' column are automatically filled with 0
            - You can have multiple subtopics under the same main topic
            - Working days exclude weekends (Friday/Saturday) and Hebrew holidays
            - Breaks can be added automatically after each main topic
            """)
            
            # Create sample data for download
            sample_data = {
                'Main Topic': [
                    'Introduction to Programming',
                    'Introduction to Programming', 
                    'Introduction to Programming',
                    'Object-Oriented Programming',
                    'Object-Oriented Programming',
                    'Object-Oriented Programming'
                ],
                'Subtopic': [
                    'Basic Concepts',
                    'Variables and Data Types',
                    'Control Structures', 
                    'Classes and Objects',
                    'Inheritance',
                    'Polymorphism'
                ],
                'Days': [3, 2, 4, 3, 2, 3]
            }
            sample_df = pd.DataFrame(sample_data)
            
            # Download button for sample
            sample_csv = sample_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Sample CSV",
                data=sample_csv,
                file_name="sample_syllabus.csv",
                mime="text/csv",
                type="primary"
            )
    
    # File upload (moved before Quick Stats to avoid UnboundLocalError)
    uploaded_file = st.file_uploader(
        "📁 Upload Syllabus CSV File",
        type=['csv'],
        help="Upload a CSV file with Main Topic, Subtopic, and Days columns"
    )
    
    # Quick Stats section - landscape below instructions
    st.header("📊 Quick Stats")
    
    # Create landscape layout for stats
    col_a, col_b, col_c, col_d = st.columns(4)
    
    if uploaded_file is None:
        with col_a:
            st.metric("Main Topics", "0")
        with col_b:
            st.metric("Total Subtopics", "0")
        with col_c:
            st.metric("Total Days", "0")
        with col_d:
            st.metric("Empty Values", "0")
    else:
        # These will be populated when file is uploaded
        pass
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
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
            help="Automatically fill empty days with 0"
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
                    
                    # Update Quick Stats with actual data
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
                                    handle_empty_days
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
        st.header("📊 Additional Info")
        st.info("""
        **💡 Quick Tips:**
        
        • Upload your CSV file to see live statistics
        • Use the sidebar to configure your schedule settings
        • Hebrew holidays are automatically excluded when enabled
        • Breaks can be added between main topics
        • Empty values in 'Days' column are filled with 0
        """)
        
        # Show current date and time
        st.subheader("🕐 Current Time")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"**Date:** {current_time}")
        
        # Show app version
        st.subheader("📱 App Info")
        st.write("**Version:** 2.0")
        st.write("**Features:** Hebrew Calendar Integration")

if __name__ == "__main__":
    main() 