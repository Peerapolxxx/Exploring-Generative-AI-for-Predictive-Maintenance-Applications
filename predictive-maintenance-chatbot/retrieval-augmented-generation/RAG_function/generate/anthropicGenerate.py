import os
import anthropic
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from RAG_function.generate.prompts_V4 import (
    SYSTEM_PROMPT,
    CONTEXT_PROMPT,
    INSTRUCTION_PROMPT
)
from RAG_function.generate.augmented import augmented_generate

# API Setup
os.environ["ANTHROPIC_API_KEY"] = ""
anthropicAi = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Conversation History Management
@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = datetime.now()

class ConversationHistory:
    def __init__(self, max_history: int = 10):
        self.messages: List[Message] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        message = Message(role=role, content=content)
        self.messages.append(message)
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_history_text(self) -> str:
        return "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages])
    
    def clear(self):
        self.messages = []

def anthropic_generate(retrieval_documents: str, conversation_history: str, question: str):
    """Generate response using Anthropic API"""
    try:
        response = anthropicAi.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.0,
            system=SYSTEM_PROMPT,  # ย้าย system prompt มาที่นี่
            messages=[
                {
                    "role": "user",
                    "content": (
                        CONTEXT_PROMPT.format(
                            retrieval_documents=retrieval_documents,
                            conversation_history=conversation_history
                        ) +
                        INSTRUCTION_PROMPT.format(
                            question=question
                        )
                    )
                }
            ]
        )
        return response
    except Exception as e:
        print(f"\nError in API call: {str(e)}")
        raise

def anthropic_chat(rerank_documents, query, conversation_history: ConversationHistory, top_k: int = 5):
    """Main chat function that handles the complete conversation flow"""
    try:
        # Generate augmented documents
        top_k =3
        augmented_documents = augmented_generate(rerank_documents, top_k)

        # Get conversation history
        history_text = conversation_history.get_history_text()
        
        # Print debug information
        print("\n=== Chat Information ===")
        print("\n1. Query:")
        print(f"{query}")
        
        print("\n2. Conversation History:")
        print(f"{history_text if history_text else '[Empty History]'}")
        
        print("\n3. Augmented Documents:")
        print(f"{augmented_documents if augmented_documents else '[No Documents]'}")
        
        print("\n=== Sending to Anthropic API ===")
        
        # Get response from Anthropic
        response = anthropic_generate(
            retrieval_documents=augmented_documents,
            conversation_history=history_text,
            question=query
        )
        
        # Add to conversation history
        conversation_history.add_message("user", query)
        conversation_history.add_message("assistant", response.content[0].text)
        
        print("\n=== Response Received ===")
        print(f"Response content: {response.content[0].text}")
        # print(f"Response content: TEST")
        
        
        return response.content
             
    except Exception as e:
        print(f"\nError in chat function: {str(e)}")
        return f"Error occurred: {str(e)}"
