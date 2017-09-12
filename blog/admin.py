from django.contrib import admin
from blog.models import *
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','category','created_time','modified_time','author']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk','name']

class TagAdmin(admin.ModelAdmin):
    list_display = ['pk','name']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Post,PostAdmin)