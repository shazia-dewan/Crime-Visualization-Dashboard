import mongomock
import pymongo
import pytest

# Use mongomock to create an in-memory MongoDB for testing
@pytest.fixture
def mock_mongo():
    client = mongomock.MongoClient()
    db = client["CrimeDatabase"]
    return db

def test_insert_arrest_data(mock_mongo):
    ArrestData = mock_mongo["CrimeCollection"]
    test_data = {"Crime": "Arson", "Number": 1000}

    # Insert the test data
    result = ArrestData.insert_one(test_data)
    assert result.acknowledged is True

    # Verify the data was inserted
    inserted_data = ArrestData.find_one({"Crime": "Arson"})
    assert inserted_data is not None
    assert inserted_data["Number"] == 1000
