from django.db import models
from django.urls import reverse

class Category(models.Model):
    name= models.CharField(max_length=30,
                           unique=True)
    slug = models.SlugField(max_length=30,
                            unique=True)
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name_plural = 'категории'
        verbose_name='категория'
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    Category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(default=0.00, 
                                   max_digits=10,
                                   decimal_places=10)
    
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']),
                  models.Index(fields=['id','slug']),
                  models.Index(fields=['-created']),
                  ]
        verbose_name_plural = 'Продукты'
        verbose_name='продукт'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product_detail',
                    args=[self.slug])

    def sell_price(self):
        if self.discount:
            return reverse(self.price - self.price * self.discount / 100, 2)
        return self.price