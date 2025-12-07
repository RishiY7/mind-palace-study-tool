# Topic Extraction Alternatives for Mind Palace

## Current Method: Heuristic-Based (Line-by-line filtering)

```python
# Looks for short lines that might be headings
# Problems: Limited accuracy, misses topics in sentence form
```

---

## 🎯 Alternative 1: **AI-Based Extraction (RECOMMENDED)**

**Most Accurate for Diverse Documents**

```python
def extract_topics_ai(text_content):
    """Use Gemini AI to intelligently extract key topics."""
    from utils.helpers import load_prompt, call_gemini, parse_json_response
    
    prompt_config = {
        "system_instruction": "You are an expert document analyst.",
        "user_instruction": "Extract the 10 most important topics from this text. Return as JSON array with topic names only: ['Topic 1', 'Topic 2', ...]"
    }
    
    response = call_gemini(prompt_config, text_content[:8000])
    topics = parse_json_response(response)
    return topics if isinstance(topics, list) else []
```

**Pros:**
- ✅ Highly accurate across different document types
- ✅ Understands context and importance
- ✅ Works with any document structure
- ✅ Extracts meaningful concepts, not just headings

**Cons:**
- ❌ Requires API call (slight latency ~1-2 seconds)
- ❌ Uses API quota

---

## 🎯 Alternative 2: **NLP with spaCy**

**Fast, Offline, Good Accuracy**

```python
def extract_topics_spacy(text_content):
    """Extract topics using spaCy NER (Named Entity Recognition)."""
    import spacy
    from collections import Counter
    
    # Load English model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text_content[:10000])
    
    # Extract named entities and important noun phrases
    topics = []
    
    # Named entities (persons, organizations, locations)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT"]:
            topics.append(ent.text)
    
    # Noun chunks (noun phrases)
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 3 and len(chunk.text) < 50:
            topics.append(chunk.text)
    
    # Remove duplicates and return top 10
    return list(dict.fromkeys(topics))[:10]
```

**Installation:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

**Pros:**
- ✅ Very fast (no API calls)
- ✅ Works offline
- ✅ No additional costs
- ✅ Good accuracy for entities and phrases

**Cons:**
- ❌ Requires model download (~50MB)
- ❌ Less context-aware than AI
- ❌ May include non-important entities

---

## 🎯 Alternative 3: **RAKE (Rapid Automatic Keyword Extraction)**

**Quick, Lightweight, Good for Keywords**

```python
def extract_topics_rake(text_content):
    """Extract keywords using RAKE algorithm."""
    from rake_nltk import Rake
    
    r = Rake(language="english")
    r.extract_keywords_from_text(text_content[:10000])
    
    # Get scored keywords
    keywords = r.get_ranked_phrases()[:10]
    return keywords
```

**Installation:**
```bash
pip install rake-nltk
```

**Pros:**
- ✅ Fast and lightweight
- ✅ No model downloads needed
- ✅ Works offline
- ✅ Good for keyword extraction

**Cons:**
- ❌ Less accurate for topics
- ❌ Returns keywords, not structured topics

---

## 🎯 Alternative 4: **TextRank (like Google PageRank for text)**

**Balanced - Good accuracy without AI**

```python
def extract_topics_textrank(text_content):
    """Extract topics using TextRank algorithm."""
    import pytextrank
    import spacy
    
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    
    doc = nlp(text_content[:10000])
    topics = [phrase.text for phrase in doc._.phrases[:10]]
    
    return topics
```

**Installation:**
```bash
pip install pytextrank spacy
python -m spacy download en_core_web_sm
```

**Pros:**
- ✅ Good balance of speed and accuracy
- ✅ Understands relationships between topics
- ✅ Works offline

**Cons:**
- ❌ Requires spaCy model
- ❌ Slightly slower than RAKE

---

## 🎯 Alternative 5: **PDF Structure Analysis**

**Best for Well-Formatted Documents**

```python
def extract_topics_from_pdf_structure(pdf_file):
    """Extract topics from PDF headings/outline."""
    from PyPDF2 import PdfReader
    
    pdf_reader = PdfReader(pdf_file)
    topics = []
    
    # Try to get PDF outline (bookmarks)
    if pdf_reader.outline:
        for item in pdf_reader.outline:
            if isinstance(item, dict):
                topics.append(item.get('/Title', ''))
            else:
                topics.append(item.title)
    
    # Filter and clean
    topics = [t.strip() for t in topics if t and len(t) > 3]
    return topics[:10] if topics else None
```

**Pros:**
- ✅ Most accurate for structured PDFs
- ✅ Extracts actual document structure
- ✅ No API calls
- ✅ Super fast

**Cons:**
- ❌ Only works if PDF has outline/bookmarks
- ❌ Fails for scanned/unstructured PDFs

---

## 📊 Comparison Table

| Method | Speed | Accuracy | Offline | Cost | Use Case |
|--------|-------|----------|---------|------|----------|
| **Heuristic (Current)** | ⚡⚡⚡ | ⭐⭐ | ✅ | Free | Quick extraction |
| **AI (Gemini)** | ⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | $$ | Any document, best quality |
| **spaCy NER** | ⚡⚡ | ⭐⭐⭐ | ✅ | Free | Entities & phrases |
| **RAKE** | ⚡⚡⚡ | ⭐⭐⭐ | ✅ | Free | Quick keywords |
| **TextRank** | ⚡⚡ | ⭐⭐⭐⭐ | ✅ | Free | Balanced approach |
| **PDF Structure** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ✅ | Free | Structured PDFs only |

---

## 🏆 RECOMMENDATION

**For Mind Palace, I recommend: AI-Based (Gemini)**

**Why?**
1. You're already using Gemini API for other features
2. Most accurate across all document types
3. Users get the best quality topics for their materials
4. Small latency (1-2s) is acceptable
5. Seamless integration with existing prompt system

**Implementation in app.py:**
```python
def extract_topics_from_text(text_content):
    """Extract topics using AI."""
    try:
        prompt_config = load_prompt('topics_prompt.json')
        response = call_gemini(prompt_config, text_content[:8000])
        topics = parse_json_response(response)
        
        if isinstance(topics, list) and topics:
            return topics
    except:
        pass
    
    # Fallback to heuristic if AI fails
    return extract_topics_heuristic(text_content)
```

**Second best option: TextRank** (if you want to avoid extra API calls)

---

## 📝 Would you like me to implement any of these alternatives?

Just let me know which one you prefer!
