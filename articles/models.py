from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

class NameSlug(models.Model):
    """This class is an abstraction for every model that needs a name and
       its slugified version along with creation and changing dates."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        """Overrides save method to slugify name by default."""
        if not self.id and not self.slug:
            # Slugify only new entries without a defined slug
            self.slug = slugify(self.name)

        super(NameSlug, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Outlet(NameSlug):
    """This class represents an information outlet."""
    website = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField()

class Category(NameSlug):
    """This class represents the article category."""
    pass

class Author(NameSlug):
    """This class represents an author."""
    profile = models.CharField(max_length=255, unique=True, default='')
    twitter = models.CharField(max_length=255, unique=True, default='')
    linkedin = models.CharField(max_length=255, unique=True, default='')
    facebook = models.CharField(max_length=255, unique=True, default='')
    website = models.CharField(max_length=255, default='')
    avatar = models.CharField(max_length=255, default='')
    about = models.TextField()