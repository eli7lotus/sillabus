# 🚀 Deploy Syllabus Calculator to Streamlit Cloud

This guide will help you deploy your Syllabus Calculator application to [Streamlit Cloud](https://share.streamlit.io).

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Git Repository**: Your code should be in a GitHub repository

## 🛠️ Setup Instructions

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository** or use an existing one
2. **Upload your files** to the repository:
   ```
   your-repo/
   ├── streamlit_app.py          # Main Streamlit application
   ├── requirements_streamlit.txt # Python dependencies
   ├── .streamlit/
   │   └── config.toml          # Streamlit configuration
   ├── sample_syllabus.csv      # Example data file
   └── README.md               # Project documentation
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: Select your GitHub repository
   - **Branch**: Choose `main` or `master`
   - **Main file path**: Enter `streamlit_app.py`
   - **App URL**: Choose a custom URL (optional)

5. **Click "Deploy"**

### Step 3: Wait for Deployment

- Streamlit will automatically install dependencies from `requirements_streamlit.txt`
- The first deployment may take 2-3 minutes
- You'll receive a URL like: `https://your-app-name.streamlit.app`

## 📁 Required Files

### 1. `streamlit_app.py`
The main application file with all the syllabus calculation logic.

### 2. `requirements_streamlit.txt`
```
streamlit>=1.28.0
pandas>=2.1.0
requests>=2.31.0
python-dateutil>=2.8.2
```

### 3. `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#4facfe"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## 🌟 Features of Streamlit Version

### ✅ **Enhanced UI/UX**
- **Sidebar Configuration**: All settings in a clean sidebar
- **Real-time Preview**: See your CSV data before processing
- **Interactive Elements**: Date pickers, checkboxes, number inputs
- **Progress Indicators**: Loading spinners and success messages
- **Responsive Design**: Works on desktop and mobile

### ✅ **Better Data Handling**
- **File Upload**: Drag-and-drop CSV file upload
- **Data Validation**: Automatic column validation
- **Preview Tables**: See your data before processing
- **Summary Statistics**: Quick overview of your syllabus

### ✅ **Improved Output**
- **Interactive Tables**: Sortable and searchable results
- **Download Buttons**: One-click CSV download
- **Schedule Summary**: Key metrics and statistics
- **Visual Feedback**: Clear success/error messages

## 🔧 Configuration Options

### **File Upload**
- Supports CSV files up to 200MB
- Automatic column validation
- Preview before processing

### **Date Settings**
- Date picker for course start date
- Defaults to current date
- Validates date ranges

### **Break Settings**
- Toggle to enable/disable breaks
- Configurable break duration (1-30 days)
- Applied after each main topic

### **Holiday Settings**
- Toggle Hebrew holiday consideration
- Automatic weekend exclusion (Friday/Saturday)
- Real-time holiday fetching from hebcal.com

## 📊 Sample Data

Include `sample_syllabus.csv` in your repository:

```csv
Main Topic,Subtopic,Days
Introduction to Programming,Basic Concepts,3
Introduction to Programming,Variables and Data Types,2
Introduction to Programming,Control Structures,4
Object-Oriented Programming,Classes and Objects,3
Object-Oriented Programming,Inheritance,2
Object-Oriented Programming,Polymorphism,3
```

## 🚀 Deployment Tips

### **Best Practices**
1. **Keep dependencies minimal**: Only include necessary packages
2. **Use specific versions**: Avoid `>=` in requirements for production
3. **Test locally first**: Run `streamlit run streamlit_app.py` locally
4. **Monitor logs**: Check Streamlit Cloud logs for any issues

### **Common Issues**
- **Import errors**: Ensure all dependencies are in requirements file
- **File size limits**: Keep CSV files under 200MB
- **API timeouts**: Handle network errors gracefully
- **Memory limits**: Optimize for Streamlit's memory constraints

### **Performance Optimization**
- **Caching**: Use `@st.cache_data` for expensive operations
- **Lazy loading**: Load data only when needed
- **Error handling**: Graceful degradation for API failures

## 🔄 Updates and Maintenance

### **Updating Your App**
1. **Push changes** to your GitHub repository
2. **Streamlit automatically redeploys** (may take a few minutes)
3. **Check the new version** at your app URL

### **Monitoring**
- **View logs** in Streamlit Cloud dashboard
- **Check usage statistics** and performance
- **Monitor API calls** to hebcal.com

## 🌐 Public Sharing

Once deployed, you can:
- **Share the URL** with others
- **Embed in websites** using iframes
- **Use as a web service** for syllabus planning
- **Integrate with other tools** via the web interface

## 📞 Support

If you encounter issues:
1. **Check Streamlit documentation**: [docs.streamlit.io](https://docs.streamlit.io)
2. **Review deployment logs** in Streamlit Cloud
3. **Test locally** to isolate issues
4. **Check GitHub issues** for common problems

---

**🎉 Your Syllabus Calculator is now live on Streamlit Cloud!**

Share your app URL and help others create better course schedules with Hebrew calendar integration. 