"""
This file houses the unit test suite for Scanning qr codes for customer goals and
makring the goals as complete
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
    Test that qr verification page does not load unless user is logged in.
    """
    res = client.get("/profile/qr-verification-rewards", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_verification_route_logged_in(client):
    """
    Test that qr verification page loads when the user is logged in.
    """
    client.post("/login", data={"username": "junaid", "password": "Junaid123"})
    res = client.get("/profile/qr-verification-rewards", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data

def test_valid_completed_reward(client):
    """
    Test that a user can mark a valid reward as complete.
    """
    rpm = RestaurantProfileManager("junaid")
    code = "junaid+5f03a9fd7aae4a086d810102+6".split("+")
    msg = rpm.complete_reward(code[0], "junaid+5f03a9fd7aae4a086d810102+6")
    assert msg == "Code has already been redeemed!"

def test_duplicate_completed_reward(client):
    """
    Test that a duplicate reward can't be completed again.
    """
    rpm = RestaurantProfileManager("junaid")
    code = "junaid+5f03a9fd7aae4a086d810102+6".split("+")
    msg = rpm.complete_reward(code[0], "junaid+5f03a9fd7aae4a086d810102+6")
    assert msg == "Code has already been redeemed!"

def test_invalid_reward(client):
    """
    Test that a user can't complete an invalid reward.
    """
    rpm = RestaurantProfileManager("junaid")
    code = "junaid+5f03a9fd7aae4a086d810102+7".split("+")
    msg = rpm.complete_reward(code[0], "junaid+5f03a9fd7aae4a086d810102+7")
    assert msg == "Invalid QR code!"



