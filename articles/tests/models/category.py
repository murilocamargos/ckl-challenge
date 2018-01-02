from django.test import TestCase
from articles.models import Category

class CategoryModelTestCase(TestCase):
    """This class defines the test suite for the Category model."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.name = "CKL Rocks"
        self.category = Category(
            name=self.name,
            slug='ckl-rocks'
        )


    def test_category_can_create(self):
        """Tests if the category model can create a category."""
        old_count = Category.objects.count()
        self.category.save()
        new_count = Category.objects.count()
        self.assertNotEqual(old_count, new_count)


    def test_category_string_repr(self):
        """Tests if the category is correctly represented."""
        self.assertEqual(str(self.category), self.name)


    def test_category_can_update_patch(self):
        """Tests if a category can be updated or patched."""
        self.category.save()

        self.category.slug = 'ckl'
        self.category.save()

        search = Category.objects.filter(slug='ckl').count()
        self.assertEqual(search, 1)


    def test_category_can_delete(self):
        """Tests if a category can be deleted."""
        self.category.save()
        self.category.delete()
        search = Category.objects.filter(name=self.name).count()
        self.assertEqual(search, 0)
