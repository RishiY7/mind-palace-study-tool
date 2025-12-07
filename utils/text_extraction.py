"""
Text extraction utilities using Hugging Face models.
Intelligently extracts topic-relevant content from documents.
"""

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("Warning: Hugging Face models not installed. Install with: pip install sentence-transformers scikit-learn")

class TopicAwareTextExtractor:
    """Extract text relevant to a specific topic using semantic similarity."""
    
    def __init__(self, model_name="nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True):
        """
        Initialize with a Hugging Face sentence transformer model.
        
        Model options:
        - "nomic-ai/nomic-embed-text-v1.5" (RECOMMENDED) - Best for long documents, 8192 token context
        - "all-MiniLM-L6-v2" - Fast, lightweight, good for short text
        - "all-mpnet-base-v2" - More accurate, slower
        """
        if not HF_AVAILABLE:
            self.model = None
            return
        
        try:
            print(f"Loading Hugging Face model: {model_name}...")
            self.model = SentenceTransformer(model_name, trust_remote_code=trust_remote_code)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def extract_topic_text(self, text, topic, max_length=8000, overlap=500):
        """
        Extract text most relevant to a specific topic using semantic similarity.
        
        Args:
            text (str): Full document text
            topic (str): Topic to search for
            max_length (int): Maximum characters to return
            overlap (int): Overlap between chunks for context
        
        Returns:
            str: Topic-relevant text excerpt (up to max_length chars)
        """
        if not HF_AVAILABLE or self.model is None:
            # Fallback to simple keyword search
            return self._fallback_extraction(text, topic, max_length)
        
        try:
            # Split text into sentences
            sentences = self._split_sentences(text)
            
            if not sentences:
                return text[:max_length]
            
            # Encode topic with search prefix for nomic model
            topic_embedding = self.model.encode(
                f"search_query: {topic}", 
                convert_to_tensor=False,
                prompt_name="search_query"
            )
            
            # Encode all sentences with document prefix for nomic model
            sentence_embeddings = self.model.encode(
                [f"search_document: {s}" for s in sentences],
                convert_to_tensor=False,
                prompt_name="search_document"
            )
            
            # Calculate similarity between topic and each sentence
            similarities = cosine_similarity([topic_embedding], sentence_embeddings)[0]
            
            # Get indices of most similar sentences
            top_indices = np.argsort(similarities)[::-1][:20]  # Get top 20 most similar
            top_indices = sorted(top_indices)  # Sort by document order
            
            # Build result by taking chunks around top sentences
            result = []
            current_length = 0
            last_idx = -10  # Prevent overlapping chunks
            
            for idx in top_indices:
                if current_length >= max_length:
                    break
                
                # Skip if too close to last added sentence
                if idx - last_idx < 3:
                    continue
                
                # Get context: current sentence + surrounding sentences
                start_idx = max(0, idx - 2)
                end_idx = min(len(sentences), idx + 3)
                
                chunk = " ".join(sentences[start_idx:end_idx])
                
                if chunk not in result:  # Avoid duplicates
                    result.append(chunk)
                    current_length += len(chunk)
                    last_idx = idx
            
            return " ".join(result)[:max_length]
            
        except Exception as e:
            print(f"Error in semantic extraction: {e}")
            return self._fallback_extraction(text, topic, max_length)
    
    def _split_sentences(self, text):
        """Split text into sentences."""
        import re
        
        # Simple sentence splitter
        sentences = re.split(r'[.!?]\s+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        return sentences
    
    def _fallback_extraction(self, text, topic, max_length):
        """Fallback: Simple keyword-based extraction."""
        # Try to find the topic in the text
        topic_lower = topic.lower()
        text_lower = text.lower()
        
        # Find the position of the topic
        pos = text_lower.find(topic_lower)
        
        if pos > -1:
            # Extract centered around the topic
            start = max(0, pos - 2000)
            end = min(len(text), pos + 6000)
            return text[start:end]
        else:
            # Topic not found, return beginning
            return text[:max_length]
    
    def extract_multiple_topics(self, text, topics, max_length_per_topic=5000):
        """
        Extract text for multiple topics.
        
        Args:
            text (str): Full document text
            topics (list): List of topics to extract
            max_length_per_topic (int): Max chars per topic
        
        Returns:
            dict: {topic: extracted_text, ...}
        """
        result = {}
        for topic in topics:
            result[topic] = self.extract_topic_text(text, topic, max_length_per_topic)
        return result


def get_topic_text(text, topic, use_semantic=True):
    """
    Convenience function to extract topic-specific text.
    
    Args:
        text (str): Full document text
        topic (str): Topic to extract
        use_semantic (bool): Use semantic similarity (requires HF models)
    
    Returns:
        str: Extracted text relevant to the topic
    """
    if use_semantic and HF_AVAILABLE:
        extractor = TopicAwareTextExtractor()
        return extractor.extract_topic_text(text, topic)
    else:
        # Simple fallback
        return _simple_keyword_extraction(text, topic)


def _simple_keyword_extraction(text, topic, max_length=8000):
    """Simple keyword-based extraction (no HF models required)."""
    topic_lower = topic.lower()
    text_lower = text.lower()
    
    # Find topic position
    pos = text_lower.find(topic_lower)
    
    if pos > -1:
        start = max(0, pos - 2000)
        end = min(len(text), pos + 6000)
        return text[start:end]
    else:
        return text[:max_length]
