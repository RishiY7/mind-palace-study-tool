# 🧠 Mind Palace - Quick Reference Guide

## 🚀 Launch Application
```powershell
streamlit run app.py
```

## 📋 Project Overview

**Mind Palace** is an AI-powered learning platform that transforms PDFs into interactive study notebooks.

### Key Features:
- ✅ **8 Functional Pages** (2 placeholders for future development)
- ✅ **AI-Powered Content Generation** using Google Gemini
- ✅ **MongoDB Data Persistence**
- ✅ **Gamified Learning** with points and achievements
- ✅ **Modular Prompt System** (JSON-based)

## 📂 File Structure

```
├── app.py                      # Main entry point (home page)
├── pages/                      # Streamlit multi-page app
│   ├── 1_📄_Summary.py        # ✅ AI summary & topics
│   ├── 2_📖_PDF_Viewer.py     # ✅ View original PDF
│   ├── 3_🎴_Flashcards.py     # ✅ Generate flashcards
│   ├── 4_📝_Quiz.py           # 🚧 Placeholder
│   ├── 5_💬_Talk_to_Doc.py    # 🚧 Placeholder
│   ├── 6_📅_Study_Scheduler.py # ✅ Create study plans
│   ├── 7_🎯_Progress_Tracker.py # ✅ Track progress
│   └── 8_🧠_Acronym_Generator.py # ✅ Memory mnemonics
├── prompts/                    # AI prompt configurations
│   ├── summary_prompt.json
│   ├── flashcard_prompt.json
│   ├── acronym_prompt.json
│   ├── scheduler_prompt.json
│   └── quiz_prompt.json
└── utils/                      # Helper modules
    ├── db.py                   # MongoDB operations
    └── helpers.py              # PDF & AI utilities
```

## 🎯 Usage Workflow

### 1️⃣ Upload PDF
- Go to home page
- Click "Choose a PDF file"
- Wait for AI processing

### 2️⃣ Explore Your Notebook
Navigate using the sidebar:

**📄 Summary**
- View AI-generated summary
- See extracted key topics

**📖 PDF Viewer**
- Read original document
- Download PDF

**🎴 Flashcards**
- Select a topic
- Generate Q&A flashcards

**📅 Study Scheduler**
- Set target days (1-365)
- Get personalized daily tasks
- Each task has points (10-20)

**🎯 Progress Tracker**
- View total score
- Track completed tasks
- Unlock achievements
- See completion percentage

**🧠 Acronym Generator**
- Choose topic or enter custom text
- Generate memory mnemonics
- Get memory tips

### 3️⃣ Complete Tasks & Earn Points
- Go to Study Scheduler
- Click ✓ to mark tasks complete
- Watch your score grow in Progress Tracker!

## 🏆 Achievement System

| Achievement | Requirement | Icon |
|------------|-------------|------|
| Getting Started | 50 points | 🌱 |
| On a Roll | 100 points | 🔥 |
| Dedicated Learner | 250 points | ⭐ |
| Master Student | 500 points | 🎓 |
| Task Master | 10 tasks | ✅ |
| Halfway There | 50% complete | 🎯 |
| Perfect Score | 100% complete | 💯 |

## 🔧 Customization

### Edit AI Prompts
Modify JSON files in `prompts/` directory:

```json
{
    "name": "Prompt Name",
    "description": "What it does",
    "system_instruction": "AI role/behavior",
    "user_instruction": "Task instructions"
}
```

### Database Collections
MongoDB stores data in two collections:
- `notebooks` - PDF content, summaries, topics, schedules
- `progress` - Completed tasks, scores

## 🐛 Common Issues

**MongoDB Connection Error**
- Ensure MongoDB is running in WSL
- Check MONGODB_URI in .env

**API Key Error**
- Verify GEMINI_API_KEY in .env
- Check API key permissions

**PDF Not Loading**
- Ensure PDF is not password-protected
- Check PDF has extractable text

## 📊 MongoDB Queries (Optional)

```javascript
// View all notebooks
db.notebooks.find()

// Check progress
db.progress.find()

// Delete all data (reset)
db.notebooks.deleteMany({})
db.progress.deleteMany({})
```

## 🚀 Development Tips

### Run Verification
```powershell
.\verify_setup.ps1
```

### View Logs
Streamlit shows logs in terminal where it's running

### Clear Cache
```powershell
streamlit cache clear
```

### Force Reload
Press `R` in browser or `Ctrl+R`

## 📝 Notes

- **Placeholders**: Quiz and Talk to Doc pages are scaffolded for future development
- **Text Limit**: AI processes first 8,000-10,000 characters for performance
- **Topics**: Auto-extracted from document structure
- **Session State**: Some data stored in browser session (flashcards, acronyms)

## 🎓 Best Practices

1. **Upload clear, well-structured PDFs** for best results
2. **Create schedule early** to maximize gamification features
3. **Review summary first** before diving into specific topics
4. **Use acronyms** for lists and key concepts
5. **Track progress daily** to stay motivated

---

**Enjoy your learning journey! 🧠✨**
