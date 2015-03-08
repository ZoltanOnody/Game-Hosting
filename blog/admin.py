from blog.models import Article
from blog.models import Category
from blog.models import Tag

from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['headline', 'category', 'date', 'active', 'comments']
    prepopulated_fields = {'url': ('headline',)}
    fieldsets = (
        (None, {'fields': ('headline', 'url')}),
        ('Article: ', {'fields': ('context', 'content', 'category', 'tags')}),
        ('Advanced settings: ', {'fields': ('active', 'comments')}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'description']
    prepopulated_fields = {'url': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'description']
    prepopulated_fields = {'url': ('name',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
