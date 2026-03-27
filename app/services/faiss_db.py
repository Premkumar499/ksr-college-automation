import os
import faiss
import numpy as np
import json
import logging

class FaissDB:
    def __init__(self, path: str, dim: int = 3072):
        self.path = path
        self.index_path = os.path.join(path, "index.faiss")
        self.meta_path = os.path.join(path, "meta.json")
        self.dim = dim
        os.makedirs(path, exist_ok=True)
        
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = {"documents": [], "metadatas": []}
            self.save()

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f)

    def add(self, embeddings: list, documents: list, metadatas: list, ids: list = None):
        if not embeddings:
            return
        
        arr = np.array(embeddings).astype("float32")
        self.index.add(arr)
        
        self.metadata["documents"].extend(documents)
        self.metadata["metadatas"].extend(metadatas)
        self.save()

    def query(self, query_embeddings: list, n_results: int = 5):
        if self.index.ntotal == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
        arr = np.array(query_embeddings).astype("float32")
        # Ensure n_results doesn't exceed total
        n_results = min(n_results, self.index.ntotal)
        if n_results == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
            
        distances, indices = self.index.search(arr, n_results)
        
        docs_res = []
        meta_res = []
        dist_res = []
        
        for i in range(len(indices)):
            cur_docs = []
            cur_meta = []
            cur_dist = []
            for j in range(len(indices[i])):
                idx = int(indices[i][j])
                if idx >= 0 and idx < len(self.metadata["documents"]):
                    cur_docs.append(self.metadata["documents"][idx])
                    cur_meta.append(self.metadata["metadatas"][idx])
                    cur_dist.append(float(distances[i][j]))
            docs_res.append(cur_docs)
            meta_res.append(cur_meta)
            dist_res.append(cur_dist)
            
        return {
            "documents": docs_res,
            "metadatas": meta_res,
            "distances": dist_res
        }

    def count(self):
        return self.index.ntotal

    def get_name(self):
        return "faiss_scholarships"
