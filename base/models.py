from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
import secrets
from django.db import IntegrityError
from django.contrib import admin
from django.conf import settings
from accountapp.models import Customer
from django.utils.translation import gettext_lazy as _


# Create your models here.
class History(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    theme_name = models.CharField(max_length=25)
    tax_rate = models.IntegerField(default=12)
    amount_paid = models.IntegerField()
    payment_choice = models.CharField(max_length=2, default="Khalti")
    invitee_count = models.IntegerField()
    plan_days = models.IntegerField()
    invitation_book_PDF = models.FileField(blank=True, default= False)
    time_of_purchase = models.CharField(max_length=25)
    expire_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.customer)+" : "+self.theme_name


# Tax differs for each country, so it must be implemented according to county
class Tax(models.Model):
    tax_country = models.CharField(max_length=20, default="Nepal")
    tax_state = models.CharField(max_length=20, default="Lumbini")
    current_tax_rate = models.FloatField(max_length=6, default=5)
    current_gst_rate = models.FloatField(max_length=6,default=12)

    def __str__(self):
        return self.current_tax_rate


class Plans(models.Model):
    color_choice = (
    ("I","Indigo"),
    ("B","Blue"),
    ("G","Green"),
    ("Y","Yellow"),
    ("O","Orange"),
    ("F","Free"),
    )
    plans = models.CharField(max_length=15, choices=color_choice, default="B")
    no_of_days = models.IntegerField(default=7)
    no_of_invitees = models.IntegerField(default=100)
    plan_price = models.IntegerField(default=777)

    class Meta(object):
        ordering = ['no_of_days']

    def __str__(self):
        return self.plans


'''
InvitationThemes holds record of all the marriage and other themes available.
As we know, all the required data fields remains same but what varies is user's selection of one design among various themes(.html file). 
It is mannualy entered by SuperAdmin
First row of MARRIAGE_DATA has default values for all Marriage Themes.
Other rows of MARRIAGE_DATA has values updated by User.
'''


THEME_CHOICES = ( 
    ("Marriage", "Marriage"), 
    ("Birthday", "Birthday"), 
    ("Opening", "Opening"), 
) 

from django.urls import reverse

class InvitationThemes(models.Model):
    theme_name = models.CharField(max_length=50)
    theme_type = models.CharField(max_length=15, blank=False,choices=THEME_CHOICES, default='Marriage')    
    theme_link = models.CharField(max_length=50, default="themes_invitation/marriage/theme_n.html")
    theme_color = models.CharField(max_length=50, default="pink")
    sample_page_location = models.CharField(max_length=200, default="themes_sample/marriage/sample_theme_n.html")
    description = models.CharField(max_length=250, default="This is detailed info for this Theme.")
    theme_image = models.ImageField(upload_to= "static/core/theme_images",max_length=50, default="static/core/theme_images/default.png")
    theme_price=  models.IntegerField(default=150)


    def __str__(self):
        return self.theme_name

    def get_absolute_url(self):
        return reverse('sample', args=[self.id, str(self.theme_name)])




'''
When user selects the order and buys it, then a row is created on MARRIAGE_DATA. After that, a row is also created in ALLORDERS.

'''

class AllOrders(models.Model):
    lang_choices = (
        ('en','English'),
        ('ne','Nepali'),
        ('wari','Newari'),
        ('hi','Hindi'),
    )

    order_status =(
        ('active','active'),
        ('expire','expire'),
    )

    PAYMENT_METHOD = (
        ('Khalti','Khalti'),
    )

    #my_theme_name, is_shared_from_socail_media, time_of_purchase, CUSTOMER(1:1), PLANS(1:1), MarriageData(1:1), InvitationThemes(1:M)
    order_name = models.CharField(max_length=50, default= "My Order")
    selected_theme = models.ForeignKey(InvitationThemes,  on_delete=models.CASCADE, blank=False)
    plans = models.ForeignKey(Plans, on_delete= models.CASCADE)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, blank=False)
    time_of_purchase = models.DateTimeField(auto_now=True ) #auto_now=False,default="" 
    invitation_language = models.CharField(max_length=50, default="en", choices= lang_choices)
    order_status =models.CharField(max_length=20, default="active", choices= order_status)
    payment_method = models.CharField(max_length=20, choices= PAYMENT_METHOD ,default="Khalti")
    payment_completed =  models.BooleanField(default=False, null = True, blank=True)

    #tax = models.ForeignKey(Tax,on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.order_name



#Payment is child of AllOrders
class Payment(models.Model):
    # paid_tax_rate
    pass



INVITE_CHOICES = ( 
    ("Wedding", "Wedding"), 
    ("Reception", "Reception"), 
    ("_", "_"), 
) 
GENDER_CHOICES =(
    ("Mr. ","Male"),("Ms. ","Female"),
)


'''
A Customer can have two or more orders.
Invitees from diff. Orders of one Customer should be differenciated so,to make each Invitee row distinct we use -
Profile - to find who's invitee is he?
AllMarriageOrders - to find to which order this invitee is associated with
'''
from django.contrib.sites.models import Site


class Invitee(models.Model):
    order = models.ForeignKey(AllOrders,on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    gender = models.CharField(max_length=5, blank=True,choices=GENDER_CHOICES)    
    address = models.CharField(max_length=50)
    inviteStatus = models.CharField( max_length = 20, choices = INVITE_CHOICES, default = 'W')
    invitee_message = models.TextField(max_length=500, blank=True, default="This is default invitee message")
    is_invitation_viewed = models.BooleanField(default=False)
    secretCode = models.CharField(max_length=10, blank=True, editable=False, unique=True)


    def __str__(self):
        return self.name
    
    @admin.display(description='Invitation Link')
    def URL(self):
        url = settings.SITE_URL+settings.INVITATION_SUB_PART+self.secretCode  #http://127.0.0.1:8000/you-are-invited/
        return url


    def Order(self):
        return self.order


    
        # To get wishes by Invitees if exists. It helps us to display/hide wish form in invitation book. if already wished- display wish with delete else - display form
    def getWishIfExists(self):
        wish = Wisher.objects.filter(invitee=self)
        if(wish.exists()):
            return wish[0]
        else: 
            return ""

    def save(self, *args, **kwargs):
        if not self.secretCode:
            self.secretCode =generateSecretCode()

            #self.secretCode = generate_random_alphanumeric(16)
            # using our function as above or anything else
        success = False
        failures = 0
        while not success:
            try:
                super(Invitee, self).save(*args, **kwargs)
            except IntegrityError:
                 failures += 1
                 if failures > 5: # or some other arbitrary cutoff point at which things are clearly wrong
                     raise
                 else:
                    # looks like a collision, try another random value
                    self.secretCode =secrets.token_hex(16)
                    #self.secretCode = generate_random_alphanumeric(16)
            else:
                 success = True


class Wisher(models.Model):
    order = models.ForeignKey(AllOrders,on_delete=models.CASCADE)
    invitee = models.OneToOneField(Invitee,on_delete=models.CASCADE)
    wishes = models.CharField(max_length=500)
    posted = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['posted']

    def __str__(self):
        return self.invitee.name

    def Invitee(self):
        return self.invitee



def generateSecretCode():
    random = secrets.token_hex(16)
    # Get all the secretCodes to verify
    all= [obj.secretCode for obj in Invitee.objects.all()]
    if random in all:
        generateSecretCode()
    else:
        return random


'''
from pyshorteners import Shortener
def shortenURL(longUrl):
    return Shortener().clckru.short(longUrl)
'''
