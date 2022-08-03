from email.policy import default
from django.db import models
import secrets
from base.models import AllOrders


# Create your models here.


class BirthdayData(models.Model):
    name = models.CharField(max_length=50)
    bd_order = models.OneToOneField(AllOrders, on_delete=models.CASCADE)
    data_name = models.CharField(max_length=50, default='Default Data')
    title_image = models.ImageField(upload_to= "static/Birthday/images/title_images", height_field=None, width_field= None, max_length=100, default= "static/Birthday/images/title_images/title_icon_default.gif")
    bd_date_text = models.CharField(max_length=50, default="20.12.2020 ")
    reception_place = models.CharField(max_length=75, default=" Riddi Siddhi Party Palace, Suddhodhan-1, Pharsatikar")
    default_invitation_msz = models.CharField(max_length=250, default="Mr. Bhaktaraj Bashyal and Mrs. Haridevi Bashyal request the honour of your presence on the auspicious occassion of the marriage ceremony of their son.")
    about_me_image = models.ImageField(upload_to= "static/Birthday/images/aboutme", height_field=None, width_field= None, max_length=100, default= "static/Birthday/images/aboutme/about_default.jpg")
    my_info = models.CharField(max_length=500, default="Hi! I am Ram Sharma currently pursing my job at Yeti International. I have completed my masters in MBA and bachelors in Computer Science. \nSuddhodhan-3, Bethani, Rupandehi")
    my_address = models.CharField(max_length=500, default="Butwal-18, Bethani, Rupandehi")
    footer_message = models.CharField(max_length=100, default=" Love, laughter and happily ever after. ")


    def __str__(self):
        return str(self.bd_order)


class Contact(models.Model):
    birthday_data = models.OneToOneField(BirthdayData, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, default='1234567898') # validators should be a list
    email = models.CharField(max_length=500, default='sample@email.com')
    twitter_link = models.CharField(max_length=500, default='ttr.com')
    fb_link = models.CharField(max_length=500, default='f.com')
    yt_link = models.CharField(max_length=500, default='yt.com')
    lnkd_link = models.CharField(max_length=500, default='link.com')
    def __str__(self):
        return self.phone


 






#(lat,long)(27.640382435658456, 83.30955395735835)
class MeetingPoint(models.Model):
    birthday_data = models.OneToOneField(BirthdayData, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=50, default='27.640382435658456')
    latitude = models.CharField(max_length=50, default='83.30955395735835')
    direction_info = models.CharField(max_length=250, default='Once you get Bethani, take Lumbini circuit road leading to West direction. Once you reach a Siyari river then take road towards North that leads directly to marriage location.')
    palace_name = models.CharField(max_length=50, default='Buddhabhumi Party palace')
    address = models.CharField(max_length=50, default='Rupandehi, Nepal')
    contact_num = models.CharField(max_length=15, default='+977-1234567897') # validators should be a list
    email_or_fb_link = models.CharField(max_length=75, default='binary.science98@gmail.com')
    
    def __str__(self):
        return self.palace_name    





