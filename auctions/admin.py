from django.contrib import admin
from django.contrib.admin.decorators import display

from .models import Category, Comment, Listing, Bid


class BidAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'user', 'get_value', 'timestamp')

    @display(ordering='listing__title', description='Listing')
    def get_title(self, obj):
        return obj.listing.title

    @display(ordering='value', description='Value')
    def get_value(self, obj):
        return '$%.2f' % obj.value


class BidInline(admin.TabularInline):
    model = Bid
    ordering = ('-value',)
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    ordering = ('-timestamp',)
    extra = 0


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'get_starting_price', 'timestamp', 'active')

    @display(ordering='starting_price', description='Starting Price')
    def get_starting_price(self, obj):
        return '$%.2f' % obj.starting_price

    inlines = [
        BidInline,
        CommentInline
    ]


class ListingInline(admin.TabularInline):
    model = Listing
    extra = 0
    fields = ((),)
    show_change_link = True
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ListingInline,
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'user', 'truncate_content', 'timestamp')

    @display(ordering='listing__title', description='Listing')
    def get_title(self, obj):
        return obj.listing.title

    @display(ordering='content', description='Content')
    def truncate_content(self, obj):
        if len(obj.content) < 70:
            return obj.content
        else:
            return obj.content[:67] + '...'


admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)