from django.db import models
from django.template.defaultfilters import slugify

class NameSlug(models.Model):
    """
    This class is an abstraction for every model that needs a name and
    its slugified version along with creation and changing dates.
    """
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
    feed_url = models.CharField(max_length=255, default='')
    description = models.TextField()

class Category(NameSlug):
    """This class represents the article category."""
    pass

class Author(models.Model):
    """This class represents an author."""
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, blank=False)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
    profile = models.CharField(max_length=255, default='')
    twitter = models.CharField(max_length=255, default='')
    linkedin = models.CharField(max_length=255, default='')
    facebook = models.CharField(max_length=255, default='')
    website = models.CharField(max_length=255, default='')
    avatar = models.CharField(max_length=255, default='')
    about = models.TextField(default='')

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

class Article(models.Model):
    title = models.CharField(max_length=255, blank=False)
    date = models.DateTimeField(blank=False)
    url = models.CharField(max_length=255, blank=False, unique=True)
    thumb = models.CharField(max_length=255, default='')
    content = models.TextField(blank=False)

    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.title)