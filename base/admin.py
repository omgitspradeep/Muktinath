from django.contrib import admin
from requests import request
from .models import History, Tax, Plans, InvitationThemes, AllOrders, Payment, Invitee, Wisher


# ADMIN ACTIONS
from import_export.admin import ExportActionMixin
from .resources import WisherResource, InviteeResource
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin




# Register your models here.

admin.site.register(History)

@admin.register(Invitee)
class InviteeAdmin(ImportExportActionModelAdmin):
	resource_class = InviteeResource
	list_display=('id','name','gender','address','inviteStatus','invitee_message','Order','URL','is_invitation_viewed')
	search_fields = ['name']


@admin.register(AllOrders)
class AllOrdersAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display=('id',"order_name","selected_theme","plans","user","time_of_purchase","invitation_language")


@admin.register(Plans)
class PlansAdmin(admin.ModelAdmin):
    list_display=('id','plans','no_of_days','no_of_invitees','plan_price')
       


@admin.register(Wisher)
class WisherAdmin(ImportExportModelAdmin):
    resource_class = WisherResource
    list_display=('id','Invitee','wishes','posted')
    search_fields = ['invitee__name']


@admin.register(InvitationThemes)
class InvitationThemesAdmin(admin.ModelAdmin):
    list_display=('id','theme_name','theme_type','theme_link','theme_color','sample_page_location','description','theme_image','theme_price')




'''
from django.http import HttpResponse
import  csv

class ExportCsvMixin:
	def export_invitees_as_csv(self, request, queryset):
		meta = self.model._meta
		field_names = ['FullName','Gender','Address','Invited On','Personal Message','Invitation URL','Your Order Name']
		response = HttpResponse(content_type = 'text/csv')
		response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)  # filename = base.invitee.csv
		writer = csv.writer(response)
		writer.writerow(field_names)
		for obj in queryset:
			row = writer.writerow([obj.name,obj.gender,obj.address,obj.inviteStatus,obj.invitee_message,obj.URL(), obj.order])
		return response
	export_invitees_as_csv.short_description = "Download Invitees to csv"


	def export_wisher_as_csv(self, request, queryset):
		response=HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="wishers.csv"'
		writer = csv.writer(response)
		writer.writerow(['Guest Name','Wishes','Date','Your Order Name'])
		for wish in queryset:
			row = writer.writerow([wish.invitee, wish.wishes, wish.posted, wish.order])
		return response
	export_wisher_as_csv.short_description = "Download Wishers to csv"


@admin.register(Wisher)
class WisherAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display=('id','Invitee','wishes','posted')
    search_fields = ['name']
    actions = ["export_wisher_as_csv",export_wisher_as_xls]

@admin.register(Invitee)
class InviteeAdmin(admin.ModelAdmin, ExportCsvMixin):
	list_display=('id','name','gender','address','inviteStatus','invitee_message','Order','URL')
	search_fields = ['name']
    actions = ["export_invitees_as_csv"]
'''