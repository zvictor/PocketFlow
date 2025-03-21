import numpy as np
import faiss

def create_index(dimension=128):
    """Create a new vector index for fast similarity search
    
    Args:
        dimension: The dimensionality of the vectors to be indexed
        
    Returns:
        tuple: (index, items_list) where:
            - index is the FAISS index for searching
            - items_list is an empty list for storing the items
    """
    # Create a flat (exact, brute-force) index for storing vectors
    index = faiss.IndexFlatL2(dimension)
    # Initialize an empty list to store the actual items
    items_list = []
    return index, items_list

def add_to_index(index, items_list, embedding, item):
    """Add an item and its vector representation to the index
    
    Args:
        index: The FAISS index
        items_list: The list of items corresponding to vectors in the index
        embedding: The vector representation of the item (numpy array)
        item: The actual item to store
        
    Returns:
        int: The position where the item was added
    """
    # Make sure the embedding is a numpy array with the right shape for FAISS
    vector = np.array(embedding).reshape(1, -1).astype(np.float32)
    
    # Add the vector to the index
    index.add(vector)
    
    # Store the item and return its position
    items_list.append(item)
    return len(items_list) - 1

def search_index(index, items_list, query_embedding, k=1):
    """Search for the k most similar items to the query vector
    
    Args:
        index: The FAISS index
        items_list: The list of items corresponding to vectors in the index
        query_embedding: The query vector (numpy array)
        k: Number of results to return (default: 1)
        
    Returns:
        tuple: (found_items, distances) where:
            - found_items is a list of the k most similar items
            - distances is a list of the corresponding distances
    """
    # Make sure we don't try to retrieve more items than exist in the index
    k = min(k, len(items_list))
    if k == 0:
        return [], []
        
    # Make sure the query is a numpy array with the right shape for FAISS
    query_vector = np.array(query_embedding).reshape(1, -1).astype(np.float32)
    
    # Search the index
    D, I = index.search(query_vector, k)
    
    # Get the items corresponding to the found indices
    found_items = [items_list[i] for i in I[0]]
    distances = D[0].tolist()
    
    return found_items, distances

# Example usage
if __name__ == "__main__":
    # Create a new index
    index, items = create_index(dimension=3)
    
    # Add some random vectors and items
    for i in range(5):
        vector = np.random.random(3)
        add_to_index(index, items, vector, f"Item {i}")
        
    print(f"Added {len(items)} items to the index")
    
    # Search for a similar vector
    query = np.random.random(3)
    found_items, distances = search_index(index, items, query, k=2)
    
    print("Query:", query)
    print("Found items:", found_items)
    print("Distances:", distances) 