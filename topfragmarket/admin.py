from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)

admin.site.register(Listing)
admin.site.register(ListingImage)

admin.site.register(Condition)

admin.site.register(Chat)
admin.site.register(ChatMessage)

admin.site.register(Thread)
admin.site.register(Comment)
