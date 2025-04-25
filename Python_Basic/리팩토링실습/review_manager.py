from book_review import BookReview
from typing import Dict, Tuple

class ReviewManager:
    def __init__(self):
        self.books: Dict[str, BookReview] = {}

    def add_review(self, title: str, score: int) -> None:
        if title not in self.books:
            self.books[title] = BookReview(title)
        self.books[title].add_review(score)

    def get_average(self, title: str) -> float:
        if title not in self.books:
            return 0.0
        return self.books[title].average_score()
    
    def get_top_book(self) -> Tuple[str, float]:
        if not self.books:
            return ("", 0.0)
        max_title = ""
        max_avg = 0.0
        for title, book in self.books.items():
            avg = book.average_score()
            if avg > max_avg or (avg == max_avg and title < max_title):
                max_title = title
                max_avg = avg
        return max_title, max_avg