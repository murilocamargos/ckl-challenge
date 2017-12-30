from django.test import TestCase
from articles.models import Author

class AuthorModelTestCase(TestCase):
    """This class defines the test suite for the Author model."""

    def setUp(self):
        """Defines the test client and other test variables."""
        self.name = "Donald Knuth"
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


    def test_author_can_update_patched(self):
        """Tests if an author can be updated or patched."""
        self.author.save()

        self.author.linkedin = 'http://linkedin.com/donald'
        self.author.save()

        search = Author.objects.filter(linkedin__contains = 'donald').count()
        self.assertEqual(search, 1)


    def test_author_can_delete(self):
        """Tests if an author can be deleted."""
        self.author.save()
        self.author.delete()
        search = Author.objects.filter(name = self.name).count()
        self.assertEqual(search, 0)