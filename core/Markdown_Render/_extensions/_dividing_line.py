from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class DividingLineExtension(Extension):
    """Adds a dividing line to the top of the document."""

    def extendMarkdown(self, md):
        """Add a DividingLinePreprocessor to the Markdown instance."""
        md.preprocessors.register(DividingLinePreprocessor(md), "dividing_line", 100)

class DividingLinePreprocessor(Preprocessor):
    REPLACE_HANDLER = {
        "---": "<hr>",
        "***": "<hr>",
        "___": "<hr>",
    }

    def run(self, lines: list[str]) -> list[str]:
        """Replace newlines with <hr> tags."""
        output: list[str] = []
        for line in lines:
            if line in self.REPLACE_HANDLER:
                output.append(self.REPLACE_HANDLER[line])
            else:
                output.append(line)
        return output