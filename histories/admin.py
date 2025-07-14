from django.contrib import admin
from .models import History, HistorySet   

# Register your models here.
admin.site.register(History)
admin.site.register(HistorySet)