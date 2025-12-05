import torch
from transformers import pipeline
from typing import List

class SentimentService:
    def __init__(self):
        print("🧠 Loading AI Sentiment Model...")
        # Check if GPU is available
        self.device = 0 if torch.cuda.is_available() else -1
        print(f"🚀 AI running on: {'GPU (RTX 3050)' if self.device == 0 else 'CPU'}")
        
        # Load pre-trained sentiment analysis model
        self.analyzer = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=self.device
        )

    def analyze_comments(self, comments: List[str]) -> float:
        """
        Analyzes a list of comments and returns a Quality Score (0-100).
        """
        if not comments:
            return 50.0 # Neutral score if no comments

        # Truncate comments to avoid token limit issues (simple approach)
        # We analyze up to 20 comments per video to keep it fast
        comments_to_analyze = comments[:20]
        
        results = self.analyzer(comments_to_analyze)
        
        # Calculate score
        # POSITIVE = 1, NEGATIVE = 0
        positive_count = 0
        for res in results:
            if res['label'] == 'POSITIVE':
                positive_count += 1
        
        # Score = Percentage of positive comments
        score = (positive_count / len(results)) * 100
        return round(score, 1)

# Singleton instance
sentiment_service = SentimentService()
