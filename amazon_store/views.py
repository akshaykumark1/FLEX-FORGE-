# myapp/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User



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


def admin(request):
    return render(request, 'admin.html')









def orders(request):
    return render(request, 'user/orders.html')  
def help(request):
    return render(request, 'user/help.html') 



def product_buy(request):
    products = Product.objects.all()

    return render(request, 'user/product_buy.html', {'products': products})

def wheretobuy(request):
    return render(request,'user/wheretobuy.html')

def buy_now(request):
    return render(request,'buy_now.html')





#-------------------seller__-------------------------

# def slogout(request):
#     request.session.flush()
#     return render(request, 'base.html')  # A custom template after logout


# @login_required(login_url='sellerin')
# def Add_product(request):
#     return render(request, 'seller/selleradd.html')


# def selleradd(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         price = request.POST.get('price')
#         category = request.POST.get('category')
#         image = request.FILES.get('image')
#         description = request.POST.get('description')

#         # Check if all required fields are provided
#         if not title or not price or not category or not image or not description:
#             messages.error(request, "All fields are required!")
#             return render(request, 'seller/selleradd.html')

#         # Create and save product object
#         product = Product(
#             title=title,
#             price=price,
#             category=category,
#             image=image,
#             description=description
#         )
#         product.save()

#         # Success message
#         messages.success(request, "Product added successfully!")
#         return redirect('sellerview')
    
#     # If GET request, render the page with empty form
#     return render(request, 'seller/selleradd.html')


# def sellerview(request):
#     products = Product.objects.all()
#     return render(request, 'seller/seller.html', {'products': products})



# def edit_product(request, id):
#     product = Product.objects.get(id=id)
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         price = request.POST.get('price')
#         category = request.POST.get('category')
#         image = request.FILES.get('image')
#         description = request.POST.get('description')


#         # Check if all required fields are provided
#         if not title or not price or not category or not description:
#             messages.error(request, "All fields are required!")
#             return render(request, 'seller/edit.html', {'product': product})

#         # Update and save product object
#         product.title = title
#         product.price = price
#         product.category = category
#         if image:
#             product.image = image
#         product.description = description
#         product.save()

#         # Success message
#         messages.success(request, "Product updated successfully!")
#         return render(request, 'seller/seller.html')
    
#     # If GET request, render the page with empty form
#     return render(request, 'seller/edit.html', {'product': product})

# def delete_view(request, id):
#     product = Product.objects.filter(pk=id).first()  # Get product by ID (or None if not found)
#     if product:
#         product.delete()  # Delete the product
#         messages.success(request, "Product deleted successfully!")  # Optional success message
#     return redirect('sellerview')

# #------------------------------------------------------------------------------#




def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()  # Get the search term
        category = request.POST.get('category', '')  # Get the selected category (if any)
        
        # Filter products based on the search term and category
        results = Products.objects.all()
        
        if searched:
            results = results.filter(name__icontains=searched)
        
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
@login_required
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
@login_required
def Cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_item_count = cart_items.count()
    return render(request, 'user/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart_item_count': cart_item_count})



@require_POST
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
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
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
    return render(request, 'user/wishlist.html') 
def addtowishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is already in wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    # For AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.title} added to your wishlist'
        })
    
    return redirect('product_buy')

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')

@login_required
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
