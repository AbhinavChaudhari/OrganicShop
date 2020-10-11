from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Purchase,Stock,Expance,SaleTrans,remainingstock,Salehistory,Purchasehistroy
from django.http import JsonResponse
from django.core import serializers
import json as simplejson
from django.http import HttpResponse
import csv
import calendar
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.contrib.auth.models import auth
import datetime
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template 
from django.contrib import messages
import sqlite3
import io
from datetime import datetime
import time
from django.core.management import call_command




def backuprestore(request):
    if request.method == 'POST':
        if 'LocalBack' in request.POST:
            try:
                print('try')
                call_command('dbbackup')
                return redirect('backuprestore')
            except:
                print('exectute')
                return redirect('backuprestore')
        if 'restorefile' in request.POST:
            try:
                print('try')
                call_command('dbrestore','--noinput')
                return redirect('backuprestore')
            except:
                print('exectute')
                return redirect('backuprestore')

       
    else:
        return render(request,'root/backup.html')


def dbbackup():
    conn = sqlite3.connect('db.sqlite3')
    newtime = time.time()
    local_time = time.ctime(newtime)
    returnt = 'backup/clientes_dump '+str(local_time.replace(':','T'))+'.sql'
    with io.open(returnt, 'w') as f:
        for linha in conn.iterdump():
            f.write('%s\n' % linha)
    print('Backup performed successfully.')
    conn.close()
    return returnt



def dbbackup():
    conn = sqlite3.connect('db.sqlite3')
    newtime = time.time()
    local_time = time.ctime(newtime)
    returnt = 'backup/clientes_dump '+str(local_time.replace(':','T'))+'.sql'
    with io.open(returnt, 'w') as f:
        for linha in conn.iterdump():
            f.write('%s\n' % linha)
    print('Backup performed successfully.')
    conn.close()
    return returnt






def export_pdf(request,saleid):
    
    st= SaleTrans.objects.get(id=saleid)
    data = {'sale': st}
    # template = get_template('root/pdf/customer.html')
    return render(request, 'root/pdf/customer.html',data)


def remaningstockexport(request):
    if  request.user.is_authenticated:

        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="remainingstockreport.csv"'
            writer = csv.writer(response)
            writer.writerow([
            
                'batch_sr_no',
                'stock_name',
            
                'pack',
                'size',
                'qty',
                'selling_price',
                
                'date',
        
            ])

            users = remainingstock.objects.filter(Q(date__gte=fromdate) & Q(date__lte=todate)).values_list(
                'batch_sr_no',
                'stock_name',
            
                'pack',
                'size',
                'qty',
                'selling_price',
                
                'date',
            )
            
        
            for user in users: 
                writer.writerow(user)
                
        


            writer.writerow([])
            writer.writerow([])

        
            writer.writerow([
                "No of Remaning Stock Stocks",len(users)
            ])  

            return response
        else:
            return render(request,'root/report/remaningstockexport.html')
    else:
        return redirect('login')

def profitloss(request):
    if  request.user.is_authenticated:
        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="ProfitLossreport.csv"'
            writer = csv.writer(response)
            sale = SaleTrans.objects.filter(Q(uploaded_at__gte=fromdate) & Q(uploaded_at__lte=todate))
            exp= Expance.objects.filter(Q(uploaded_at__gte=fromdate) & Q(uploaded_at__lte=todate))

            profit_list=[]
            
            for st in sale: 
                
                get_batch= Stock.objects.get(batch_sr_no=st.batch_no)
                vandor_price_total =(get_batch.vandor_price)*st.qty
                sale_price_total =(st.price)*st.qty
                abc= sale_price_total-vandor_price_total
                
                
                profit_list.append(abc)
            
            getexe =[]
            for i in exp:
                getexe.append(i.price) 

            profitloss=sum(profit_list) - sum(getexe)
            
            
            if profitloss >0:
                # writer.writeheader()
                writer.writerow([
                    "from",fromdate,"To",todate
                    
                ])
                writer.writerow([
                    "No Of Sale",len(sale)
                ])


                writer.writerow([
                    "No Of Expance",len(exp)
                ])
                writer.writerow([
                    "Total profit",profitloss
            ])
                
            else:
                writer.writerow([
                    "from",fromdate,"To",todate
                ])
                writer.writerow([
                    "No Of Sale",len(sale)
                ])
                writer.writerow([
                    "Total loss",profitloss
            ])
                
            

            return response
        else:
            return render(request,'root/report/profitloss.html')
    else:
        return redirect('login')
        
def importfile(request):
    return





def logout(request):
    auth.logout(request)
    return redirect('login')

def report(request):

    return render(request,"root/report/report.html")

def purchasereport(request):
    if  request.user.is_authenticated:
        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Purchasereport.csv"'
            writer = csv.writer(response)

            writer.writerow([
                'vandor_name',
                'mobile_no',
                'batch_sr_no',
                'stock_name',
                'vandor_price',
                'pack',
                'size',
                'qty',
                'selling_price',
                'total',
                'paid',
                'remaining',
                'remark',
                'date',
        
            ])

            users = Purchase.objects.filter(Q(date__gte=fromdate) & Q(date__lte=todate)).values_list(
                'vandor_name',
                'mobile_no',
                'batch_sr_no',
                'stock_name',
                'vandor_price',
                'pack',
                'size',
                'qty',
                'selling_price',
                'total',
                'paid',
                'remaining',
                'remark',
                'date',
            )
            
        
            for user in users: 
                writer.writerow(user)
                
        


            writer.writerow([])
            writer.writerow([])

        
            writer.writerow([
                "No of Stocks",len(users)
            ])  

            return response
        else:
            return render(request,'root/report/purchasereport.html')  
    else:
        return redirect('login')  

def stockreport(request):
    if  request.user.is_authenticated:
        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stockreport.csv"'
            writer = csv.writer(response)

            writer.writerow([
                'batch_sr_no',
                'stock_name',
                'vandor_price',
                'pack',
                'size',
                'qty',
                'selling_price',
                'date',
        
            ])

            users = Stock.objects.filter(Q(date__gte=fromdate) & Q(date__lte=todate)).values_list(
                'batch_sr_no',
                'stock_name',
                'vandor_price',
                'pack',
                'size',
                'qty',
                'selling_price',
                'date',
            )
            
        
            for user in users: 
                writer.writerow(user)
                
        


            writer.writerow([])
            writer.writerow([])

        
            writer.writerow([
                "No of Stocks",len(users)
            ])  

            return response
        else:
            return render(request,'root/report/stockreport.html')
    else:
        return redirect('login')

def expancereport(request):
    if  request.user.is_authenticated:
        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Expancereport.csv"'
            writer = csv.writer(response)

            writer.writerow([
                'name',
                'remark',
                'price',
                'uploaded_at',
        
            ])

            users = Expance.objects.filter(Q(uploaded_at__gte=fromdate) & Q(uploaded_at__lte=todate)).values_list(
                'name',
                'remark',
                'price',
                'uploaded_at',
            )
            
            total =0
            for user in users: 
                writer.writerow(user)
                total += user[2]
        


            writer.writerow([])
            writer.writerow([])

            writer.writerow([
                "Total Expance", total
                
            ])

            writer.writerow([
                "No of Expances",len(users)
            ])  

            return response
        else:
            return render(request,'root/report/expancereport.html')
    else:
        return redirect('login')

def salereport(request):
    if  request.user.is_authenticated:
        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            option = request.POST['option_choice']   
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="salereport.csv"'
            writer = csv.writer(response)
        
            writer.writerow([
                'CustomerName',
                'CustomerContact',
                'batch_no',
                'stock_name',
                'size',
                'qty',
                'price',
                'paid',
                'remaining',
                'remark',
                'total',
                'option',
                'uploaded_at',
        
            ])
            if option == '':

                users = SaleTrans.objects.filter(Q(uploaded_at__gte=fromdate) & Q(uploaded_at__lte=todate)).values_list(
                    'CustomerName',
                    'CustomerContact',
                    'batch_no',
                    'stock_name',
                    'size',
                    'qty',
                    'price',
                    'paid',
                    'remaining',
                    'remark',
                    'total',
                    'option',            
                    'uploaded_at',            
                )
            else:
                users = SaleTrans.objects.filter(Q(uploaded_at__gte=fromdate) & Q(uploaded_at__lte=todate), option=option,).values_list(
                    'CustomerName',
                    'CustomerContact',
                    'batch_no',
                    'stock_name',
                    'size',
                    'qty',
                    'price',
                    'paid',
                    'remaining',
                    'remark',
                    'total',
                    'option',            
                    'uploaded_at',
                )
            
            total =0
            remaining =0
            paid =0
            for user in users: 
                writer.writerow(user)
                total += user[10]
                remaining +=user[8]
                paid += user[7]

            writer.writerow([])
            writer.writerow([])

            writer.writerow([
                "Paid ",paid
            ])
            writer.writerow([
                "remainings ",remaining
            ])
            writer.writerow([
                "Total Sale",total
            ])
            writer.writerow([
                "No of sale",len(users)
            ])    
            return response
        else:
            return render(request,'root/report/salereport.html')
    else:
        return redirect('login')

def saleremaining(request):
    if  request.user.is_authenticated:

        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            option = request.POST['remaining']   
            print(option)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="salereport.csv"'
            writer = csv.writer(response)
        
            writer.writerow([
                'CustomerName',
                'CustomerContact',
                'batch_no',
                'stock_name',
                'size',
                'qty',
                'price',
                'paid',
                'remaining',
                'remark',
                'total',
                'option',
                'uploaded_at',
        
            ])
            if option == '':
                messages.error(request, 'Enter Remaining amount .')
                return redirect('saleremaining')
                

            
            else:
                users = SaleTrans.objects.filter(Q(uploaded_at__gte=fromdate) & Q(uploaded_at__lte=todate), remaining__gte=option,).values_list(
                    'CustomerName',
                    'CustomerContact',
                    'batch_no',
                    'stock_name',
                    'size',
                    'qty',
                    'price',
                    'paid',
                    'remaining',
                    'remark',
                    'total',
                    'option',            
                    'uploaded_at',
                )
            
            total =0
            remaining =0
            paid =0
            for user in users: 
                writer.writerow(user)
                total += user[10]
                remaining +=user[8]
                paid += user[7]

            writer.writerow([])
            writer.writerow([])

            
            writer.writerow([
                "remainings ",remaining
            ])
            
            writer.writerow([
                "No of remaining amt User",len(users)
            ])    
            return response
        else:
            return render(request,'root/report/saleremaining.html')
    else:
        return redirect('login')
    
def purchaseremaining(request):
    if  request.user.is_authenticated:
        if request.method =="POST":
            fromdate= request.POST['fromdate']
            todate = request.POST['todate']
            option = request.POST['remaining']   
            print(option)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="purchaseremaining.csv"'
            writer = csv.writer(response)
        
            writer.writerow([
                'vandor_name',
                'mobile_no',
                'batch_sr_no',
                'stock_name',
                'vandor_price',
                'pack',
                'size',
                'qty',
                'selling_price',
                'total',
                'paid',
                'remaining',
                'remark',
                'date',
        
            ])
            if option == '':
                messages.error(request, 'Enter Remaining amount')
                return redirect('saleremaining')
            

           
            else:
                users = Purchase.objects.filter(Q(date__gte=fromdate) & Q(date__lte=todate), remaining__gte=option,).values_list(
                    'vandor_name',
                    'mobile_no',
                    'batch_sr_no',
                    'stock_name',
                    'vandor_price',
                    'pack',
                    'size',
                    'qty',
                    'selling_price',
                    'total',
                    'paid',
                    'remaining',
                    'remark',
                    'date',
                )
            
            total =0
            remaining =0
            paid =0
            for user in users: 
                writer.writerow(user)
                total += user[10]
                remaining +=user[8]
                paid += user[7]

            writer.writerow([])
            writer.writerow([])

            
            writer.writerow([
                "remainings ",remaining
            ])
            
            writer.writerow([
                "No of remaining amt User",len(users)
            ])    
            return response
        else:
            return render(request,"root/report/purchaseremaining.html")
    else:
        return redirect('login')


def remainingStock(request):
    if  request.user.is_authenticated:
        st= remainingstock.objects.all()
        
        

        if request.method == "POST":
            if Stock.objects.filter(batch_sr_no=request.POST['batch_sr_no']).exists():
                print('Query Availvbale')
                messages.error(request, 'The Batch No already Exist Try new one')
            else:
                
                stock =Stock()
                remainingStock=remainingstock()
                size = str(request.POST['size'])+" "+str(request.POST['unit'])
                stock.batch_sr_no = request.POST['batch_sr_no']
                stock.stock_name = request.POST['stock_name']
                stock.vandor_price = request.POST['vandor_price']
                stock.pack = request.POST['pack']
                stock.size = size
                stock.qty = request.POST['qty']
                stock.selling_price = request.POST['selling_price']

                remainingStock.batch_sr_no = request.POST['batch_sr_no']
                remainingStock.stock_name = request.POST['stock_name']
                remainingStock.vandor_price = request.POST['vandor_price']
                remainingStock.pack = request.POST['pack']
                remainingStock.size = size
                remainingStock.qty = request.POST['qty']
                remainingStock.selling_price = request.POST['selling_price']
                stock.save()
                remainingStock.save()
                
                return redirect("remainingStock")
        else:
            return render(request, 'root/remaining_stock/r_stock.html',{'stocks':st})
    else:
        return redirect('login')


def sale_Edit(request,saleid):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            # if '' in request.POST:
        
            st = SaleTrans.objects.get(id= saleid)
            st.price = request.POST['price']
            st.total = request.POST['total']
            st.paid = request.POST['paid']
            st.remaining = request.POST['remaining']
            st.remark = request.POST['remark']
            st.option = request.POST['option_method']
            st.save()
            return redirect('sales')
        else:
            sale = SaleTrans.objects.get(id =saleid)
            return render(request,'root/sales/sale_edit.html',{'stock':sale})
    else:
        return redirect('login')
    

def getBatchData(request):
    
    stockdata = Stock.objects.filter(batch_sr_no = request.GET['batch_no'])
    tmpJson = serializers.serialize("json",stockdata)
    tmpObj = simplejson.loads(tmpJson)
    return JsonResponse(simplejson.dumps(tmpObj) , safe=False)




def purchasehistory(request,purchaseid):
    if  request.user.is_authenticated:
        purchase = Purchase.objects.get(id=purchaseid)
        his = Purchasehistroy.objects.filter(user=purchase)
        rowHis = his

        if request.method =='POST':
            if 'makePayment' in request.POST:
                ptm = Purchasehistroy()
                
                ptm.user = purchase
                ptm.total = purchase.total
                ptm.paid =request.POST['hispaid']
                ptm.remark= request.POST['remark']
                ptm.remaining = purchase.remaining - int(request.POST['hispaid'])
                purchase.remaining= purchase.remaining - int(request.POST['hispaid'])
                purchase.paid = purchase.paid + int(request.POST['hispaid'])
                purchase.save()
                ptm.save()
                return redirect('purchase')
        else:        
            return render(request,"root/purchase/purchasepay.html",{'purchase':purchase,'his':his})
    else:
        return redirect('login')


def payhistroy(request,saleid):
   
    sale = SaleTrans.objects.get(id=saleid)
    his = Salehistory.objects.filter(user=sale)
    rowHis = his

    if request.method =='POST':
        if 'makePayment' in request.POST:
            ptm = Salehistory()
            
            ptm.user = sale
            ptm.total = sale.total
            ptm.paid =request.POST['hispaid']
            ptm.remark= request.POST['remark']
            ptm.remaining = sale.remaining - int(request.POST['hispaid'])
            sale.remaining= sale.remaining - int(request.POST['hispaid'])
            sale.paid = sale.paid + int(request.POST['hispaid'])
            sale.save()
            ptm.save()
            return redirect('sales')
             
    return render(request,"root/sales/payhistroy.html",{'sale':sale,'his':his})


    


def EditSale(request):
    if request.method == 'POST':
        # if '' in request.POST:
        
        data = Stock.objects.get(batch_sr_no=request.POST['batch_no'])
        if data.qty ==0:
            messages.error(request, 'The Quantity of '+request.POST['stock_name']+' is zero')
            return redirect('sales')

        else:
            st = SaleTrans()
            st.batch_no = request.POST['batch_no']
            st.CustomerName = request.POST['customer_name']
            st.CustomerContact = request.POST['customer_contact']
            st.stock_name = request.POST['stock_name']
            st.size = request.POST['size']
            st.qty = request.POST['qty']
            st.price = request.POST['price']
            st.paid = request.POST['paid']
            st.remaining = request.POST['remaining']
            st.remark = request.POST['remark']
            st.total = request.POST['total']
            st.option = request.POST['option_method'] 
            st.save()

            his = Salehistory()
            his.user = st
            his.total=request.POST['total']
            his.paid =request.POST['paid']
            his.remaining =request.POST['remaining']
            his.remark =request.POST['remark']
            his.save()

            mystock = Stock.objects.get(batch_sr_no=request.POST['batch_no'])
            mystock.qty = int(mystock.qty) - int(request.POST['qty'])
            mystock.save()
            return redirect('sales')
    else:
        
        stocks = Stock.objects.all().order_by('-id')
        return render(request,'root/sales/editSales.html',{'stocks':stocks})


def getpdf(request,salehisid):
    st= Purchasehistroy.objects.get(id=salehisid)
    data = {'sale': st}
    # template = get_template('root/pdf/customer.html')
    return render(request, 'root/pdf/customer.html',data)

def sales(request):
    if  request.user.is_authenticated:
        st = SaleTrans.objects.all().order_by('-id')
        return render(request, 'root/sales/sales.html',{"st":st})
    else:
        return redirect('login')

# Create your views here.
def desktop(request):
    parsal = SaleTrans.objects.filter(option="Parsal").count()
    counter = SaleTrans.objects.filter(option="Counter").count()
    
    
    price=[]
    
    for i in range(1,13):
        data = SaleTrans.objects.filter(uploaded_at__month=i)
        value=0
        for j in data:
            value += j.paid
        price.append(value)

    return render(request,'root/desktop/desktop.html',{'parsal':parsal,'counter':counter,'price':price })


def purchase(request):
    if  request.user.is_authenticated:
        if request.method == 'POST':
            if Stock.objects.filter(batch_sr_no=request.POST['batch_sr_no']).exists():
                print('Query Availvbale')
                messages.error(request, 'The Batch No already Exist Try new one')
                return redirect('purchase')
            
            else:
                purchase=Purchase()
                stock= Stock()
                size =str(request.POST['size'])+" "+str(request.POST['unit'])
                purchase.vandor_name = request.POST['vandor_name']
                purchase.mobile_no = request.POST['mobile_no']
                purchase.batch_sr_no = request.POST['batch_sr_no']
                purchase.stock_name = request.POST['stock_name']
                purchase.vandor_price = request.POST['vandor_price']
                purchase.pack = request.POST['pack']
                purchase.size = size
                purchase.qty = request.POST['qty']
                purchase.selling_price = request.POST['selling_price']
                purchase.total = request.POST['total']
                purchase.remark = request.POST['remark']
                purchase.paid = request.POST['paid']
                purchase.remaining = request.POST['remaining']
                purchase.save()

                his = Purchasehistroy()
                his.user = purchase
                his.total=request.POST['total']
                his.paid =request.POST['paid']
                his.remaining =request.POST['remaining']
                his.remark =request.POST['remark']
                his.save()


                # stock 
                stock.batch_sr_no = request.POST['batch_sr_no']
                stock.stock_name = request.POST['stock_name']
                stock.vandor_price = request.POST['vandor_price']
                stock.pack = request.POST['pack']
                stock.size = size
                stock.qty = request.POST['qty']
                stock.selling_price = request.POST['selling_price']
                
                stock.save()
                
                return redirect("purchase") 

            
        else:
            purchase = Purchase.objects.all().order_by('-id')
            return render(request, 'root/purchase/purchase.html',{ 'purchases':purchase } ) 
    else:
        return redirect('login')   




# def purchaseEdit(request, purchaseid):
   
#     purchase = Purchase.objects.get(pk=purchaseid)
#     allPurchaseList = Purchase.objects.get(pk=purchaseid)
    
#     if request.method == 'POST':
    

#         purchase.vandor_name = request.POST['vandor_name']
#         purchase.mobile_no = request.POST['mobile_no']
#         purchase.batch_sr_no = request.POST['batch_sr_no']
#         purchase.stock_name = request.POST['stock_name']
#         # purchase.vandor_price = request.POST['vandor_price']
#         purchase.pack = request.POST['pack']
#         purchase.size = request.POST['size']
#         purchase.qty = request.POST['qty']
#         purchase.selling_price = request.POST['selling_price']
#         # purchase.total = request.POST['total']
#         # purchase.remark = request.POST['remark']
#         # purchase.paid = request.POST['paid']
#         # purchase.remaining = request.POST['remaining']
#         purchase.save()

        

#         stock = Stock.objects.get(batch_sr_no=request.POST['batch_sr_no'])
#         stock.batch_sr_no = request.POST['batch_sr_no']
#         stock.stock_name = request.POST['stock_name']
#         # stock.vandor_price = request.POST['vandor_price']
#         stock.pack = request.POST['pack']
#         stock.size = request.POST['size']
#         stock.qty = request.POST['qty']
#         # stock.selling_price = request.POST['selling_price']
#         stock.save()

#         return redirect('purchase')
#     else: 
#         return render(request, 'root/purchase/purchaseEdit.html',{'allPurchaseLists':allPurchaseList})

def saleImport(request):
    pass

def purchaseDelete(request,purchaseid):
    st = Purchase.objects.get(pk=purchaseid)
    stock = Stock.objects.get(batch_sr_no=st.batch_sr_no)
    
    if request.method == 'POST':
        st.delete()
        stock.delete()
        
        return redirect('purchase')
    else:
        return render(request, 'root/purchase/purchaseDelete.html',{'st':st})


 

def stock(request):
    if  request.user.is_authenticated:
        st= Stock.objects.all().order_by('-id')
        return render(request,'root/stock/stock.html',{'stocks':st})
    else:
        return redirect('login')

    

def expance(request):
    if  request.user.is_authenticated:
        expance=Expance()
        if request.method == "POST":
            
            expance.name = request.POST['name']
            expance.remark = request.POST['remark']
            expance.price = request.POST['price']
            expance.save()
            return redirect('expance')
        else:
            st = Expance.objects.all() 
            return render(request, "root/expance/expance.html",{"exp":st})
    else:
        return redirect('login')



def expanceEdit(request, expanceid):
   
    expance = Expance.objects.get(pk=expanceid)
    allPurchaseList = Expance.objects.get(pk=expanceid)
    
    if request.method == 'POST':
    

        expance.name = request.POST['name']
        expance.remark = request.POST['remark']
        expance.price = request.POST['price']
  
        expance.save()
        return redirect('expance')
    else: 
        return render(request, "root/expance/expanceEdit.html",{'allPurchaseLists':allPurchaseList})
        


    
def expanceDelete(request,expanceid):
    st = Expance.objects.get(pk=expanceid)
    if request.method == 'POST':
        st.delete()
        return redirect('expance')
    else:
        return render(request, "root/expance/expanceDelete.html",{'st':st})



# export 

def saleExport(request):
    if  request.user.is_authenticated:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sale.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'CustomerName',
            'CustomerContact',
            'batch_no',
            'stock_name',
            'size',
            'qty',
            'price',
            'total',
            'paid',
            'remaining',
            'remark',
            'option',
            'uploaded_at',
        ])

        users = SaleTrans.objects.all().values_list(
            'CustomerName',
            'CustomerContact',
            'batch_no',
            'stock_name',
            'size',
            'qty',
            'price',
            'total',
            'paid',
            'remaining',
            'remark',
            'option',
            'uploaded_at',
        )

        for user in users:
            writer.writerow(user)

        return response
    else:
        return redirect('login')

def purchaseExport(request):
    if  request.user.is_authenticated:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Purchase.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Vandor_name',
            'Mobile_no',
            'batch_sr_no',
            'Stock_name',
            'Vandor_price',
            'Pack',
            'Size',
            'Qty',
            'Selling Price',
            'Total',
            'Paid',
            'Remaining',
            'Remark',
            'Date',
        ])

        users = Purchase.objects.all().values_list(
            'vandor_name',
            'mobile_no',
            'batch_sr_no',
            'stock_name',
            'vandor_price',
            'pack',
            'size',
            'qty',
            'selling_price',
            'total',
            'paid',
            'remaining',
            'remark',
            'date',
        )
        for user in users:
            writer.writerow(user)

        return response
    else:
        return redirect('login')


def expanceExport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Expance.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'name',
        'remark',
        'price',
        'uploaded_at',
    ])

    users = Expance.objects.all().values_list(
        'name',
        'remark',
        'price',
        'uploaded_at',
    )
    for user in users:
        writer.writerow(user)

    return response



def stockExport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Stock.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'batch_sr_no',
        'stock_name',
        'vandor_price',
        'pack',
        'size',
        'qty',
        'selling_price',
        'date',
    ])

    users = Stock.objects.all().values_list(
        'batch_sr_no',
        'stock_name',
        'vandor_price',
        'pack',
        'size',
        'qty',
        'selling_price',
        'date',
    )
    for user in users:
        writer.writerow(user)

    return response
