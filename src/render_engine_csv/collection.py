import csv
import os
from typing import List, Type

from render_engine.collection import Collection

from .parsers import CSVPageParser  # Import your CSVPageParser

class CSVCollection(Collection):
    PageParser = CSVPageParser  # type: ignore # Use the CSVPageParser for parsing CSV content

    def __init__(self, content_path: str | None = None, content: str | None = None):
        super().__init__()

        if content_path:
            self.load_csv_files(content_path)

    def load_csv_files(self, directory_path: str):
        """
        Load CSV files from a directory.
        :param directory_path: The path to the directory containing CSV files.
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory '{directory_path}' not found.")

        csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
        for csv_file in csv_files:
            csv_file_path = os.path.join(directory_path, csv_file)
            self.add_page(csv_file, csv_file_path)

    def add_page(self, page_name: str, content_path: str):
        """
        Add a page to the collection using a CSV file.
        :param page_name: The name of the page.
        :param content_path: The path to the CSV file.
        """
        content = self.Parser.read_csv(content_path)
        super().add_page(page_name, content)

    @property
    def pages(self):
        """
        Iterate through the pages in the collection.
        """
        for page_name, content in self._pages.items():
            yield page_name, content
