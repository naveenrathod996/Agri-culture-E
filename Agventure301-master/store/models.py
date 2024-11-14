from django.db import models
from django.contrib.auth.models import User

# Create your models here.

USER_TYPE = (
    ("1", "Customer"),
    ("2", "Seller"),
)
class Customer(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null = False, blank=False)
    type = models.CharField(max_length=30,choices=USER_TYPE,default=1)

    def __str__(self):
        return self.name

    def typeof(self):
        if self.type == "2":
            return True
        else:
            return False


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    orig = models.DecimalField(max_digits=7, decimal_places=2)
    prod_quantity = models.IntegerField(default=0, null=True, blank=False)
    fruit = models.BooleanField(default=False, null=True, blank=False)
    vegetable = models.BooleanField(default=False, null=True, blank=False)
    seed = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null = True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_discount(self):
        var1 = self.orig - self.price
        var2 = var1/self.orig
        total = 100 * var2
        return total

    @property
    def fru(self):
        if self.fruit == True:
            return True
        else:
            return False

    @property
    def vege(self):
        if self.vegetable == True:
            return True
        else:
            return False

    @property
    def isseed(self):
        if self.seed == True:
            return True
        else:
            return False

ORDER_STATUS = (
    ("1", "Order Placed"),
    ("2", "Shipping"),
    ("3", "Delivered"),
)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False, default="name")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=30,choices=ORDER_STATUS,default=1)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Language(models.Model):
    name = models.CharField(max_length=20)
  
    def __str__(self):
        return f"{self.name}"
