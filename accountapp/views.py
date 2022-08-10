from django.shortcuts import render
from django.contrib.auth import authenticate
from django.urls import reverse

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated

from .models import Customer
from base.models import AllOrders
from base.serializers import AllOrdersSerializer
from accountapp.renderers import CustomerRenderer
from accountapp.serializers import (
    CustomerRegistrationSerializer, 
    CustomerLoginSerializer, 
    CustomerProfileSerializer, 
    CustomerChangePasswordSerializer,
    SendPasswordRestEmailSerializer,
    CustomerPasswordResetSerializer
    )

import requests

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CustomerRegistrationView(APIView):
    renderer_classes = [CustomerRenderer]
    def post(self, request, format=None):
        try:
            serializer = CustomerRegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                customer = serializer.save()
                token=get_tokens_for_user(customer)
                return Response({'flag':1,'token':token}, status= status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'flag':0,'errors':str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CustomerLoginView(APIView):
    renderer_classes = [CustomerRenderer]
    def post(self, request, format=None):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            pwd = serializer.data.get('password')

            user = authenticate(email = email, password = pwd)
            if user is not None:
                
                #Token
                token=get_tokens_for_user(user)

                #Profile
                cust = Customer.objects.get(id=user.id)
                cust_seri = CustomerProfileSerializer(cust)

                #Orders
                user_order = AllOrders.objects.filter(user=cust)
                order_seri = AllOrdersSerializer(user_order, many=True)

                #Themes
                themes = requests.get("http://"+request.get_host()+reverse('themes_pag'))
                all_themes = "not avl"
                if themes.status_code==200:
                    all_themes = themes.json()

                context = {
                    "flag":1,
                    "token":token,
                    "my_profile":cust_seri.data,
                    "my_orders": order_seri.data,
                    "all_themes": all_themes
                }
                return Response(context, status= status.HTTP_200_OK)
            else:
                return Response({'flag':0,'errors':{'non_field_errors':['Email or Password is not valid.']}} , status= status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
class CustomerLoginViewJWT(APIView):
    #authentication_classes=[JWTAuthentication]

    def post(self, request, format=None):

        try:
            token = request.POST.get('token')
            access_token = AccessToken(token)

            customer = Customer.objects.get(id = access_token['user_id'])

            #Profile
            cust_seri = CustomerProfileSerializer(customer)
        
            #Orders
            user_order = AllOrders.objects.filter(user=customer)
            order_seri = AllOrdersSerializer(user_order, many=True)
        
            #Themes
            themes = requests.get("http://"+request.get_host()+reverse('themes_pag'))
            all_themes = "not avl"
            if themes.status_code==200:
                all_themes = themes.json()
            context = {
                "flag":1,
                "my_profile":cust_seri.data,
                "my_orders": order_seri.data,
                "all_themes": all_themes
            }
            return Response(context, status= status.HTTP_200_OK)
        except Exception as e:
            context = {"flag":0,"msg": e}
            return Response(context, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
    
    

class CustomerProfileView(APIView):
    renderer_classes = [CustomerRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = CustomerProfileSerializer(request.user)
        return Response(serializer.data, status= status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [CustomerRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = CustomerChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'flag':1,'msg':'Password changed successfully'}, status= status.HTTP_200_OK)
        return Response({'flag':0,'msg':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class SendPasswordResetEmailView(APIView):
    renderer_classes = [CustomerRenderer]
    def post(self, request, format=None):
        try:
            serializer = SendPasswordRestEmailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # Send email here....
                return Response({'flag':1,'msg':'Password Reset link sent. Please Check your email.'}, status= status.HTTP_200_OK)
            else:
                return Response({'flag':0,'msg':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'flag':0, 'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CustomerPasswordResetView(APIView):
    renderer_classes = [CustomerRenderer]
    def post(self, request, uid, token, format=None):
        try:
            serializer = CustomerPasswordResetSerializer(data=request.data, context ={'uid':uid, 'token':token})
            if serializer.is_valid(raise_exception=True):
                return Response({'flag':1,'msg':'Password Reset successfully.', }, status= status.HTTP_200_OK)
            else:
                return Response({'flag':0, 'msg':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'flag':0, 'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)


