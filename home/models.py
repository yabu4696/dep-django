from django.db import models

class Item_category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name
    
