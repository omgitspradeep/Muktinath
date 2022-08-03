from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()#Creating Router object
router.register('orderapi', views.OrderViewset, basename='orderapi' )#Registering OrderViewset with Router
router.register('mgalleryapi',views.GalleryViewSet, basename='mgalleryapi') # for CRUD but for list use another api



urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/<int:selectedorderid>',views.dashboard, name='dashboard'),
    path('orders/',views.myorders, name='orders'),
    path('transactions/',views.transactions, name='transactions'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('support/',views.support, name='support'),
    path('sample/<int:themeid>/<str:theme_name>', views.sample, name='sample'),

    path('signup/',views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),


    path('accounts/', include('allauth.urls')),


    #path('logout/',views.logout, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('add-order/',views.add_order, name='add-order'),
    path('orders/nimto/<int:order_id>', views.nimto, name='nimto'),
    path('add_invitee/<int:order_id>', views.add_invitee, name='add_invitee'),
    path('payment/<int:theme_id>',views.payment, name='payment'),

    #invitation
    path('you-are-invited/<str:inviteeCode>/',views.you_are_invited, name='you_are_invited'),

    #create and delete wish by invitee
    path('wishCD', views.wishCD, name='wishCD'),
    path('orders/viewAs/<int:order_id>/', views.viewAs, name='viewAs'),
    path('ddd/<int:order_id>', views.getViewForDownload, name='ddd'),
    path('send/', views.send, name='send'),
    #Payment
    path('api/verify_payment',views.verify_payment,name='verify_payment'),



    #APIs - mobile and web
    path('api/themes/',views.ThemesViewSet.as_view(),name='themes'),  # It works for both home and search i.e. http://127.0.0.1:8000/themes/
    path('api/all_guests/<int:order_id>', views.getAllGuestData, name='all_guests'),
    
    #Invitees
    path('api/inviteesapi/', views.crudInviteesAPI.as_view(), name='invitees'),
    path('api/inviteesapi/<int:invitee_id>/', views.crudInviteesAPI.as_view(), name='invitees'),
    
    #Wishers
    path('api/wisherapi/', views.crudWisherAPI.as_view(), name='wishers'),
    path('api/wisherapi/<int:wisher_id>/', views.crudWisherAPI.as_view(), name='wishers'),

    #Orders
    path('api/my_orders/<str:user_name>/', views.getAllOrders, name='all_orders'),
    path('api/', include(router.urls)),  # here apis of Orders and Order DATA are available

    #Order DATA
    path('api/data/<int:order_id>/<str:request_for>/',views.UserDataForHisOrders, name = 'datas'),
    path('api/data/',views.UserDataForHisOrders, name = 'datas'),
    




]