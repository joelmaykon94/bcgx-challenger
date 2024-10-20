from langchain_community.document_loaders import PyMuPDFLoader
import os
import unicodedata
import re
from nltk.corpus import stopwords


class CleanText:
 def remove_accents_and_special_characters(text):

    # Normalize the text to separate accents from letters
    normalized_text = unicodedata.normalize('NFKD', text)
    
    # Remove accents by discarding non-ASCII characters
    text_without_accents = normalized_text.encode('ASCII', 'ignore').decode('utf-8')
    
    # Remove any special characters (keeping letters and numbers)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_without_accents)

    # Convert the content to lowercase
    clean_text = clean_text.lower()
    return clean_text