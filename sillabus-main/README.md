# 📚 Syllabus Calculator

A powerful web application that generates course schedules with Hebrew calendar integration, automatically excluding holidays and weekends.

## 🌟 Features

- **📊 CSV Upload & Processing** - Upload syllabus files with hierarchical topic structure
- **📅 Hebrew Calendar Integration** - Automatically fetches and excludes Hebrew holidays
- **🔄 Flexible Data Handling** - Supports empty values in CSV files with automatic filling
- **⏰ Break Management** - Optional breaks after each main topic
- **🎨 Modern UI** - Beautiful, responsive web interface
- **📤 CSV Export** - Download generated schedules as CSV files

## 🚀 Quick Start

### Option 1: Use the Live App (Recommended)
Visit the live application: **[Syllabus Calculator on Streamlit Cloud](https://your-app-name.streamlit.app)**

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/syllabus-calculator.git
cd syllabus-calculator

# Install dependencies
pip install -r requirements_streamlit.txt

# Run the application
streamlit run streamlit_app.py
```

## 📋 How to Use

### 1. Prepare Your CSV File
Your syllabus CSV file must contain these columns:
- `Main Topic` - The main topic/category (can repeat for multiple subtopics)
- `Subtopic` - Specific subtopic within the main topic
- `Days` - Number of working days allocated for this subtopic

### 2. Example CSV Format
```csv
Main Topic,Subtopic,Days
Introduction to Programming,Basic Concepts,3
Introduction to Programming,Variables and Data Types,2
Object-Oriented Programming,Classes and Objects,3
```

### 3. Upload and Configure
1. **Upload your CSV file**
2. **Set the course start date**
3. **Configure options:**
   - Add breaks after main topics (optional)
   - Set break duration in working days
   - Handle empty values in 'Days' column
   - Include/exclude Hebrew holidays and weekends
4. **Generate the schedule**
5. **Download the resulting CSV file**

## 🔧 Configuration Options

### Break Settings
- **Add breaks**: Enable to add breaks after each main topic
- **Break duration**: Number of working days for each break

### Data Processing Settings
- **Handle empty values**: Automatically fill empty 'Days' values with default
- **Default days**: Number of days to assign when 'Days' column is empty

### Holiday Settings
- **Consider holidays**: When enabled, automatically excludes Hebrew holidays
- **API source**: Uses hebcal.com for Hebrew calendar data

## 📅 Working Days

- **Working days**: Sunday - Thursday
- **Weekends**: Friday and Saturday
- **Holidays**: Automatically fetched from hebcal.com API

## 📤 Output Format

The generated `course_schedule.csv` contains:

| Column | Description |
|--------|-------------|
| `Main Topic` | The main topic (or "Break" for break periods) |
| `Subtopic` | The subtopic (or "Break Period" for breaks) |
| `Start Date` | Start date in YYYY-MM-DD format |
| `End Date` | End date in YYYY-MM-DD format |
| `Duration (Days)` | Number of working days allocated |

## 🌐 API Integration

The application integrates with the [hebcal.com](https://www.hebcal.com/) API to fetch Hebrew holidays:

- **Endpoint**: `https://www.hebcal.com/hebcal`
- **Parameters**: 
  - `v=1` (version)
  - `cfg=json` (JSON format)
  - `maj=on` (major holidays)
  - `mod=on` (modern holidays)
  - `nh=on` (new holidays)
  - `d=on` (diaspora)
  - `lg=s` (language)

## 📁 Sample Files

- `sample_syllabus_fixed.csv` - Complete syllabus example
- `sample_syllabus_with_empty.csv` - Example with empty values

## 🛠️ Technical Details

### Built With
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP library for API calls
- **Python-dateutil** - Date utilities

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python with pandas for data processing
- **API**: hebcal.com for Hebrew calendar data
- **Deployment**: Streamlit Cloud

## 🔒 Security Features

- **File size limits**: Maximum 200MB file upload
- **File type validation**: Only accepts CSV files
- **Input sanitization**: Validates all user inputs
- **Error handling**: Comprehensive error management

## 🚀 Deployment

This application is deployed on [Streamlit Cloud](https://share.streamlit.io) for easy access and sharing.

### Deployment Files
- `streamlit_app.py` - Main application
- `requirements_streamlit.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `sample_syllabus_*.csv` - Example data files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [hebcal.com](https://www.hebcal.com/) for Hebrew calendar API
- [Streamlit](https://streamlit.io/) for the web framework
- [Pandas](https://pandas.pydata.org/) for data processing

## 📞 Support

If you encounter any issues:
1. Check the [documentation](DEPLOYMENT_GUIDE.md)
2. Review the [troubleshooting guide](QUICK_DEPLOY.md)
3. Open an issue on GitHub

---

**🎉 Happy scheduling! 📅✨**

*Built with ❤️ for educators and course planners* 