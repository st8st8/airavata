from django.db import models
from django.contrib.sites.models import Site


class Page(models.Model):

    site = models.ForeignKey(Site)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title