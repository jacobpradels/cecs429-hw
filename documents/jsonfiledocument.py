from io import StringIO
import json
from pathlib import Path
from .document import Document
from typing import Iterable

class JsonFileDocument(Document):
    def __init__(self, id : int, path: Path):
        super().__init__(id)
        self.path = path
    
    @property
    def title(self) -> str:
        with open(self.path) as file:
            data = json.load(file)
            return data["title"]

    def get_content(self) -> Iterable[str]:
        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)
            return StringIO(data["body"])

    @staticmethod
    def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
        """A factory method to create a JsonFileDocument around the given file path."""
        return JsonFileDocument(doc_id, abs_path)