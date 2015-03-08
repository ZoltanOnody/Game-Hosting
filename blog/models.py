from redactor.fields import RedactorField

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256, blank=True)
    url = models.SlugField(max_length=32, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategória"
        verbose_name_plural = "Kategórie"
        ordering = ["name"]


class Tag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=256, blank=True)
    url = models.SlugField(max_length=32, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Značka"
        verbose_name_plural = "Značky"
        ordering = ["name"]


class Article(models.Model):
    headline = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    context = models.TextField(max_length=1024, blank=True)
    content = RedactorField(verbose_name=u'Text')

    url = models.SlugField(max_length=50, blank=True, unique=True)

    comments = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, auto_now_add=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = "Článok"
        verbose_name_plural = "Články"
        ordering = ["-date"]
