from review.code_fixer import CodeFixer

broken = """
def hello(
"""

fixed = CodeFixer().fix(
    broken,
    "'(' was never closed",
)

print(fixed)