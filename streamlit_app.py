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

    /* Streamlit specific elements */
    .stApp {
        font-family: 'Roboto', sans-serif !important;
    }

    .stMarkdown {
        font-family: 'Roboto', sans-serif !important;
    }

    .stText {
        font-family: 'Roboto', sans-serif !important;
    }

    .stDataFrame {
        font-family: 'Roboto', sans-serif !important;
    }

    .stMetric {
        font-family: 'Roboto', sans-serif !important;
    }

    .stButton {
        font-family: 'Roboto', sans-serif !important;
    }

    .stDownloadButton {
        font-family: 'Roboto', sans-serif !important;
    }

    .stDateInput {
        font-family: 'Roboto', sans-serif !important;
    }

    .stNumberInput {
        font-family: 'Roboto', sans-serif !important;
    }

    .stCheckbox {
        font-family: 'Roboto', sans-serif !important;
    }

    .stSelectbox {
        font-family: 'Roboto', sans-serif !important;
    }

    .stFileUploader {
        font-family: 'Roboto', sans-serif !important;
    }

    .stSidebar {
        font-family: 'Roboto', sans-serif !important;
    }

    .stAlert {
        font-family: 'Roboto', sans-serif !important;
    }

    .stSuccess {
        font-family: 'Roboto', sans-serif !important;
    }

    .stError {
        font-family: 'Roboto', sans-serif !important;
    }

    .stWarning {
        font-family: 'Roboto', sans-serif !important;
    }

    .stInfo {
        font-family: 'Roboto', sans-serif !important;
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

    /* Summary section metrics styling */
    .summary-metrics .stMetric {
        padding: 0.1875rem;
        min-height: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transform: scale(0.25);
        transform-origin: center;
    }

    .summary-metrics .stMetric > div {
        font-size: 25% !important;
        line-height: 0.8;
    }

    .summary-metrics .stMetric label {
        font-size: 25% !important;
        line-height: 0.8;
        margin-bottom: 0.0625rem;
        max-height: 0.8em;
        overflow: hidden;
    }

    .summary-metrics .stMetric [data-testid="metric-container"] {
        font-size: 25% !important;
        line-height: 0.8;
    }

    .summary-metrics .stMetric [data-testid="metric-container"] > div {
        font-size: 25% !important;
        line-height: 0.8;
    }

    .summary-metrics .stMetric [data-testid="metric-container"] label {
        font-size: 25% !important;
        line-height: 0.8;
        max-height: 0.8em;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
    }

    .summary-metrics .stMetric [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 25% !important;
        line-height: 0.8;
        max-height: 0.8em;
        overflow: hidden;
    }

    /* Override Streamlit metric value font size */
    .st-emotion-cache-1rrh444 {
        font-size: 1.5rem !important;
        color: rgb(38, 39, 48);
        padding-bottom: 0.25rem;
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
        color: white !important;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        font-family: 'Roboto', sans-serif;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .stDownloadButton > button *,
    .stButton > button * {
        color: white !important;
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

def calculate_schedule_stats(schedule_df, start_date, end_date, consider_holidays, additional_free_days=None):
    """Calculate additional statistics for the schedule"""
    stats = {}
    
    # Calculate break days
    break_days = schedule_df[schedule_df['Main Topic'].str.contains('Break')]['Duration (Days)'].sum()
    stats['break_days'] = break_days
    
    # Calculate holiday days and get holiday list
    holiday_days = 0
    holiday_list = []
    if consider_holidays:
        # Get Hebrew holidays for the schedule period
        holidays = set()
        holiday_names = {}
        
        for year in range(start_date.year, end_date.year + 1):
            year_holidays = get_hebrew_holidays(year)
            holidays.update(year_holidays)
            
            # Get holiday names for this year
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
                for item in data.get('items', []):
                    if item.get('category') in ['holiday', 'roshchodesh']:
                        date_str = item.get('date')
                        if date_str:
                            holiday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                            holiday_names[holiday_date] = item.get('title', 'Unknown Holiday')
            except:
                pass
        
        # Add additional free days
        if additional_free_days:
            holidays.update(additional_free_days)
            for date in additional_free_days:
                holiday_names[date] = "Additional Free Day"
        
        # Count holidays and build list
        current_date = start_date
        while current_date <= end_date:
            if current_date in holidays:
                holiday_days += 1
                holiday_name = holiday_names.get(current_date, "Unknown Holiday")
                holiday_list.append(f"{holiday_name} - {current_date.strftime('%Y-%m-%d')}")
            current_date += timedelta(days=1)
    
    stats['holiday_days'] = holiday_days
    stats['holiday_list'] = holiday_list
    
    # Calculate Fridays and Saturdays
    friday_saturday_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in [4, 5]:  # Friday = 4, Saturday = 5
            friday_saturday_days += 1
        current_date += timedelta(days=1)
    
    stats['friday_saturday_days'] = friday_saturday_days
    
    return stats

def calculate_exam_dates(schedule_df, syllabus_df):
    """Calculate exam dates for each main topic that contains 'exam' or 'milestone'"""
    exam_dates = []
    
    # Get unique main topics from syllabus (excluding breaks)
    main_topics = syllabus_df['Main Topic'].unique()
    
    for topic in main_topics:
        # Only include topics that contain 'exam' or 'milestone' (case insensitive)
        if 'exam' in topic.lower() or 'milestone' in topic.lower():
            # Find the last subtopic for this main topic in the schedule
            topic_schedule = schedule_df[schedule_df['Main Topic'] == topic]
            
            if not topic_schedule.empty:
                # Get the end date of the last subtopic for this topic
                last_row = topic_schedule.iloc[-1]
                end_date = datetime.strptime(last_row['End Date'], '%Y-%m-%d').date()
                
                # Exam is typically 1-2 working days after the topic ends
                exam_date = get_next_working_day(end_date + timedelta(days=1), set())
                
                exam_dates.append({
                    'Main Topic': topic,
                    'Exam Date': exam_date.strftime('%Y-%m-%d'),
                    'Day of Week': exam_date.strftime('%A')
                })
    
    return exam_dates

def add_colors_to_schedule(schedule_df):
    """Add light background colors to schedule dataframe based on main topics"""
    # Define light colors for different topics
    light_colors = [
        '#f0f8ff',  # Light blue
        '#f0fff0',  # Light green
        '#fff0f0',  # Light red
        '#f0f0ff',  # Light purple
        '#fffff0',  # Light yellow
        '#f0ffff',  # Light cyan
        '#fff8f0',  # Light orange
        '#f8f0ff',  # Light lavender
        '#f0fff8',  # Light mint
        '#fff0f8',  # Light pink
    ]
    
    # Get unique main topics (excluding breaks)
    main_topics = []
    for topic in schedule_df['Main Topic']:
        if 'Break' not in topic and topic not in main_topics:
            main_topics.append(topic)
    
    # Create color mapping
    color_mapping = {}
    for i, topic in enumerate(main_topics):
        color_mapping[topic] = light_colors[i % len(light_colors)]
    
    # Apply colors and formatting to dataframe
    def format_rows(row):
        topic = row['Main Topic']
        if 'Break' in topic:
            # For breaks, use the same color as the main topic
            base_topic = topic.replace(' - Break', '')
            color = color_mapping.get(base_topic, '#f5f5f5')
        else:
            color = color_mapping.get(topic, '#f5f5f5')
        
        # Create styling for each column
        styles = []
        for col in row.index:
            if col == 'Main Topic':
                # Bold text for Main Topic column
                styles.append(f'background-color: {color}; font-weight: bold;')
            else:
                # Regular styling for other columns
                styles.append(f'background-color: {color};')
        
        return styles
    
    return schedule_df.style.apply(format_rows, axis=1)

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
    
    # Summary section - will be populated when file is uploaded
    if uploaded_file is not None:
        # This will be populated when file is uploaded
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
                                    
                                    # Summary section - combined statistics
                                    st.header("📊 Summary")
                                    
                                    # Calculate all statistics
                                    start_date_schedule = datetime.strptime(schedule_df.iloc[0]['Start Date'], '%Y-%m-%d').date()
                                    end_date_schedule = datetime.strptime(schedule_df.iloc[-1]['End Date'], '%Y-%m-%d').date()
                                    total_calendar_days = (end_date_schedule - start_date_schedule).days + 1
                                    working_days = schedule_df[~schedule_df['Main Topic'].str.contains('Break')]['Duration (Days)'].sum()
                                    
                                    # Get additional stats
                                    additional_stats = calculate_schedule_stats(
                                        schedule_df, start_date_schedule, end_date_schedule, 
                                        consider_holidays, additional_free_days if additional_free_days else None
                                    )
                                    
                                    # Calculate exam dates
                                    exam_dates = calculate_exam_dates(schedule_df, syllabus_df)
                                    
                                    # Display combined statistics in landscape layout
                                    st.markdown('<div class="summary-metrics">', unsafe_allow_html=True)
                                    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                                    
                                    with col1:
                                        st.metric("📅 Start Date", start_date_schedule.strftime('%Y-%m-%d'))
                                    
                                    with col2:
                                        st.metric("📅 End Date", end_date_schedule.strftime('%Y-%m-%d'))
                                    
                                    with col3:
                                        st.metric("📅 Calendar Days", total_calendar_days)
                                    
                                    with col4:
                                        st.metric("⏱️ Total Days", syllabus_df['Days'].sum(skipna=True))
                                    
                                    with col5:
                                        st.metric("⏸️ Break Days", additional_stats['break_days'])
                                    
                                    with col6:
                                        # Holiday Days with tooltip
                                        holiday_tooltip = ""
                                        if additional_stats.get('holiday_list'):
                                            holiday_tooltip = "\n".join(additional_stats['holiday_list'])
                                        else:
                                            holiday_tooltip = "No holidays in this period"
                                        
                                        st.metric(
                                            "🎉 Holiday Days", 
                                            additional_stats['holiday_days'],
                                            help=holiday_tooltip
                                        )
                                    
                                    with col7:
                                        st.metric("📅 Fridays/Saturdays", additional_stats['friday_saturday_days'])
                                    
                                    with col8:
                                        st.metric("📚 Main Topics", len(syllabus_df['Main Topic'].unique()))
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Display exam dates if available
                                    if exam_dates:
                                        st.subheader("📝 Exam Schedule")
                                        st.markdown('<div class="summary-metrics">', unsafe_allow_html=True)
                                        exam_cols = st.columns(len(exam_dates))
                                        
                                        for i, exam in enumerate(exam_dates):
                                            with exam_cols[i]:
                                                st.metric(
                                                    exam['Main Topic'],
                                                    exam['Exam Date'],
                                                    exam['Day of Week']
                                                )
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Show schedule with colors
                                    st.subheader("📋 Generated Schedule")
                                    colored_schedule = add_colors_to_schedule(schedule_df)
                                    st.dataframe(colored_schedule, use_container_width=True)
                                    
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
                                    

                                
                            except Exception as e:
                                st.error(f"⚠️ Error generating schedule: {str(e)}")
                    
                    # Display existing schedule if available
                    elif 'schedule_df' in st.session_state and st.session_state.schedule_df is not None:
                        schedule_df = st.session_state.schedule_df
                        
                        # Summary section - combined statistics
                        st.header("📊 Summary")
                        
                        # Calculate all statistics
                        start_date_schedule = datetime.strptime(schedule_df.iloc[0]['Start Date'], '%Y-%m-%d').date()
                        end_date_schedule = datetime.strptime(schedule_df.iloc[-1]['End Date'], '%Y-%m-%d').date()
                        total_calendar_days = (end_date_schedule - start_date_schedule).days + 1
                        working_days = schedule_df[~schedule_df['Main Topic'].str.contains('Break')]['Duration (Days)'].sum()
                        
                        # Get additional stats
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
                        
                        additional_stats = calculate_schedule_stats(
                            schedule_df, start_date_schedule, end_date_schedule, 
                            consider_holidays, additional_free_days if additional_free_days else None
                        )
                        
                        # Calculate exam dates
                        exam_dates = calculate_exam_dates(schedule_df, syllabus_df)
                        
                        # Display combined statistics in landscape layout
                        st.markdown('<div class="summary-metrics">', unsafe_allow_html=True)
                        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                        
                        with col1:
                            st.metric("📅 Start Date", start_date_schedule.strftime('%Y-%m-%d'))
                        
                        with col2:
                            st.metric("📅 End Date", end_date_schedule.strftime('%Y-%m-%d'))
                        
                        with col3:
                            st.metric("📅 Calendar Days", total_calendar_days)
                        
                        with col4:
                            st.metric("⏱️ Total Days", syllabus_df['Days'].sum(skipna=True))
                        
                        with col5:
                            st.metric("⏸️ Break Days", additional_stats['break_days'])
                        
                        with col6:
                            # Holiday Days with tooltip
                            holiday_tooltip = ""
                            if additional_stats.get('holiday_list'):
                                holiday_tooltip = "\n".join(additional_stats['holiday_list'])
                            else:
                                holiday_tooltip = "No holidays in this period"
                            
                            st.metric(
                                "🎉 Holiday Days", 
                                additional_stats['holiday_days'],
                                help=holiday_tooltip
                            )
                        
                        with col7:
                            st.metric("📅 Fridays/Saturdays", additional_stats['friday_saturday_days'])
                        
                        with col8:
                            st.metric("📚 Main Topics", len(syllabus_df['Main Topic'].unique()))
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display exam dates if available
                        if exam_dates:
                            st.subheader("📝 Exam Schedule")
                            st.markdown('<div class="summary-metrics">', unsafe_allow_html=True)
                            exam_cols = st.columns(len(exam_dates))
                            
                            for i, exam in enumerate(exam_dates):
                                with exam_cols[i]:
                                    st.metric(
                                        exam['Main Topic'],
                                        exam['Exam Date'],
                                        exam['Day of Week']
                                    )
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Show schedule with colors
                        st.subheader("📋 Generated Schedule")
                        colored_schedule = add_colors_to_schedule(schedule_df)
                        st.dataframe(colored_schedule, use_container_width=True)
                        
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
                        

                
            except Exception as e:
                st.error(f"⚠️ Error reading CSV file: {str(e)}")
                st.info("Please ensure your file is a valid CSV format")
        else:
            st.info("📁 Please upload a CSV file to get started")
    


if __name__ == "__main__":
    main() 