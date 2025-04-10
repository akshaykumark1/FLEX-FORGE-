# myapp/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .forms import *
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt




def home(request):
    product=Product.objects.all()
    return render(request, 'base.html',{'product':product})
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            if  user.is_superuser:
                return redirect('admin')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'signin.html')
def signup(request):
    if request.method == 'POST':  
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Corrected line to use create_user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('signin')  

    return render(request, "signup.html")



def userlogout(request):
    request.session.flush()
    return render(request, 'base.html')









def orders(request):
    return render(request, 'user/orders.html')  
def help(request):
    return render(request, 'user/help.html') 



def product_buy(request):
    products = Product.objects.all()

    return render(request, 'user/product_buy.html', {'products': products})

def wheretobuy(request):
    return render(request,'user/wheretobuy.html')

def buy_now(request,product_id):    
    return render(request,'buy_now.html')



##########################admin#####################

def admin(request):
    context = {
        'products': Product.objects.all(),
        'orders': Order.objects.all(),
        'users': User.objects.all(),
        'categories': Category.objects.all(),
        'addresses': Address.objects.all(),
        'wishlist': Wishlist.objects.all(),
        'products_count': Product.objects.count(),
        'orders_count': Order.objects.count(),
        'users_count': User.objects.count(),
        'categories_count': Category.objects.count(),
    }
    return render(request, 'admin/admin.html', context)





def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProductForm()
    return render(request, 'admin/add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin')

# Order Views
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin')

# User Views
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin')

# Category Views
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

################################################################################

def search1(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()  # Get the search term
        category = request.POST.get('category', '')  # Get the selected category (if any)
        
        # Filter products based on the search term and category
        results = Product.objects.all()
        
        if searched:
            results = results.filter(title__icontains=searched)
        
        if category:
            # Dynamically filter based on the category field
            category_filter = {f"{category}": True}
            results = results.filter(**category_filter)

        return render(request, 'user/search.html', {'searched': searched, 'category': category, 'results': results})
    
    # Render the empty search page for GET requests
    return render(request, 'user/search.html', {'searched': '', 'category': '', 'results': []})

def product_display(request):
    products = Product.objects.all()
    
    return render(request, 'user/product_buy.html', {'products': products})
#_---------------------------cart-------------------------------#

# Add to cart functionality
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('product_not_found')  

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1, 'price': product.price}  # ✅ Fixed: 'price' instead of 'totalprice'
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.price = cart_item.quantity * cart_item.product.price
            cart_item.save()
        
        return redirect('cart')
    else:
        return redirect('signin')

# View cart (standalone template)
def Cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_item_count = cart_items.count()
    return render(request, 'user/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart_item_count': cart_item_count})



def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return redirect('cart')
    
    cart_item.calculate_price()
    cart_item.save()
    return redirect('cart')

# Remove from cart
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')



# For implementing Add to Cart button in product detail page
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)  # Changed from filter() to get_object_or_404()
    cart_product_ids = []
    
    if request.user.is_authenticated:
        cart_product_ids = list(Cart.objects.filter(user=request.user).values_list('product_id', flat=True))
        cart_item_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0 
    
    context = {
        'product': product,
        'cart_item_count': cart_item_count,
        'cart_product_ids': cart_product_ids
    }
    return render(request, 'user/product_detail.html', context)

#----------------------------wishlist------------------------------------------------------#

def wishlist(request):
    
    wishlist_items=Wishlist.objects.filter(user=request.user)
    return render(request, 'user/wishlist.html',{'wishlist_items':wishlist_items}) 


def addtowishlist(request, product_id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.title} added to your wishlist'
        })
    
    return redirect('home') 
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')

def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'user/wishlist.html', context)   



def account(request):
    return render(request, 'accounts/account.html')

def address(request):
    return render(request,'accounts/address.html')

def security(request):
    return render(request,'accounts/security.html')




# payment section

def index(request):
    return render(request, "index.html")

def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        order_id = razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()

        return render(
            request,
            "index.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,

            },
        )

    return render(request, "index.html")




@csrf_exempt
def callback(request):

    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status}) 
            # or return redirect(function name of callback giving html page)
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status}) 
            # or return redirect(function name of callback giving html page)
    else:
     payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
     provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")

     order = Order.objects.get(provider_order_id=provider_order_id)
     order.payment_id = payment_id
     order.status = PaymentStatus.FAILURE
     order.save()

    return render(request, "callback.html", context={"status": order.status}) 
    # or return redirect(function name of callback giving html page)