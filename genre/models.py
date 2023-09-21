from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver


class Genre(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Genre)
def category_slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
