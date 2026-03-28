import os
import chromadb
import uuid

class ChromaWrapper:
    def __init__(self, path: str, collection_name: str = "scholarships"):
        self.path = path
        os.makedirs(path, exist_ok=True)
        # Using persistent client for local storage
        self.client = chromadb.PersistentClient(path=self.path)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add(self, embeddings: list = None, documents: list = None, metadatas: list = None, ids: list = None):
        if not documents:
            return

        if not ids:
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]

        if embeddings:
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        else:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

    def query(self, query_embeddings: list = None, query_texts: list = None, n_results: int = 5):
        if self.collection.count() == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        n_results = min(n_results, self.collection.count())
        if n_results == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        if query_embeddings:
            res = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )
        else:
            res = self.collection.query(
                query_texts=query_texts,
                n_results=n_results
            )
        return res

    def count(self):
        return self.collection.count()

    def get_name(self):
        return self.collection.name
