from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced 
from .forms import CustomRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


#create your view here
class ProductView(View):
    def get(self,request):
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        return render(request,'app/home.html',
                      {'topwear':topwear,'bottomwear':bottomwear,'mobile':mobile,'laptop':laptop})

        
# def home(request):
#  return render(request, 'app/home.html')

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailsView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',
                      {'product':product})

def add_to_cart(request):
    user =request.user
    product_id = request.GET.get('prod_id')
    product =  Product.objects.get(id=product_id)
    Cart(user=user,product=product).save() 
    # return render(request, 'app/addtocart.html')
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
               tempamount = (p.quantity *p.product.selling_price)
               amount += tempamount
               totalamount = amount + shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')
# def plus_Cart(request):
#     if request.method == "GET":
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity += 1
#         c.save() 
#         amount = 0.0
#         shipping_amount = 70.0
#         total_amount = 0.0
#         cart_product = [p for p in Cart.objects.all() if p.user == request.user]   
#         for p in cart_product:
#                tempamount = (p.quantity *p.product.selling_price)
#                amount += tempamount
#                totalamount = amount + shipping_amount   
               
#         data = {
#                    'quantity':c.quantity,
#                    'amount':amount,
#                    'totalamount':totalamount
#                }
#         return JsonResponse(data)
     

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M') 
    elif data == 'Samsung' or data == 'Redme' or data == 'OnePlus'or data == 'I-Phone':
        mobiles = Product.objects.filter(category='M').filter(brand=data) 
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(selling_price__lt=10000) 
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(selling_price__gt=10000) 
        
        
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def topwear(request,data=None):
    if data == None:
            topwears = Product.objects.filter(category='TW') 
    elif data == 'mol' or data == 'Peter England' or data == 'Human'or data == 'Adidas' or data == 'Nike':
        topwears = Product.objects.filter(category='M').filter(brand=data) 
    elif data == 'below':
        topwears = Product.objects.filter(category='M').filter(selling_price__lt=10000) 
    elif data == 'above':
        topwears = Product.objects.filter(category='M').filter(selling_price__gt=10000) 
    return render(request, 'app/topwear.html',{'topwears':topwears})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation..!! Resigtered Successfully..!!')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
        
        
        
        
        
    

def checkout(request):
 return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self,request):
     form = CustomerProfileForm()
     return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,state=state,zipcode=zipcode,city=city)
            reg.save()
            messages.success(request,'Congratulations....!! Profile Updated Succcessfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
        