from email.policy import default
from pyexpat import model
from django import forms
from .models import AllOrders, Invitee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AllThemeOrdersForm(forms.ModelForm):
    #selected_theme = forms.ChoiceField(choices=[(x.theme_name) for x in InvitationThemes.objects.all()], widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta: 
        model= AllOrders
        fields = ['order_name', 'selected_theme', 'plans','invitation_language']
        # make  'selected_theme' field as read-only


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,help_text= '100 characters of fewer.')
    last_name = forms.CharField(max_length=100,help_text= '100 characters of fewer.')
    email = forms.EmailField(max_length=150, help_text='150 characters of fewer.')
    address = forms.CharField(max_length=45)

    class Meta: 
        model= User
        fields = ['username', 'first_name', 'last_name','email','address', 'password1','password2']
        


class MarriageInviteeForm(forms.ModelForm):
    name = forms.CharField(max_length=25)
    class Meta: 
        model= Invitee
        fields = ['name', 'gender','address','inviteStatus','invitee_message']


class BDInviteeForm(forms.ModelForm):
    name = forms.CharField(max_length=25)
    inviteStatus = forms.CharField(widget=forms.HiddenInput(), initial='_') 
    class Meta: 
        model= Invitee
        fields = ['name', 'gender','address','invitee_message']




from django.utils.translation import gettext_lazy as _

def mobile_no(value):
  if value< 10:
    raise forms.ValidationError(_("Number should not be less than 10"))



'''

{% if selected_order.selected_theme.theme_type == "Marriage" %}
{%endif%}

'''