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
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Modern color palette and variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        --secondary-gradient: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
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

    /* Global font family */
    * {
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
    }

    /* Global styles */
    .main {
        background: var(--bg-color);
        padding: 2rem 0;
    }

    /* Modern header with clean and compact design */
    .main-header {
        background: var(--primary-gradient);
        padding: 0.75rem 2rem;
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
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 2;
        letter-spacing: -0.01em;
        font-family: 'Roboto', sans-serif;
    }

    .main-header h1 small {
        font-size: 1.2rem;
        opacity: 1;
        font-weight: 400;
        letter-spacing: 0.01em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
        margin-left: 0.5rem;
    }

    .main-header p {
        font-size: 0.85rem;
        opacity: 1;
        position: relative;
        z-index: 2;
        font-weight: 400;
        letter-spacing: 0.01em;
        margin-bottom: 0;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
        display: inline-block;
        vertical-align: middle;
    }

    /* Responsive header */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.6rem 1rem;
            border-radius: 12px;
        }
        
        .main-header h1 {
            font-size: 1.3rem;
        }
        
        .main-header p {
            font-size: 0.75rem;
        }
    }

    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 1.1rem;
        }
        
        .main-header p {
            font-size: 0.7rem;
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

    /* Modern buttons with header design */
    .stDownloadButton > button,
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        letter-spacing: -0.01em;
        font-family: 'Roboto', sans-serif;
    }

    .stDownloadButton > button::before,
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        z-index: 1;
    }

    .stDownloadButton > button > span,
    .stButton > button > span {
        position: relative;
        z-index: 2;
    }

    .stDownloadButton > button:hover,
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: var(--secondary-gradient);
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
        .main-header {
            padding: 0.6rem 1rem;
            border-radius: 12px;
        }
        
        .main-header h1 {
            font-size: 1.3rem;
            display: block;
        }
        
        .main-header h1 small {
            font-size: 1rem;
            display: block;
            margin-left: 0;
            margin-top: 0.25rem;
        }
    }

    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 1.1rem;
        }
        
        .main-header h1 small {
            font-size: 0.9rem;
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

def calculate_schedule(syllabus_df, start_date, add_break, break_days, consider_holidays, additional_free_days=None):
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
    
    # Handle empty values - always fill with 0
    if syllabus_df['Days'].isna().any():
        syllabus_df['Days'] = syllabus_df['Days'].fillna(0)
    
    # Get holidays if needed
    holidays = set()
    if consider_holidays:
        current_year = start_date.year
        holidays = get_hebrew_holidays(current_year)
        holidays.update(get_hebrew_holidays(current_year + 1))
    
    # Add additional free days
    if additional_free_days:
        holidays.update(additional_free_days)
    
    schedule_data = []
    current_date = start_date
    
    # Process rows in original order from CSV file
    for index, row in syllabus_df.iterrows():
        main_topic = row['Main Topic']
        subtopic = row['Subtopic']
        
        # Check if this is a new main topic (first occurrence)
        is_new_main_topic = True
        for prev_row in schedule_data:
            if prev_row['Main Topic'] == main_topic:
                is_new_main_topic = False
                break
        
        # Handle NaN values and convert to integer
        days_value = row['Days']
        if pd.isna(days_value):
            st.error(f"❌ Invalid value in 'Days' column for subtopic '{subtopic}'. Please ensure all days values are numbers.")
            return pd.DataFrame()
        days_needed = int(days_value)
        
        # Find the next working day to start
        if is_new_main_topic:
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
        
        # Add break after each main topic if enabled (only after the last subtopic of the topic)
        if add_break and break_days > 0:
            # Check if this is the last subtopic of the current main topic
            is_last_subtopic = True
            for next_index in range(index + 1, len(syllabus_df)):
                if syllabus_df.iloc[next_index]['Main Topic'] == main_topic:
                    is_last_subtopic = False
                    break
            
            if is_last_subtopic:
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
        <h1>📋 Syllabus Calculator. <small>Generate course schedules with Hebrew calendar integration</small></h1>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section - full width
    with st.container():
        # File upload with full width
        uploaded_file = st.file_uploader(
            "Upload Your Syllabus",
            type=['csv'],
            help="Upload a CSV file with Main Topic, Subtopic, and Days columns.",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: **{uploaded_file.name}**")
    
    # Quick Stats section - landscape below instructions
    st.header("📊 Quick Stats")
    
    # Create landscape layout for stats
    col_a, col_b, col_c = st.columns(3)
    
    if uploaded_file is None:
        with col_a:
            st.metric("📚 Main Topics", "0")
        with col_b:
            st.metric("📝 Total Subtopics", "0")
        with col_c:
            st.metric("⏱️ Total Days", "0")
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
        st.subheader("⏸️ Break Settings")
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
        
        # Holiday settings
        st.subheader("🎉 Holiday Settings")
        consider_holidays = st.checkbox(
            "Consider Hebrew holidays and weekends?",
            value=True,
            help="Automatically exclude Hebrew holidays and weekends"
        )
        
        # Additional Free Days section
        st.subheader("🏖️ Additional Free Days")
        st.info("Add custom free days that will be excluded from the schedule")
        
        # Date range option
        use_date_range = st.checkbox(
            "Add date range?",
            help="Select a range of dates to exclude"
        )
        
        date_range_start = None
        date_range_end = None
        if use_date_range:
            col_range1, col_range2 = st.columns(2)
            with col_range1:
                date_range_start = st.date_input(
                    "From",
                    help="Start date of free period"
                )
            with col_range2:
                date_range_end = st.date_input(
                    "To",
                    help="End date of free period"
                )
        
        # Single dates option
        use_single_dates = st.checkbox(
            "Add single dates?",
            help="Select individual dates to exclude"
        )
        
        single_dates = []
        if use_single_dates:
            num_single_dates = st.number_input(
                "Number of single dates",
                min_value=1,
                max_value=10,
                value=1,
                help="How many individual dates to add"
            )
            
            for i in range(num_single_dates):
                single_date = st.date_input(
                    f"Free Date {i+1}",
                    help=f"Select free date {i+1}"
                )
                single_dates.append(single_date)
        

    
    # Main content area
    with st.container():
        st.header("📊 Course Schedule")
        
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
                    

                    
                    # Update Quick Stats with actual data
                    with col_a:
                        st.metric("📚 Main Topics", len(syllabus_df['Main Topic'].unique()))
                    
                    with col_b:
                        st.metric("📝 Total Subtopics", len(syllabus_df))
                    
                    with col_c:
                        # Calculate total days excluding NaN values
                        total_days = syllabus_df['Days'].sum(skipna=True)
                        st.metric("⏱️ Total Days", total_days)
                    
                    # Create a hash of current parameters to detect changes
                    current_params_hash = hash((
                        str(start_date),
                        str(add_break),
                        str(break_days),
                        str(consider_holidays),
                        str(use_date_range),
                        str(date_range_start),
                        str(date_range_end),
                        str(use_single_dates),
                        str(single_dates)
                    ))
                    
                    # Check if we need to regenerate schedule
                    regenerate_needed = (
                        uploaded_file is not None and 
                        ('schedule_df' not in st.session_state or
                         st.session_state.get('params_hash') != current_params_hash)
                    )
                    
                    if regenerate_needed:
                        # Generate schedule automatically
                        with st.spinner("🔄 Generating schedule..."):
                            try:
                                # Prepare additional free days
                                additional_free_days = set()
                                
                                # Add date range if specified
                                if use_date_range and date_range_start and date_range_end:
                                    current_date_range = date_range_start
                                    while current_date_range <= date_range_end:
                                        additional_free_days.add(current_date_range)
                                        current_date_range += timedelta(days=1)
                                
                                # Add single dates if specified
                                if use_single_dates and single_dates:
                                    for single_date in single_dates:
                                        if single_date:
                                            additional_free_days.add(single_date)
                                
                                # Calculate schedule
                                schedule_df = calculate_schedule(
                                    syllabus_df, start_date, add_break, break_days, consider_holidays, 
                                    additional_free_days if additional_free_days else None
                                )
                                
                                # Check if schedule was generated successfully
                                if schedule_df.empty:
                                    st.error("❌ Failed to generate schedule. Please check your data and try again.")
                                else:
                                    # Save schedule and parameters to session state
                                    st.session_state.schedule_df = schedule_df
                                    st.session_state.params_hash = current_params_hash
                                    
                                    # Display results
                                    st.success("🎉 Schedule generated successfully!")
                                    
                                    # Show additional free days info
                                    if additional_free_days:
                                        st.info(f"🏖️ Excluded {len(additional_free_days)} additional free day(s) from the schedule")
                                    
                                    # Show schedule
                                    st.subheader("📋 Generated Schedule")
                                    st.dataframe(schedule_df, use_container_width=True)
                                    
                                    # Download button
                                    csv_buffer = io.StringIO()
                                    schedule_df.to_csv(csv_buffer, index=False)
                                    csv_str = csv_buffer.getvalue()
                                    
                                    st.download_button(
                                        label="⬇️ Download course_schedule.csv",
                                        data=csv_str,
                                        file_name="course_schedule.csv",
                                        mime="text/csv",
                                        type="primary"
                                    )
                                    
                                    # Schedule summary
                                    st.subheader("📈 Schedule Summary")
                                    col_x, col_y, col_z = st.columns(3)
                                    
                                    with col_x:
                                        st.metric("📋 Total Schedule Items", len(schedule_df))
                                    
                                    with col_y:
                                        start_date_schedule = datetime.strptime(schedule_df.iloc[0]['Start Date'], '%Y-%m-%d').date()
                                        end_date_schedule = datetime.strptime(schedule_df.iloc[-1]['End Date'], '%Y-%m-%d').date()
                                        total_days = (end_date_schedule - start_date_schedule).days + 1
                                        st.metric("📅 Total Calendar Days", total_days)
                                    
                                    with col_z:
                                        working_days = schedule_df[~schedule_df['Main Topic'].str.contains('Break')]['Duration (Days)'].sum()
                                        st.metric("⏱️ Total Working Days", working_days)
                                
                            except Exception as e:
                                st.error(f"⚠️ Error generating schedule: {str(e)}")
                    
                    # Display existing schedule if available
                    elif 'schedule_df' in st.session_state and st.session_state.schedule_df is not None:
                        schedule_df = st.session_state.schedule_df
                        
                        # Show schedule
                        st.subheader("📋 Generated Schedule")
                        st.dataframe(schedule_df, use_container_width=True)
                        
                        # Download button
                        csv_buffer = io.StringIO()
                        schedule_df.to_csv(csv_buffer, index=False)
                        csv_str = csv_buffer.getvalue()
                        
                        st.download_button(
                            label="⬇️ Download course_schedule.csv",
                            data=csv_str,
                            file_name="course_schedule.csv",
                            mime="text/csv",
                            type="primary"
                        )
                        
                        # Schedule summary
                        st.subheader("📈 Schedule Summary")
                        col_x, col_y, col_z = st.columns(3)
                        
                        with col_x:
                            st.metric("📋 Total Schedule Items", len(schedule_df))
                        
                        with col_y:
                            start_date_schedule = datetime.strptime(schedule_df.iloc[0]['Start Date'], '%Y-%m-%d').date()
                            end_date_schedule = datetime.strptime(schedule_df.iloc[-1]['End Date'], '%Y-%m-%d').date()
                            total_days = (end_date_schedule - start_date_schedule).days + 1
                            st.metric("📅 Total Calendar Days", total_days)
                        
                        with col_z:
                            working_days = schedule_df[~schedule_df['Main Topic'].str.contains('Break')]['Duration (Days)'].sum()
                            st.metric("⏱️ Total Working Days", working_days)
                
            except Exception as e:
                st.error(f"⚠️ Error reading CSV file: {str(e)}")
                st.info("Please ensure your file is a valid CSV format")
        else:
            st.info("📁 Please upload a CSV file to get started")
    


if __name__ == "__main__":
    main() 