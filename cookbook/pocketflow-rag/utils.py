import os
import numpy as np
from openai import OpenAI

def call_llm(prompt):    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def get_simple_embedding(text):
    # Create a 128-dim vector to store character frequencies
    embedding = np.zeros(128, dtype=np.float32)
    
    # Count character frequencies in the text
    for char in text:
        embedding[ord(char) % 128] += 1.0
    
    # Normalize the vector to unit length
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding /= norm
    
    return embedding

def get_embedding(text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    
    # Extract the embedding vector from the response
    embedding = response.data[0].embedding
    
    # Convert to numpy array for consistency with other embedding functions
    return np.array(embedding, dtype=np.float32)

def fixed_size_chunk(text, chunk_size=2000):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])
    return chunks

if __name__ == "__main__":
    print("=== Testing call_llm ===")
    prompt = "In a few words, what is the meaning of life?"
    print(f"Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"Response: {response}")

    print("=== Testing embedding function ===")
    
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "Python is a popular programming language for data science."
    
    # Test the simple embedding function
    # emb1 = get_embedding(text1)
    # emb2 = get_embedding(text2)
    
    # print(f"Embedding 1 shape: {emb1.shape}")
    # print(f"Embedding 2 shape: {emb2.shape}")
    
    # # Calculate similarity (dot product)
    # similarity = np.dot(emb1, emb2)
    # print(f"Similarity between texts: {similarity:.4f}")
    
    # # Compare with a different text
    # text3 = "Machine learning is a subset of artificial intelligence."
    # emb3 = get_embedding(text3)
    # similarity13 = np.dot(emb1, emb3)
    # similarity23 = np.dot(emb2, emb3)
    
    # print(f"Similarity between text1 and text3: {similarity13:.4f}")
    # print(f"Similarity between text2 and text3: {similarity23:.4f}")
    
    # # These simple comparisons should show higher similarity 
    # # between related concepts (text2 and text3) than between
    # # unrelated texts (text1 and text3)
    
    # Test OpenAI embeddings (requires API key)
    print("\nTesting OpenAI embeddings (requires API key):")
    oai_emb1 = get_embedding(text1)
    oai_emb2 = get_embedding(text2)
    print(f"OpenAI Embedding 1 shape: {oai_emb1.shape}")
    oai_similarity = np.dot(oai_emb1, oai_emb2)
    print(f"OpenAI similarity between texts: {oai_similarity:.4f}")