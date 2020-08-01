"""
This file houses the unit test suite for viewing the goal customization interface
of a restaurant profile.
"""
import os
import sys
import pytest
from bson.objectid import ObjectId

sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from restaurants_app import app
from modules.restaurant_profile_manager import RestaurantProfileManager

@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()

def test_verification_route_no_login(client):
    """
    Test that goal customization page does not load unless user is logged in.
    """
    res = client.get("/profile/qr-verification", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_verification_route_logged_in(client):
    """
    Test that goal customization page loads when the user is logged in.
    """
    client.post("/login", data={"username": "junaid", "password": "Junaid123"})
    res = client.get("/profile/qr-verification", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data

def test_valid_completed_goal(client):
    """
    Test that a user cannot add a goal when they're not logged in.
    """
    rpm = RestaurantProfileManager("junaid")
    code = "junaid+5ef5009bccd1e88ead4cd076+0".split("+")
    msg = rpm.complete_goal(code[0], code[1], code[2])
    assert msg == "This goal has already been completed!"

def test_duplicate_completed_goal(client):
    """
    Test that a user cannot add a goal when they're not logged in.
    """
    rpm = RestaurantProfileManager("junaid")
    code = "junaid+5ef5009bccd1e88ead4cd076+0".split("+")
    msg = rpm.complete_goal(code[0], code[1], code[2])
    assert msg == "This goal has already been completed!"

def test_invalid_goal(client):
    """
    Test that a user cannot add a goal when they're not logged in.
    """
    rpm = RestaurantProfileManager("junaid")
    code = "junaid+5ef5009bccd1e88ead4cd076+1".split("+")
    msg = rpm.complete_goal(code[0], code[1], code[2])
    assert msg == "Invalid QR code!"



