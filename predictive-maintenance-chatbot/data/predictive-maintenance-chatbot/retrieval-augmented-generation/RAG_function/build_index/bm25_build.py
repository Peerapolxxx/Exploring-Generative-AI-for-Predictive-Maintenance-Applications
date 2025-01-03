import os
import json
import pickle
import re
from rank_bm25 import BM25Okapi



class bm25_build:
    def __init__(self):
        self.bm25_model = None
        self.documents = None
        
    def tokenization(self, text):
    
        """Tokenizes text by lowering case, removing unwanted characters, and splitting by spaces."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove unwanted characters
        return text.split()
        
    def load_bm25_store(self, load_bm25Store_dir):
        # ตรวจสอบว่าโฟลเดอร์มีอยู่หรือไม่
        if os.path.exists(load_bm25Store_dir):
            print(f"Directory exists: {load_bm25Store_dir}")
            
            # แสดงรายการไฟล์ในโฟลเดอร์
            files = os.listdir(load_bm25Store_dir)
            if files:
                print("Files in directory:")
                for file in files:
                    print(f"- {file}")
                    
                    # โหลด BM25 model จากไฟล์ BM25Model.pkl
                    if file == 'BM25Model.pkl':
                        bm25Model_file_path = os.path.join(load_bm25Store_dir, file)
                        with open(bm25Model_file_path, 'rb') as f:
                            self.bm25_model = pickle.load(f)
                            print(f"Loaded BM25 model from {bm25Model_file_path}")
                    
                    # โหลด documents จากไฟล์ documents.json
                    if file == 'documents.json':
                        json_file_path = os.path.join(load_bm25Store_dir, file)
                        with open(json_file_path, "r", encoding="utf-8") as f:
                            self.documents = json.load(f)
            
            else:
                print("No files found in the directory.")
        else:
            print(f"Directory does not exist: {load_bm25Store_dir}")
        
        # ตรวจสอบว่า bm25_model และ documents ถูกโหลดหรือไม่
        if self.bm25_model is None:
            raise FileNotFoundError("BM25 model file not found in the directory.")
        if self.documents is None:
            raise FileNotFoundError("Documents file not found in the directory.")
        
        print("BM25 model and documents loaded successfully.")
    
    def bestMatching_search(self, query, n=1):
        # ตรวจสอบว่า bm25_model และ documents ถูกโหลดก่อนเรียก search
        if self.bm25_model is None or self.documents is None:
            raise ValueError("BM25 model or documents not loaded. Call load_bm25_model() first.")
        
        tokenized_query = self.tokenization(query)
        
        # คำนวณคะแนน BM25 ค้นหาเอกสารที่ตรงกับ query ที่สุด
        doc_scores = self.bm25_model.get_scores(tokenized_query)
        
        # เลือกเอกสารอันดับต้น ๆ พร้อมคะแนน
        top_n=n
        top_indices = doc_scores.argsort()[-top_n:][::-1]  # ดัชนีของคะแนนสูงสุดเรียงลำดับจากมากไปน้อย

        # สร้างผลลัพธ์พร้อมคะแนน
        results = [
            {
            "page_content": self.documents[idx]['page_content'],
            "bm25_score": round(float(doc_scores[idx]), 9), 
            # "bm25_score": float(doc_scores[idx]),
            "rank": rank + 1,
            "content_tokenizer": self.documents[idx]['content_tokenizer'],
            "metadata": self.documents[idx]['metadata']
            }
            for rank, idx in enumerate(top_indices)
        ]
                
        return results