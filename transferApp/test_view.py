from django.test import TestCase

# Create your tests here.
def test_hisotry_auth(client):
    response = client.get(path='/history')
    assert response.status_code==301