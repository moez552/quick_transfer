import random
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save,post_delete
from .utils import send_account_verification
# Create your models here.
class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=10)
@receiver(post_delete,sender=EmailVerification)
def activate_user(sender,instance,*args,**kwargs):
    profile = Profile.objects.get(user=instance.user)
    profile.verified = True
    profile.save()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified =models.BooleanField(default=False)
    balance = models.FloatField()
    max_withdraw= models.FloatField()
    created_date = models.DateTimeField(default=now,editable=False)
    def __str__(self):
        return self.user.first_name + ' '+self.user.last_name
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,balance=0,max_withdraw=200)
        key = ''.join(str(i) for i in random.sample(range(1, 10), 8))
        EmailVerification.objects.create(user=instance,key=key)
        send_account_verification(key,instance.first_name,instance.email)
class History(models.Model):
    TRANSACTIONS_TYPES = [
        ('DP', 'Deposit'),
        ('WD', 'Withdraw'),
        ('TR','Transfer')]
    STATUS_CHOICES =  [
        ('PN', 'Pending'),
        ('SS', 'Success'),
        ('FL', 'Fail')]
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True, related_name="receiver")
    transaction_type = models.CharField(choices=TRANSACTIONS_TYPES,max_length=20)
    amount = models.FloatField()
    created_date = models.DateTimeField(default=now, editable=False)
    status = models.CharField(choices = STATUS_CHOICES,max_length=10,default=STATUS_CHOICES[1])
    def save(self, *args, **kwargs):
        if not self.profile.verified:
            raise ValidationError(_('Account is not verified'),code=4)
        if self.transaction_type=='TR' and not self.receiver:
            raise ValidationError(_('Receiver must be specified'),code=3)
        if self.profile==self.receiver:
            raise ValidationError(_('Invalid receiver'),code=4)

        if self.transaction_type in ['WD','TR']:
            if self.profile.balance < self.amount:
                raise ValidationError(_('Insufficient funds'),code=0)
            if self.profile.max_withdraw-self.amount<0:
                raise ValidationError(_('Reached limit'),code=1)
        super(History, self).save(*args, **kwargs)
    def __str__(self):
        if self.profile:
            return str(self.status)+' '+str(self.transaction_type)+' of  '+str(self.amount)+' '+self.profile.user.first_name + ' '+self.profile.user.last_name
        else:
            return 'unknown'

@receiver(post_save, sender=History)
def make_transaction(sender, instance, created, **kwargs):
    if created:
        value = instance.amount if instance.transaction_type=='DP' else instance.amount*(-1)
        profile = Profile.objects.get(id=instance.profile.id)  
        profile.balance = value + profile.balance
        profile.max_withdraw = profile.max_withdraw - instance.amount if instance.transaction_type!='PD' else profile.max_withdraw
        profile.save()
        if instance.transaction_type=='TR':
            receiver = Profile.objects.get(id=instance.receiver.id)
            receiver.balance = receiver.balance + instance.amount
            receiver.save()





