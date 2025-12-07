# 🧠 Mind Palace - AI-Powered Learning Platform

An interactive, multi-page Streamlit application that transforms your PDF documents into comprehensive learning notebooks using AI-powered features.

## 🌟 Features

### Core Functionality
- **📤 PDF Upload & Processing** - Automatically extract text and generate structured notebooks
- **🤖 AI-Powered Analysis** - Uses Google Gemini API for intelligent content processing
- **💾 MongoDB Integration** - Persistent storage for notebooks and progress tracking

### Learning Tools

1. **📄 Summary Page**
   - AI-generated concise summaries
   - Automatic extraction of key topics and sections
   - Document statistics and analytics

2. **📖 PDF Viewer**
   - View your original PDF within the app
   - Download option for offline access

3. **🎴 Flashcard Generator**
   - Topic-based flashcard generation
   - Question/answer format for effective learning
   - AI-powered content extraction

4. **📝 Interactive Quiz** (Placeholder)
   - Coming soon: Multiple-choice quizzes
   - Instant feedback and scoring

5. **💬 Talk to Doc** (Placeholder)
   - Coming soon: RAG-powered chatbot
   - Ask questions about your document
   - Context-aware responses

6. **📅 Study Scheduler**
   - Personalized study plans based on target dates
   - Breaks content into 4-5 manageable daily tasks
   - Flexible scheduling (1-365 days)

7. **🎯 Progress Tracker**
   - Gamification with point system
   - Track completed tasks
   - Achievement badges
   - Visual progress bars and statistics

8. **🧠 Acronym Generator**
   - Create mnemonic devices for key concepts
   - Topic-based or custom text input
   - Memory tips and best practices

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB installed and running locally
- Google Gemini API key

### Installation

1. **Clone or navigate to the project directory:**
   ```powershell
   cd "c:\Users\vishn\PROJECT\STEP BY STEP DEC 7"
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   
   The `.env` file should contain:
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-flash-lite-latest
   MONGODB_URI=mongodb://127.0.0.1:27017/mind_palace
   ```

4. **Start MongoDB:**
   ```powershell
   # Make sure MongoDB is running on localhost:27017
   ```

5. **Run the application:**
   ```powershell
   streamlit run app.py
   ```

6. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
STEP BY STEP DEC 7/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env                           # Environment configuration
├── utils/
│   ├── __init__.py
│   ├── db.py                      # MongoDB database operations
│   └── helpers.py                 # PDF processing and AI helpers
├── prompts/
│   ├── summary_prompt.json        # Summary generation prompt
│   ├── flashcard_prompt.json     # Flashcard generation prompt
│   ├── scheduler_prompt.json     # Study scheduler prompt
│   └── acronym_prompt.json       # Acronym generation prompt
└── pages/
    ├── 1_📄_Summary.py
    ├── 2_📖_PDF_Viewer.py
    ├── 3_🎴_Flashcards.py
    ├── 4_📝_Quiz.py
    ├── 5_💬_Talk_to_Doc.py
    ├── 6_📅_Study_Scheduler.py
    ├── 7_🎯_Progress_Tracker.py
    └── 8_🧠_Acronym_Generator.py
```

## 🎯 Usage Guide

### Creating a Notebook

1. **Upload a PDF** - Click "Choose a PDF file" on the home page
2. **Wait for processing** - The AI will generate a summary and extract topics
3. **Navigate pages** - Use the sidebar to access different features

### Study Workflow

1. **📄 Review Summary** - Start with the AI-generated overview
2. **📅 Create Schedule** - Set your target completion date
3. **🎴 Generate Flashcards** - Create study materials for each topic
4. **🧠 Make Mnemonics** - Use acronyms to remember key concepts
5. **🎯 Track Progress** - Mark tasks complete and earn points

## 🔧 Technical Stack

- **Frontend:** Streamlit
- **AI/LLM:** Google Gemini API (gemini-flash-lite-latest)
- **Database:** MongoDB
- **PDF Processing:** PyPDF2
- **Environment Management:** python-dotenv

## 📝 Prompt Management

All AI prompts are stored as JSON files in the `prompts/` directory. Each prompt file contains:

- `name` - Descriptive name of the prompt
- `description` - What the prompt does
- `system_instruction` - System-level instructions for the AI
- `user_instruction` - User-facing prompt template

This design allows for easy customization and version control of AI prompts.

## 🎮 Gamification System

- **Points per task:** 10-20 points (defined in schedule)
- **Achievements:**
  - 🌱 Getting Started (50 points)
  - 🔥 On a Roll (100 points)
  - ⭐ Dedicated Learner (250 points)
  - 🎓 Master Student (500 points)
  - ✅ Task Master (10 tasks completed)
  - 🎯 Halfway There (50% completion)
  - 💯 Perfect Score (100% completion)

## 🔮 Future Enhancements

- [ ] Interactive quiz generation with multiple-choice questions
- [ ] RAG-powered chatbot for document Q&A
- [ ] Multi-document support
- [ ] Export study materials (PDF, Anki cards)
- [ ] Collaborative learning features
- [ ] Mobile app version
- [ ] Advanced analytics and insights

## 🐛 Troubleshooting

### MongoDB Connection Issues
```powershell
# Verify MongoDB is running
Get-Process mongod
```

### API Key Errors
- Check that your `.env` file contains the correct `GEMINI_API_KEY`
- Ensure the API key has proper permissions

### PDF Processing Errors
- Ensure the PDF is not password-protected
- Check that the PDF contains extractable text (not scanned images)

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Streamlit for the amazing web framework
- MongoDB for data persistence

---

**Happy Learning! 🎓**
