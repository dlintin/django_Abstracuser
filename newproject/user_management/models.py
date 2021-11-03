
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, phone, password):
        if not phone:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
	phone = models.CharField(
		verbose_name='phone',
		max_length=14,
		unique=True,
	)
	user_type = models.CharField(max_length=10, default="user", null=True, blank=True,
									  choices=[('user', 'user'),
											   ('admin', 'admin'),])
	password = models.CharField(max_length=200)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()

	USERNAME_FIELD = 'phone'

	def __str__(self):
		return self.phone

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin