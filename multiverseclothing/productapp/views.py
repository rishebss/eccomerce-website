from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import json
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from itertools import chain
from operator import attrgetter
from .models import Product,Magazine,Shop,Cart,OrderCart,Like,OrderDesign
from django.contrib.auth.decorators import login_required
from .models import Selection
from django.conf import settings
from decimal import Decimal
from .models import UserProfile
import razorpay
from django.core.paginator import Paginator
from .forms import MagazineForm,ShopForm
from django.views import View

from django.http import JsonResponse, HttpResponseBadRequest

import logging
from django.http import Http404
from django.contrib import messages


def allproducts(request):
    tag = request.GET.get('tag')  # Get the tag from the query parameters
    products = Product.objects.all().order_by('-created_at')

    if tag:
        products = products.filter(tag=tag)  # Filter products by the selected tag

    tags = Product.objects.values_list('tag', flat=True).distinct()  # Get distinct tags

     # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'allproducts.html', {'products': products, 'tags': tags,'page_obj': page_obj})





def fetch_products(request):
    query = request.GET.get('tag', '').strip()
    title_query = request.GET.get('title', '').strip()

    products = Product.objects.all().order_by('-created_at')

    if query:
        products = products.filter(tag__icontains=query)

    if title_query:
        products = products.filter(title__icontains=title_query)

    products_data = [
        {
            'id': product.product_id,
            'name': product.title,
            'photo': product.image.url,
            'size': product.size,
            'price': product.price,
        } for product in products
    ]

    return JsonResponse({'products': products_data})

def toggle_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Load the JSON body
        product_id = data.get('product_id')  # Get product_id from JSON
        
        product = get_object_or_404(Product, id=product_id)
        like, created = Like.objects.get_or_create(user=request.user, product=product)

        if not created:
            # If the user already liked it, unlike it
            like.delete()
            return JsonResponse({'liked': False})

        return JsonResponse({'liked': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def liked_products(request):
    if request.user.is_authenticated:
        liked_product_ids = Like.objects.filter(user=request.user).values_list('product_id', flat=True)
        liked_products = Product.objects.filter(id__in=liked_product_ids)
    else:
        liked_products = []

    return render(request, 'likes.html', {'liked_products': liked_products})

def category_view(request, tag):
    products = Product.objects.filter(tag=tag).order_by('-created_at')
    return render(request, 'category.html', {'products': products, 'tag': tag})


def details(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    liked_products = Like.objects.filter(user=request.user).values_list('product', flat=True)
    colors = product.color.split(',')
    sizes = product.size.split(',')
    color_map = {
        'Green': '#008000',
        'Red': '#FF0000',
        'White': '#FFFFFF',
        'Black': '#000000',
        'Brown': '#A52A2A',
        'Blue': '#0000FF',
        'Lavender': '#E6E6FA',
        'Grey': '#808080',
        'Orange': '#FFA500',
        'Cream': '#FFFDD0',
        'Pink': '#FFC0CB',
        'Mauve': '#E0B0FF',
        'Yellow': '#FFFF00',
        'Tan': '#D2B48C',
    }
    
    color_codes = [(color, color_map.get(color, '#000000')) for color in colors]
    return render(request, 'details.html', {'product': product, 'color_codes': color_codes,'sizes':sizes,'liked_products':liked_products})


@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        selected_color = request.POST['color']
        selected_size = request.POST['size']
        selection = Selection.objects.create(
            user=request.user,
            product=product,
            selected_color=selected_color,
            selected_size=selected_size
        )
        return redirect('productapp:purchase', selection_id=selection.id)

    return render(request, 'product_detail.html', {'product': product})




def save_details(request):
    if request.method == "POST":
        recipient_name = request.POST.get('recipient_name')
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        city = request.POST.get('city')

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Update UserProfile with the form data
        user_profile.recipient_name = recipient_name
        user_profile.shipping_address = shipping_address
        user_profile.phone_number = phone_number
        user_profile.state = state
        user_profile.city = city
        user_profile.details_saved = True
        user_profile.save()

        messages.success(request, 'Details saved successfully.')
        return redirect('productapp:account')

    return redirect('purchase')



def account(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if not user_profile:
        user_profile = None
    return render(request, 'accounts.html', {'user_profile': user_profile})

def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        recipient_name = request.POST.get('recipient_name')
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Update UserProfile with the form data
        user_profile.recipient_name = recipient_name
        user_profile.shipping_address = shipping_address
        user_profile.phone_number = phone_number
        user_profile.state = state
        user_profile.city = city
        user_profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('productapp:account')

    return render(request, 'edit.html', {'user_profile': user_profile})


def uploadmagazine(request):
    if request.method == 'POST':
        form = MagazineForm(request.POST, request.FILES)
        files = request.FILES.getlist('pic')

        if len(files) > 15:
            messages.error(request, 'You cannot upload more than 15 images.')
        elif form.is_valid():
            for f in files:
                Magazine.objects.create(pic=f)
            messages.success(request, 'Magazine uploaded successfully.')
            return redirect('productapp:uploadmagazine')  # Redirect to clear the form
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MagazineForm()

    return render(request, 'uploadmagazine.html', {'form': form})

def magazine(request):
    magazines = Magazine.objects.all()
    return render(request, 'magazine.html', {'magazines': magazines})

# def shop(request):
#     category = request.GET.get('category', 'all')
#     if category == 'all':
#         shop = Shop.objects.all()
#     else:
#         shop = Shop.objects.filter(cat=category)
#     return render(request, 'shopproduct.html', {'shop': shop})

def shop(request):
    category = request.GET.get('category', 'all')
    gen = request.GET.get('gen', 'all')

    # Initial QuerySet
    shop = Shop.objects.all().order_by('-created_at')

    # Filter by category
    if category != 'all':
        shop = shop.filter(cat=category)

    # Filter by gen
    if gen != 'all':
        shop = shop.filter(gen=gen)

    return render(request, 'shopproduct.html', {'shop': shop})


def fetch_shop(request):
    category = request.GET.get('category', 'all')
    gen = request.GET.get('gen', None)

    # Start with all products
    shop = Shop.objects.all().order_by('-created_at')

    # Apply the gender filter if provided
    if gen:
        shop = shop.filter(gen=gen)

    # Apply the category filter if not 'all'
    if category != 'all':
        shop = shop.filter(cat=category)

    # Prepare the product data for JSON response
    shop_data = [
        {
            'id': product.id,
            'name': product.name,
            'photo': product.photo1.url,
            'size': product.size,
            'price': product.price,
        } for product in shop
    ]

    return JsonResponse({'shop': shop_data})



def shopdetail(request, id):
    product = get_object_or_404(Shop, id=id)
    return render(request, 'shopdetail.html', {'product': product})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        shop_item = get_object_or_404(Shop, id=product_id)

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=shop_item)

        if created:
            messages.success(request, 'Item added to cart!')
        else:
            messages.info(request, 'Item already in cart!')

    return redirect('productapp:view_cart')


@login_required
def view_cart(request):
    # Retrieve the cart items linked to the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(float(item.product.price) for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('productapp:view_cart')


def purchase(request, selection_id):
    selection = get_object_or_404(Selection, id=selection_id)
    user_profile = UserProfile.objects.filter(user=request.user).first()

    if request.method== "POST":
        amount_str=request.POST.get("amount")

        if amount_str is None:
            print("Amount is missing from POST data")
            return HttpResponseBadRequest("Amount is missing")

        try:
            amount = int(amount_str) * 100
        except ValueError:
            print("Invalid amount format")
            return HttpResponseBadRequest("Invalid amount format")
        client = razorpay.Client(auth=('rzp_test_dTWp25pBQ5jW81', 'Sg6ymJfWNf4atGBsqXhuaALE'))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        design=OrderDesign(user=request.user,info=user_profile,design_name=selection.product.title,amount=amount_str,designcolor=selection.selected_color,designsize=selection.selected_size,payment_id=payment['id'])
        design.save()

        return render(request, "purchase.html", {'payment': payment})

    return render(request, 'purchase.html', {'selection': selection, 'user_profile': user_profile})

@never_cache
def checkout_summary(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(float(item.product.price) for item in cart_items)
    user_profile = UserProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        amount_str = request.POST.get("amount")
        
        if amount_str is None:
            print("Amount is missing from POST data")
            return HttpResponseBadRequest("Amount is missing")

        try:
            amount = int(amount_str) * 100
        except ValueError:
            print("Invalid amount format")
            return HttpResponseBadRequest("Invalid amount format")

        client = razorpay.Client(auth=('rzp_test_dTWp25pBQ5jW81', 'Sg6ymJfWNf4atGBsqXhuaALE'))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        # Create OrderCart entries for each item
        for item in cart_items:
            OrderCart.objects.create(
                user=request.user,
                info=user_profile,
                product_name=item.product.name,
                color=item.product.color,
                size=item.product.size,
                amount=item.product.price,
                payment_id=payment['id']
            )
        
        return render(request, "summary.html", {'payment': payment})

    return render(request, 'summary.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'user_profile': user_profile
    })

@never_cache
@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        payment_id = ""
        for key, val in a.items():
            if key == "razorpay_order_id":
                payment_id = val
                break
        
        # Update OrderCart status
        user_order = OrderCart.objects.filter(payment_id=payment_id).first()
        if user_order:
            user_order.paid = True
            user_order.save()

            # Retrieve the cart items and delete products
            cart_items = Cart.objects.filter(user=user_order.user)
            for item in cart_items:
                # Deleting product by name or another unique attribute
                Shop.objects.filter(name=item.product.name).delete()
                item.delete()  # Also remove the cart items

    response = render(request, "success.html")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    return response

@csrf_exempt
def designsuccess(request):
    if request.method == "POST":
        a = request.POST
        payment_id=""
        for key,val in a.items():
            if key == "razorpay_order_id":
                payment_id=val
                break
        user = OrderDesign.objects.filter(payment_id=payment_id).first()
        user.paid = True
        user.save()
    return render(request, "designsuccess.html")



def userorders(request):
    shop_orders = OrderCart.objects.filter(user=request.user, paid=True)
    design_orders = OrderDesign.objects.filter(user=request.user, paid=True)
    
    # Combine both querysets and sort by 'created_at' in reverse order (newest first)
    all_orders = sorted(
        chain(shop_orders, design_orders), 
        key=attrgetter('created_at'), 
        reverse=True
    )

    return render(request, 'orders.html', {'orders': all_orders})

def about(request):
    return render(request,"about.html")



# admin dashboard functions below

def faculty(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')

        if name == 'multiverseadmin' and password == 'multiverse@2024':
            return redirect('productapp:dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, "cred.html")

def dashboard(request):
    user_count = User.objects.count()

    # Count total orders for both OrderCart and OrderDesign
    cart_order_count = OrderCart.objects.filter(paid=True).count()
    design_order_count = OrderDesign.objects.filter(paid=True).count()

    # Total orders
    total_orders = cart_order_count + design_order_count

    # Get the current user's orders for both shop products and design products
    cart_orders = OrderCart.objects.filter(paid=True)
    design_orders = OrderDesign.objects.filter(paid=True)

    # Add the order type to distinguish between OrderCart and OrderDesign
    for order in cart_orders:
        order.order_type = "OrderCart"
    for order in design_orders:
        order.order_type = "OrderDesign"

    # Combine the two querysets and order by 'created_at' field in descending order
    all_orders = sorted(
        chain(cart_orders, design_orders),
        key=lambda order: order.created_at,
        reverse=True
    )

    cart_revenue = OrderCart.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0
    design_revenue = OrderDesign.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0

    # Total paid orders
    total_paid_orders = cart_order_count + design_order_count

    # Total revenue (sum of both cart and design revenues)
    total_revenue = float(cart_revenue) + float(design_revenue)

    return render(request, 'dashboard.html', {
        'orders': all_orders,
        'user_count': user_count,
        'total_orders': total_orders,
        'total_paid_orders': total_paid_orders,
        'total_revenue': total_revenue
    })

def admin_product_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'adminallproducts.html', {'products': products})

def admin_shop_view(request):
    shops = Shop.objects.all().order_by('-created_at')
    return render(request, 'adminallshops.html', {'shops': shops})

def upload_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but manually set the 'cat' field
            shop_instance = form.save(commit=False)
            shop_instance.cat = request.POST.get('cat', '')  # Get the 'cat' value from POST data
            shop_instance.save()
            return redirect('productapp:shop')
    else:
        form = ShopForm()
    return render(request, 'uploadshop.html', {'form': form})


def uploadproduct(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        title = request.POST.get('title')
        product_id = request.POST.get('product_id')
        tag = request.POST.get('tag')
        price = request.POST.get('price')
        color = request.POST.get('color')
        size = request.POST.get('size')

        product = Product(
            image=image,
            title=title,
            product_id=product_id,
            tag=tag,
            price=price,
            color=color,
            size=size

        )
        product.save()

        return redirect('productapp:admin_product_view')

    return render(request, 'uploadproducts.html', )


def admin_order_detail(request, order_id, order_type):
    if order_type == "OrderCart":
        order = get_object_or_404(OrderCart, id=order_id)
    elif order_type == "OrderDesign":
        order = get_object_or_404(OrderDesign, id=order_id)
    
    context = {
        'order': order,
        'order_type': order_type,
    }
    return render(request, 'adminorderdetail.html', context)