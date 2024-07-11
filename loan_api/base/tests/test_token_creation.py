from loan_api.base.models import User
from rest_framework.test import APIClient


def test_token_creation(db):
    """
    Certifies that a token is returned when making
    a POST request to /api-auth-token/.
    """
    user = User.objects.create(email='email@email.com')
    user.set_password('pass')
    user.save()
    client = APIClient()
    resp = client.post("/api-auth-token/", data={"username": "email@email.com", "password": 'pass'})
    assert resp.json().get('token', None) is not None
