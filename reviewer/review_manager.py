"""
Review Manager
"""

from reviewer.reviewer_agent import ReviewerAgent


class ReviewManager:

    def __init__(self):

        self.reviewer = ReviewerAgent()

    def review(self, code):

        result = self.reviewer.review(code)

        print()

        print("========== REVIEW ==========")

        print(f"Passed : {result.passed}")
        print(f"Score  : {result.score}")
        print(f"Feedback : {result.feedback}")

        print("============================")

        return result