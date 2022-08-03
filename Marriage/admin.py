from django.contrib import admin
from .models import MarriageData, Contact, Gallery, Testimonials, Parents, MeetingPoint

# Register your models here.
admin.site.register(Contact)
admin.site.register(Testimonials)
admin.site.register(Parents)
admin.site.register(MeetingPoint)


@admin.register(MarriageData)
class MarriageDataAdmin(admin.ModelAdmin):
    list_display=('id','name','marriage_order','data_name','title_image','bride_groom_name','marry_date_text','engagement_date','wedding_day','janti_prasthan_time','janti_prsthan_place','reception_date','reception_time','reception_place','default_invitation_msz','about_us_image','groom_info','bride_info','groom_address', 'bride_address','footer_message','header_image')
    search_fields = ['name']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display=("id","marriage_data","title","image","detail")



