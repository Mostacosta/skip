from nakdepaybackend.pagination import CustomResultsSetPagination
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404



class AutomatorView (APIView, CustomResultsSetPagination):
    permission_classes = [permissions.AllowAny] 
    serializer_class = None
    get_serializer_class = None
    model = None
    with_pagination = False
    exclude = []

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk=None):
        if "get" in self.exclude:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = None
        if not self.get_serializer_class:
            self.get_serializer_class = self.serializer_class
        if pk:
            object = self.get_object(pk)
            serializer = self.get_serializer_class(object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            object = self.model.objects.all()
            if(self.with_pagination == True):
                object = self.paginate_queryset(object, request)
                serializer = self.get_serializer_class(object, many=True)
                return Response(self.get_paginated_response(serializer.data), status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer_class(object, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if "post" in self.exclude:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if "put" in self.exclude:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        object = self.get_object(pk)
        serializer = self.serializer_class(
            object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if "delete" in self.exclude:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
