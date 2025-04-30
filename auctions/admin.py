from django.contrib import admin
from .models import User,Listing,Comment,Bid,WatchList,Like,Category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchList)
admin.site.register(Like)
admin.site.register(Category, CategoryAdmin)