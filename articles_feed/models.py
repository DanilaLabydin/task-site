from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Articles'
        verbose_name_plural = 'Articles'
        ordering = ['-time_update', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
        ordering = ['id']
