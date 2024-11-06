from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


from .form import OrderCreationForm, ProductCreationForm
from userapp.models import Customers, Orders, Product, Product_Image
from vendors.decorators import vendors_only,unauthenticated_user
from allauth.account.decorators import verified_email_required

# @login_required(login_url="vendor-login")
# @vendors_only
@verified_email_required
def index(request):

    return render(request,"adminapp/index.html")


@login_required(login_url="vendor-login")
@vendors_only
def sales(request):
    user = request.user
    if user.is_vendor:
        sales = Orders.objects.filter(payment="PAID",order_product__vendor=user,)
    else:
        sales = Orders.objects.filter(payment="PAID")
    context = {"sales":sales}

    return render(request,"adminapp/sales.html",context)

@login_required(login_url="vendor-login")
@vendors_only
def purchase(request):

    return render(request,"adminapp/index.html")


@login_required(login_url="vendor-login")
@vendors_only
def expence(request):

    return render(request,"adminapp/index.html")


@login_required(login_url="vendor-login")
@vendors_only
def payment(request):

    return render(request,"adminapp/index.html")

@login_required(login_url="vendor-login")
@vendors_only
def daybook(request):

    return render(request,"adminapp/index.html")

@login_required(login_url="vendor-login")
@vendors_only
def ledger(request):

    return render(request,"adminapp/index.html")

@login_required(login_url="vendor-login")
@vendors_only
def finalaccount(request):

    return render(request,"adminapp/index.html")


@login_required(login_url="vendor-login")
@vendors_only
def customer(request):

    return render(request,"adminapp/index.html")

@login_required(login_url="vendor-login")
@vendors_only
def supplier(request):

    return render(request,"adminapp/index.html")

@login_required(login_url="vendor-login")
@vendors_only
def product(request):
  
    if request.user.is_vendor:
        product = Product.objects.filter(vendor = request.user)
    else:
        product = Product.objects.all()
    form = ProductCreationForm
    
    
    if request.method == 'POST':
        form = ProductCreationForm(request.POST ,request.FILES)
        print(request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.vendor = request.user
            form.save()
            return redirect('product')
        else:
            return HttpResponse("file cant upload")

    
    context= {"form":form,"product":product}
    return render(request,"adminapp/product.html",context)

@login_required(login_url="vendor-login")
@vendors_only
def product_update(request,pk):
    order = get_object_or_404(Product,id=pk)
    form = ProductCreationForm(instance=order)
    if request.method == 'POST':
        print(request.POST)
        form = ProductCreationForm(request.POST, request.FILES,instance=order)
        if form.is_valid():
            form.save()
        return redirect('product')
    context = {'form':form}
    return render (request,"adminapp/product_update.html",context)

@login_required(login_url="vendor-login")
@vendors_only
def product_delete(request,pk):
    order = get_object_or_404(Product,id=pk)
    # if request.method == "POST":
    order.delete()
    return redirect('product')

	


@login_required(login_url="vendor-login")
@vendors_only
def setting(request):

    return render(request,"adminapp/index.html")


@login_required(login_url="vendor-login")
@vendors_only
def order(request):
    user = request.user

    if user.is_vendor:
        order = Orders.objects.filter(order_product__vendor=user)
    else:
        order = Orders.objects.all()
    form = OrderCreationForm(user=user)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('order')
        else:
            return HttpResponse("file cant upload") 
    context= {"form":form,"order":order}
    return render(request,"adminapp/order.html",context)


@login_required(login_url="vendor-login")
@vendors_only
def order_update(request,pk):
    order = get_object_or_404(Orders,id=pk)
    form = OrderCreationForm(instance=order,user=request.user)


    if request.method == 'POST':
        form = OrderCreationForm(request.POST, request.FILES,instance=order,user=request.user)
        if form.is_valid():

            form.save()
        return redirect('order')
    context = {'form':form}
    return render (request,"adminapp/order_update.html",context)

@login_required(login_url="vendor-login")
@vendors_only
def order_delete(request,pk):
    print(pk)
    order = get_object_or_404(Orders,id=pk)
    # if request.method == "POST":
    order.delete()
    return redirect('order')


@login_required(login_url="vendor-login")
@vendors_only
def product_as_per_customer(request,pk):
    
    orders = Orders.objects.filter(order_by=pk)
    print(orders)
    context ={"orders":orders}

    return render(request,"adminapp/customer_order.html",context)


