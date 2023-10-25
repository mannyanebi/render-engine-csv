import csv
from typing import List, Dict, Any, Tuple
from render_engine.parsers.base_parsers import BasePageParser
import enum

class Direction(enum.Enum):
    LESS_THAN = 1
    GREATER_THAN = 2

class CSVPageParser(BasePageParser):
    """
    Parser for CSV content.
    """

    def __init__(self, config: dict):
        """
        Initialize the CSVPageParser with a configuration dictionary.
        :param config: A dictionary specifying how to parse rows and columns.
        """
        super().__init__()
        self.config = config

    def parse_row(self, row: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        """
        Parse a row of CSV data according to the provided configuration.
        :param row: A dictionary representing a CSV row with column names as keys.
        :return: A tuple containing attributes (dictionary) and content (string).
        """
        content_column = self.config.get("content_column")
        if content_column and content_column in row:
            content = row[content_column]
            row.pop(content_column)
        else:
            content = ""

        # You can add more customization logic here based on the configuration

        return row, content

    def read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read a CSV file and return a list of dictionaries.
        Each dictionary represents a row with column names as keys.
        :param file_path: The path to the CSV file.
        :return: A list of dictionaries representing the CSV data.
        """
        data = []
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parsed_row, content = self.parse_row(row)
                data.append(parsed_row)
        return data

    def filter_by(self, field_name: str, field_value: str, direction: Direction):
        """
        Filter CSV data based on a given field, value, and direction.
        :param field_name: The name of the field to filter.
        :param field_value: The value to compare.
        :param direction: The filter direction (Direction.LESS_THAN or Direction.GREATER_THAN).
        """
        data = self.read_csv(self.content_path)
        filtered_data = []

        for row in data:
            if direction == Direction.LESS_THAN:
                if row.get(field_name) is not None and row[field_name] < field_value:
                    filtered_data.append(row)
            elif direction == Direction.GREATER_THAN:
                if row.get(field_name) is not None and row[field_name] > field_value:
                    filtered_data.append(row)
            else:
                # Handle other cases or simply pass
                pass

        return filtered_data
