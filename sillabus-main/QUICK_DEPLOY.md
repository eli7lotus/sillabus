# ⚡ Quick Deploy Checklist

## 🚀 Streamlit Cloud (Recommended)

### Files Needed for GitHub Repo:
```
📁 your-repo/
├── streamlit_app.py          # ✅ Main app
├── requirements_streamlit.txt # ✅ Dependencies  
├── .streamlit/config.toml    # ✅ Config
├── sample_syllabus_fixed.csv # ✅ Example data
└── README.md                # ✅ Documentation
```

### Deploy Steps:
1. **Create GitHub repo** and upload files above
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in** with GitHub
4. **Click "New app"**
5. **Configure**:
   - Repository: `your-repo`
   - Branch: `main`
   - Main file: `streamlit_app.py`
6. **Click "Deploy"**
7. **Wait 2-3 minutes** for deployment
8. **Share URL**: `https://your-app-name.streamlit.app`

## 🔧 Flask Deployment

### Local Test:
```bash
pip install -r requirements.txt
python app.py
# Access: http://localhost:5000
```

### Production Options:
- **Heroku**: Add `Procfile` and `gunicorn`
- **DigitalOcean**: App Platform
- **AWS/GCP**: Container deployment

## ✅ Pre-Deploy Checklist

- [ ] **Tested locally** with sample data
- [ ] **Fixed NaN error** (handled in code)
- [ ] **Validated CSV format** (use `sample_syllabus_fixed.csv`)
- [ ] **Checked all features** work
- [ ] **Error handling** implemented
- [ ] **Documentation** complete

## 🛠️ Troubleshooting

### Common Issues:
1. **"cannot convert float NaN to integer"** → Enable "Handle empty values" option
2. **Import errors** → Check requirements.txt
3. **API timeouts** → App handles gracefully
4. **File upload issues** → Check CSV format

### Data Requirements:
- ✅ Columns: `Main Topic`, `Subtopic`, `Days`
- ✅ All `Days` values are numbers (empty values supported)
- ✅ UTF-8 encoding

## 📞 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Flask Docs**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Full Guide**: See `DEPLOYMENT_GUIDE.md`

---

**🎉 Ready to deploy! Choose Streamlit Cloud for easiest setup.** 