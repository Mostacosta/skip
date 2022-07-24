from urllib import response
from nakdepaybackend.pagination import CustomResultsSetPagination
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import PaymentRequest, Utility, UtilityRequests
from core.serializer.utility_serializer import UtilityGetSerializer, UtilityRequestGetSerializer, UtilityRqeuestSerializer,UtilitySerializer
from datetime import datetime

def utility_payment_crone():
    now = datetime.now().date()
    requests = UtilityRequests.objects.filter(create_date=now)
    for request in requests:
        resp = request.sender.check_balance(request.amount)
        if resp:
            request_ = PaymentRequest(sender=request.sender,receiver=request.utility.user
            ,type=PaymentRequest.pay,response=PaymentRequest.accept,amount=request.amount)
            request_.save()
            request.request = request_
            request.save()





class UtilityView(APIView,CustomResultsSetPagination):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objs = Utility.objects.all()
        object = self.paginate_queryset(objs, request)
        serializer = UtilityGetSerializer(object, many=True)
        return Response(self.get_paginated_response(serializer.data), status=status.HTTP_200_OK)

    def post(self,request):
        serializer = UtilityRqeuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)