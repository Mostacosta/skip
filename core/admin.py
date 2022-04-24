from django.contrib import admin
from core.models import Notfication, PaymentRequest, User,Code,Version
# Register your models here.

admin.site.register(User)
admin.site.register(Code)
admin.site.register(Version)
admin.site.register(Notfication)
admin.site.register(PaymentRequest)
