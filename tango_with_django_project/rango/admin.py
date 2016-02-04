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
        (None,        {'fields': ['name','slug']}),
        ('Popularity info', {'fields': ['views', 'likes'],
                             'classes': ['collapse']}),
    ]

    inlines = [PageInLine]

    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)
#admin.site.register(Page, PageAdmin)