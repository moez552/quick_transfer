# Create your tests here.
import json
from django.test import TestCase, Client
from django.urls import reverse
from transferApp.models import History,Profile,EmailVerification
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.history = reverse('history')
        self.login = reverse('token_obtain_pair')
        self.user = Profile.objects.create(username='unique1',email='unique1@email.com',profile_type='PL',first_name='test',last_name='case',verified=True,balance=100)
        self.user.set_password('T3stP@ssWord')
        self.user.save()
        self.user1 = Profile.objects.create(username='unique2',email='unique2@email.com',profile_type='PL',first_name='test',last_name='case2',verified=True,balance=100)
        self.user1.set_password('T3stP@ssWord')
        self.user1.save()
        response = self.client.post(self.login,{'email':'unique1@email.com','password':'T3stP@ssWord'})
        d = json.loads(response.content)
        self.token = d['access']
        History.objects.create(profile=self.user,transaction_type='WD',amount=10).save()
        History.objects.create(profile=self.user,transaction_type='WD',amount=20).save()
        History.objects.create(profile=self.user1,transaction_type='WD',amount=30).save()
        History.objects.create(profile=self.user1,transaction_type='WD',amount=40).save()

    def test_hisotry_auth(self):
        response = self.client.get(self.history)
        self.assertEqual(response.status_code,401)
    def test_history_of_a_user(self):
        response = self.client.get(self.history,**{'HTTP_AUTHORIZATION': f'Bearer {self.token}'})
        expected_res = [{"transaction_type":"WD","amount":10.0,"created_date":"2022-11-01T22:30:03.684965Z","status":"('SS', 'Success')"},{"transaction_type":"WD","amount":20.0,"created_date":"2022-11-01T22:30:03.684965Z","status":"('SS', 'Success')"}]
        res = json.loads(response.content)
        for i in range(len(res)):
            res[i].pop('created_date')
            expected_res[i].pop('created_date')
        self.assertEqual(res, expected_res)
