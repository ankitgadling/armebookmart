from django.contrib import admin
from .models import  UserEbook,PdfToMp3,Order
# Register your models here.
admin.site.register(UserEbook)
admin.site.register(PdfToMp3)
admin.site.register(Order)
