from django.contrib import admin

from notes.models import CustomUser, Notes

admin.site.register(Notes)
admin.site.register(CustomUser)
