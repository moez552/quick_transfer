from transferApp.models import History,Profile,EmailVerification
from django.test import TestCase
from django.core.exceptions import ValidationError

class TestModels(TestCase):
    """"
    testing profile, History and EmailVerification model
    """
    def setUp(self):
        self.user = Profile.objects.create(username='unique1',email='unique1@email.com',profile_type='PL',first_name='test',last_name='case',verified=True,balance=100)
        self.user.set_password('T3stP@ssWord')
        self.user.save()
    def test_validate_Email_verification(self):
        """"
        validate that a new verification code will be inserted whenever a new user is added
        """
        c = EmailVerification.objects.filter(user=self.user).count()
        self.assertEqual(c,1)
    def test_create_trasactions(self):
        """Testing Transactions"""
        History.objects.create(profile=self.user,transaction_type='WD',amount=10).save()
        self.user = Profile.objects.get(id=self.user.id)
        self.assertEqual(self.user.balance,90.0)
        self.assertEqual(self.user.max_withdraw,190.0)
        with self.assertRaises(ValidationError):
            History.objects.create(profile=self.user,transaction_type='WD',amount=1000).save()
        with self.assertRaises(ValidationError):
            History.objects.create(profile=self.user,transaction_type='TR',amount=10,receiver=self.user).save()





