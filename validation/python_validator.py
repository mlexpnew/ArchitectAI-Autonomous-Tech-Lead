"""
Python Validator

Checks whether generated Python code is syntactically valid.
"""

import ast


class PythonValidator:

    @staticmethod
    def validate(code: str):

        try:

            ast.parse(code)

            return True, None

        except SyntaxError as e:

            return False, str(e)