from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import random
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValidationError(_('The Email must be set'))
        if not extra_fields.get('first_name'):
            raise ValidationError(_('The first_name must be set'))
        if not extra_fields.get('last_name'):
            raise ValidationError(_('The last_name must be set'))
        if not extra_fields.get('profile_type'):
            raise ValidationError(_('The profile_type must be set'))
        if not extra_fields.get('business_name') and extra_fields.get('profile_type')=='BS':
            raise ValidationError(_('The business_name must be set'))
        print(extra_fields.get('first_name'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', 'super')
        extra_fields.setdefault('last_name', 'admin')
        extra_fields.setdefault('business_name', '')
        extra_fields.setdefault('profile_type', 'PR')
        extra_fields.setdefault('username',''.join(str(i) for i in random.sample(range(1, 10), 8)))
        #extra_fields.setdefault('username', ''.join(str(i) for i in random.sample(range(1, 10), 8)))
        if extra_fields.get('is_staff') is not True:
            raise ValidationError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
