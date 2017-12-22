from django.db import models
from django.template.defaultfilters import slugify

class Author(models.Model):
    """This class represents an author."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    twitter = models.CharField(max_length=255, unique=True)
    linkedin = models.CharField(max_length=255, unique=True)
    facebook = models.CharField(max_length=255, unique=True)
    about = models.TextField()

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

        super(Author, self).save(*args, **kwargs)