from datetime import date
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models import Max


class Faculty(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty_of_department')
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_superuser = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, position, identifier, password=None, ):
        if not email:
            raise ValueError('Students must have email')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          position=position,
                          identifier=identifier)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, identifier, password=None):
        if not email:
            raise ValueError('Students must have email')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          identifier=identifier)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    identifier = models.PositiveIntegerField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        if not self.is_admin:
            self.is_staff = self.isDepartmentStaff()
            self.is_superuser = self.position.is_superuser
            if not self.isIdentifierValid():
                self.identifier = self.generateIdentifier()
            # self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def generateIdentifier(self):
        if get_user_model().objects.filter(position=self.position).count() == 0:
            identifier = self.getFirstIdentifier()
        else:
            last_same_position_identifier = \
                get_user_model().objects.filter(position=self.position).aggregate(Max('identifier'))[
                    'identifier__max']
            identifier = last_same_position_identifier + 1
            if int(str(last_same_position_identifier)[:2]) is not int(str(date.today().year)[2:]):
                identifier = self.getFirstIdentifier()

        return identifier

    def getFirstIdentifier(self):
        return int(
            str(date.today().year)[2:] + str(self.position.department.faculty.id).zfill(2) + str(
                self.position.department.id).zfill(2) + str(
                self.position.id) + '0001')

    def isIdentifierValid(self):
        try:
            if not self.isNone():
                if not self.isExist() or self.isSame():
                    return True
        except AttributeError:
            pass
        return False

    def isNone(self):
        return False if self.identifiere is not None else True

    def isExist(self):
        return True if get_user_model().objects.filter(identifier=self.identifier).count == 0 else False

    def isSame(self):
        return self.identifier == get_user_model().objects.get(identifier=self.identifier).identifier

    def isDepartmentStaff(self):
        return True if not self.position.department.is_student else False
