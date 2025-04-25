# from review_manager import ReviewManager
from typing import List

class BookReview:
    def __init__(self, title: str):
        self.title: str = title
        self.scores: List[int] = []

    def add_review(self, score: int) -> None:
        self.scores.append(score)
    
    def average_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)