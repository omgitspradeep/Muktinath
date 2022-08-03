from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator


# Create your models here.


# Creating Custom user manager for our usermodel "Customer"
class CustomerManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone_number, country, address, password=None, password2=None):
        """
        Creates and saves a User with the given email,name, last_name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name=first_name,  # No need to normalize name
            last_name = last_name,
            phone_number=phone_number,
            country = country,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, phone_number, country, address, password=None, password2=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            country = country,
            address=address,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user




phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
country_choices = (
    ("Nepal","Nepal"),
    ("India","India"),
    ("China","China"),
    ("Japan","Japan"),
    ("USA","USA"),
    ("England","England"),
    ("Germany","Germany"),
    ("Canada","Canada"),
    ("South Korea","South Korea"),
    ("Sri Lanka","Sri Lanka"),
    ("Bhutan","Bhutan"),
    ("Indonesia","Indonesia"),
    ("Singapore","Singapore"),
    ("Dubai","Dubai"),
    ("Sudia Arabia","Sudia Arabia"),
    ("Israel","Israel"),
    ("Argentina","Argentina"),
    ("Spain","Spain"),
    ("Brazil","Brazil"),
    )



class Customer(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=20, verbose_name='Username',unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex],max_length=17, blank=True) # validators should be a list
    country = models.CharField(max_length=100, choices= country_choices ,default="Nepal")
    address = models.CharField(max_length=100, blank='')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number','country','address']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name +" "+self.last_name

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



'''
One application of normalizing emails is to prevent multiple signups. 
If our application lets the public to sign up, our application might
attract the "unkind" types, and they could attempt to sign up multiple 
times with the same email address by mixing symbols, upper and lower cases 
to make variants of the same email address.

i.e. For email addresses, foo@bar.com and foo@BAR.com are equivalent;
the domain part is case-insensitive according to the RFC specs.
Normalizing means providing a canonical representation, so that any two 
equivalent email strings normalize to the same thing.



'''