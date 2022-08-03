from .models import InvitationThemes, AllOrders, Invitee, Wisher
from accountapp.models import Customer
from rest_framework import serializers


class InvitationThemesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationThemes
        fields = '__all__'


class AllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllOrders
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class InviteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitee
        fields = '__all__'

class WisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wisher
        fields = '__all__'


