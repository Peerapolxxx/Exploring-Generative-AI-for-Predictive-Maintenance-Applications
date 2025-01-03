from typing import Dict, List


def augmented_generate(documents: List[Dict], top_k: int = 5) -> str:
    """
    Generate augmented context from monitoring data
    
    Args:
        documents (List[Dict]): List of equipment monitoring data
        top_k (int): Number of top relevant entries to use
        
    Returns:
        str: Formatted monitoring data text
    """
    monitoring_text = ""
    
    # Ensure we don't exceed the documents length
    top_k = min(top_k, len(documents))
    
    # Process each document
    for doc in documents[:top_k]:
        try:
            # Extract content from metadata if available, otherwise use page_content
            content = (
                doc.get("metadata", {}).get("contextualized_content") or 
                doc.get("metadata", {}).get("content") or 
                doc.get("page_content", "")
            )
            
            if content:
                monitoring_text += f"<monitoring_data>\n{content}\n</monitoring_data>\n"
            else:
                print(f"Warning: No monitoring data found")
                
        except Exception as e:
            print(f"Error processing monitoring data: {str(e)}")
            continue
            
    return monitoring_text