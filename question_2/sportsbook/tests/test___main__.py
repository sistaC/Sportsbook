from fastapi.testclient import TestClient
from sportsbook.__main__ import app
from sportsbook.database import fetch_values

from conftest import execute_query

client = TestClient(app)

def test_post_sport():
    body = {
    "sport_name": "test",
    "slug": "test",
    "active": True
    }
    response = client.post("/sport", json=body)
    assert response.status_code == 200
    assert response.json() == 'Inserted successfully with id 1'

    response = client.post("/sport", json=body)
    assert response.status_code == 400
    response.json()['message'] == 'UNIQUE constraint failed: sports.sport_name'

def test_post_sport_error():
    body = {
    "sport_name": "@%^Test",
    "slug": "string",
    "active": True
    }
    response = client.post("/sport", json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Value error, Sports name cannot contain special characters'

def test_post_event():
    body = {
    "event_name": "test",
    "slug": "test",
    "active": True,
    "type": "inplay",
    "sport_name": "test",
    "status": "pending",
    "scheduled_start": "2023-08-30T14:22:43.608Z"
    }

    response = client.post("/event", json=body)
    assert response.status_code == 200
    assert response.json() == 'Inserted successfully with id 1'

    response = client.post("/event", json=body)
    assert response.status_code == 400
    response.json()['message'] == 'UNIQUE constraint failed: events.event_name'

    body['sport_name'] = "test1"
    response = client.post("/event", json=body)
    assert response.status_code == 400

def test_post_event_error():
    body = {
    "event_name": "@#^&*",
    "slug": "test",
    "active": True,
    "type": "inplay",
    "sport_name": "test",
    "status": "pending",
    "scheduled_start": "2023-08-30T14:22:43.608Z"
    }

    response = client.post("/event", json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Value error, Events name cannot contain special characters'

    body = {
    "event_name": "test",
    "slug": "test",
    "active": True,
    "type": "inplayss",
    "sport_name": "test",
    "status": "pending",
    "scheduled_start": "2023-08-30T14:22:43.608Z"
    }

    response = client.post("/event", json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Event type should be one among ['preplay', 'inplay']"

    body = {
    "event_name": "test",
    "slug": "test",
    "active": True,
    "type": "inplay",
    "sport_name": "test",
    "status": "unknown",
    "scheduled_start": "2023-08-30 14:22:43.60"
    }

    response = client.post("/event", json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Event status should be one among ['pending', 'started', 'ended', 'cancelled']"

def test_post_selection():
    body = {
    "selection_name": "test",
    "event_name": "test",
    "price": 32.12,
    "active": True,
    "outcome": "void"}

    response = client.post("/selection", json=body)
    assert response.status_code == 200
    assert response.json() == 'Inserted successfully with id 1'

    response = client.post("/selection", json=body)
    assert response.status_code == 400
    response.json()['message'] == 'UNIQUE constraint failed: selections.selection_name'

def test_post_selection_error():
    body = {
    "selection_name": "@!235",
    "event_name": "test",
    "price": 32.12,
    "active": True,
    "outcome": "unknown"}

    response = client.post("/selection", json=body)
    assert response.status_code == 422
    body = {
    "selection_name": "test",
    "event_name": "test",
    "price": 32.12,
    "active": True,
    "outcome": "unknown"}

    response = client.post("/selection", json=body)
    assert response.status_code == 422

def test_put_sport():
    body = {
            "update": {
                "slug": "test1"
            },
            "condition": {
                "sport_name": "test1"
            }
            }
    response = client.put("/sport", json=body)
    assert response.status_code == 400

    body = {
            "update": {
                "slug": "test1"
            },
            "condition": {
                "sport_name": "test"
            }
            }
    response = client.put("/sport", json=body)
    assert response.status_code == 200
    query = 'SELECT * from sports where sport_name = "test"' 
    rows = execute_query(query)
    assert rows[0]['slug'] == "test1"

    body = {
        "update": {
            "sport_name": "test1"
        },
        "condition": {
            "id": 1
        }
        }
    response = client.put("/sport", json=body)
    assert response.status_code == 200

    query = 'SELECT * from events where sport_name = "test1"' 
    rows = execute_query(query)
    assert len(rows) == 1

def test_put_event():
    body = {
            "update": {
                "slug": "test1"
            },
            "condition": {
                "event_name": "test_none"
            }
        }
    
    response = client.put("/event", json=body)
    assert response.status_code == 400

    body = {
            "update": {
                "slug": "test1"
            },
            "condition": {
                "event_name": "test"
            }
            }
    response = client.put("/event", json=body)
    assert response.status_code == 200
    query = 'SELECT * from events where event_name = "test"' 
    rows = execute_query(query)
    assert rows[0]['slug'] == "test1"

    body = {
        "update": {
            "event_name": "test1",
            "active": False
        },
        "condition": {
            "id": 1
        }
        }
    response = client.put("/event", json=body)
    assert response.status_code == 200

    query = 'select * from sports where sport_name = "test1"'
    rows = execute_query(query)
    assert rows[0]['active'] == 0

    query = 'SELECT * from selections where event_name = "test1"' 
    rows = execute_query(query)
    assert len(rows) == 1

    body = {
        "update": {
            "event_name": "test1",
            "active": False
        },
        "condition": {
            "id": 2
        }
        }
    response = client.put("/event", json=body)
    assert response.status_code == 400
    
def test_put_selection():
    body = {
            "update": {
                "price": 1.1
            },
            "condition": {
                "selection_name": "test_none"
            }
        }
    
    response = client.put("/selection", json=body)
    assert response.status_code == 400

    body = {
            "update": {
                "price": 1.1
            },
            "condition": {
                "selection_name": "test"
            }
        }
    response = client.put("/selection", json=body)
    assert response.status_code == 200
    query = 'SELECT * from selections where selection_name = "test"' 
    rows = execute_query(query)
    assert rows[0]['price'] == 1.1

    body = {
        "update": {
            "selection_name": "test1",
            "active": False
        },
        "condition": {
            "id": 1
        }
        }
    response = client.put("/selection", json=body)
    assert response.status_code == 200

    query = 'SELECT * from selections where id = 1' 
    rows = execute_query(query)
    assert rows[0]['selection_name'] == 'test1'

    query = 'select * from events where event_name = "test1"'
    rows = execute_query(query)
    assert rows[0]['active'] == 0