from django.contrib import admin

from blog import models

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status"]


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Tag, admin.ModelAdmin)
admin.site.register(models.Category, admin.ModelAdmin)
