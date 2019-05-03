from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('machine:product_list_by_category', args=[self.slug])


class Machine(models.Model):
    category = models.ForeignKey(Category, related_name='machines', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.IntegerField(default=10)

    class Meta:
        ordering = ('?',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('machine:product_detail', args=[self.id, self.slug])

