from django.contrib import admin

# Register your models here.
from polls.models import *


admin.site.register(MyUser)
admin.site.register(MediaPeofile)
admin.site.register(MyPost)