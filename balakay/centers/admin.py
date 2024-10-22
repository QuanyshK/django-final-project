from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Center)
admin.site.register(Section)
admin.site.register(Schedule)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(FavoriteSection)

