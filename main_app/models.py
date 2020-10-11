from django.db import models
from datetime import date

# Create your models here.
class Purchase(models.Model):
    vandor_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    batch_sr_no = models.CharField(max_length=100)
    stock_name = models.CharField(max_length=100)
    vandor_price = models.IntegerField(default="0")
    pack = models.IntegerField(default="0")
    size = models.CharField(max_length=100)
    qty = models.IntegerField(default="0")
    selling_price = models.IntegerField(default="0")
    total = models.IntegerField(default="0")
    date = models.DateField(auto_now_add=True,)
    paid = models.IntegerField(default="0")
    remaining = models.IntegerField(default="0")
    remark = models.CharField(max_length=100 )

    def __str__(self):
        return "%s %s" % (self.vandor_name, self.batch_sr_no)

class Stock(models.Model):
    batch_sr_no = models.CharField(max_length=100)
    stock_name = models.CharField(max_length=100)
    vandor_price = models.IntegerField(default="0")
    pack = models.IntegerField(default="0")
    size = models.CharField(max_length=100)
    qty = models.IntegerField(default="0")
    selling_price = models.IntegerField(default="0")
    date = models.DateField(auto_now_add=True)





class SaleTrans(models.Model):
    
    CustomerName = models.CharField(max_length=256)
    CustomerContact =models.CharField(max_length=256)
    batch_no =models.CharField(max_length=256)
    stock_name =models.CharField(max_length=256)
    size = models.CharField(max_length=100)
    qty = models.IntegerField(default="0")
    price = models.IntegerField(default="0")
    paid = models.IntegerField(default="0")
    remaining = models.IntegerField(default="0")
    remark = models.CharField(max_length=100 )
    total = models.IntegerField(default="0")
    option = models.CharField(max_length=50)
    
    uploaded_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.stock_name)

   

class Expance(models.Model):
     
    name = models.CharField(max_length=256)
    remark =models.CharField(max_length=256)
    price = models.IntegerField(default=0)
    uploaded_at = models.DateField(auto_now_add=True)
    
class remainingstock(models.Model):
    batch_sr_no = models.CharField(max_length=100)
    stock_name = models.CharField(max_length=100)
    pack = models.IntegerField(default="0")
    size = models.CharField(max_length=100)
    qty = models.IntegerField(default="0")
    selling_price = models.IntegerField(default="0")
    date = models.DateField(auto_now_add=True)

class Salehistory(models.Model):
    user = models.ForeignKey(SaleTrans ,on_delete=models.CASCADE,blank=True,null=True)
    total = models.IntegerField()
    paid = models.IntegerField()
    remaining = models.IntegerField()
    remark = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

class Purchasehistroy(models.Model):
    user = models.ForeignKey(Purchase ,on_delete=models.CASCADE,blank=True,null=True)
    total = models.IntegerField()
    paid = models.IntegerField()
    remaining = models.IntegerField()
    remark = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)