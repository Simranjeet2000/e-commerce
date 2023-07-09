from django.db import models
import datetime


class Category(models.Model):
    cat_name = models.CharField(max_length=30)
    cat_image = models.ImageField(upload_to="shop/uploadedimages",default="")

    def __str__(self):
        return self.cat_name
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    
    @staticmethod
    def get_all_categories_byid(id):
        return Category.objects.get(id = id)
    
    
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    desc1 = models.CharField(max_length=300, null=True, blank=True)
    desc2 = models.CharField(max_length=300, null=True, blank=True)
    desc3 = models.CharField(max_length=300, null=True, blank=True)
    desc4 = models.CharField(max_length=300, null=True, blank=True)
    desc5 = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    prod_image = models.ImageField(upload_to="shop/uploadedimages",default="")

    def __str__(self):
        return self.product_name
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_byId(category_id): 
        return Product.objects.filter(category = category_id) 
    
    @staticmethod
    def get_all_cart_byId(id): 
        return Product.objects.filter(id__in = id) 
    

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name


    def register(self):
        self.save()

    def emailexist(self):
        if Customer.objects.filter(email = self.email):
            return True
        else:
            return False
        

    @staticmethod
    def get_customer_byemail(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False
        
    

class Order(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=100, default="", blank=True)
    phone = models.CharField(max_length=50, default="", blank=True)
    date = models.DateField(default=datetime.datetime.today)


    def place_order(self):
        self.save()