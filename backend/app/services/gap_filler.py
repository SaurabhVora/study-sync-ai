from sentence_transformers import SentenceTransformer, util
from typing import List
import torch

class GapFillerService:
    def __init__(self):
        print("🧩 Loading Gap Filler AI Model...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # We use a lightweight model for semantic similarity
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
        
        # Knowledge Base: Ideal sub-topics for known subjects
        # In a real app, this would come from a database or LLM generation
        self.knowledge_base = {
            "Operating Systems": [
                "Process Management", "CPU Scheduling", "Deadlocks", 
                "Memory Management", "Virtual Memory", "File Systems", 
                "I/O Systems", "Security and Protection"
            ],
            "Data Structures": [
                "Arrays", "Linked Lists", "Stacks", "Queues", 
                "Trees", "Graphs", "Hashing", "Sorting Algorithms"
            ]
        }

    def find_gaps(self, current_topics: List[str], required_topics: List[str]) -> List[str]:
        """
        Identifies missing key concepts by comparing user's current topics against a required list.
        """
        if not required_topics or not current_topics:
            return required_topics or []

        missing_topics = []

        # Encode both lists
        required_embeddings = self.model.encode(required_topics, convert_to_tensor=True)
        current_embeddings = self.model.encode(current_topics, convert_to_tensor=True)

        # Check each required topic against current topics
        for i, req_topic in enumerate(required_topics):
            # Calculate similarity with all current topics
            # We use cosine similarity
            cosine_scores = util.cos_sim(required_embeddings[i], current_embeddings)
            
            # Get the best match score
            best_match_score = torch.max(cosine_scores).item()
            
            # If the best match is below a threshold (e.g., 0.5), it's a gap!
            if best_match_score < 0.5:
                print(f"⚠️ Gap Detected: '{req_topic}' (Best match score: {best_match_score:.2f})")
                missing_topics.append(req_topic)

        return missing_topics

# Singleton
gap_filler_service = GapFillerService()
