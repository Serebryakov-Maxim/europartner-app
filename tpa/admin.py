from django.contrib import admin
from .models import Machine, Event, Job, Cycle, MachineStatus

admin.site.register(Machine)
admin.site.register(MachineStatus)
admin.site.register(Cycle)
admin.site.register(Event)
admin.site.register(Job)

