from django.contrib import admin
from .models import BirthdayData, Contact, MeetingPoint

# Register your models here.
admin.site.register(Contact)
admin.site.register(MeetingPoint)


@admin.register(BirthdayData)
class BirthdayDataAdmin(admin.ModelAdmin):
    list_display=("id","name","bd_order","data_name","title_image","bd_date_text","reception_place","default_invitation_msz","about_me_image","my_info","my_address","footer_message",)
    search_fields = ["name"]


