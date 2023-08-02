from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'product'
    name = models.CharField(max_length=50)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    limitDate = models.DateField()
    priority = models.CharField(
        max_length=15,
        choices=(
            ('fundamental', 'Fundamental'),
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        )
    )
    finState = models.BooleanField(default=False)
    ejecState = models.BooleanField(default=False)
    
class Category(models.Model):
    class Meta:
        db_table = 'category'
    service = models.CharField(max_length=50)
    transport     = models.CharField(max_length=50)
    food    = models.CharField(max_length=50)
    study   = models.CharField(max_length=50)
    work1   = models.CharField(max_length=50)
    work2   = models.CharField(max_length=50)
    housing  = models.CharField(max_length=50)
    health   = models.CharField(max_length=50)
    salary  = models.CharField(max_length=50)
    debt   = models.CharField(max_length=50)
    other   = models.CharField(max_length=50)