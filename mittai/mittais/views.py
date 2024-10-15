from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Movie, Cart, CartItem, Order, Category, Product,  TopBrands
from .models import NewLaunch
from .payment_gateway import process_payment  # Make sure this is defined elsewhere
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def home(request):
    movies = Movie.objects.all()
    categories = Category.objects.filter(is_active=True)
    TopBrandss = TopBrands.objects.all()
    return render(request, "index.html", {'movies': movies, 'categories':categories, 'TopBrandss': TopBrandss})

def Topbrands(request, id):
    
    topbrand = get_object_or_404(TopBrands, id=id)
    
    # Render the template with the topbrand data
    return render(request, 'TopBrand.html', {'topbrand': topbrand})
# myapp/views.py




def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)  # Log the user in
                messages.success(request, "Login successful!")
                return redirect('home')  # Ensure 'home' is a valid URL name
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "login.html", {'form': form})





def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to login page
    else:
        form = RegistrationForm()
    
    return render(request, "sign_up.html", {'form': form})
    
    
def mittaidetails(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "mittaidetails.html", {'movie': movie})
def NewLaunch(request, NL):
    NewLaunchs = get_object_or_404(Movie, NL=NL)
    return render(request, "NewLaunch.html", {'NewLaunch': NewLaunchs})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'categorydetails.html', {'category': category, 'products': products})

def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'category_list.html', {'categories': categories})

def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[movie_id] = cart.get(movie_id, 0) + 1
        request.session['cart'] = cart

    messages.success(request, f"{movie.title} has been added to your cart!")
    return redirect('home')

def remove_from_cart_view(request, movie_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, movie_id=movie_id)
            cart_item.delete()
            messages.success(request, f"{cart_item.movie.title} has been removed from your cart.")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in your cart.")
    else:
        cart = request.session.get('cart', {})
        if str(movie_id) in cart:
            del cart[str(movie_id)]
            request.session['cart'] = cart
            messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in your cart.")

    return redirect('cart_view')

def cart_view(request):
    cart_items = []
    total = 0

    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = [{'movie': item.movie, 'quantity': item.quantity} for item in cart.items.all()]
    else:
        cart = request.session.get('cart', {})
        for movie_id, quantity in cart.items():
            movie = get_object_or_404(Movie, id=movie_id)
            cart_items.append({'movie': movie, 'quantity': quantity})

    total = sum(item['movie'].price * item['quantity'] for item in cart_items)
    return render(request, 'Cart.html', {'cart_items': cart_items, 'total': total})

def checkout_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        order = Order.objects.create(
            movie=movie,
            user=request.user if request.user.is_authenticated else None,
            amount=movie.price,
            status='Pending'
        )
        messages.success(request, f"You have successfully purchased {movie.title}!")
        return redirect('thank_you')
    
    return render(request, 'checkout.html', {'movie': movie})



@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        payment_data = request.body
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
def thank_you_view(request):
    return render(request, 'thank_you.html')
