from import_export import resources
from .models import Invitee, Wisher
from import_export.fields import Field
from django.contrib.sites.models import Site
from django.conf import settings


# This FILE IS USED FOR exporting and importing FROM ADMIN PANEL.
class WisherResource(resources.ModelResource):
    # Change column Name
    order__order_name = Field(attribute='order__order_name', column_name='Order Name')
    invitee__name = Field(attribute='invitee__name', column_name='Invitee Name')
    class Meta:
        model = Wisher
        fields = ('invitee__name', 'wishes', 'posted', 'order__order_name')
        #exclude = ('id', )
        export_order = ('invitee__name', 'wishes', 'order__order_name', 'posted')


class InviteeResource(resources.ModelResource):
    order__order_name = Field(attribute='order__order_name', column_name='Order Name')
    invitee_message = Field(attribute='invitee_message', column_name='Invitation Words')
    inviteStatus = Field(attribute='inviteStatus', column_name='Invitation Status')
    url = Field(column_name='Invitation Link') # Since url is not in our Model as a field so we add a new field "url" 

    class Meta:
        model = Invitee
        fields = ('name', 'gender', 'address', 'inviteStatus','invitee_message','order__order_name','url')
        export_order = ('name', 'gender', 'address', 'inviteStatus','invitee_message','order__order_name','url')

    # We cannot directly call model methods in resources, so we dehydrate it.
    def dehydrate_url(self, invitee):
            baseUrl = Site.objects.get_current().domain                 
            link ="http://"+baseUrl+settings.INVITATION_SUB_PART+invitee.secretCode
            return link

#The default field for object identification is id, we can optionally set which fields are used as the id when importing: