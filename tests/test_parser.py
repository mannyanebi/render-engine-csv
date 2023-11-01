import csv
import os
import tempfile
import pytest

from render_engine_csv.parsers import CSVPageFileParser
from render_engine_csv.csv_filters import Direction  # Import the Direction enum

# Create a fixture to generate a temporary CSV file for testing
@pytest.fixture
def temp_csv_file():
    data = [
        {"Name": "Alice", "Age": "25", "City": "New York"},
        {"Name": "Bob", "Age": "31", "City": "Los Angeles"},
        {"Name": "Charlie", "Age": "35", "City": "Chicago"},
    ]

    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Name", "Age", "City"])
        writer.writeheader()
        writer.writerows(data)

    yield csv_file.name
    os.remove(csv_file.name)

def test_parse_content_path(temp_csv_file):
    parser = CSVPageFileParser()
    data, content = parser.parse_content_path(temp_csv_file)

    assert isinstance(data, list)
    assert len(data) == 3
    assert content == ""

def test_exclude_columns(temp_csv_file):
    parser = CSVPageFileParser()
    data, _ = parser.parse_content_path(temp_csv_file)

    # Exclude the "City" column
    extras = {"exclude_columns": ["City"]}
    filtered_data = parser.exclude_columns(data, extras["exclude_columns"])
    
    assert len(filtered_data) == 3  # All rows should be retained
    assert all("City" not in row for row in filtered_data)

    # Exclude both "Name" and "Age" columns
    extras = {"exclude_columns": ["Name", "Age"]}
    filtered_data = parser.exclude_columns(data, extras["exclude_columns"])
    
    assert len(filtered_data) == 3  # All rows should be retained
    assert all("Name" not in row and "Age" not in row for row in filtered_data)

def test_filter_by(temp_csv_file):
    parser = CSVPageFileParser()
    data, _ = parser.parse_content_path(temp_csv_file)

    # Filter by "Age" values less than 30
    extras = {"filter_by": [("Age", Direction.LESS_THAN, 30)]}
    filtered_data = parser.filter_by(data, extras["filter_by"])
    
    assert len(filtered_data) == 1  # Rows with "Age" less than 30
    assert all(int(row["Age"]) < 30 for row in filtered_data)

    # Filter by "Age" values greater than or equal to 30
    extras = {"filter_by": [("Age", Direction.GREATER_THAN, 30)]}
    filtered_data = parser.filter_by(data, extras["filter_by"])
    
    assert len(filtered_data) == 2  # Rows with "Age" greater than or equal to 30
    assert all(int(row["Age"]) >= 30 for row in filtered_data)
