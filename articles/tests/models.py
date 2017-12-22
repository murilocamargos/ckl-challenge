from django.test import TestCase
from ..models import Author

class AuthorModelTestCase(TestCase):
    """This class defines the test suite for the Author model."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.name = "Murilo Camargos"
        self.author = Author(name = self.name)

    def test_author_can_create(self):
        """Tests if the author model can create an author."""
        old_count = Author.objects.count()
        self.author.save()
        new_count = Author.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_author_string_representation(self):
        """Tests if the author is correctly represented."""
        self.assertEqual(str(self.author), self.name)

    def test_author_default_slug(self):
        """Tests if the author's name is slugyfied by default."""
        self.author.save()
        self.assertEqual(self.author.slug, 'murilo-camargos')

    def test_author_defined_slug(self):
        """Tests if the model accepts a user defined slug."""
        self.author.slug = 'john-doe'
        self.author.save()
        self.assertEqual(self.author.slug, 'john-doe')