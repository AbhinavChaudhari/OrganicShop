from django.contrib import admin
from .models import Purchase,Stock,Expance,SaleTrans,remainingstock,Salehistory
from import_export.admin import ImportExportModelAdmin

# Register your models here.



@admin.register(Purchase)
class PurchaseAdmin(ImportExportModelAdmin):
    list_display = ('id', 
    'batch_sr_no',
    'stock_name',
    'pack',
    'size',
    'qty',
    'selling_price',
    'total',
)


@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
    list_display = ('id', 
    'batch_sr_no',
    'stock_name',
    'pack',
    'size',
    'qty',
    'selling_price',
    
)


@admin.register(SaleTrans)
class SaleTransAdmin(ImportExportModelAdmin):
    list_display = ('id', "CustomerName",'CustomerContact','batch_no','stock_name','size','qty','price'
    
    
   
)

@admin.register(Expance)
class expanceAdmin(admin.ModelAdmin):
    list_display = ('id', 
    'name',
    'remark',
    'price',
   
)

@admin.register(remainingstock)
class remainingstockAdmin(admin.ModelAdmin):
    list_display = ('id', 
    
    
    
   
)


@admin.register(Salehistory)
class SalehistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 
    
    
    
   
)