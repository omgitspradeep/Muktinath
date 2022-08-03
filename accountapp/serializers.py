from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from accountapp.models import Customer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

from accountapp.utils import Util


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = Customer
        fields = ['email', 'first_name','last_name','phone_number','country', 'address', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # Validating password and confirm password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match.')
        return super().validate(attrs)

    def create(self, validate_data):
        return Customer.objects.create_user(**validate_data)


class CustomerLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = Customer
        fields = ['email', 'password']


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','email', 'first_name','last_name','phone_number','country', 'address']


class CustomerChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'},write_only=True) 
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'},write_only=True) 
    class Meta:
        model = Customer
        fields=['password','password2']

    # Validating old password and new password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password == password2:
            raise serializers.ValidationError('Old Password and new Password are same.')
        
        user.set_password(password2)
        user.save()
        return attrs


class SendPasswordRestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if Customer.objects.filter(email=email).exists():
            cust = Customer.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(cust.id))
            token = PasswordResetTokenGenerator().make_token(cust)
            link = "127.0.0.1:8000/api/user/reset-password/"+uid+"/"+token
            print("LINK: ",link)
            
            #SEND EMAIL
            
            body = 'Click following link to Reset your password.\n'+link
            data = {
                'subject':'Reset your password',
                'body':body,
                'to_email':cust.email

            }

            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr("Provided email address is not registered. Please Check and try again.")
        #return super().validate(attrs)






class CustomerPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'},write_only=True) 
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'},write_only=True) 
    class Meta:
        fields=['password','password2']

    # Validating old password and new password
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('Password and confirm Password does not match.')

            id = smart_str(urlsafe_base64_decode(uid))
            user = Customer.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not valid or expired.')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not valid or expired.')


