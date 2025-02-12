from django.contrib import admin
from .models import WorkArea, Sensor, Parameter, ValueParameter

admin.site.register(WorkArea)
admin.site.register(Sensor)
admin.site.register(Parameter)
admin.site.register(ValueParameter)
