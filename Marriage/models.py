from email.policy import default
from django.db import models
import secrets
from base.models import AllOrders


# Create your models here.


class MarriageData(models.Model):
    name = models.CharField(max_length=50)
    marriage_order = models.OneToOneField(AllOrders, on_delete=models.CASCADE)
    data_name = models.CharField(max_length=50, default='Default Data')
    title_image = models.ImageField(upload_to= "static/Marriage/images/title_images", height_field=None, width_field= None, max_length=100, default= "static/Marriage/images/title_images/title_icon_default.gif")
    bride_groom_name = models.CharField(max_length=50, default="Ram & Sita")
    marry_date_text = models.CharField(max_length=50, default="20.12.2020 ")
    engagement_date = models.CharField(max_length=50, default="Friday, 2077 - 08 - 26 (11th December 2020) ")
    wedding_day = models.CharField(max_length=50, default="Sunday, 2077 - 09 - 05 (20th December 2020) ")
    janti_prasthan_time = models.CharField(max_length=50, default="10 a.m ")
    janti_prsthan_place = models.CharField(max_length=50, default="Suddhodhan-3, Bethani, Rupandehi ")
    reception_date = models.CharField(max_length=50, default="Tuesday, 2077 - 09 - 07 (22nd December 2020)")
    reception_time = models.CharField(max_length=50, default=" From 3 P.M. to 8 P.M. ")
    reception_place = models.CharField(max_length=75, default=" Riddi Siddhi Party Palace, Suddhodhan-1, Pharsatikar")
    default_invitation_msz = models.CharField(max_length=250, default="Mr. Bhaktaraj Bashyal and Mrs. Haridevi Bashyal request the honour of your presence on the auspicious occassion of the marriage ceremony of their son.")
    about_us_image = models.ImageField(upload_to= "static/Marriage/images/aboutus", height_field=None, width_field= None, max_length=100, default= "static/Marriage/images/aboutus/about_default.jpg")
    groom_info = models.CharField(max_length=500, default="Hi! I am Ram Sharma currently pursing my job at Yeti International. I have completed my masters in MBA and bachelors in Computer Science. \nSuddhodhan-3, Bethani, Rupandehi")
    bride_info = models.CharField(max_length=500, default="Hi! I am Neha Dahal currently working as leading architect in Lumbini Provinance. I have completed my masters in Civil Engineering from Oxford university.\nButwal-18, Bethani, Rupandehi")
    groom_address = models.CharField(max_length=500, default="Butwal-18, Bethani, Rupandehi")
    bride_address = models.CharField(max_length=500, default="Suddhodhan-3, Bethani, Rupandehi")
    footer_message = models.CharField(max_length=100, default=" Love, laughter and happily ever after. ")
    #bgd_color = models.CharField(max_length=25)
    header_image = models.ImageField(upload_to= "static/Marriage/images/background", height_field=None, width_field= None, default= "static/Marriage/images/background/default_header_bg.jpg")


    def __str__(self):
        return str(self.marriage_order)


class Contact(models.Model):
    marriage_data = models.OneToOneField(MarriageData, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, default='1234567898') # validators should be a list
    email = models.CharField(max_length=500, default='sample@email.com')
    twitter_link = models.CharField(max_length=500, default='ttr.com')
    fb_link = models.CharField(max_length=500, default='f.com')
    yt_link = models.CharField(max_length=500, default='yt.com')
    lnkd_link = models.CharField(max_length=500, default='link.com')
    
    def __str__(self):
        return self.phone


class Gallery(models.Model):
    marriage_data = models.ForeignKey(MarriageData,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to= "static/Marriage/images/gallery", height_field=None, width_field= None, max_length=100)
    detail = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title    


class Testimonials(models.Model):
    marriage_data = models.OneToOneField(MarriageData,on_delete=models.CASCADE)
    grand_parents = models.CharField(max_length=500, default='Hajurbuwa, Hajurama')  # hint: Hajurbuwa, Hajurama or Hajurbuwa / Hajurama
    parents = models.CharField(max_length=500, default='Thulobuwa/THuliama, uncle/aunt' ) # hint: Thulobuwa/THuliama, uncle/aunt
    brothers = models.CharField(max_length=500, default='Thoulo dai/ thulibhauju, sanodai/ kanchi bhauju ') # hint: Thoulo dai/ thulibhauju, sanodai/ kanchi bhauju 
    sisters = models.CharField(max_length=500 , default='Thulididi / Thulovinaju') # hint: Thulididi / Thulovinaju
    nephews = models.CharField(max_length=500 , default='male/ female, female, male, ....') # hint: male/ female, female, male, ....
    cousins = models.CharField(max_length=500 , default='male/ female, female, male, ....') # hint: male/ female, female, male, ....
    maternal = models.CharField(max_length=500, default='mama/ maiju, mama/maiju, ....' ) # hint: mama/ maiju, mama/maiju, ....

    def __str__(self):
        return str(self.marriage_data)  



class Parents(models.Model):
    marriage_data = models.OneToOneField(MarriageData,on_delete=models.CASCADE)
    bride_father_fullname = models.CharField(max_length=50, default="Dr. Ghanshyam Sharma")
    bride_mother_fullname = models.CharField(max_length=50, default="Dr. Radha Sharma")
    groom_father_fullname = models.CharField(max_length=50, default="Prof. Vidya Bhandari")
    groom_mother_fullname = models.CharField(max_length=50, default="Er. Shova Bhandari")
    bride_father_image =  models.ImageField(upload_to= "static/Marriage/images/parents", height_field=None, width_field= None, max_length=100, default="static/Marriage/images/parents/bd.png")
    bride_mother_image =  models.ImageField(upload_to= "static/Marriage/images/parents", height_field=None, width_field= None, max_length=100, default="static/Marriage/images/parents/bm.png")
    groom_father_image =  models.ImageField(upload_to= "static/Marriage/images/parents", height_field=None, width_field= None, max_length=100, default="static/Marriage/images/parents/gd.png")
    groom_mother_image =  models.ImageField(upload_to= "static/Marriage/images/parents", height_field=None, width_field= None, max_length=100, default="static/Marriage/images/parents/gm.png")

    def __str__(self):
        return str(self.marriage_data)    


#(lat,long)(27.640382435658456, 83.30955395735835)
class MeetingPoint(models.Model):
    marriage_data = models.OneToOneField(MarriageData, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=50, default='27.640382435658456')
    latitude = models.CharField(max_length=50, default='83.30955395735835')
    direction_info = models.CharField(max_length=250, default='Once you get Bethani, take Lumbini circuit road leading to West direction. Once you reach a Siyari river then take road towards North that leads directly to marriage location.')
    palace_name = models.CharField(max_length=50, default='Buddhabhumi Party palace')
    address = models.CharField(max_length=50, default='Rupandehi, Nepal')
    contact_num = models.CharField(max_length=15, default='+977-1234567897') # validators should be a list
    email_or_fb_link = models.CharField(max_length=75, default='binary.science98@gmail.com')
    
    def __str__(self):
        return self.palace_name    





