import csv
from typing import List, Dict, Any, Tuple, Type
from render_engine.parsers.base_parsers import BasePageParser
import enum

class Direction(enum.Enum):
    LESS_THAN = 1
    GREATER_THAN = 2



Page = Type[Any]

class CSVPageFileParser(BasePageParser):
    """
    Parses a CSV file into page data.
    """

    @staticmethod
    def parse_content_path(content_path: str, page: Page | None = None) -> Tuple[List[Dict[str, Any]], str]:
        """
        Read a CSV file and return a list of dictionaries.
        Each dictionary represents a row with column names as keys.
        :param file_path: The path to the CSV file.
        :param page: The Page object associated with the content.
        :return: A tuple containing the list of dictionaries representing the CSV data and an empty string.
        """
        data = []
        extras = getattr(page, "parser_extras", [])
        with open(content_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

        # Apply filter_by to exclude specific columns based on parser_extras
        filtered_data = CSVPageFileParser.filter_by(data, extras)
        return filtered_data, ""
    

    @staticmethod
    def filter_by(data: List[Dict[str, Any]], extras: List[str]) -> List[Dict[str, Any]]:
        """
        Filter the CSV data by excluding specific columns based on the extras provided.
        :param data: The list of dictionaries representing the CSV data.
        :param extras: A dictionary containing the names of columns to exclude.
        :return: The filtered list of dictionaries.
        """
        if not extras:
            return data

        # Create a set of column names to exclude
        exclude_columns = set(extras)

        # Filter the data by excluding the specified columns
        filtered_data = []
        for row in data:
            filtered_row = {col: val for col, val in row.items() if col not in exclude_columns}
            filtered_data.append(filtered_row)

        return filtered_data

    
