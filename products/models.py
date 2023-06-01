from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Product(models.Model):
    title = models.CharField(max_length=255,)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)
    owner = models.ForeignKey(
        'auth.User',
        related_name='product',
        on_delete=models.CASCADE)
    highlighted = models.TextField()

    class Meta:
        ordering = ["title"]
        verbose_name_plural = ("products")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)


class Review(models.Model):
    title = models.CharField(max_length=255,)
    description = models.TextField()
    grade = models.DecimalField(
        max_digits=1, decimal_places=1,)
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE,)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)
    author = models.ForeignKey(
        'auth.User',
        related_name='review',
        on_delete=models.CASCADE)
    highlighted = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)
