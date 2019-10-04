from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

CODE_MAXLEN = 10000
FLAGS_MAXLEN = 512

class Course(models.Model):
    title = models.CharField(max_length=256)

class Chapter(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Lesson(models.Model):
    title = models.CharField(max_length=128)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    example_code = models.CharField(max_length=CODE_MAXLEN, blank=True)
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN, blank=True)

class MyAccountManager(BaseUserManager):

    def create_user(self, username, password=None): # Params depend on REQUIRED_FIELDS of CustomUser
        if not username:
            raise ValueError("Users must have a username!")

        user =  self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username            = models.CharField(max_length=64, primary_key=True)
    password            = models.CharField(max_length=128)
    email               = models.EmailField(verbose_name='email', max_length=256, unique=True)
    enrolled_in         = models.ManyToManyField(Course, blank=True)
    owned               = models.ManyToManyField(Course, blank=True, related_name='owned_courses')
    completed_lessons   = models.ManyToManyField(Lesson, blank=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class SolutionSet(models.Model):
    ordering = models.IntegerField
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    stdin = models.CharField(max_length=2048)
    stdout = models.CharField(max_length=2048)

class Submission(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    code = models.CharField(max_length=CODE_MAXLEN)
    compiler_flags = models.CharField(max_length=FLAGS_MAXLEN)
    passed = models.BooleanField(default=False)
