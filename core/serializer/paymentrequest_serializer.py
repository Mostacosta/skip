from nakdepaybackend.serializer import DynamicFieldsModelSerializer
from core.models import PaymentRequest
from core.serializer.user_serializer import SignUpSerializer

class PaymentRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = "__all__"


class PaymentRequestGetSerializer(DynamicFieldsModelSerializer):

    sender = SignUpSerializer()
    receiver = SignUpSerializer()
    
    class Meta:
        model = PaymentRequest
        fields = "__all__"

