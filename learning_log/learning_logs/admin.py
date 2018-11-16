from django.contrib import admin

# Register your models here.

from learning_logs.models import Topic
admin.site.register(Topic)

from .models import Entry
admin.site.register(Entry)
