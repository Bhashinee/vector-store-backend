import nltk
from typing import List, Union

# Download required NLTK data (only needs to run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def chunk_data(data: str, chunk_type: str, chunk_size: int = 100, max_chunk_size: int = 500, overlap: int = 0) -> List[str]:
    """
    Chunk the input data based on the specified chunking type with optional overlap.
    
    Args:
        data (str): The input text to be chunked
        chunk_type (str): Type of chunking ('sentence', 'word', 'character', 'recursive')
        chunk_size (int): Target size of chunks (for word and character types)
        max_chunk_size (int): Maximum allowed size for recursive chunking
        overlap (int): Amount of overlap between chunks (unit depends on chunk_type)
    
    Returns:
        List[str]: List of chunks based on specified type
    
    Raises:
        ValueError: If invalid chunk_type or invalid overlap value provided
    """
    chunk_type = chunk_type.lower()
    
    if not data or not isinstance(data, str):
        return []
    
    if overlap < 0:
        raise ValueError("Overlap must be non-negative")
    
    # Sentence-based chunking with overlap
    if chunk_type == 'sentence':
        sentences = nltk.sent_tokenize(data)
        if overlap >= len(sentences):
            raise ValueError("Overlap cannot be larger than the number of sentences")
        chunks = []
        step = max(1, chunk_size - overlap)
        for i in range(0, len(sentences), step):
            end = min(i + chunk_size, len(sentences))
            chunk = " ".join(sentences[i:end])
            chunks.append(chunk)
        return chunks
    
    # Word-based chunking with overlap
    elif chunk_type == 'word':
        words = data.split()
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk_size for word chunking")
        chunks = []
        step = max(1, chunk_size - overlap)
        for i in range(0, len(words), step):
            end = min(i + chunk_size, len(words))
            chunk = " ".join(words[i:end])
            chunks.append(chunk)
        return chunks
    
    # Character-based chunking with overlap
    elif chunk_type == 'character':
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk_size for character chunking")
        chunks = []
        step = max(1, chunk_size - overlap)
        for i in range(0, len(data), step):
            end = min(i + chunk_size, len(data))
            chunk = data[i:end]
            chunks.append(chunk)
        return chunks
    
    # Recursive chunking with overlap
    elif chunk_type == 'recursive':
        def recursive_split(text: str, max_size: int, overlap_size: int) -> List[str]:
            if len(text) <= max_size:
                return [text.strip()]
            
            # Try splitting by paragraph
            if '\n\n' in text:
                parts = text.split('\n\n')
                result = []
                for i, part in enumerate(parts):
                    if len(part) > max_size:
                        result.extend(recursive_split(part, max_size, overlap_size))
                    else:
                        result.append(part.strip())
                        # Add overlap from next chunk if available
                        if i < len(parts) - 1 and overlap_size > 0:
                            next_part = parts[i + 1][:overlap_size]
                            result[-1] += "\n\n" + next_part
                return result
            
            # Try splitting by sentence
            sentences = nltk.sent_tokenize(text)
            if len(sentences) > 1:
                result = []
                current_chunk = ""
                for i, sentence in enumerate(sentences):
                    if len(current_chunk) + len(sentence) <= max_size:
                        current_chunk += " " + sentence if current_chunk else sentence
                    else:
                        if current_chunk:
                            # Add overlap from current sentence
                            if overlap_size > 0 and len(sentence) > overlap_size:
                                current_chunk += " " + sentence[:overlap_size]
                            result.append(current_chunk.strip())
                        if len(sentence) > max_size:
                            result.extend(recursive_split(sentence, max_size, overlap_size))
                        else:
                            current_chunk = sentence
                if current_chunk:
                    result.append(current_chunk.strip())
                return result
            
            # Split by words with overlap
            words = text.split()
            result = []
            current_chunk = []
            current_length = 0
            
            for i, word in enumerate(words):
                if current_length + len(word) + 1 <= max_size:
                    current_chunk.append(word)
                    current_length += len(word) + 1
                else:
                    if current_chunk:
                        chunk = " ".join(current_chunk)
                        # Add overlap from next words
                        if overlap_size > 0 and i < len(words):
                            overlap_words = " ".join(words[i:i+overlap_size])[:overlap_size]
                            chunk += " " + overlap_words
                        result.append(chunk)
                    if len(word) > max_size:
                        result.extend([word[j:j+max_size] for j in range(0, len(word), max_size - overlap_size)])
                    else:
                        current_chunk = [word]
                        current_length = len(word) + 1
            if current_chunk:
                result.append(" ".join(current_chunk))
            return result
        
        return recursive_split(data, max_chunk_size, overlap)
    
    else:
        raise ValueError("Invalid chunk_type. Supported types: 'sentence', 'word', 'character', 'recursive'")
