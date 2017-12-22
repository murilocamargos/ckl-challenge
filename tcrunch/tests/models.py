from django.test import TestCase
from ..models import Author

class AuthorModelTestCase(TestCase):
    """This class defines the test suite for the Author model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.name = "Murilo Camargos"
        self.author = Author(name = self.name)

    def test_author_can_create(self):
        """Test if the author model can create an author."""
        old_count = Author.objects.count()
        self.author.save()
        new_count = Author.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_author_string_representation(self):
        """Test if the author is correctly represented."""
        self.assertEqual(str(self.author), self.name)

    def test_author_default_slug(self):
        self.author.save()
        self.assertEqual(self.author.slug, 'murilo-camargos')

    def test_author_defined_slug(self):
        self.author.slug = 'john-doe'
        self.author.save()
        self.assertEqual(self.author.slug, 'john-doe')