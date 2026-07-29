"""
Base Backend Generator
"""

from generators.ai.code_generator import AICodeGenerator


class BaseGenerator:

    def __init__(self):

        self.ai = AICodeGenerator()

    def generate(self, prompt: str):

        return self.ai.generate(prompt)