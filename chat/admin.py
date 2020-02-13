from django.contrib import admin

from .models import Room,ReadMessages,UnreadMessages

admin.site.register(Room)
admin.site.register(ReadMessages)
admin.site.register(UnreadMessages)
