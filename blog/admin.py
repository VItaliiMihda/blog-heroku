from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_pub')
    exclude = ('slug',)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
