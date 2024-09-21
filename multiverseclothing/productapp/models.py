from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import jsonfield

class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, unique=True)
    price=models.CharField(max_length=250)
    tag = models.CharField(max_length=25)
    color = models.CharField(max_length=225)
    size = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Selection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_color = models.CharField(max_length=50)
    selected_size = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    details_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Magazine(models.Model):
    pic=models.ImageField(upload_to="magazine/")


    def __str__(self):
        return f"Magazine {self.id}"


class Shop(models.Model):
    photo1 = models.ImageField(upload_to="shop/")
    photo2 = models.ImageField(upload_to="shop/")
    photo3 = models.ImageField(upload_to="shop/")
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=225)
    size = models.CharField(max_length=225)
    price = models.CharField(max_length=250)
    design = models.CharField(max_length=400, blank=False)
    fit = models.CharField(max_length=400, blank=False)
    occasion = models.CharField(max_length=400, blank=False)
    sleeve = models.CharField(max_length=400, blank=False)
    neck = models.CharField(max_length=400, blank=False)
    wash_care = models.CharField(max_length=400, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cat = models.CharField(max_length=255, blank=False)
    gen = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shop {self.id}"

    def get_categories(self):
        return self.cat.split(",")  # Split the string into a list

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class OrderCart(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     info=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
     product_name = models.CharField(max_length=255)
     color = models.CharField(max_length=225)
     size = models.CharField(max_length=225)
     amount = models.CharField(max_length=10)
     payment_id = models.CharField(max_length=100)
     paid = models.BooleanField(default=False)
     order_confirmed = models.BooleanField(default=True)
     shipped = models.BooleanField(default=False)
     delivered = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return f"{self.user.username} - {self.amount}"

class OrderDesign(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     info=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
     design_name = models.CharField(max_length=255)
     designcolor = models.CharField(max_length=225)
     designsize = models.CharField(max_length=225)
     amount = models.CharField(max_length=10)
     payment_id = models.CharField(max_length=100)
     paid = models.BooleanField(default=False)
     order_confirmed = models.BooleanField(default=True)
     shipped = models.BooleanField(default=False)
     delivered = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return f"{self.user.username} - {self.amount}"



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.product.title}"


