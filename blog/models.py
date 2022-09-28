from datetime import datetime
from tabnanny import verbose
from django.db import models
from autoslug import AutoSlugField
from PIL import Image


def get_category_id():
    category, _ = Category.objects.get_or_create(name=Category.DEFAULT_NAME)
    return category.id


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="наименование"
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Category(models.Model):

    DEFAULT_NAME = ""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = "категории"

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name='наименование'
        )
    slug = AutoSlugField(populate_from="title", unique=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft")

    body = models.TextField(
        verbose_name='описание'
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='дата публикации')
    updated_date = models.DateTimeField(blank=True, null=True, verbose_name='дата дата обновления')

    tags = models.ManyToManyField(to=Tag, related_name="posts", blank=True, verbose_name='теги')
    category = models.ForeignKey(
        to=Category,
        related_name="posts",
        default=get_category_id,
        on_delete=models.SET_DEFAULT,
        blank=False,
        null=False,
        verbose_name='категория'
    )

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

    feature_image = models.ImageField(
        upload_to="uploads/", null=True, blank=True, verbose_name='картинка')

    @property
    def excerpt(self):
        character_limit = 150
        if len(self.body) < character_limit:
            excerpt = self.body
        else:
            excerpt = self.body[:character_limit] + "..."

        return excerpt

    def save(self, **kwargs):
        self.updated_date = datetime.now()
        super().save(**kwargs)

    def publish(self):
        self.published_date = datetime.now()
        self.status = "published"
        self.save()

    def __str__(self):
        return self.title
