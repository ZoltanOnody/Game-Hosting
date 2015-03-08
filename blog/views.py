from blog.models import Article
from blog.models import Tag
from blog.models import Category
from blog.functions import info_to_sidebar

from django.shortcuts import render
from django.shortcuts import get_object_or_404


def home(request):
    articles = Article.objects.filter(active=True)

    context = {
        'articles': articles,
        'title': "Blog",
    }
    context.update(info_to_sidebar())

    return render(request, 'blog/home.html', context)


def single(request, slug):
    article = get_object_or_404(Article, url=slug, active=True)

    context = {
        'article': article,
        'title': article.headline,
    }
    context.update(info_to_sidebar())

    return render(request, 'blog/single.html', context)


def category(request, slug):
    cat = get_object_or_404(Category, url=slug)
    articles = Article.objects.filter(category=cat, active=True)

    context = {
        'category': cat,
        'articles': articles,
        'title': "Kategória: " + cat.name
    }
    context.update(info_to_sidebar())

    return render(request, 'blog/category.html', context)


def tag(request, slug):
    tg = get_object_or_404(Tag, url=slug)
    articles = Article.objects.filter(tags=tg, active=True)

    context = {
        'tag': tg,
        'articles': articles,
        'title': "Značka: " + tg.name
    }
    context.update(info_to_sidebar())

    return render(request, 'blog/tag.html', context)
