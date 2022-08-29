#Prebuilt
from pydoc import plain
from telnetlib import STATUS
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse,HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as loginUser, logout as logOutUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib import messages

from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from django.template.loader import render_to_string  
from django.template import loader

from datetime import datetime, timedelta, timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from django.core.mail import send_mail
from django.core.mail import EmailMessage  
from django.core.serializers import serialize 


from django.utils.translation import gettext as _
from django.utils import translation
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str 

#CUstom 

from . import sampledata
from .serializers import InvitationThemesSerializer, CustomerSerializer, InviteeSerializer, PlansSerializer,WisherSerializer,AllOrdersSerializer

from .models import AllOrders, Plans
from .tokens import account_activation_token  

from base.forms import SignupForm, AllThemeOrdersForm, MarriageInviteeForm,BDInviteeForm
from base.models import AllOrders, Invitee, Wisher,InvitationThemes

from Marriage.serializers import MarraigeDataSerializer, MarriageContactDataSerializer, MarraigeMeetingPointDataSerializer, MarraigeTestimonialsDataSerializer, MarraigeParentsDataSerializer, MarraigeGalleryDataSerializer
from Marriage.models import Contact as MContact, MarriageData ,MeetingPoint as MMeetingPoint, Testimonials, Parents,Gallery   
from Birthday.models import Contact as BDContact, BirthdayData,MeetingPoint as BDMeetingPoint

from muktinath.mypaginations import MyPageNumberPagination

from accountapp.models import Customer



#DRF
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

#MISC
import plotly.graph_objects as go
import pytz
import json
import os
import requests

from base import serializers


# Create your views here.

socail_ips = ['127.0.0.1','127.0.0.2']


#API
class ThemesViewSet(generics.ListAPIView):
    queryset = InvitationThemes.objects.all()
    serializer_class = InvitationThemesSerializer
    filter_backends = [SearchFilter]
    search_fields = ['$theme_name']


class ThemesViewSetPag(generics.ListAPIView):
    queryset = InvitationThemes.objects.all().order_by("id")
    serializer_class = InvitationThemesSerializer
    pagination_class = MyPageNumberPagination

    
#Temporary
def sampleAPI(request, themeid,theme_name):
    theme_selected= InvitationThemes.objects.get(id=themeid)
    template_to_render= theme_selected.sample_page_location
    if(theme_selected.theme_type=="Marriage"):
        return render(request, template_to_render,context={"theme_name":theme_name,"wishes": sampledata.wishes,"data":sampledata.data, "contact":sampledata.contact,"aboutus":sampledata.aboutus, "parents":sampledata.parents, "meetingPoint":sampledata.meetingPoint,"testi":sampledata.testimonials, "gallery":sampledata.gallery, "inviteeObj":sampledata.inviteeObj})
    else:
        return render(request,template_to_render,context={'title':theme_name, 'msg':'Happy Birthday dear'})

    
@api_view(['GET'])
def getAllGuestData(request,order_id):

    items=[]
    user_order = AllOrders.objects.get(id=order_id)
    guests = Invitee.objects.filter(order=user_order)

    for g in guests:
        guestWishObject = g.getWishIfExists()
        if(guestWishObject!=""):
            items.append({'id':g.id, 'order': user_order.id, 'name': g.name, 'gender': g.gender, 'address':g.address, 'inviteStatus':g.inviteStatus, 'invitee_message':g.invitee_message, 'is_invitation_viewed':g.is_invitation_viewed, 'url':g.URL(),'wish':guestWishObject.wishes, 'wishId':guestWishObject.id, 'wishPosted':guestWishObject.posted})
        else:
            items.append({'id':g.id, 'order': user_order.id, 'name': g.name, 'gender': g.gender, 'address':g.address, 'inviteStatus':g.inviteStatus, 'invitee_message':g.invitee_message, 'is_invitation_viewed':g.is_invitation_viewed, 'url':g.URL(),'wish':'', 'wishId':0, 'wishPosted':''})

    return JsonResponse(items,safe=False)



'''

            try:
                order_id = serializer.data['order']
                reverseUrl= "http://"+request.get_host()+reverse('all_guests', args=[order_id])
                print(reverseUrl)
                guests = requests.get(reverseUrl)
                all_guests = "not avl"
                if guests.status_code == 200:
                    all_guests = guests.json() 
                else:
                    return JsonResponse({"flag":0,"msg": "Something went wrong while fetching All guests!"},status=HTTP_404_NOT_FOUND)
            except:
                return JsonResponse({"flag":0,"msg": "Something went wrong while fetching All guests!"},status=HTTP_400_BAD_REQUEST)

'''


def getGuestDataAfterInviteeCreateOrUpdate(request,order_id):
    try:
        reverseUrl= "http://"+request.get_host()+reverse('all_guests', args=[order_id])
        print(reverseUrl)
        guests = requests.get(reverseUrl)
        all_guests = "not avl"
        if guests.status_code == 200:
            all_guests = guests.json() 
            return all_guests
        else:
            return ""
    except:
        return ""



class crudInviteesAPI(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, invitee_id = None, format = None):
        try:
            if invitee_id is not None:
                invitee =  Invitee.objects.get(id=invitee_id)
                #requested_user = request.user
                #if invitee.order.user != requested_user:
                #    return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)

                serializer = InviteeSerializer(invitee, status=HTTP_200_OK)
                return Response(serializer.data)
            invitees =  Invitee.objects.all()
            serializer = InviteeSerializer(invitees, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)

    #PROBLEM: check user with same name and address for same order already exists.
    def post(self, request, format = None):
        serializer = InviteeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            order_id = serializer.data['order']
            all_guests= getGuestDataAfterInviteeCreateOrUpdate(request, order_id)
            if(all_guests!= ""):
                return Response(all_guests, status=HTTP_200_OK)
            else:
                return Response({'flag':0,'msg':'New invitee is created. But, Failed while getting all invitees. Server issue.'},status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


    def put(self, request, invitee_id, format = None):
        # Partial= True
        try:
            if invitee_id is not None:
                invitee =  Invitee.objects.get(id=invitee_id)
                serializer = InviteeSerializer(invitee,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                order_id = serializer.data['order']
                all_guests= getGuestDataAfterInviteeCreateOrUpdate(request, order_id)
                if(all_guests!= ""):
                    return Response(all_guests, status=HTTP_200_OK)
                else:
                    return Response({'flag':0,'msg':'New invitee is created. But, Failed while getting all invitees. Server issue.'},status=HTTP_400_BAD_REQUEST)

            else:
                return Response({'flag':0,'msg':'Provided invitee is not valid'},status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg':str(e)}, status= HTTP_404_NOT_FOUND)


    def delete(self, request, invitee_id = None, format = None):
        try:
            if invitee_id is not None:
                invitee =  Invitee.objects.get(pk=invitee_id)
                order_id= invitee.order.id
                print(order_id,"--------------------------------------")
                invitee.delete()

                all_guests= getGuestDataAfterInviteeCreateOrUpdate(request, order_id)
                if(all_guests!= ""):
                    return Response(all_guests, status=HTTP_200_OK)
                else:
                    return Response({'flag':0,'msg':'invitee is deleted. But, Failed while getting all invitees. Server issue.'},status=HTTP_400_BAD_REQUEST)

            else:
                return Response({'flag':2,'msg':'ID is missing'},status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)
    


class crudWisherAPI(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, wisher_id=None, format = None):
        try:
            if wisher_id is not None:
                wisher =  Wisher.objects.get(id=wisher_id)
                requested_user = request.user
                if wisher.order.user != requested_user:
                    return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)

                serializer = WisherSerializer(wisher)
                return Response(serializer.data, status=HTTP_200_OK)
            return Response({'flag':2,'msg':'All data unavailable now'}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)


    def post(self, request, format = None):
        requested_user = request.user
        serializer = WisherSerializer(data = request.data)
        if serializer.is_valid():
            order_of_user = AllOrders.objects.get(id=serializer.validated_data['order'].id)
            if requested_user != order_of_user.user:
                return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)
            else:
                serializer.save()

                order_id = serializer.data['order']
                all_guests= getGuestDataAfterInviteeCreateOrUpdate(request, order_id)
                if(all_guests!= ""):
                    return Response(all_guests, status=HTTP_200_OK)
                else:
                    return Response({'flag':0,'msg':'New Wish is created. But, Failed while getting all invitees. Server issue.'},status=HTTP_400_BAD_REQUEST)

        return Response({'flag':0, 'msg':serializer.errors}, status = HTTP_400_BAD_REQUEST)

    def put(self, request, wisher_id = None, format = None):
        # Partial= True
        try:
            if wisher_id is not None:
                wisher =  Wisher.objects.get(id=wisher_id)
                if wisher.order.user != request.user:
                    return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)

                serializer = WisherSerializer(wisher,data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                    order_id = serializer.data['order']
                    all_guests= getGuestDataAfterInviteeCreateOrUpdate(request, order_id)
                    if(all_guests!= ""):
                        return Response(all_guests, status=HTTP_200_OK)
                    else:
                        return Response({'flag':0,'msg':'Wish is updated. But, Failed while getting all invitees. Server issue.'},status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'msg':str(e)}, status= HTTP_404_NOT_FOUND)


    def delete(self, request, wisher_id = None, format = None):
        try:
            if wisher_id is not None:
                wisher =  Wisher.objects.get(pk=wisher_id)
                if wisher.order.user != request.user:
                    return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)

                order_id = wisher.order.id
                wisher.delete()
                all_guests= getGuestDataAfterInviteeCreateOrUpdate(request, order_id)
                if(all_guests!= ""):
                    return Response(all_guests, status=HTTP_200_OK)
                else:
                    return Response({'flag':0,'msg':'New Wish is created. But, Failed while getting all invitees. Server issue.'},status=HTTP_400_BAD_REQUEST)

            else:
                return Response({'flag':2,'msg':'ID is missing'},status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg':str(e)}, status= HTTP_404_NOT_FOUND)




@api_view(['GET']) 
def getAllOrders(request,user_name):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    items=[]
    usr = Customer.objects.get(username=user_name)
    if usr != request.user:
        return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)

    if usr is not None:
        user_order = AllOrders.objects.filter(user=usr).values()
        return JsonResponse( list(user_order), safe=False)
    else:
        return JsonResponse(items,safe=False)



class OrderViewset(viewsets.ViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]


    #def list(self,request):
        #user_order = AllOrders.objects.all()
        #serializer = AllOrdersSerializer(user_order,many = True)
        #return Response(serializer.data)


    def retrieve(self, request, pk):
        id = pk
        try:
            if id is not None:
                orders = AllOrders.objects.get(id = id)
                # Check if api request is sent by authentic user.
                if orders.user != request.user:
                    return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)
                
                serializer = AllOrdersSerializer(orders,many = False)
                return Response(serializer.data, status= HTTP_200_OK)
        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)



    def create(self, request):
        order_for_user = Customer.objects.get(id=request.data.get('user'))

        # Check if api request is sent by authentic user.
        if order_for_user != request.user:
            return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)


        try:
            serializer = AllOrdersSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()

                newlyCreatedOrder = AllOrders.objects.get(id=serializer.data['id'])

                #Once order is saved Check if given order is of Marriage or Birthday.
                ordered_theme_is = newlyCreatedOrder.selected_theme.theme_type 
                # IF USER SELECTS MARRIAGE THEME THEN CREATE MARRIAGE DATA
                if(ordered_theme_is=='Marriage'):
                    createMarriageData(newlyCreatedOrder)
                elif (ordered_theme_is == 'Birthday'):
                    createBirthDayData(newlyCreatedOrder)
                else:
                    pass
                
                # Send email confirming the Order
                sendEmail(newlyCreatedOrder, order_for_user)
            
                return Response(serializer.data, status= HTTP_200_OK)
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)


    def update(self, request, pk):
        id = pk
        try:
            user_order = AllOrders.objects.get(id=id)
            serializer = AllOrdersSerializer(user_order,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= HTTP_200_OK)
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)
  


    def destroy(self, request, pk):
        id=pk
        try:
            if id is not None:
                order =  AllOrders.objects.get(id=id)
                order.delete()
                return Response({'flag':1,'msg':'Successful'})
            else:
                return Response({'flag':0,'msg':'ID is missing'})
        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)




def createMarriageData(newlyCreatedOrder):
    #title_icon =  createTitleIcon(color="pink",size=50, text="Ramlal Awantika",filename="title_"+str(new_order.id)+".png")
    # Create MarraigeData record here...
    my_data = MarriageData( name = newlyCreatedOrder.order_name, marriage_order = newlyCreatedOrder)
    my_data.save()                                                                              
    #Create all subrecords for MarriageData
    MContact(marriage_data=my_data).save()
    MMeetingPoint(marriage_data=my_data).save()
    Testimonials(marriage_data=my_data).save()
    Parents(marriage_data=my_data).save()


def createBirthDayData(newlyCreatedOrder):
    my_data = BirthdayData( name = newlyCreatedOrder.order_name, bd_order = newlyCreatedOrder)
    my_data.save()
    BDContact(birthday_data=my_data).save()
    BDMeetingPoint(birthday_data=my_data).save()


def sendEmail(newlyCreatedOrder,user):
    plan = newlyCreatedOrder.plans
    #expire_time = newlyCreatedOrder.time_of_purchase + timedelta(days= plan.no_of_days)
    expire_time = newlyCreatedOrder.time_of_purchase + timedelta(minutes= plan.no_of_days)
    
    # Schedule a task where Order is deactivated when plan expires. Send a email also.
    
    #schedule, created = CrontabSchedule.objects.get_or_create(month_of_year = expire_time.month, day_of_month= expire_time.day, hour= expire_time.hour, minute= expire_time.minute) # If not created creates a schedule object that runs exactly at 1:10 am
    #PeriodicTask.objects.create(crontab = schedule, name = 'expiring_order'+str(expire_time), task = 'base.tasks.marriage_order_expire', args = json.dumps((newlyCreatedOrder.id,newlyCreatedOrder.user.id,)), one_off= True)
    
    mail_subject = 'Order has been placed ' 
    message = render_to_string('emails/order_placed_email.tpl', {  
                    'full_name': user.get_full_name,  
                    'ordered_date': newlyCreatedOrder.time_of_purchase,  
                    'expiry_date':expire_time,
                    'plan':plan,  
                })
            
    to_email = user.email  
    email = EmailMessage( mail_subject, message, to=[to_email])  
    email.send()


class GalleryViewSet(viewsets.ViewSet):

    # It provides single Image from gallery
    def retrieve(self, request, pk): #pk = Gallery image id
        try:
            gallery_photo = Gallery.objects.get(id=pk)
            serializer = MarraigeGalleryDataSerializer(gallery_photo)
            return Response(serializer.data, status= HTTP_200_OK)
        except Exception:
            return Response({'flag':0,'msg':'No images in Gallery to show.'})

    def create(self, request):
        serializer = MarraigeGalleryDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_200_OK)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        try:
            gallery_photo = Gallery.objects.get(id=pk)
            serializer = MarraigeGalleryDataSerializer(gallery_photo, data= request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= HTTP_200_OK)
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'flag':0,'msg':'No images in Gallery to show.'}, status= HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        if pk is not None:
            try:
                photo =  Gallery.objects.get(id=pk)
                photo.delete()
                return Response({'flag':1,'msg':'Photo deleted successfully'}, status= HTTP_200_OK)
            except Exception:
                return Response({'flag':0,'msg':'No images in Gallery to delete.'}, status= HTTP_400_BAD_REQUEST)

        else:
            return Response({'flag':0,'msg':'ID is missing'}, status= HTTP_400_BAD_REQUEST)




# ORDER DATA APIS
# request_for is the indication which specifies what data user is looking for 
# PROBLEM : Should provide data only if he/she is owner of that order.
@csrf_exempt
@api_view(["GET", "PUT"])
def UserDataForHisOrders(request, order_id, request_for):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    try:

        user_order = AllOrders.objects.get(id=order_id)
        # Do further processing only if requested user with token is eligible for requested service. i.e. if he/she is owner of order.
        requested_user_id = request.user
        if user_order.user != requested_user_id:
            return Response({'flag':6,'msg':'You cannot request this operation.'}, status= HTTP_400_BAD_REQUEST)

        theme_type = user_order.selected_theme.theme_type
        if(theme_type=='Marriage'):
            main_data= MarriageData.objects.get(marriage_order=user_order)

            # Main Marriage Data
            if(request_for=="marriage_all_data"):
                return MarriageAllDataApi(request, main_data)
            elif (request_for=="marriage_main_data"):
                return MarriageMainDataApi(request, main_data)

            # Marriage Contact Data
            elif (request_for=="marriage_contact_data"):
                return MarriageContactDataApi(request, main_data)

            # Marriage Testimonials Data
            elif (request_for=="marriage_testimonials_data"):
                return MarriageTestimonialsDataApi(request, main_data)

            # Marriage Gallery Data
            elif (request_for=="marriage_gallery_data"):
                return MarriageGalleryApi(request, main_data)

            # Marriage Parents Data
            elif (request_for=="marriage_parents_data"):
                return MarriageParentsDataApi(request, main_data)

            # Marriage Meeting point Data
            elif (request_for=="marriage_mp_data"): # 
                return MarriageMeetingPointDataApi(request, main_data)

            else:
                return JsonResponse({'flag':0,'msg':'Bad Request'},safe=False)

        elif(theme_type=='Birthday'):
            return JsonResponse({'flag':1,'msg':'Congratulations! Birthday'},safe=False)



        else:
            return JsonResponse({'flag':1,'msg':'Congratulations! Opening'},safe=False)
    
    except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)





@api_view(['GET']) 
def viewAsAPI(request, order_id):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    return getDataAndDisplay(request, order_id)



@api_view(['GET']) 
def plansAndLanguages(request):
    #authentication_classes=[JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    try:
        pla = Plans.objects.all()
        lang = AllOrders.lang_choices       
        languages= [dict(k=value, v=label) for value, label in lang] 
        payment_gateways = AllOrders.PAYMENT_METHOD
        gateways= [dict(k=value, v=label) for value, label in payment_gateways] 
        serializer = PlansSerializer(pla, many=True)
            #return Response({"msz":"Somethinng went Right"}, status= HTTP_200_OK)
        return Response({'plans': serializer.data, 'lang': languages, 'payment': gateways}, status= HTTP_200_OK)
    except Exception as e:
        return Response({'flag':0,'msg':str(e)})



@api_view(['GET'])
def dashboardAPI(request,selectedorderid):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    all_orders = AllOrders.objects.filter(user=request.user)
    
    if all_orders.count()==0:
        return render(request, 'dashboard_mobile.html', context= {"orderisnone":True})
        
    if selectedorderid==0:
        selectedorderid=all_orders.first().id
    selected_order= AllOrders.objects.get(id=selectedorderid)
    myplan =selected_order.plans

    print("OOOOOOOOOONE 1")


    # RSVP INVITEES
    labels = ['Responded','Not Responded']
    values = [45,55]
    colors= ['mediumturquoise','gold']
    fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.1, 0])])
    fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    plot1 = fig1.to_html(full_html=False)


    print("OOOOOOOOOONE 2")

    # INVITEES DETAIL: Bar graph 
    createdInviteesData = Invitee.objects.filter(order=selected_order)
    createdInvitees =createdInviteesData.count()
    noOfInviteesWhoViewInvitation = createdInviteesData.filter(is_invitation_viewed=True).count()
    noOfInviteesWhoViewInvitationAndWished = Wisher.objects.filter(order= selected_order).count()
    
    Y =['Total Invitees','Created Invitees','Invitation Seen by Invitees','Invitees Who Wished']
    X =[myplan.no_of_invitees,createdInvitees,noOfInviteesWhoViewInvitation,noOfInviteesWhoViewInvitationAndWished]
    fig2 = go.Figure(go.Bar(
                x=X,
                y=Y,
                orientation='h'))

    #data = [go.Bar(x = X,y = Y)]  # for vertical  
    #fig2 = go.Figure(data=data)
    plot2 = fig2.to_html(full_html=False)

    print("OOOOOOOOOONE 3")

    # Donations: Bar graph 
    # Use `hole` to create a donut-like pie chart
    fig3 = go.Figure(data=[go.Pie(labels=['Prof. Ram Yadav','Er. Shyam Bastola','Dr. Geeta Tiwari','Ms. Neetu Karmacharya'], values=[4500, 2500, 1053, 500], hole=.3)])
    fig3.add_annotation(x= 0.5, y = 0.5,text = 'रु',font = dict(size=20,family='Verdana', color='green'), showarrow = False)
    plot3 = fig3.to_html(full_html=False)

    print("OOOOOOOOOONE 4")


    # Order Expiry Days: Half donut 
    plan_days= myplan.no_of_days    # plan: 10 days, today: 7th day, 
    days_till_now= get_days(selected_order.time_of_purchase) # how many days since Ordered

    print("OOOOOOOOOONE 5")

    fig4 = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = days_till_now,
        mode = "gauge+number+delta",
        title = {'text': "Days"},
        delta = {'reference': 2*days_till_now-plan_days, 'increasing': {'color': "darkgreen"}},  #  What value we put in referance, "delta= value-reference" so, reference is calculated by given formula because delta should give remaining days or exceeding days (i.e total - gone_days = value- reference)
        gauge = {'axis': {'range': [None, plan_days]},
                 'steps' : [
                     {'range': [0, 5], 'color': "lightgray"},
                     {'range': [5, 8], 'color': "gray"}],
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 9.5}}))

    fig4.update_layout(font = {'color': "darkblue", 'family': "Arial"})
    plot4 = fig4.to_html(full_html=False)
    context = {'selectedorderid':selectedorderid, 'analytics':'Water','invitees':createdInvitees,'total_donation':20000, 'total_plan_days':plan_days,'plot_div_invitee': plot1,'plot_invitees_detail': plot2, 'plot_donation':plot3 , 'plot_plan_expiry':plot4}

    print("OOOOOOOOOONE 6")

    return render(request, 'dashboard_mobile.html', context= context)















#Web

def mytest(request):
    print("-------------------------------")
    print("IP REQUEST IS HIT")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("IP ADDRESS", ip)
    return render(request, 'zoke.html',context={"ip":ip})




@login_required(login_url='accounts/login')
def myorders(request):
    form = AllThemeOrdersForm()
    orders = AllOrders.objects.filter(user=request.user).order_by('time_of_purchase')
    return render(request, 'orders.html',context={"form":form,"orders":orders})



@login_required(login_url='accounts/login')
def sample(request, themeid,theme_name):
    theme_selected= InvitationThemes.objects.get(id=themeid)
    template_to_render= theme_selected.sample_page_location
    if(theme_selected.theme_type=="Marriage"):
        return render(request, template_to_render,context={"theme_name":theme_name,"wishes": sampledata.wishes,"data":sampledata.data, "contact":sampledata.contact,"aboutus":sampledata.aboutus, "parents":sampledata.parents, "meetingPoint":sampledata.meetingPoint,"testi":sampledata.testimonials, "gallery":sampledata.gallery, "inviteeObj":sampledata.inviteeObj})
    else:
        return render(request,template_to_render,context={'title':theme_name, 'msg':'Happy Birthday dear'})




def add_order(request):
    if request.user.is_authenticated:
        user = request.user
        form =AllThemeOrdersForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_order = form.save(commit=False)
            new_order.user= user
            new_order.time_of_purchase=datetime.now(tz=pytz.timezone("Asia/Kathmandu"))
            new_order.save()

            ordered_theme_is = new_order.selected_theme.theme_type 
            # IF USER SELECTS MARRIAGE THEME THEN CREATE MARRIAGE DATA
            if(ordered_theme_is=='Marriage'):
                #title_icon =  createTitleIcon(color="pink",size=50, text="Ramlal Awantika",filename="title_"+str(new_order.id)+".png")
                # Create MarraigeData record here...
                createMarriageData(new_order)

            elif (ordered_theme_is == 'Birthday'):
                createBirthDayData(new_order)

            else:
                pass             

            #2022-04-25 03:41:58
            # Send email confirming the Order
            sendEmail(new_order, user)
            #  Reference :https://github.com/artemrizhov/django-mail-templated
            
            return redirect('orders')
        else:
            return render(request, 'orders.html', context={"form":form})


def login(request):
    print("Hello LOGIN")
    
    if request.user.is_authenticated:  # if user types login but user is already logged in
        return redirect('home')
    else:
        if request.method == 'GET':
            form = AuthenticationForm()
            context= {"form": form}
            return render(request, 'accounts/login.html', context=context)
        else:
            form = AuthenticationForm(request= request, data = request.POST or None)
            if form.is_valid():
                usrname=form.cleaned_data.get('username')
                passwrd=form.cleaned_data.get('password')
                user = authenticate(username=usrname, password=passwrd)
                if user is not None:
                    loginUser(request, user)

                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('home')
            else:
                context= {"form": form}
                return render(request, 'accounts/login.html', context=context)



@login_required(login_url='accounts/login')
def home(request):
    all_themes = InvitationThemes.objects.all()
    context = {
        "themes" : all_themes,
    }
    return render(request, 'index.html', context= context)




@login_required(login_url="accounts/login")
def dashboard(request,selectedorderid):
    all_orders = AllOrders.objects.filter(user=request.user)
    
    if all_orders.count()==0:
        return render(request, 'dashboard.html', context= {"orderisnone":True})
        
    if selectedorderid==0:
        selectedorderid=all_orders.first().id
    selected_order= AllOrders.objects.get(id=selectedorderid)
    myplan =selected_order.plans

    print("OOOOOOOOOONE 1")


    # RSVP INVITEES
    labels = ['Responded','Not Responded']
    values = [45,55]
    colors= ['mediumturquoise','gold']
    fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.1, 0])])
    fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    plot1 = fig1.to_html(full_html=False)


    print("OOOOOOOOOONE 2")

    # INVITEES DETAIL: Bar graph 
    createdInviteesData = Invitee.objects.filter(order=selected_order)
    createdInvitees =createdInviteesData.count()
    noOfInviteesWhoViewInvitation = createdInviteesData.filter(is_invitation_viewed=True).count()
    noOfInviteesWhoViewInvitationAndWished = Wisher.objects.filter(order= selected_order).count()
    
    Y =['Total Invitees','Created Invitees','Invitation Seen by Invitees','Invitees Who Wished']
    X =[myplan.no_of_invitees,createdInvitees,noOfInviteesWhoViewInvitation,noOfInviteesWhoViewInvitationAndWished]
    fig2 = go.Figure(go.Bar(
                x=X,
                y=Y,
                orientation='h'))

    #data = [go.Bar(x = X,y = Y)]  # for vertical  
    #fig2 = go.Figure(data=data)
    plot2 = fig2.to_html(full_html=False)

    print("OOOOOOOOOONE 3")

    # Donations: Bar graph 
    # Use `hole` to create a donut-like pie chart
    fig3 = go.Figure(data=[go.Pie(labels=['Prof. Ram Yadav','Er. Shyam Bastola','Dr. Geeta Tiwari','Ms. Neetu Karmacharya'], values=[4500, 2500, 1053, 500], hole=.3)])
    fig3.add_annotation(x= 0.5, y = 0.5,text = 'रु',font = dict(size=20,family='Verdana', color='green'), showarrow = False)
    plot3 = fig3.to_html(full_html=False)

    print("OOOOOOOOOONE 4")


    # Order Expiry Days: Half donut 
    plan_days= myplan.no_of_days    # plan: 10 days, today: 7th day, 
    days_till_now= get_days(selected_order.time_of_purchase) # how many days since Ordered

    print("OOOOOOOOOONE 5")

    fig4 = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = days_till_now,
        mode = "gauge+number+delta",
        title = {'text': "Days"},
        delta = {'reference': 2*days_till_now-plan_days, 'increasing': {'color': "darkgreen"}},  #  What value we put in referance, "delta= value-reference" so, reference is calculated by given formula because delta should give remaining days or exceeding days (i.e total - gone_days = value- reference)
        gauge = {'axis': {'range': [None, plan_days]},
                 'steps' : [
                     {'range': [0, 5], 'color': "lightgray"},
                     {'range': [5, 8], 'color': "gray"}],
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 9.5}}))

    fig4.update_layout(font = {'color': "darkblue", 'family': "Arial"})
    plot4 = fig4.to_html(full_html=False)
    context = {'allorders':all_orders,'selectedorderid':selectedorderid, 'analytics':'Water','invitees':createdInvitees,'total_donation':20000, 'total_plan_days':plan_days,'plot_div_invitee': plot1,'plot_invitees_detail': plot2, 'plot_donation':plot3 , 'plot_plan_expiry':plot4}

    print("OOOOOOOOOONE 6")

    return render(request, 'dashboard.html', context= context)



def get_days(order_date):
    now =datetime.now(timezone.utc)
    return (now-order_date).days


@login_required(login_url="accounts/login")
def transactions(request):
    return render(request, 'transactions.html', context= {})



@login_required(login_url="accounts/login")
def aboutus(request):
    return render(request, 'aboutus.html', context= {})



@login_required(login_url="accounts/login")
def support(request):
    return render(request, 'support.html', context= {})


def signup(request):
    if request.user.is_authenticated:  # if user types signup but user is already logged in
        return redirect('home')
    else:

        if request.method == 'GET':
            form = SignupForm()
            context ={
                "form" : form
            }
            return render(request, 'account/signup.html', context=context)
        else:
            print(request.POST)
            form = SignupForm(request.POST)
            context ={
                "form" : form 
                }
            if form.is_valid():

                # SAVE FORM IN Memory not in Database
                myuser = form.save(commit= False)
                myuser.first_name = form.cleaned_data.get('first_name')
                myuser.last_name = form.cleaned_data.get('last_name')
                myuser.email = form.cleaned_data.get('email')
                #username = form.cleaned_data.get('username')
                #password = form.cleaned_data.get('password1')
                address = form.cleaned_data.get('address')
                phone_number = form.cleaned_data.get('phone_number')

                #user cannot login until link is confirmed
                myuser.is_active = False
                myuser.save()


                # TO get the domain of the current site
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id' 

                # we used the EmailMessage() function to send mail along with the subject, message. 
                # Email message create by a template "signup_acc_active_email.html".
                message = render_to_string('signup_acc_active_email.html', {  
                    'user': myuser,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),  
                    'token':account_activation_token.make_token(myuser),  
                })
                to_email = form.cleaned_data.get('email')  
                email = EmailMessage( mail_subject, message, to=[to_email])  
                email.send()  
                return HttpResponse('Please confirm your email address to complete the registration')  
                #Customer.objects.create(user=myuser,first_name=first_name,last_name=last_name,address=address,phone_number=phone_number,email=email)

                #return redirect('login')
            else:
                return render(request, 'account/signup.html', context=context)



class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myuser = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            myuser = None

        # Checks if token is already used
        if myuser is not None and account_activation_token.check_token(myuser, token):
            myuser.is_active = True
            myuser.save()
            # Create Customer based on user
            #Customer.objects.create(user=myuser,first_name=first_name,last_name=last_name,address=address,phone_number=phone_number,email=email)

            loginUser(request, myuser, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')



@login_required(login_url='accounts/login')
def profile(request):
    print("hello world")

    #cust = Customer.objects.get(user = request.user)
    pro =request.user

    print(pro.username+"")
    data = {
            "username":pro.username,
            "name": pro.first_name+ " " +pro.last_name,
            "email": pro.email,
            "phone": pro.phone_number,
            "country":pro.country,
            "address": pro.address,
        }
    
    return render(request, 'user_profile.html', context=data)


'''
refresh_from_db() - > It handles synchronism issue i.e. reloading the database after the signal so that our profile instance will load. Once profile instance loads, set the cleaned data to the fields and save the user model.
'''



@login_required(login_url='accounts/login')
def logout(request):
    logOutUser(request)
    return redirect('login')




@login_required(login_url='accounts/login')
def nimto(request, order_id):
    selected_order = AllOrders.objects.get(id=order_id)
    order_type = selected_order.selected_theme.theme_type
    if(order_type == "Marriage"):
        form = MarriageInviteeForm()
    elif(order_type == "Birthday"):
        form = BDInviteeForm(initial={'inviteStatus': '_'})
    else:
        pass

    invitees = Invitee.objects.filter(order__id=order_id).order_by('name')
    wishers = Wisher.objects.filter(order__id=order_id).order_by('posted')
    return render(request, 'create_invitees_wishes.html',context={"form":form, "invitees":invitees, "wishers":wishers, "order":selected_order})


@login_required(login_url='accounts/login')
def add_invitee(request,order_id):
    selected_order = AllOrders.objects.get(id=order_id)
    order_type = selected_order.selected_theme.theme_type

    if request.user.is_authenticated:
        if(order_type == "Marriage"):
            form =MarriageInviteeForm(request.POST)
        elif(order_type == "Birthday"):
            form = MarriageInviteeForm(request.POST)
        else:
            pass

        if form.is_valid():
            new_invitee = form.save(commit=False)
            new_invitee.order= selected_order
            new_invitee.save()
            print("------------------invitee is added------------")

            return redirect('nimto',order_id=order_id)
        else:
            return render(request, 'create_invitees_wishes.html', context={"form":form})




#For guest when hits invitation link.
'''
Steps to be followed:
1. Get invitee object using secret code.
2. Save sitevisited to true
3. Save session.
4. Get MarriageData (Contact, gallery, testimonial, parents & meeting_point) using order object of invitee.
5. Get Wishes of all wisher with function of model getWishesIfExists()
6. get Template location of  "MarriageTheme.theme_link"
7. render Page with link_template and context -> MarriageData, Wishes 

8. List ip of all social medias and if view is called from these ips then mark "is_invitation_viewed" as false.

'''


def you_are_invited(request, inviteeCode):
    print("Inside you are invited")

    ip = request.META.get('REMOTE_ADDR')
    try:
        invitedGuest=Invitee.objects.get(secretCode=inviteeCode) #0
        print(f"Your id is :{inviteeCode} and {invitedGuest.name}")
        #1 Change invitation book's language accoding to ordered language
        translation.activate(invitedGuest.order.invitation_language)
        

        #2 Update the value to set the user has visited site.
        if not invitedGuest.is_invitation_viewed and requestNotFromSocialMedia(ip):  
            invitedGuest.is_invitation_viewed=True
            invitedGuest.save()
        
        #3 We store seesion everytime. User visits landing page because they can request landing page from same browser appending different inviteeCode in url
        request.session['guestsession']=inviteeCode
        print(f"Your session is :{inviteeCode}")

    except Exception as e:
        # No user with requested inviteeCode
        print(e)
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


    invitation_theme = invitedGuest.order.selected_theme

    print("GUESTTTT: " +str(invitedGuest.order))

    if(invitation_theme.theme_type == "Marriage"):
        m_data = MarriageData.objects.get(marriage_order=invitedGuest.order) #4
        testimonials = Testimonials.objects.get(marriage_data=m_data)
        contact = MContact.objects.get(marriage_data=m_data)
        parents = Parents.objects.get(marriage_data=m_data)
        meetingPoint = MMeetingPoint.objects.get(marriage_data=m_data)
        gallery = Gallery.objects.filter(marriage_data=m_data)
        #'Invitee' object has no attribute 'siteVisited'
        wishes = Wisher.objects.filter(order=invitedGuest.order) #5
        if len(wishes) == 0:
            context={"alreadyWished":0, "data":m_data, "contact":contact, "parents":parents, "meetingPoint":meetingPoint, "testi":testimonials, "gallery":gallery, "inviteeObj":invitedGuest}
        else:
            # Has this invitee already wished? if so, don't show wish form in landing page.
            context={"wishes": wishes,"alreadyWished":alreadyWished(inviteeCode,wishes),"data":m_data, "contact":contact, "parents":parents, "meetingPoint":meetingPoint,"testi":testimonials, "gallery":gallery,"inviteeObj":invitedGuest}


    elif(invitation_theme.theme_type == "Birthday"):
        bd_data = BirthdayData.objects.get(bd_order=invitedGuest.order) #4
        contact = BDContact.objects.get(birthday_data=bd_data)
        meetingPoint = BDMeetingPoint.objects.get(birthday_data=bd_data)
        wishes = Wisher.objects.filter(order=invitedGuest.order) #5
        if len(wishes) == 0:
            context={"alreadyWished":0, "data":bd_data, "contact":contact, "meetingPoint":meetingPoint, "inviteeObj":invitedGuest}
        else:
            # Has this invitee already wished? if so, don't show wish form in landing page.
            context={"wishes": wishes,"alreadyWished":alreadyWished(inviteeCode,wishes),"data":bd_data, "contact":contact, "meetingPoint":meetingPoint,"inviteeObj":invitedGuest}

    else:
        pass
    
    template_to_render = invitation_theme.theme_link  #6
    print("---------------------",template_to_render)

    return render(request, template_to_render,context=context)


#8 Verify if ip requesting page is from any social media that happened when user share their invitation link through them. 
def requestNotFromSocialMedia(ip_address):
    if ip_address in socail_ips:
        return False

    return True


def alreadyWished(inviteeCode, wisherObjs):
    flag=0
    for wisherObj in wisherObjs:
        if (inviteeCode==wisherObj.invitee.secretCode):
           flag=1
           break
    return flag


def getSessionID(request):
    return request.session['guestsession']




#Implement AJAX in frontend and remove redirection to nimto;  wishCD ===> WISH Create Delete 
def wishCD(request):
    if request.method == "POST":
        print("-------------HOME POST------------")
        inviteeCode = getSessionID(request)
        wish = request.POST.get('Wish')
        invitedGuest=Invitee.objects.get(secretCode=inviteeCode)
        print(f" ID: {inviteeCode} and WISH: {wish}")
        Wisher.objects.create(invitee=invitedGuest,wishes=wish, order= invitedGuest.order)
        return HttpResponseRedirect(reverse('you_are_invited',args=(inviteeCode,) ))

    elif request.method == "GET":
        print("-------------HOME GET------------")
        inviteeCode=getSessionID(request)
        try:
            inviteeObj=Invitee.objects.get(secretCode=inviteeCode)
            Wisher.objects.get(invitee=inviteeObj).delete()
            return JsonResponse({"status":"1","msg":"Successful"})  
        except Exception as e:
            return JsonResponse({"status":"0","msg":"Unsuccessful"})
    else:
        return HttpResponse("No page found GET")



# We need to authenticate wheter order id belongs to User who sends request for viewAs
@login_required(login_url='login')
def viewAs(request, order_id):
    return getDataAndDisplay(request, order_id);


# Not used for now since we 
def getViewForDownload(request,order_id):

    #check if user is ligit for viewas request i.e user is requesting for his own order's view
    marriageOrder = AllOrders.objects.get(id=order_id)

    print("Inside getView download")
    data = MarriageData.objects.get(marriage_order=marriageOrder) #4
    contact = MContact.objects.get(marriage_data=data)
    testimonials = Testimonials.objects.get(marriage_data=data)
    parents = Parents.objects.get(marriage_data=data)
    meetingPoint = MMeetingPoint.objects.get(marriage_data=data)
    gallery = Gallery.objects.filter(marriage_data=data)        
    wishes = Wisher.objects.filter(order=marriageOrder) #5
    template_to_render = data.marriage_order.selected_theme.theme_link  #6
    # Do not show wishing form
    if len(wishes) == 0:
        return render(request, template_to_render,context={"alreadyWished":1, "data":data, "contact":contact, "parents":parents, "meetingPoint":meetingPoint, "testi":testimonials, "gallery":gallery })        
    return render(request, template_to_render,context={"wishes": wishes,"alreadyWished":1,"data":data, "contact":contact, "parents":parents, "meetingPoint":meetingPoint,"testi":testimonials, "gallery":gallery})


from PIL import Image, ImageDraw, ImageFont
from django.core.files import File


def createTitleIcon(color ="red",filename="title.png", text="Sita Ram", size=50):
    font_english = "Arial.ttf"
    font_devnagri = "static/fonts/NotoSansDevanagari-ExtraBold.ttf"
    location="static/title_icons/"+filename

    print("Inside tile icon creation" +filename)
    fnt = ImageFont.truetype(font_english, size)
    image = Image.new(mode = "RGB", size = (int(size/2)*len(text)+30,size+40), color = color)
    draw = ImageDraw.Draw(image)
    # draw text
    draw.text((10,10), text, font=fnt, fill=(255,255,255))
    # save file
    image.save(location)

    return File(open(location, 'rb'))


# createTitleIcon("pink","order1.png", "Pradeep Seeta",13)



def send(request):

    mail_subject = "New Year Wish"
    message ="Dear Pradeep, Happy new year to you. May this year bring you prosperity."
    to_mail = "binary.science98@gmail.com"
    send_mail(
        subject = mail_subject,
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list= [to_mail],
        fail_silently = False,
    )

    return HttpResponse("DOne")



# For errors

def page_not_found_view(request,exception):    
    data={}
    return render(request, 'page404.html', context=data)

def bad_request_view(request,exception):
    data = {}
    return render(request,'page400.html', context=data)


def error_view(request):
    data = {}
    return render(request,'page500.html', context=data)


def permission_denied_view(request,exception):
    data = {}
    return render(request,'page403.html', context=data)


def csrf_failure(request,reason=""):
    ctx = {'message': 'some custom messages'}
    return render(request,'page403.html', ctx)





#PAYMENT


@csrf_exempt
def verify_payment(request):
   data = request.POST
   product_id = data['product_identity']
   token = data['token']
   amount = data['amount']

   url = "https://khalti.com/api/v2/payment/verify/"
   payload = {
   "token": token,
   "amount": amount
   }
   headers = {
   "Authorization": "Key test_secret_key_7392a1f9f80744c4a1c2e466c9cd6fd1"
   }
   

   response = requests.post(url, payload, headers = headers)
   
   response_data = json.loads(response.text)
   status_code = str(response.status_code)

   if status_code == '400':
      response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
      return response



   import pprint 
   print("Hello world")
   pp = pprint.PrettyPrinter(indent=4)
   pp.pprint(response_data)
   
   return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)



@login_required(login_url='accounts/login')
def payment(request, theme_id):
    selected_theme = InvitationThemes.objects.get(id=theme_id)
    initial_dict ={
        "selected_theme" : selected_theme
    }
    form = AllThemeOrdersForm(initial= initial_dict)

    return render(request, 'payment.html',context={"form":form})




# USEFUL METHODS
@csrf_exempt
def MarriageAllDataApi(request, main_data):
    if request.method == 'GET':
        try:
            # MainData
            mainDataSerializer = MarraigeDataSerializer(main_data)

            #Contact
            contactDetail = MContact.objects.get(marriage_data=main_data)
            contactSerializer = MarriageContactDataSerializer(contactDetail)

            #Testimonials
            testi = Testimonials.objects.get(marriage_data=main_data)
            testimonialSerializer = MarraigeTestimonialsDataSerializer(testi)

            #Gallery
            gallery = Gallery.objects.filter(marriage_data=main_data.id)
            gallerySerializer = MarraigeGalleryDataSerializer(gallery, many= True)

            #Parents
            parents = Parents.objects.get(marriage_data=main_data)
            parentsSerializer = MarraigeParentsDataSerializer(parents)

            #MeetingPoint
            location = MMeetingPoint.objects.get(marriage_data=main_data)
            locationSerializer = MarraigeMeetingPointDataSerializer(location)

            return Response({
                'main_data':mainDataSerializer.data,
                'contact':contactSerializer.data,
                'galleries':gallerySerializer.data,
                'meetingpoint':locationSerializer.data,
                'parents':parentsSerializer.data,
                'testimonials':testimonialSerializer.data,
            }, status= HTTP_200_OK)

        except Exception as e:
            return Response({'flag':0,'msg':str(e)}, status= HTTP_404_NOT_FOUND)
    else:
        return Response({'flag':0,'msg':'This operation not allowed'}, status= HTTP_404_NOT_FOUND)


@csrf_exempt
def MarriageMainDataApi(request, marriage_data):
    if request.method == 'GET':
        serializer = MarraigeDataSerializer(marriage_data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MarraigeDataSerializer(marriage_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_200_OK)
        else:
            return Response({'msg':'Sorry! Try again '}, status= HTTP_404_NOT_FOUND)
    else:
        return Response({'msg':'Not Allowed'}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def MarriageContactDataApi(request, main_data):
    contact_detail = MContact.objects.get(marriage_data=main_data)
    if request.method == 'GET':
        serializer = MarriageContactDataSerializer(contact_detail)
        return Response(serializer.data, status= HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = MarriageContactDataSerializer(contact_detail, data =request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status= HTTP_200_OK)
        else:
            return Response({'msg':'Sorry! Try again '}, status= HTTP_404_NOT_FOUND)
 
    else:
        return Response({'msg':'This operation is not allowed'}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def MarriageTestimonialsDataApi(request, main_data):
    testi = Testimonials.objects.get(marriage_data=main_data)
    if request.method == 'GET':
        serializer = MarraigeTestimonialsDataSerializer(testi)
        return Response(serializer.data, status= HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = MarraigeTestimonialsDataSerializer(testi, data =request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status= HTTP_200_OK)
        else:
            return Response({'msg':'Sorry! Try again '}, status= HTTP_404_NOT_FOUND)
     
    else:
        return Response({'msg':'This operation is not allowed'}, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
def MarriageGalleryApi(request, main_data):
    try:
        gallery = Gallery.objects.filter(marriage_data=main_data.id)
        if request.method == 'GET':
            serializer = MarraigeGalleryDataSerializer(gallery, many= True)
            return Response( serializer.data, status= HTTP_200_OK)
        else:
            return Response({'msg':'Not Allowed'}, status= HTTP_400_BAD_REQUEST)
    except Exception:
            return Response({'msg':'No images in Gallery to show.Or Given order does not exitst.'}, status= HTTP_404_NOT_FOUND)


@csrf_exempt
def MarriageParentsDataApi(request, main_data):
    parents = Parents.objects.get(marriage_data=main_data)
    if request.method == 'GET':
        serializer = MarraigeParentsDataSerializer(parents)
        return Response( serializer.data, status= HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = MarraigeParentsDataSerializer(parents, data =request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status= HTTP_200_OK)
        else:
            return Response({'msg':'Sorry! Try again '}, status= HTTP_404_NOT_FOUND)
     
    else:
        return Response({'msg':'This operation is not allowed'}, status=HTTP_400_BAD_REQUEST)



@csrf_exempt
def MarriageMeetingPointDataApi(request, main_data):
    location = MMeetingPoint.objects.get(marriage_data=main_data)
    if request.method == 'GET':
        serializer = MarraigeMeetingPointDataSerializer(location)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MarraigeMeetingPointDataSerializer(location, data =request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status= HTTP_200_OK)
        else:
            return Response({'msg':'Sorry! Try again '}, status= HTTP_404_NOT_FOUND)
    else:
        return Response({'msg':'This operation is not allowed'}, status=HTTP_400_BAD_REQUEST)

 



def getDataAndDisplay(request, order_id):
    user =request.user
    ordered_invitation = AllOrders.objects.get(id=order_id)
    invitation_type = ordered_invitation.selected_theme.theme_type
    
    #check if user is ligit for viewas request i.e user is requesting for his own order's view

    if(ordered_invitation.user == user):
        print("User is ligit")
        if(invitation_type == "Marriage"):
            # check if it is for view or download
            print("Inside View")
            data = MarriageData.objects.get(marriage_order=ordered_invitation) #4
            contact = MContact.objects.get(marriage_data=data)
            testimonials = Testimonials.objects.get(marriage_data=data)
            parents = Parents.objects.get(marriage_data=data)
            meetingPoint = MMeetingPoint.objects.get(marriage_data=data)
            gallery = Gallery.objects.filter(marriage_data=data)        
            wishes = Wisher.objects.filter(order=ordered_invitation) #5
            template_to_render = data.marriage_order.selected_theme.theme_link  #6
            # Do not show wishing form
            if len(wishes) == 0:
                return render(request, template_to_render,context={"alreadyWished":1, "data":data, "contact":contact, "parents":parents, "meetingPoint":meetingPoint, "testi":testimonials, "gallery":gallery }, status= HTTP_200_OK)        
            return render(request, template_to_render,context={"wishes": wishes,"alreadyWished":1,"data":data, "contact":contact, "parents":parents, "meetingPoint":meetingPoint,"testi":testimonials, "gallery":gallery}, status= HTTP_200_OK)

        
        elif (invitation_type == "Birthday"):

            print("Inside View")
            template_to_render = ordered_invitation.selected_theme.theme_link  
            print(template_to_render)               
            return render(request, template_to_render,context={})

        elif (invitation_type == "Opening"):
            return HttpResponse("This is opening theme sample", status= HTTP_200_OK)
   
        else:
            return HttpResponse("Nothing", status= HTTP_200_OK)

    else:
        # Display page not found here...
        print("Requested marriage order is not of user's... ")
        return HttpResponse("Operation not allowed.", status= HTTP_400_BAD_REQUEST)


