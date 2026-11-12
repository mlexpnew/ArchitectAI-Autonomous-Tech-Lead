from reviewer.review_manager import ReviewManager


code = """
def hello():
    print("Hello World")
"""


ReviewManager().review(code)