from django.test import TestCase
from articles.models import Author, Outlet, Category, Article
from django.utils import timezone

class ArticleModelTestCase(TestCase):
    """This class defines the test suite for the Article model."""

    def setUp(self):
        """Defines the test client and other test variables."""

        # Add items needed to test foreign keys' constraints
        self.outlets = [
            Outlet.objects.create(
                name='Tech Crunch',
                website='http://techcrunch.com'
            ),
            Outlet.objects.create(
                name='Mashable',
                website='http://mashable.com'
            ),
            Outlet.objects.create(
                name='Cheesecake Labs',
                website='http://cheesecakelabs.com'
            ),
        ]

        self.categories = [
            Category.objects.create(
                name='Culture',
                slug='culture'
            ),
            Category.objects.create(
                name='Finance',
                slug='finance'
            ),
        ]

        self.authors = [
            Author.objects.create(
                name='Bill Gates'
            ),
            Author.objects.create(
                name='Guido van Rossum'
            ),
            Author.objects.create(
                name='Ada Lovelace'
            ),
        ]

        # Add some articles
        self.articles = [
            Article(
                title='Article 1',
                date=str(timezone.now()),
                url='art1',
                content='Article 1',
                outlet_id=self.outlets[0].id
            ),
            Article(
                title='Article 2',
                date=str(timezone.now()),
                url='art2',
                content='Article 2',
                outlet_id=self.outlets[1].id
            ),
            Article(
                title='Article 3',
                date=str(timezone.now()),
                url='art3',
                content='Article 3',
                outlet_id=self.outlets[1].id
            ),
            Article(
                title='Article 4',
                date=str(timezone.now()),
                url='art4',
                content='Article 4',
                outlet_id=self.outlets[0].id
            ),
        ]

        self.article = Article.objects.create(
            title='Article',
            date=str(timezone.now()),
            url='art',
            content='Article',
            outlet_id=self.outlets[2].id
        )


    def test_article_can_create(self):
        """Tests if the article model can create different articles."""
        old_count = Article.objects.count()

        for article in self.articles:
            article.save()

        new_count = Article.objects.count()
        self.assertEqual(old_count, new_count - 4)


    def test_article_assign_authors(self):
        """Tests if a newly created article's author is correct."""
        author1 = self.authors[0]
        author2 = self.authors[1]

        self.article.authors.add(author1)
        self.article.save()
        qty = Article.objects.filter(authors__in=[author1]).count()
        self.assertEqual(qty, 1)

        self.article.authors.add(author2)
        self.article.save()
        qty = Article.objects.filter(authors__in=[author1, author2]).count()
        self.assertEqual(qty, 2)


    def test_article_check_outlet(self):
        """Tests if a newly created article's outlet is correct."""
        self.assertEqual(self.article.outlet, self.outlets[2])


    def test_article_assign_categories(self):
        """Tests assigning of multiple categories to an article."""
        cat1 = self.categories[0]
        cat2 = self.categories[1]

        self.article.categories.add(cat1)
        self.article.save()
        qty = Article.objects.filter(categories__in=[cat1]).count()
        self.assertEqual(qty, 1)

        self.article.categories.add(cat2)
        self.article.save()
        qty = Article.objects.filter(categories__in=[cat1, cat2]).count()
        self.assertEqual(qty, 2)


    def test_article_delete_outlet(self):
        """Tests if cascade deletion is working for outlets."""

        # This test shouldn't change anything besides the outlet's active
        # attribute due to the disabling of hard deletes for this model.

        for article in self.articles:
            article.save()

        old_count = Article.objects.count()
        self.outlets[0].delete()
        new_count = Article.objects.count()

        self.assertEqual(old_count, new_count)
