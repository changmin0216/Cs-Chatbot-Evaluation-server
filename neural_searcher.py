from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from config import QDRANT_URL, QDRANT_API_KEY
import math
import time

class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="mps")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
    def search(self, text: str):
        # Convert text query into vector
        start = time.time()
        math.factorial(100000)
        vector = self.model.encode(text).tolist()
        end = time.time()
        print(f"answer text embedding time{end - start:.5f} sec")

        # Use `vector` for search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,  # If you don't want any filters for now
            limit=5,  # 5 the most closest results is enough
        )
        # `search_result` contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads


