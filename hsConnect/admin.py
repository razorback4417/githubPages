from django.contrib import admin
from .models import Subject, Tutor, TutorSubject, Request

# Register your models here.

admin.site.register(Subject)
admin.site.register(Tutor)

admin.site.register(TutorSubject)
admin.site.register(Request)
