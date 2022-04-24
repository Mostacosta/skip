from django.conf import settings
from django.http import Http404
from nakdepaybackend.views import AutomatorView
from core.models import PaymentRequest
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializer.paymentrequest_serializer import PaymentRequestSerializer,PaymentRequestGetSerializer
import qrcode
import os
import base64

class PaymentRequestView (AutomatorView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = PaymentRequestSerializer
    get_serializer_class = PaymentRequestGetSerializer
    model = PaymentRequest
    with_pagination = True
    exclude = []

    def post(self, request):
        request.data["sender"] = request.user.pk
        return super().post(request)

class PaymentView(APIView):

    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self, pk):
        try:
            return PaymentRequest.objects.get(pk=pk)
        except:
            raise Http404

    def post(self,request):

        type_ = request.data["type"]
        if type_ == PaymentRequest.pay:
            request.data["response"] = PaymentRequest.accept
            resp = request.user.check_balance(request.data["amount"])
            if resp:
                pr = PaymentRequestView()
                resp_ = pr.post(request)
                return resp_
            return Response ("You dont have enough money",status=status.HTTP_400_BAD_REQUEST)
        elif type_ ==  PaymentRequest.request:
            pr = PaymentRequestView()
            resp = pr.post(request)
            return resp
        return Response ("You dont have enough money",status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        object = self.get_object(pk)
        print(object,"######################################################")
        if object.response == PaymentRequest.accept and request.data["response"]==PaymentRequest.accept:
            return Response ("you already accepted this order before",status=status.HTTP_400_BAD_REQUEST)
        if (request.data["response"] == PaymentRequest.accept and object.receiver.check_balance(object.amount)) or (
            request.data["response"] == PaymentRequest.reject):
            print("in","@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
            serializer = PaymentRequestSerializer(
                object, data=request.data, partial=True)
            if serializer.is_valid():
                print("idsadn","$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$") 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("you dont have enough money", status=status.HTTP_400_BAD_REQUEST)


class GenerateQR (APIView):

    permission_classes = [permissions.IsAuthenticated] 

    def image_as_base64(self,image_file, format='png'):
        """
        :param `image_file` for the complete path of image.
        :param `format` is format for image, eg: `png` or `jpg`.
        """
        if not os.path.isfile(image_file):
            return None
        
        encoded_string = ''
        with open(image_file, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read())
        return 'data:image/%s;base64,%s' % (format, encoded_string)


    def post(self, request, *args, **kwargs):
        user = request.user
        amount = request.data['amount']
        img = qrcode.make(f'{user.id},{user.full_name},{amount}')
        file_name = f'{user.full_name}_{amount}_{user.id}_generatedqr.jpg'
        path = settings.MEDIA_ROOT+"\\qrcode\\"+file_name
        img.save(path)
        img_base_64 = self.image_as_base64(path)
        return Response ({'img':img_base_64})



