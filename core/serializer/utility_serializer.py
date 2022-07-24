from core.serializer.paymentrequest_serializer import PaymentRequestGetSerializer
from core.serializer.user_serializer import SignUpSerializer
from nakdepaybackend.serializer import DynamicFieldsModelSerializer
from core.models import PaymentRequest, Utility, UtilityRequests

class UtilitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Utility
        fields = "__all__"


class UtilityGetSerializer(DynamicFieldsModelSerializer):
    user = SignUpSerializer()
    class Meta:
        model = Utility
        fields = "__all__"

class UtilityRqeuestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UtilityRequests
        fields = "__all__"


class UtilityRequestGetSerializer(DynamicFieldsModelSerializer):
    utility = UtilityGetSerializer()
    user = SignUpSerializer()
    request = PaymentRequestGetSerializer()
    class Meta:
        model = UtilityRequests
        fields = "__all__"


