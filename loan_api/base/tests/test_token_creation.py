from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


def test_token_creation(db):
    """
    Certifies that a token is returned when making
    a POST request to /api-auth-token/.
    """
    User = get_user_model()
    user = User.objects.create(email='email@email.com')
    user.set_password('pass')
    user.save()
    client = APIClient()
    resp = client.post("/api-auth-token/", data={"username": "email@email.com", "password": 'pass'})
    assert resp.json().get('token', None) is not None
