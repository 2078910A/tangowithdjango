from django.contrib import admin
from rango.models import Category, Page

#class PageAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['category']}),
#        ('Page info', {'fields': ['title', 'url']}),
#    ]

class PageInLine(admin.TabularInline):
    model = Page
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,        {'fields': ['name']}),
        ('Popularity info', {'fields': ['views', 'likes'],
                             'classes': ['collapse']}),
    ]
    inlines = [PageInLine]

admin.site.register(Category, CategoryAdmin)
#admin.site.register(Page, PageAdmin)

# Register your models here.
