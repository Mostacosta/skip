from asyncore import read
from django.dispatch import receiver
from django.http import Http404
from nakdepaybackend.pagination import CustomResultsSetPagination
from nakdepaybackend.views import AutomatorView
from core.models import Notfication, PaymentRequest
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializer.notfication_serializer import NotficationSerializer,NotficationGetSerializer
from django.db.models import Q

class NotficationRequestView (AutomatorView):
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = NotficationSerializer
    get_serializer_class = NotficationGetSerializer
    model = Notfication
    with_pagination = True
    exclude = []

    def post(self, request):
        request["sender"] = request.user.pk
        return super().post(request)

class UserNotficationViewCount(APIView):

    permission_classes = [permissions.IsAuthenticated] 

    def get(self,request):
        notfications = Notfication.objects.filter(receiver=request.user,read=False)
        count_ = notfications.count()
        return Response ({"noti_count":count_})


class UserNotficationView(APIView,CustomResultsSetPagination):

    permission_classes = [permissions.IsAuthenticated] 

    def get(self,request):
        notfications = Notfication.objects.filter(receiver=request.user,read=False)
        for notification in notfications:
            notification.read = True
            notification.save()
        count_ = notfications.count()
        notfications_ = Notfication.objects.filter(Q(receiver=request.user) and
        (Q(request__type=PaymentRequest.pay) | (Q(request__type=PaymentRequest.request)and Q(request__response=PaymentRequest.pending)))).order_by("-created_at")
        object = self.paginate_queryset(notfications_, request)
        serializer = NotficationGetSerializer(object, many=True)
        res=self.get_paginated_response(serializer.data)
        res["noti_count"]=count_
        return Response(res, status=status.HTTP_200_OK)
