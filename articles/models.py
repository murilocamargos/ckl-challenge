from django.db import models
from django.template.defaultfilters import slugify



class CustomQuerySet(models.QuerySet):
    """This class handles queryset model soft delete."""
    def delete(self):
        self.update(active = False)



class ActiveManager(models.Manager):
    """This class manages models that cannot be hard delete."""
    def active(self):
        """Get all active objects of a given model."""
        return self.model.objects.filter(active = True)

    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)



class Outlet(models.Model):
    """This class represents an information outlet."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    website = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    objects = ActiveManager()

    def delete(self):
        """Does not allow hard deletes."""
        self.active = False
        self.save()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)



class Category(models.Model):
    """This class represents the article category."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)



class Author(models.Model):
    """This class represents an author."""
    name = models.CharField(max_length=255, blank=False)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, null=True)
    twitter = models.CharField(max_length=255, default='')
    facebook = models.CharField(max_length=255, default='')
    linkedin = models.CharField(max_length=255, default='')
    profile = models.CharField(max_length=255, default='')
    website = models.CharField(max_length=255, default='')
    avatar = models.TextField(default='')
    about = models.TextField(default='')


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)



class Article(models.Model):
    """This class represents an article."""
    title = models.CharField(max_length=255, blank=False)
    date = models.DateTimeField(blank=False)
    url = models.CharField(max_length=255, blank=False, unique=True)
    thumb = models.CharField(max_length=255, default='')
    content = models.TextField(blank=False)

    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.title)