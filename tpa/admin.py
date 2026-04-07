from django.contrib import admin
from .models import Machine, Event, Job, Cycle, MashineStatus

admin.site.register(Machine)
admin.site.register(MashineStatus)
admin.site.register(Cycle)
admin.site.register(Event)
admin.site.register(Job)

