from django.shortcuts import render
from rest_framework.decorators import api_view

from core.models import Version
from rest_framework.response import Response


# Create your views here.


@api_view(['POST'])
def check_app(request):
    version_ = request.data.get("version", "")
    obj = Version.objects.filter(version=version_)
    if obj.exists():
        obj = obj.first()
        return Response({"status": obj.status})

    return Response({"status": False})