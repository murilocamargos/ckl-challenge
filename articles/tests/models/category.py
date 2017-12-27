from django.test import TestCase
from articles.models import Category

class CategoryModelTestCase(TestCase):
    """This class defines the test suite for the Category model."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.name = "CKL Rocks"
        self.category = Category(name = self.name)


    def test_category_can_create(self):
        """Tests if the category model can create a category."""
        old_count = Category.objects.count()
        self.category.save()
        new_count = Category.objects.count()
        self.assertNotEqual(old_count, new_count)


    def test_category_string_representation(self):
        """Tests if the category is correctly represented."""
        self.assertEqual(str(self.category), self.name)


    def test_category_default_slug(self):
        """Tests if the category's name is slugified by default."""
        self.category.save()
        self.assertEqual(self.category.slug, 'ckl-rocks')


    def test_category_defined_slug(self):
        """Tests if the model accepts a user defined slug."""
        self.category.slug = 'cheesecake'
        self.category.save()
        self.assertEqual(self.category.slug, 'cheesecake')