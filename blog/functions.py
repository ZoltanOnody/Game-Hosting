from blog.models import Category
from blog.models import Tag


def info_to_sidebar():
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'sidebar_categories': categories,
        'sidebar_tags': tags,
    }
    return context
