from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ()
)

# Create your models here.
class ProductsModel(models.Model):
    """
    Represents a product in the e-commerce system.

    Attributes:
    - title (str): The title or name of the product. Limited to 100 characters.
    - price (float): The price of the product.

    Methods:
    - __str__: Returns the string representation of the product, which is its title.
    """
    title = models.CharField(max_length=100)
    price = models.FloatField()
    

    def __str__(self):
        return str(self.title)


class OrderProductsModel(models.Model):
    """
    Represents a product included in an order.

    Attributes:
    - product (ProductsModel): The product associated with this order item.

    Methods:
    - __str__: Returns the string representation of the order item, which is the title of the associated product.
    """
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title
    
    
class OrderModel(models.Model):
    """
    Represents an order made by a user in the e-commerce system.

    Attributes:
    - user (User): The user who placed the order.
    - products (ManyToManyField): The products included in the order, linked through OrderProductsModel.
    - start_date (DateTimeField): The date and time when the order was created.
    - ordered_date (DateTimeField): The date and time when the order was finalized.
    - ordered (bool): Indicates if the order has been placed or not.

    Methods:
    - __str__: Returns the string representation of the order, which is the username of the user who placed it.
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProductsModel)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    