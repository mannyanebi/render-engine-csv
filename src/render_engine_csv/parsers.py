import csv
from typing import List, Dict, Any, Tuple, Type
from render_engine.parsers.base_parsers import BasePageParser
from .csv_filters import Direction  # Import the Direction enum

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
        extras = getattr(page, "parser_extras", {})

        # Extract column exclusion and filtering options from parser_extras
        exclude_columns = extras.get("exclude_columns", [])
        filter_options = extras.get("filter_by", [])

        with open(content_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

        # Apply exclude_columns to exclude specific columns
        filtered_data = CSVPageFileParser.exclude_columns(data, exclude_columns)

        # Apply filter_by to filter data based on provided filtering options
        filtered_data = CSVPageFileParser.filter_by(filtered_data, filter_options)

        return filtered_data, ""

    @staticmethod
    def exclude_columns(data: List[Dict[str, Any]], exclude_columns: List[str]) -> List[Dict[str, Any]]:
        """
        Exclude specific columns from the CSV data.
        :param data: The list of dictionaries representing the CSV data.
        :param exclude_columns: A list of column names to exclude.
        :return: The filtered list of dictionaries.
        """
        if not exclude_columns:
            return data

        # Create a set of column names to exclude
        exclude_columns_set = set(exclude_columns)

        # Filter the data by excluding the specified columns
        filtered_data = []
        for row in data:
            filtered_row = {col: val for col, val in row.items() if col not in exclude_columns_set}
            filtered_data.append(filtered_row)

        return filtered_data

    @staticmethod
    def filter_by(data: List[Dict[str, Any]], filter_options: List[Tuple[str, Direction, Any]]) -> List[Dict[str, Any]]:
        """
        Filter the CSV data based on filtering options.
        :param data: The list of dictionaries representing the CSV data.
        :param filter_options: A list of filtering options as tuples (column, direction, value).
        :return: The filtered list of dictionaries.
        """
        if not filter_options:
            return data

        filtered_data = []
        for row in data:
            include_row = True
            for column, direction, value in filter_options:
                if direction == Direction.LESS_THAN:
                    if int(row.get(column, 0)) >= value:
                        include_row = False
                        break
                elif direction == Direction.GREATER_THAN:
                    if int(row.get(column, 0)) <= value:
                        include_row = False
                        break

            if include_row:
                filtered_data.append(row)

        return filtered_data
