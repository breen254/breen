from django.contrib import admin
from .models import Post, Group, DeliveryRequest

admin.site.register(Group)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('name',)
    
    
admin.site.register(DeliveryRequest)