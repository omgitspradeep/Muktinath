from time import sleep
import pytz
from base.models import AllOrders, History
from accountapp.models import Customer
from base.views import myorders
from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string  


@shared_task(bind=True)
def marriage_order_expire(self, order_id,user_id):
    print("INSIDE TASK")
    user = Customer.objects.get(id = user_id)
    marr_order = AllOrders.objects.get(id = order_id)
    myplan = marr_order.plans
    history = History.objects.create(
        customer=user,
        theme_name= marr_order.marraige_theme,
        amount_paid= myplan.plan_price,
        invitee_count = myplan.no_of_invitees,
        plan_days = myplan.no_of_days,
        time_of_purchase = marr_order.time_of_purchase,
        )
    marr_order.delete()
    print("---------------------------------------------------------")
    print(" "*50)
    print(f"EMAIL:   Your order {marr_order.order_name} is expired.Thank you for allowing us to serve you.")
    print("---------------------------------------------------------")

    msg =f" The invitation book you created on {myorders.time_of_purchase} had validity till now. We are always there to convey your invitation for marriages, Birthdays, Bratabanda and more auspicious occassions."
    to_email = 'odnkndgvxlcfldobfl@bvhrk.com'  
    send_order_expire_email(marr_order.order_name,user.get_full_name, to_email)
    return "Task completed"


def send_order_expire_email(ordername, user_fullname, expire_msg,to_email):
    mail_subject = f'Your Order {ordername} is expired.' 
    message = render_to_string('emails/order_expire.tpl', {  
        'full_name': user_fullname, 
        'msg': expire_msg
    })
    email = EmailMessage( mail_subject, message, to=[to_email])  
    email.send() 
    print("Expire email is sent")



'''
customer
theme_name
tax_rate ->def
amount_paid 
payment_choice ->def
invitee_count
plan_days
invitation_book_PDF ->def
time_of_purchase
expire_date->def
'''

