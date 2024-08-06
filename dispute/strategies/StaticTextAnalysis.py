

class StaticTextAnalysisStrategy:

    def __init__(self):
        pass

    def analyze(self, text: str) -> bool:
        return text.strip() == ""