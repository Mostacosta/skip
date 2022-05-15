from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions,status,generics,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import User,Code
from core.serializer.user_serializer import CustomTokenObtainPairSerializer, SignUpSerializer
from django.http import Http404
import requests
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from nakdepaybackend.pagination import CustomResultsSetPagination, CustomResultsSetPagination1
import qrcode
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        user = User.objects.filter(
            Q(email=request.data['phone']) | Q(phone=request.data['phone'])
        )
        try:
            request.data['email'] = user[0].email
        except:
            pass

        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


def send_code(phone, msg):
    sms_id = 'Div systems'
    sms_password = 'aN6Sm6FqLI'
    sms_username = '06z923rW'

    code_obj = Code.objects.create(phone=phone)
    code = code_obj.code
    try:
        url = f"https://smsmisr.com/api/webapi/?username={sms_username}&password={sms_password}&language=1&" \
            f"sender={sms_id}&mobile='{phone}'" \
            f"&message={msg} {code}"
        response = requests.request("POST", url)
        print(response.json())
        if response.json()["code"] == "4901":
            return "200"
        return "400"
    except:
        print("hi")
        return "400"

class CheckPhone (APIView):
    def post (self,request):
        phone = request.data["phone"]
        user = User.objects.filter(phone=phone)
        if user.exists():
            return Response ("User found")
        send_code(phone,"user this code to verify your phone number")
        return Response ("user not found",status=status.HTTP_400_BAD_REQUEST)

class SignUpView (APIView):

    def verif_phone(self,phone):
        try:
            code = Code.objects.get(phone=phone)
            if code.verify:
                return code
            else:
                return Response ("verify your phone first",status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response ("verify your phone first",status=status.HTTP_400_BAD_REQUEST)      

    def post(self,request):
        #phone = request.data['phone']
        #self.verif_phone(phone)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.pop('password')
            user = User(**serializer.validated_data)
            user.set_password(password)
            img = qrcode.make(f'{user.id},{user.full_name}')
            file_name = f'{user.full_name}_staticqr.jpg'
            path = settings.MEDIA_ROOT+"\\qrcode\\"+file_name
            img.save(path)
            user.static_qr = path
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response ({"access":token.key},status=status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class CodeResponseView (APIView):
    def post(self, request):
        code = request.data.get("code", None)
        phone = request.data.get("phone",None)
        try:
            code_obj = Code.objects.get(code=code,phone=phone)
            if timezone.now() < code_obj.create_date + timedelta(minutes=5):
                code_obj.verify = True
                code_obj.save()
                return Response("phone is verified")
            else:
                code_obj.delete()
                return Response("code is expired", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Code is invalid", status=status.HTTP_400_BAD_REQUEST)

class FingerPrintView(APIView):
    def post(self,request):
        finger_print = request.data["finger_print"]
        users = User.objects.filter(finger_print=finger_print)
        print(users)
        if users.exists():
            user = users.first()
            token, created = Token.objects.get_or_create(user=user)
            serializer = SignUpSerializer(user)
            return Response ({"data":serializer.data,"access":token.key}) 
        return Response ("user not found",status=status.HTTP_400_BAD_REQUEST)

class Contacts (APIView,CustomResultsSetPagination):

    permission_classes = [permissions.IsAuthenticated] 

    def post(self,request):
        contacts = request.data['contacts']
        for contact in contacts:
            user = User.objects.filter(phone=contact)
            if user.exists():
                request.user.friends.add(user.first().pk)
        return Response ("contacts are added")

    def get (self,request):
        users = request.user.friends.all()
        object = self.paginate_queryset(users, request)
        serializer = SignUpSerializer(object, many=True)
        return Response(self.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


class SearchUsers (APIView,CustomResultsSetPagination):

    permission_classes = [permissions.IsAuthenticated] 

    def get (self,request):
        filter_phone = request.GET.get("phone",None)
        filter_fullname = request.GET.get("full_name",None)
        filter_pk = request.GET.get("pk",None)
        contacts = request.user.friends.all()
        if filter_phone:
            objects = contacts.filter(phone__contains=filter_phone)
        elif filter_fullname:
            objects = contacts.filter(full_name__contains=filter_fullname)
        elif filter_pk:
            objects = User.objects.filter(pk=filter_pk)
        
        object = self.paginate_queryset(objects, request)
        serializer = SignUpSerializer(object, many=True)
        return Response(self.get_paginated_response(serializer.data), status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    phone = request.data['phone']
    password = request.data['password']
    user = authenticate(request, phone=phone, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response ({"access":token.key},status=status.HTTP_201_CREATED)
    else:
        return Response ({'error':'username or password are not correct'},status=status.HTTP_400_BAD_REQUEST)
