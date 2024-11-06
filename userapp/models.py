
import uuid
from colorfield.fields import ColorField
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from adminapp.models import User
from django_quill.fields import QuillField

class Main_Category(models.Model):
    name = models.CharField(max_length= 100,unique=True)
    
    slug = models.SlugField(blank=True,null=True,default=uuid.uuid1)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Main_Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE,null=True,related_name="sub_category")
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True,null=True,default=uuid.uuid1)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sub_Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.main_category.name + " "+ self.name

class Category(models.Model):
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.SET_NULL,null=True,related_name="category")
    catagoryname = models.CharField(max_length=50,)
    slug = models.SlugField(unique= True ,blank=True,null=True,default=uuid.uuid1)

    def __str__(self):
        return self.sub_category.main_category.name + " "+ self.sub_category.name + " " + self.catagoryname 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.sub_category.main_category.name + " "+ self.sub_category.name + " " + self.catagoryname)
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    brantitem = models.CharField(max_length=50)
    def __str__(self):
        return self.brantitem

class Product_type(models.Model):
    product_type = models.CharField( max_length=100)
    def __str__(self):
        return self.product_type

class Color(models.Model):
    color_name = models.CharField(max_length=255,blank=True)
    color_code= ColorField(default='#FF0000')
    def __str__(self) -> str:
        return self.color_code + " " + self.color_name

class Tags(models.Model):
    tag_name = models.CharField(max_length=255,blank=True)

    def __str__(self) -> str:
        return self.tag_name

class metadata(models.Model):
    field = models.CharField( max_length=50)
    value = models.CharField( max_length=50)
    def __str__(self):
        return self.field


    


class Product(models.Model):

    COLLECTION_TYPE= (
    ("Featured","Featured"),
    ("On sale","On sale"),
    ("Top selling","Top selling"),
    ("Deals","Deals"),
    ("Clearance","Clearance")
    )
    
    vendor = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)    
    pro_name = models.CharField(max_length=200)
    Pro_desc = QuillField()
    ratings = models.IntegerField()
    pro_catagory = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    pro_brnd = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name="brands")
    pro_collection = models.CharField(max_length=100, choices=COLLECTION_TYPE,blank=True)
    tags = models.ManyToManyField(Tags,blank=True)
    color  = models.ManyToManyField(Color,blank=True)
    product_type = models.ManyToManyField(Product_type,blank=True,related_name="product_types")
    price = models.IntegerField()
    after_discount = models.IntegerField(blank=True,null=True)
    total_quantity = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to="product/",null=True,blank=True)
    is_retail = models.BooleanField(default=0)
    discount = models.IntegerField(blank=True,null=True,default=0)
    slug = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.pro_name

    def save(self, *args, **kwargs):
        if self.discount is not None and self.discount is not 0:
            price = self.price 
            discount = self.discount
            self.after_discount = price-price*discount/100
        else:
            self.after_discount = 0
        self.slug = slugify(self.pro_name)
        super(Product, self).save(*args, **kwargs)
    



    @property
    def product_rate(self):
        return (self.rate_product/5)*100

    

    @property
    def get_absolute_image_url(self):
        # return "{0}{1}".format(settings.MEDIA_URL, self.main_image)
        return self.main_image
    

    @property
    def product_collection(self):
        return self.pro_collection          


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banner/",blank=True,null=True)
    desc = models.CharField(max_length=255,blank=True,null=True)
    product = models.ManyToManyField(Product,blank=True,related_name="pros")
    def __str__(self) -> str:
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=255,blank=True)
    desc = models.CharField(max_length=500,blank=True)
    background_image = models.ImageField(upload_to="slider/",blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default=None,null=True)

    

    def __str__(self):
        return self.title




class Events(models.Model):
    event_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    product = models.ManyToManyField(Product,default=None,null=True)
    slug = models.SlugField(blank=True,unique=True)

        
    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.event_name)
        super(Events, self).save(*args, **kwargs)



class Product_Image(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE, related_name="product_image")
    proimg = models.CharField(max_length=500)
    @property
    def get_absolute_image_url(self):
        # return "{0}{1}".format(settings.MEDIA_URL, self.proimg)
        return self.proimg

    

class Product_extra_information(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    discription = models.TextField(max_length=1000)

    def __str__(self):
        return self.product.pro_name

class SEO(models.Model):
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    seo_title = models.CharField( max_length=150)
    seo_description =  models.CharField( max_length=150)
    meta_data = models.ForeignKey(metadata, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.slug

class Giftcard(models.Model):
    cardname = models.CharField( max_length=150)
    cardimage = models.ImageField(upload_to="giftcard")
    cardamount = models.IntegerField()
    def __str__(self):
        return self.cardname




class Customers(models.Model):
    customer = models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    contact = models.IntegerField()
    address1 = models.CharField( max_length=150)
    address2 = models.CharField( max_length=150)
    city = models.CharField( max_length=150)
    zip_code = models.CharField(max_length=255)
    country = models.CharField( max_length=150)
    nearest_location = models.CharField( max_length=150)
    note = models.CharField( max_length=150)
    def __str__(self):
        return self.first_name




class Orders(models.Model):
    PAYMENTTYPE = (('PAID', 'PAID'), ('UNPAID', 'UNPAID'))
    PRODUCTDELIVARY = (('NEW', 'NEW'), ('APPROVED', 'APPROVED'),('CANCLE','CANCLE'),('DISPATCHED','DISPATCHED'),('RECIVED','RECIVED'))
    order_date = models.DateTimeField(auto_now=True)
    order_by = models.ForeignKey(User, on_delete=models.CASCADE)
    order_product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    payment = models.CharField(max_length=100, null=True, choices=PAYMENTTYPE,default="UNPAID")
    total_amount = models.FloatField(blank=True,null=True)
    delivery_status = models.CharField(max_length=100, null=True, choices=PRODUCTDELIVARY,default="NEW")
    
    
    def __str__(self):
        return self.order_by.email


    

class Size(models.Model):
    size_name= models.CharField(max_length=255,blank=True)
    def __str__(self) -> str:
        return self.size_name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="varients")
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)