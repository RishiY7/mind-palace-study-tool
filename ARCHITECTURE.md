# 🧠 Mind Palace - Architecture & Logic Guide

## 📍 Where the PDF is Stored

### Storage Location: **MongoDB Database**

```
Database: mind_palace
Collection: notebooks
Document Structure:
{
  "_id": ObjectId("..."),
  "filename": "document.pdf",
  "pdf_content": "JVBERi0xLjQKJeLj...(BASE64 ENCODED BINARY)",
  "text_content": "This is the extracted text from...",
  "summary": "AI-generated summary...",
  "topics": ["Topic 1", "Topic 2", ...],
  "schedule": [...],
  "schedule_days": 7,
  "created_at": ISODate("2025-12-07..."),
  "updated_at": ISODate("2025-12-07...")
}
```

### Key Storage Details

| Field | Type | Purpose |
|-------|------|---------|
| `pdf_content` | **Base64 String** | Entire PDF file encoded as text (stored in MongoDB) |
| `text_content` | **String** | Extracted text from PDF (for AI processing) |
| `summary` | **String** | AI-generated summary |
| `topics` | **Array** | Extracted key topics |
| `schedule` | **Array** | Study plan with daily tasks |
| `schedule_days` | **Number** | Duration of study plan |

---

## 🔄 Complete Application Workflow

### **Phase 1: PDF Upload & Processing**

```
User uploads PDF
    ↓
PDF File (binary) received by Streamlit
    ↓
EXTRACTION (utils/helpers.py)
    ├─ Extract text using PyPDF2 → text_content
    └─ Encode binary to Base64 → pdf_content
    ↓
PROCESSING
    ├─ Send text_content to Gemini API with summary_prompt.json
    ├─ Receive AI-generated summary
    └─ Extract topics from text (heuristic algorithm)
    ↓
STORAGE (MongoDB)
    └─ db.save_notebook()
        ├─ filename: uploaded_file.name
        ├─ pdf_content: base64_string
        ├─ text_content: extracted_text
        ├─ summary: ai_summary
        ├─ topics: list_of_topics
        └─ MongoDB assigns ObjectId(_id)
    ↓
SUCCESS
    └─ Return notebook_id to user
```

### **Phase 2: User Selects Notebook**

```
User clicks notebook in sidebar
    ↓
Set session_state.current_notebook = notebook_id
    ↓
All pages use this ID to:
    ├─ Retrieve notebook from MongoDB
    ├─ Display content
    └─ Update progress
```

### **Phase 3: Feature Pages Workflow**

#### **3.1 Summary Page**
```
User clicks "Summary" page
    ↓
Get current notebook from MongoDB
    ↓
Display:
    ├─ AI summary (from notebook['summary'])
    ├─ Topics list (from notebook['topics'])
    └─ Statistics (word count, char count)
```

#### **3.2 PDF Viewer Page**
```
User clicks "PDF Viewer" page
    ↓
Get current notebook from MongoDB
    ↓
Retrieve pdf_content (Base64 string)
    ↓
Decode Base64 → Binary PDF
    ↓
Render in HTML iframe using data URI
    ↓
User can:
    ├─ View PDF inline
    └─ Download original PDF
```

#### **3.3 Flashcards Page**
```
User selects topic from dropdown
    ↓
User clicks "Generate Flashcards"
    ↓
Send to Gemini API:
    ├─ prompt: flashcard_prompt.json
    ├─ text: notebook['text_content'][:8000]
    └─ topic: selected_topic
    ↓
Gemini returns JSON with flashcards:
    [
      {"question": "Q1?", "answer": "A1"},
      {"question": "Q2?", "answer": "A2"},
      ...
    ]
    ↓
Parse JSON response
    ↓
Store in session_state.flashcards
    ↓
Display in expandable cards (cached in browser session)
```

#### **3.4 Study Scheduler Page**
```
User enters target days (1-365)
    ↓
User clicks "Generate Schedule"
    ↓
Send to Gemini API:
    ├─ prompt: scheduler_prompt.json
    ├─ text: notebook['text_content'][:8000]
    └─ days: user_input
    ↓
Gemini returns JSON:
    [
      {
        "day": 1,
        "tasks": [
          {"description": "Read Section 1", "points": 10},
          {"description": "Review concepts", "points": 15},
          ...
        ]
      },
      ...
    ]
    ↓
Save to MongoDB:
    └─ db.save_schedule(notebook_id, schedule, days)
    ↓
Display schedule in expanders
    ↓
User marks tasks complete:
    └─ Click ✓ button
        ↓
        db.mark_task_complete(notebook_id, day, task_idx, points)
        ├─ Add task_id to completed_tasks array
        └─ Increment total_score by points
```

#### **3.5 Progress Tracker Page**
```
User opens Progress Tracker
    ↓
Get progress from MongoDB:
    └─ db.get_progress(notebook_id)
        └─ Returns {completed_tasks: [...], total_score: 120}
    ↓
Calculate metrics:
    ├─ total_tasks = count all tasks in schedule
    ├─ completed = len(completed_tasks)
    └─ completion_rate = completed / total_tasks * 100
    ↓
Display:
    ├─ Total score (prominently)
    ├─ Progress bar
    ├─ Achievements (unlocked based on score/tasks)
    ├─ Stats (tasks completed, completion %)
    └─ Recent activity
```

#### **3.6 Acronym Generator Page**
```
User selects topic OR enters custom text
    ↓
User clicks "Generate Acronym"
    ↓
Send to Gemini API:
    ├─ prompt: acronym_prompt.json
    ├─ text: (if custom) custom_text or (if topic) notebook['text_content']
    └─ topic: selected_topic or "Custom Text"
    ↓
Gemini returns mnemonic explanation:
    "NASA stands for National Aeronautics and Space Administration..."
    ↓
Store in session_state.acronym_result
    ↓
Display in formatted box with memory tips
```

---

## 🗄️ MongoDB Collections

### **Collection 1: notebooks**
```javascript
{
  _id: ObjectId,
  filename: String,
  pdf_content: String (Base64),
  text_content: String,
  summary: String,
  topics: Array<String>,
  schedule: Array<Object>,
  schedule_days: Number,
  created_at: Date,
  updated_at: Date
}
```

### **Collection 2: progress**
```javascript
{
  _id: ObjectId,
  notebook_id: String,
  completed_tasks: Array<String>,  // ["1_0", "1_1", "2_0"]
  total_score: Number,
  created_at: Date,
  updated_at: Date
}
```

---

## 🔌 API Integration (Google Gemini)

### **How Prompts Work**

Each prompt JSON file follows this structure:

```json
{
  "name": "Feature Name",
  "description": "What it does",
  "system_instruction": "You are an expert...",
  "user_instruction": "Based on the provided text, generate..."
}
```

### **Gemini API Call Flow**

```
1. Load prompt JSON from prompts/ directory
   ↓
2. Create GenerativeModel with system_instruction
   ↓
3. Format user_instruction with variables (e.g., {topic}, {days})
   ↓
4. Combine user_instruction + actual document text
   ↓
5. Send to Gemini API: model.generate_content(full_prompt)
   ↓
6. Receive response text
   ↓
7. Parse JSON (if needed) or return as string
   ↓
8. Display or store result
```

### **Example: Flashcard Generation**

```python
# Load prompt
prompt_config = load_prompt('flashcard_prompt.json')

# Format instruction
user_instruction = prompt_config['user_instruction'].format(topic="Photosynthesis")
# Result: "Based on the provided text for the topic 'Photosynthesis', generate 5 flashcards..."

# Combine with text
full_prompt = user_instruction + "\n\n" + notebook['text_content'][:8000]

# Call API
response = model.generate_content(full_prompt)

# Parse result
flashcards = parse_json_response(response.text)
```

---

## 🔐 Session Management

### **Streamlit Session State Variables**

```python
st.session_state = {
    'current_notebook': 'ObjectId123...',      # Active notebook
    'flashcards': [...],                       # Cached flashcard results
    'selected_topic': 'Photosynthesis',        # Last selected topic
    'acronym_result': 'NASA stands for...',    # Last acronym result
    'messages': [...]                          # Chat history (Talk to Doc)
}
```

### **Why Session State?**
- Keeps data while user navigates between pages
- Avoids re-generating content on page refresh
- Stores temporary UI state (selected dropdowns, etc.)

---

## 🎯 Data Flow Summary

```
┌─────────────────────────────────────────────────────┐
│                   USER UPLOADS PDF                  │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  app.py (Upload)   │
        │  - Extract text    │
        │  - Encode to Base64│
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────────┐
        │ Gemini API Processing  │
        │ - Generate summary     │
        │ - Extract topics       │
        └─────────┬──────────────┘
                  │
        ┌─────────▼─────────────────┐
        │  MongoDB Storage          │
        │  notebooks collection     │
        └─────────┬─────────────────┘
                  │
    ┌─────────────┴────────────────────────────────┐
    │                                              │
┌───▼──────────┐  ┌──────────┐  ┌──────────────┐ │
│ Summary Page │  │Flashcard │  │Study Planner │ │
└──────────────┘  │Generator │  └──────────────┘ │
                  └──────────┘                    │
                  ┌──────────┐  ┌──────────────┐ │
                  │ PDF View │  │ Progress     │ │
                  └──────────┘  └──────────────┘ │
                  ┌──────────┐  ┌──────────────┐ │
                  │ Acronym  │  │ Quiz (TODO)  │ │
                  └──────────┘  └──────────────┘ │
                                                  │
                ┌─────────────────────────────────▼──┐
                │    MongoDB Progress Collection     │
                │  - Completed tasks                 │
                │  - Score tracking                  │
                └────────────────────────────────────┘
```

---

## 🚀 Key Technologies & Why They're Used

| Technology | Purpose | Why Chosen |
|------------|---------|-----------|
| **Streamlit** | Web Framework | Fast multi-page apps, great for data apps |
| **MongoDB** | Database | Document-based, perfect for varying notebook structures |
| **Google Gemini** | AI/LLM | Free tier, fast, excellent for text generation |
| **PyPDF2** | PDF Processing | Lightweight, extracts text from PDFs |
| **Base64 Encoding** | PDF Storage | Convert binary PDF to text string for MongoDB |
| **Session State** | Caching | Keep data between page navigations |

---

## 💡 Security & Performance Notes

### **PDF Storage Method**
- ✅ PDFs stored as Base64 strings (text) in MongoDB
- ✅ Retrieved and decoded when needed
- ✅ Can be downloaded by user anytime
- ⚠️ Large PDFs (>50MB) will be slow due to Base64 overhead

### **Text Limiting**
- Text is limited to first 8,000-10,000 characters for API calls
- Prevents long processing times and API costs
- Sufficient for generating summaries and study materials

### **Progress Tracking**
- Lightweight task IDs ("day_taskindex") stored in array
- Efficient scoring updates using MongoDB $inc operator
- No complex queries needed

---

## 🔧 Common Operations Reference

### **Save a Notebook**
```python
notebook_id = db.save_notebook(
    filename="document.pdf",
    pdf_content=base64_string,
    text_content=extracted_text,
    summary=ai_summary,
    topics=topic_list
)
```

### **Retrieve Notebook**
```python
notebook = db.get_notebook(notebook_id)
pdf_bytes = base64.b64decode(notebook['pdf_content'])
```

### **Update Schedule**
```python
db.save_schedule(notebook_id, schedule_json, days=7)
```

### **Mark Task Complete**
```python
db.mark_task_complete(notebook_id, day=1, task_index=0, points=10)
```

### **Get Progress**
```python
progress = db.get_progress(notebook_id)
total_score = progress['total_score']
completed_tasks = progress['completed_tasks']
```

---

This is the complete architecture behind Mind Palace!
