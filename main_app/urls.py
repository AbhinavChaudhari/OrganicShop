from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.desktop, name= "desktop" ),
    # path('desktop/', views.desktop, name= "desktop" ),

    # purchase
    path('purchase/', views.purchase, name= "purchase" ),
    # path('purchase/edit/<purchaseid>', views.purchaseEdit, name= "purchaseEdit" ),
    path('purchase/delete/<purchaseid>', views.purchaseDelete, name= "purchaseDelete" ),
    path('purchase/purchasehistory/<purchaseid>', views.purchasehistory, name= "purchasehistory" ),
    

    # sale 
    path('sales/',views.sales,name="sales"),
    
    path('EditSale/',views.EditSale,name="EditSale"),
    path('getBatchData/',views.getBatchData,name="getBatchData"),
    path('sales/edit/<saleid>',views.sale_Edit,name="sale_Edit"),
    path('sales/payhistroy/<saleid>',views.payhistroy,name="payhistroy"),



    # stock 
    path('stock/', views.stock,name="stock"),
    
    # expance
    path('expance/', views.expance,name="expance"),
    path('expance/edit/<expanceid>', views.expanceEdit,name="expanceEdit"),
    path('expance/delete/<expanceid>', views.expanceDelete,name="expanceDelete"),


    # export
    path('saleexport',views.saleExport,name='saleExport'),
    path('purchaseexport',views.purchaseExport,name='purchaseExport'),
    path('expanceexport',views.expanceExport,name='expanceExport'),
    path('stockexport',views.stockExport,name='stockExport'),
    path('remaningstockexport',views.remaningstockexport,name='remaningstockexport'),

    # remaining stock 
    path('remainingstock',views.remainingStock,name='remainingStock'),

    # report
    path('report',views.report,name='report'),
    path('salereport',views.salereport,name='salereport'),
    path('purchasereport',views.purchasereport,name='purchasereport'),
    path('stockreport',views.stockreport,name='stockreport'),
    path('expancereport',views.expancereport,name='expancereport'),
    path('profitloss',views.profitloss,name='profitloss'),
    path('purchaseremaining',views.purchaseremaining,name='purchaseremaining'),
    path('saleremaining',views.saleremaining,name='saleremaining'),
   
    # path('report/salemonthly',views.salemonthly,name='salemonthly'),
    # path('report/salemonthlyreport',views.salemonthlyreport,name='salemonthlyreport'),

    # pdf
    path('export_pdf/<saleid>',views.export_pdf,name='export_pdf'),
    path('backuprestore/', views.backuprestore,name="backuprestore"),
  
   
    path('logout',views.logout,name="logout"),
    

    

    
]
