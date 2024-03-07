from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductStock

@receiver(post_save, sender=Product)
def create_product_stock(sender, instance, created, **kwargs):
    if created:
        ProductStock.objects.create(product=instance, quantity=0)
