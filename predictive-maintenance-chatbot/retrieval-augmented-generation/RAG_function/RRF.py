import json

def reciprocal_rank_fusion(top_vector_documents_search, top_bm25_documents_search, top_k=3):
   # ฟังก์ชันสำหรับคำนวณคะแนน Reciprocal Rank Fusion (RRF)
   def get_rrf_score(rank):
      return round(1 / (60 + rank), 9)
      # return 1 / (60 + rank)

   combined_results = {}

   # ประมวลผลเอกสารจากผลการค้นหาแบบเวกเตอร์
   for doc in top_vector_documents_search:
      doc_id = doc["metadata"]["chunk_id"]
      if doc_id not in combined_results:
         combined_results[doc_id] = {
            "page_content": doc["page_content"],
            "rrf_score": 0,
            "metadata": doc["metadata"],
         }
      combined_results[doc_id]["rrf_score"] += get_rrf_score(doc["rank"])

   # ประมวลผลเอกสารจากผลการค้นหาแบบ BM25
   for doc in top_bm25_documents_search:
      doc_id = doc["metadata"]["chunk_id"]
      if doc_id not in combined_results:
         combined_results[doc_id] = {
            "page_content": doc["page_content"],
            "rrf_score": 0,
            "metadata": doc["metadata"],
         }
      combined_results[doc_id]["rrf_score"] += get_rrf_score(doc["rank"])

   # จัดเรียงผลลัพธ์รวมตามคะแนน RRF ในลำดับจากมากไปน้อย
   sorted_items = sorted(
        combined_results.items(), 
        key=lambda x: x[1]["rrf_score"], 
        reverse=True
   )

   results = []
   # วนซ้ำผ่านผลลัพธ์ที่จัดอันดับใหม่และสร้างผลลัพธ์
   for rank, (doc_id, item) in enumerate(sorted_items[:top_k]):  
      result = {
         "page_content": item["page_content"],
         "rrf_score": round(float(item["rrf_score"]), 9),
         "rank": rank + 1,
         "metadata": item["metadata"]
      }
      results.append(result)

   return results
