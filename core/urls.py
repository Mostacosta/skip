from django.urls import path, re_path
from core.views.notfication_view import NotficationRequestView, UserNotficationView, UserNotficationViewCount
from core.views.paymentrequest_view import GenerateQR, PaymentRequestView, PaymentView
from core.views.user_view import CheckPhone, CodeResponseView, Contacts, CustomTokenObtainPairView, FingerPrintView, SearchUsers, SignUpView, login
from core.views.version_view import check_app
from django.conf.urls.static import static
from django.conf import settings
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet 



app_name = "core"

urlpatterns = [
    path('auth/jwt/create', CustomTokenObtainPairView.as_view(),
         name='custom_token_obtain_pair'),
    path("check_phone",CheckPhone.as_view()),
    path("signup",SignUpView.as_view()),
    path("code_response",CodeResponseView.as_view()),
    path("finger_print",FingerPrintView.as_view()),
    path('check', check_app),
    path('contacts',Contacts.as_view()),
    path('request/<str:pk>',PaymentRequestView.as_view()),
    path('request',PaymentRequestView.as_view()),
    path("pay/<str:pk>",PaymentView.as_view()),
    path("pay",PaymentView.as_view()),
    path('search_user',SearchUsers.as_view()),
    path('notfication',NotficationRequestView.as_view()),
    path('notfication/<str:pk>',NotficationRequestView.as_view()),
    path('notfication_user',UserNotficationView.as_view()),
    path("noti_count",UserNotficationViewCount.as_view()),
    re_path(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view(
        {'post': 'create'}), name='create_fcm_device'),
    path('generate_qr',GenerateQR.as_view()),
    path('login',login),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)