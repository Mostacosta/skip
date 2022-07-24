from email import message
import imp
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.http import request
from .models import Notfication, PaymentRequest, User
from rest_framework.authtoken.models import Token
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


@receiver(post_save, sender=PaymentRequest)
def send_noti_payment(sender, instance, created, **kwargs):
    print("start")
    if created:
        print("created")
        if instance.type == PaymentRequest.pay:
            instance.sender.balance -= instance.amount
            instance.receiver.balance += instance.amount
            web_devices = FCMDevice.objects.filter(user=instance.receiver)
            print(web_devices)
            body_ = f'{instance.sender.full_name} just send you {instance.amount} to your account'
            Notfication.objects.create(receiver=instance.receiver,request=instance,message=body_)
            if web_devices.exists():
                web_devices.send_message(Message(notification=Notification(title="alert", body=body_)))
        elif instance.type == PaymentRequest.request and instance.response == PaymentRequest.pending:
            web_devices = FCMDevice.objects.filter(user=instance.receiver)
            print(web_devices)
            body_ = f'{instance.sender.full_name} want {instance.amount} from you'
            Notfication.objects.create(receiver=instance.receiver,request=instance,message=body_)
            if web_devices.exists():
                web_devices.send_message(Message(notification=Notification(title="alert", body=body_),data={"payload":str(instance.pk)}))
    else:
        if instance.type == PaymentRequest.request and instance.response == PaymentRequest.accept:
            instance.sender.balance += instance.amount
            instance.receiver.balance -= instance.amount
            web_devices = FCMDevice.objects.filter(user=instance.sender)
            print(web_devices)
            body_ = f'{instance.receiver.full_name} just send you {instance.amount} to your account'
            Notfication.objects.create(receiver=instance.sender,request=instance,message=body_)
            if web_devices.exists():
                web_devices.send_message(Message(notification=Notification(title="alert", body=body_)))
        elif instance.type == PaymentRequest.request and instance.response == PaymentRequest.reject:
            web_devices = FCMDevice.objects.filter(user=instance.sender)
            print(web_devices)
            body_ = f'{instance.receiver.full_name} refused to send you {instance.amount} you asked for'
            Notfication.objects.create(receiver=instance.sender,request=instance,message=body_)
            if web_devices.exists():
                web_devices.send_message(Message(notification=Notification(title="alert", body=body_)))
    instance.sender.save()
    instance.receiver.save()



@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(user=instance)

