from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
#from home.models import News

#from importlib import import_module
#News = import_module('home.models').News


# Create your models here.

'''class Role(models.Model):
    ADMIN = 1
    SPECIAL_USER = 2
    REGULAR_USER = 3

    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (SPECIAL_USER, 'Special User'),
        (REGULAR_USER, 'Regular User'),
    ]

    role_type = models.IntegerField(choices=USER_TYPE_CHOICES, null=True)   # It is the role_id field #I deleted the role_name field
    work_experience = models.CharField(max_length=100) 

    def __str__(self): 
        return f"{self.pk} - {self.get_role_type_display()}"  '''


'''class Role(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=100)
    work_experience = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.role_id} - {self.role_name}'   '''






class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    family = models.CharField(max_length=75)
    phone_number = models.CharField(max_length=11, unique=True)

    ADMIN = 1
    SPECIAL_USER = 2
    REGULAR_USER = 3

    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (SPECIAL_USER, 'Special User'),
        (REGULAR_USER, 'Regular User'),
    ]
    role_type = models.IntegerField(choices=USER_TYPE_CHOICES, null=True)   # limit_choices_to={'role_type__in': [1, 2]}
    work_experience = models.CharField(max_length=100, null=True, blank=True)
    # role = models.OneToOneField(on_delete=models.CASCADE, related_name='roles', null=True)  # role_id
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'   # unique must be True #this field is for authenticate by phone_number
    REQUIRED_FIELDS = ['phone_number', 'name', 'family']     # Just ask us to createsuperuser
    objects = UserManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):  # Does the user have a specific permission?
        return True                      # Simplest possible answer: Yes, always

    def has_module_perms(self, app_label):  # Does the user have permissions to view the app `app_label`?
        return True                         # Simplest possible answer: Yes, always

    @property
    def is_staff(self):
        return self.is_admin


'''class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
'''


'''class NewsLikeDislike(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')  #چه کسی لایک میکنه
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislike')  #چه کسی دیس لایک میکنه
    from_news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='like_news') # چه خبری لایک میشه
    to_news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='dislike_news') # چه خبری دیس لایک میشه
    created = models.DateTimeField(auto_now_add=True)   #چه زمانی لایک کردنه اتفاق افتاده

    def __str__(self):
        return f'{self.from_user} likeing {self.from_news} and {self.to_user} dislikeing {self.to_news}'
'''





'''class UserReport(models.Model):
    user_report_id = models.IntegerField(primary_key=True, verbose_name='user_report_id')
    user_id1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userID1')
    user_id2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userID2')
    report_text = models.TextField()
    register_date = models.DateTimeField(auto_now_add=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments')'''

