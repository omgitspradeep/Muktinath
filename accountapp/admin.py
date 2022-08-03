from django.contrib import admin
from accountapp.models import Customer
from django.contrib.auth.admin import UserAdmin as BaseCustomerAdmin

# Register your models here.

class CustomerModelAdmin(BaseCustomerAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','username','email', 'first_name','last_name', 'phone_number','country','address','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','phone_number','country', 'address')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'first_name', 'last_name','phone_number','country','address','password1', 'password2'),
        }),
    )
    search_fields = ('email','username')
    ordering = ('username',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Customer, CustomerModelAdmin)
