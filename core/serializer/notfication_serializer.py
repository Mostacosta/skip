from core.serializer.paymentrequest_serializer import PaymentRequestGetSerializer
from nakdepaybackend.serializer import DynamicFieldsModelSerializer
from core.models import Notfication, PaymentRequest
from core.serializer.user_serializer import SignUpSerializer



class NotficationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Notfication
        fields = "__all__"


class NotficationGetSerializer(DynamicFieldsModelSerializer):

    request = PaymentRequestGetSerializer()
    receiver = SignUpSerializer()
    
    class Meta:
        model = Notfication
        fields = "__all__"