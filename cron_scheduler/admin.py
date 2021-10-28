from django.contrib import admin

# Register your models here.
from .models import Switch,Action,ActionType


admin.site.register(Switch)
admin.site.register(ActionType)
admin.site.register(Action)

