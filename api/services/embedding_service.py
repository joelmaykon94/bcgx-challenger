import asyncio
import os
from openai import OpenAI
import numpy as np
from framework.utils.pdf_utils import extract_text_from_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def create_embedding(text: str):
    """
    Asynchronously creates an embedding vector for the given text using the OpenAI API.

    Args:
        text (str): The text for which the embedding will be generated.

    Returns:
        list of float: A list representing the embedding vector of the input text, or None if an error occurs.

    Raises:
        ValueError: If the response from the OpenAI API is invalid or empty.
        Exception: Any other exceptions raised during the process are caught and logged.
    """
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.embeddings.create(model="text-embedding-ada-002", input=text)
        )
        if response and len(response.data) > 0:
            return response.data[0].embedding
        else:
            raise ValueError("Invalid response from OpenAI embedding service.")
    except Exception as e:
        print(f"Error while creating embedding: {e}")
        return None

async def create_embedding_batch(texts: list):
    """
    Asynchronously creates embedding vectors for a batch of texts using the OpenAI API.

    Args:
        texts (list of str): A list of texts for which embeddings will be generated.

    Returns:
        list of list of float: A list containing embedding vectors for each input text.

    Raises:
        RuntimeError: If an error occurs while generating embeddings for the batch of texts.
    """
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.embeddings.create(model="text-embedding-ada-002", input=texts)
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        raise RuntimeError(f"Error creating batch embeddings: {str(e)}") from e


async def process_text_and_generate_embeddings(pdf_content):
    """
    Extracts text from a PDF and generates embeddings for text chunks.
    Args:
        pdf_content (bytes): The binary content of the PDF.
    Returns:
        tuple: The extracted text and valid embeddings.
    """
    extracted_text = extract_text_from_pdf(pdf_content)
    text_chunks = split_text_into_chunks(extracted_text)

    embedding_tasks = [create_embedding(chunk) for chunk in text_chunks]
    embedding_vectors = await asyncio.gather(*embedding_tasks)

    valid_embeddings = []
    for embedding_vector in embedding_vectors:
        if isinstance(embedding_vector, list):
            embedding_array = np.array(embedding_vector, dtype=np.float32)
            if embedding_is_valid(embedding_array):
                valid_embeddings.append(embedding_array)

    return extracted_text, valid_embeddings

def split_text_into_chunks(text):
    """
    Splits text into manageable chunks for embedding.
    Args:
        text (str): The text to split.
    Returns:
        list: List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    return text_splitter.split_text(text)

def embedding_is_valid(embedding_array):
    """
    Validates if the embedding array is valid.
    Args:
        embedding_array (np.array): The embedding array.
    Returns:
        bool: Whether the embedding is valid.
    """
    return embedding_array.ndim == 1 and embedding_array.shape[0] == 1536 and not np.isnan(embedding_array).any()
