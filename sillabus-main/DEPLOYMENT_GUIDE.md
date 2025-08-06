# 🚀 Deployment Guide: Syllabus Calculator

This guide covers deployment options for both Flask and Streamlit versions of the Syllabus Calculator application.

## 📋 Quick Start Options

### Option 1: Streamlit Cloud (Recommended) ⭐
- **Easiest deployment**
- **Free hosting**
- **Automatic updates**
- **No server management**

### Option 2: Flask with Traditional Hosting
- **More control**
- **Custom domain**
- **Production-ready**

## 🌟 Streamlit Cloud Deployment

### Prerequisites
1. **GitHub Account** - [github.com](https://github.com)
2. **Streamlit Account** - [share.streamlit.io](https://share.streamlit.io)

### Step-by-Step Instructions

#### 1. Prepare Your Repository
```bash
# Create a new GitHub repository
# Upload these files to your repo:
├── streamlit_app.py          # Main application
├── requirements_streamlit.txt # Dependencies
├── .streamlit/
│   └── config.toml          # Configuration
├── sample_syllabus_fixed.csv # Example data
└── README.md                # Documentation
```

#### 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - **Repository**: Your GitHub repo
   - **Branch**: `main` or `master`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose custom name (optional)
5. Click "Deploy"

#### 3. Wait for Deployment
- First deployment: 2-3 minutes
- Automatic dependency installation
- URL format: `https://your-app-name.streamlit.app`

### Required Files for Streamlit

#### `streamlit_app.py`
Complete Streamlit application with:
- File upload handling
- Data validation
- Error handling
- Hebrew calendar integration
- Schedule generation

#### `requirements_streamlit.txt`
```
streamlit>=1.28.0
pandas>=2.1.0
requests>=2.31.0
python-dateutil>=2.8.2
```

#### `.streamlit/config.toml`
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

## 🔧 Flask Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:5000
```

### Production Deployment Options

#### Option A: Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Add to `requirements.txt`:
   ```
   gunicorn==20.1.0
   ```
3. Deploy to Heroku

#### Option B: DigitalOcean App Platform
1. Connect GitHub repository
2. Select Python environment
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn app:app`

#### Option C: AWS/GCP/Azure
- Use container deployment
- Set up load balancer
- Configure environment variables

## 🛠️ Troubleshooting

### Common Issues

#### 1. "cannot convert float NaN to integer"
**Cause**: Empty or non-numeric values in CSV
**Solution**: 
- Enable "Handle empty values" option in the app
- Use `sample_syllabus_with_empty.csv` as template
- Set default days for empty values
- Check for empty cells in Excel/Google Sheets

#### 2. Import Errors
**Cause**: Missing dependencies
**Solution**:
- Check `requirements_streamlit.txt` includes all packages
- Ensure versions are compatible
- Test locally first

#### 3. API Timeout
**Cause**: Network issues with hebcal.com
**Solution**:
- Application handles gracefully
- Shows warning message
- Continues without holidays

#### 4. File Upload Issues
**Cause**: File size or format problems
**Solution**:
- Keep CSV files under 200MB
- Ensure UTF-8 encoding
- Check column names match exactly

### Data Validation

#### CSV Format Requirements
```csv
Main Topic,Subtopic,Days
Topic 1,Subtopic A,3
Topic 1,Subtopic B,2
Topic 2,Subtopic C,4
```

#### Validation Rules
- ✅ All columns present: `Main Topic`, `Subtopic`, `Days`
- ✅ All `Days` values are positive integers (empty values can be handled automatically)
- ✅ UTF-8 encoding
- ✅ CSV format (not Excel)

### Testing Your Deployment

#### 1. Test with Sample Data
```bash
# Use the provided sample file
sample_syllabus_fixed.csv
```

#### 2. Test Different Scenarios
- ✅ Single main topic
- ✅ Multiple main topics
- ✅ With breaks enabled
- ✅ With holidays disabled
- ✅ Different start dates

#### 3. Test Error Handling
- ❌ Empty CSV file
- ❌ Missing columns
- ❌ Non-numeric days
- ❌ Empty cells

## 📊 Performance Optimization

### Streamlit Optimizations
- **Caching**: Use `@st.cache_data` for expensive operations
- **Lazy Loading**: Load data only when needed
- **Error Handling**: Graceful degradation

### Flask Optimizations
- **WSGI Server**: Use Gunicorn in production
- **Static Files**: Serve via CDN
- **Database**: Consider caching for holidays

## 🔒 Security Considerations

### File Upload Security
- File type validation (CSV only)
- File size limits (200MB max)
- Input sanitization
- Temporary file handling

### API Security
- Rate limiting for hebcal.com API
- Error handling for network issues
- No sensitive data storage

## 📈 Monitoring and Maintenance

### Streamlit Cloud
- **Logs**: Available in dashboard
- **Usage**: Automatic statistics
- **Updates**: Automatic on git push

### Flask Deployment
- **Logs**: Application logs
- **Health Checks**: `/health` endpoint
- **Monitoring**: Set up alerts

## 🌐 Public Sharing

### Streamlit Cloud
- **Public URL**: Share directly
- **Embedding**: Use iframe
- **Custom Domain**: Not supported

### Flask Deployment
- **Custom Domain**: Full control
- **SSL**: Automatic with most providers
- **CDN**: Optional for performance

## 📞 Support

### Getting Help
1. **Check logs** in deployment platform
2. **Test locally** to isolate issues
3. **Review error messages** carefully
4. **Check documentation** for platform-specific issues

### Common Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Flask Documentation](https://flask.palletsprojects.com)
- [GitHub Issues](https://github.com/your-repo/issues)

---

## 🎉 Success Checklist

Before sharing your deployed app:

- [ ] **Tested with sample data**
- [ ] **Verified error handling**
- [ ] **Checked mobile responsiveness**
- [ ] **Tested all features**
- [ ] **Documented usage instructions**
- [ ] **Shared with test users**

**🎊 Congratulations! Your Syllabus Calculator is now live and ready to help educators create better course schedules!** 