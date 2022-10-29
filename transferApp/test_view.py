from django.test import TestCase
import json
# Create your tests here.
def test_hisotry_auth(client):
    response = client.get(path='/history')
    assert response.status_code==301
def test_history_of_user(client):
    response = client.post('/api/token',{'email':'zoucloud157@gmail.com','password':'Kira52078789'},content_type='application/json',format='json')
    print(response)
    assert True
