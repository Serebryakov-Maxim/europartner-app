from django.contrib import admin
from .models import Pressform, TypeWork, Work, Progress, MediaFile

admin.site.register(Pressform)
admin.site.register(TypeWork)
admin.site.register(Work)
admin.site.register(Progress)
admin.site.register(MediaFile)
