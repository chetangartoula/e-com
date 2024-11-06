
from django.http import Http404, HttpResponse
import json
from django.conf import settings
from django.core.mail import send_mail
from django.utils.text import slugify

from userapp.recentview import RecentView
from .cart import Cart
from django.db.models import Q,Min,Max,Avg
from django.shortcuts import render,redirect, resolve_url
from .models import Banner, Brand, Color, Customers, Events, Main_Category, Orders, Product_Image, Category, Slider,Product, Sub_Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .whishlist import Whishlist
from django.contrib.auth import authenticate, logout,login
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from allauth.account.forms import SignupForm
from django.template.loader import render_to_string
from django.contrib import messages




def index(request):
    form = SignupForm
    products = Product.objects.all()
    pro = products[:10]
    evt = Events.objects.all().first()
    sli = Slider.objects.all().order_by("-id")[:3]
    top_banner = Banner.objects.all().first()

    recent_product_id = request.session.get("recent_view")

    p_id = []
    if recent_product_id is not None:
        for key  in recent_product_id:
            p_id.append(key)
    recent_product_view = products.filter(id__in = p_id)
    
    
    
    on_sale = []
    Featured =[]
    Top_selling =[]
    
    for product in products:
        if "Featured" in str(product.product_collection):
            Featured.append(product)


        elif "On sale" in str(product.product_collection):
            on_sale.append(product)

        elif "Top selling" in str(product.product_collection):
            Top_selling.append(product)
    sale_product = products.filter(pro_collection="On sale").order_by("-updated_at")[:2]    
    offer_product = products.filter(pro_collection="Deals").latest("updated_at")
    
    
    
    
   

    context={"slider":sli,"product":on_sale,"Featured":Featured,
    "top_banner":top_banner,"form":form,"events":evt,"recent_product_view":recent_product_view,
    "product":pro,"offer_product": offer_product,"sale_product":sale_product,
    "onsale":on_sale,"Topselling":Top_selling,}

    return render(request,"userapp/index.html",context)

def category_page(request,cat_slug):
    product = Product.objects.filter(pro_catagory__slug=cat_slug)
    context={"products":product,"slug":cat_slug,}
    return render(request,"userapp/category_page.html",context)


def productdetails(request,slug):
    prod = get_object_or_404(Product,slug=slug)
    
   
    cart = RecentView(request)

    cart.add(product=prod)
    

    varients = prod.varients.all()
    
   
    context={"product":prod,"varients":varients,}
    return render(request,"userapp/product_details.html",context)


def wishlist_add(request, id):
    wishlist = Whishlist(request)
    product = Product.objects.get(id=id)
    wishlist.add(product=product)
    return redirect("index")

def wishlist_item_clear(request, id):
    wishlist = Whishlist(request)
    product = Product.objects.get(id=id)
    wishlist.remove(product)
    return redirect("wishlist_detail")

def wishlist_detail(request):
    return render(request,"userapp/wishlist.html")


@csrf_exempt
def shop_page(request):
    color = request.GET.get("color")
    cate_ = request.GET.get("category")
    sub_cate_ = request.GET.get("sub_category")
    main_cate_ = request.GET.get("main_category")
    product_slug = request.GET.get("product",None)
    
    form = SignupForm
    
    cat = Category.objects.all()[:10]
    brands = Brand.objects.all()
    colors = Color.objects.all()
    all_products = Product.objects.all().order_by("-updated_at")
    minimum_price = all_products.aggregate(Min("price"))
    maxmimum_price = all_products.aggregate(Max("price"))
    avg_price = all_products.aggregate(Avg("price"))

    if main_cate_ is not None and main_cate_ is not "":
        all_products = all_products.filter(pro_catagory__sub_category__main_category__slug=slugify(main_cate_))


    if product_slug is not None and product_slug is not "":
        all_products = all_products.filter(slug=slugify(product_slug))

 
    if color is not None:
        all_products = all_products.filter(color__id=color)
    
    if cate_ is not None:
        all_products = all_products.filter(pro_catagory__slug=cate_)

    if sub_cate_ is not None:
        all_products = all_products.filter(pro_catagory__sub_category__slug=sub_cate_)



    page_num = request.GET.get('page', 1)
    paginator = Paginator(all_products, 10)
    
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {"products":page_obj,"Category":cat,"avg_price":avg_price,"brands":brands,"minimum_price":minimum_price,"maxmimum_price":maxmimum_price,"colors":colors,"form":form}
    return render(request,"userapp/shop.html",context)




def search_result(request):
    query =request.GET.get("term")
    result = []
    obj = Product.objects.filter(pro_name__icontains=query)
    for res in obj:
        
        result.append(res.id)
        result.append(res.pro_name)
    
    
    return JsonResponse(list(result),safe=False)


@csrf_exempt
def filter_result(request):
    
    
    # maximum_price = 
    if request.method == "POST":
       
        brand = request.POST.getlist("brands[]")
        categories = request.POST.getlist("category[]")
        

        allProducts = Product.objects.all().order_by('-id').distinct()

        if len(categories) > 0:
            allProducts = allProducts.filter(pro_catagory__id__in=categories).distinct()
            print(allProducts)

        if len(brand) > 0:
            allProducts = allProducts.filter(pro_brnd__id__in=brand).distinct()


        page_num = request.GET.get('page', 1)
        paginator = Paginator(allProducts, 10)
    
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)


        t = render_to_string('userapp/ajax/product-list.html', {'product': page_obj})
        
        
        return JsonResponse({"data":t},safe=False)
    


def cart_add(request, pk):
    cart = Cart(request)
    product = Product.objects.get(id=pk)
    cart.add(product=product)
    r = request.session["cart"]
    data = render_to_string("userapp/ajax/cart_mini.html",{"r":r})

    return JsonResponse({"message": len(request.session['cart']),"data":data})


def item_clear(request, id):
    next_page = request.GET.get("next")
    print(next_page)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    messages.success(request,f'Your {product} is clear now !!!')

    url = resolve_url(next_page)
    print(url)

    return redirect(url)

@csrf_exempt
def item_increment(request, id):
    if request.method != "POST" :
        return JsonResponse("Cant acess ",safe=False)

    qty = json.loads(request.body)
    qty=qty.get("produc_qty")
    cart = Cart(request)
   
    product = Product.objects.get(id=id)
    cart.add(product=product,quantity=qty)

    new_item = request.session["cart"].get(str(id))
    total_price = int(new_item["price"])*int(new_item["quantity"])
    messages.success(request,"Product added")
    return JsonResponse({"total_price":total_price},safe=False)

@csrf_exempt
def item_decrement(request, id):
    if request.method != "POST" :
        return JsonResponse("Cant acess ",safe=False)
    qty = json.loads(request.body)
    qty=qty.get("produc_qty")
    cart = Cart(request)

    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    
    new_item = request.session["cart"].get(str(id))
    total_price = int(new_item["price"])*int(new_item["quantity"])


    return JsonResponse({"total_price":total_price},safe=False)


def cart_clear(request):
    
    cart = Cart(request)
    cart.clear()
    messages.success(request,f'Your Cart is clear now !!!')
    return redirect("cart_detail")


def cart_detail(request):
   

    return render(request, 'userapp/cart_detail.html')


@login_required(login_url="customerlogin")
@csrf_exempt
def place_order(request):
    if request.method =="POST":
        data = json.loads(request.body)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        company_name = data.get("company_name")
        country = data.get("country")
        address1 = data.get("address1")
        address2= data.get("address2")
        city = data.get("city")
        state = data.get("state")
        postcode = data.get("postcode")
        phonenumber =data.get("phonenumber")
        email = data.get("email")
        note = data.get("notes")

        cart  = request.session["cart"]
        user = cart.get("userid")
        
        if user is None:
            obj =  Customers.objects.create(user =request.user,first_name = first_name,last_name=last_name,email=email,address1=address1,address2=address2,city=city,zip_code= postcode,country=country,nearest_location =state,note=note,
               contact=phonenumber )
            obj.is_customer = True
            obj.save()
            for key,value in cart.items():
                product_id = (value['product_id'])
                prodct_qty = float((value['quantity']))
                product_price = float(value['price'])        
                total_ammount = prodct_qty * product_price
                x = Orders.objects.create(order_by= request.user,order_product_id=product_id,total_amount=total_ammount)
                x.save()
            subject = 'welcome to GFG world'
            message = f'Hi {first_name + last_name}, thank you for purchase the product.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )


        
       
        return JsonResponse("this is me ",safe=False)
    return render(request, "userapp/checkout.html")





def wat_on_sale(request):
    return HttpResponse("<h1> Site will lunching soon </h1>")


def how_to_order(request):
    return HttpResponse("<h2> Site will lunching soon </h2>")


def faqs(request):
    return HttpResponse("<h2> Site will lunching soon </h2>")


def user_logout(request):
    messages.info(request,f"Good by {request.user.username}")
    logout(request)
   
    return redirect("index")


def customerregister(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        
        if form.is_valid():
            print("form_valid")
            form.save(request)
            messages.success(request,f'Your account has been created. You can log in now!')
            return redirect('customerlogin')
        else:
            for i, (key, value) in enumerate(form.errors.items()):
              messages.success(request,value[0]) 
            return redirect("customerlogin")
    else:
        raise Http404


def customerlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'Welcome Back {user.username} !!!')
            return redirect('/')
        else:
            messages.error(request,'Credentials not matched')
            return redirect('customerlogin')
    else:
        return render(request,"userapp/components/auth/signup-login2.html")



def retail_shop(request):
    color = request.GET.get("color")
    cate_ = request.GET.get("category")
    sub_cate_ = request.GET.get("sub_category")
    main_cate_ = request.GET.get("main_category")
    product_slug = request.GET.get("product",None)
    
    form = SignupForm
    
    cat = Category.objects.all()[:10]
    brands = Brand.objects.all()
    colors = Color.objects.all()
    all_products = Product.objects.filter(is_retail=True).order_by("-updated_at")
    minimum_price = all_products.aggregate(Min("price"))
    maxmimum_price = all_products.aggregate(Max("price"))
    avg_price = all_products.aggregate(Avg("price"))

    if main_cate_ is not None and main_cate_ is not "":
        all_products = all_products.filter(pro_catagory__sub_category__main_category__slug=slugify(main_cate_))


    if product_slug is not None and product_slug is not "":
        all_products = all_products.filter(slug=slugify(product_slug))

 
    if color is not None:
        all_products = all_products.filter(color__id=color)
    
    if cate_ is not None:
        all_products = all_products.filter(pro_catagory__slug=cate_)

    if sub_cate_ is not None:
        all_products = all_products.filter(pro_catagory__sub_category__slug=sub_cate_)



    page_num = request.GET.get('page', 1)
    paginator = Paginator(all_products, 10)
    
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {"products":page_obj,"Category":cat,"avg_price":avg_price,"brands":brands,"minimum_price":minimum_price,"maxmimum_price":maxmimum_price,"colors":colors,"form":form}
    return render(request,"userapp/vendor_shop.html",context)