import csv
import os
import tempfile

import pytest

from render_engine_csv.parsers import CSVPageFileParser

# Create a fixture to generate a temporary CSV file for testing
@pytest.fixture
def temp_csv_file():
    data = [
        {"Name": "Alice", "Age": "25", "City": "New York"},
        {"Name": "Bob", "Age": "30", "City": "Los Angeles"},
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

def test_filter_by(temp_csv_file):
    parser = CSVPageFileParser()
    data, _ = parser.parse_content_path(temp_csv_file)

    # Filter by excluding the "City" column
    extras = ["City"]
    filtered_data = parser.filter_by(data, extras)
    
    assert len(filtered_data) == 3  # All rows should be retained
    assert all("City" not in row for row in filtered_data)

    # Filter by excluding the "Age" column
    extras = {"Age"}
    filtered_data = parser.filter_by(data, extras)

    
    assert len(filtered_data) == 3  # All rows should be retained
    assert all("Age" not in row for row in filtered_data)

    # Filter by excluding both "Name" and "Age" columns
    extras = {"Name", "Age"}
    filtered_data = CSVPageFileParser.filter_by(data, extras)
    
    assert len(filtered_data) == 3  # All rows should be retained
    assert all("Name" not in row and "Age" not in row for row in filtered_data)
