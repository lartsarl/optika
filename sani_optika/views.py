from django.shortcuts import render

# Create your views here.
import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader

from .forms import SignupForm, LoginForm, AddToCartForm, ReviewForm, AppointmentForm, FinalAppointmentForm, WishListForm, RatingForm
from .models import Category, Product, User, Order, ProductOrder, Review, Location, LocationSlot, WishList, StarRating
from .utils import handle_uploaded_file

from django.forms.models import model_to_dict

def index(request):
    categories = Category.objects.order_by('-name')
    reviews = Review.objects.order_by('-id')
    template = loader.get_template('sani_optika/index.html')
    context = {
        'categories': categories,
        'reviews': reviews
    }
    return HttpResponse(template.render(context, request))

def online_shop(request):
    categories = Category.objects.order_by('-name')
    reviews = Review.objects.order_by('-id')
    template = loader.get_template('base_online.html')
    context = {
        'categories': categories,
        'reviews': reviews
    }
    return HttpResponse(template.render(context, request))

def about_us(request):
    template = loader.get_template('sani_optika/about_us.html')
    return HttpResponse( template.render({}, request))

def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']

            user = User(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address
                )

            user.save()

            request.session['username'] = username
            request.session['cart'] = []

            # redirect to a new URL:
            return HttpResponseRedirect('/sani_optika')
        else:
            print("###### INVALID #####")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'sani_optika/signup.html', {'form': form})

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)

            except User.DoesNotExist:
                user = None
            
            if user:
                if user.password == password:
                    request.session['username'] = username
                    request.session['cart'] = []
            else:
                print("Invalid username and/or password")
                return HttpResponseRedirect('/sani_optika/login')

            # redirect to a new URL:
            return HttpResponseRedirect('online_shop')
        else:
            print("###### INVALID #####")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'sani_optika/login.html', {'form': form})

def logout(request):
    if 'username' in request.session:
        del request.session['username']

    return render(request, 'sani_optika/login.html')

def products(request, id):
    products = Product.objects.filter(category=id)
    categories = Category.objects.order_by('-name')
    ratings = StarRating.objects.all()
    template = loader.get_template('sani_optika/products.html')
    context = {
        'products': products,
        'categories': categories,
        'star_ratings': ratings
    }
    return HttpResponse(template.render(context, request))

def add_to_cart(request):
    if 'username' in request.session:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = AddToCartForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                product_id = int(form.cleaned_data['product_id'])
                quantity = int(form.cleaned_data['quantity'])

                item = {
                    "product_id": product_id,
                    "quantity": quantity
                }

                if not 'cart' in request.session or not request.session['cart']:
                    request.session['cart'] = [item]
                else:
                    cart = request.session['cart']
                    for index, prod in enumerate(cart):
                        if prod['product_id'] == product_id:
                            prod['quantity'] += quantity
                            if prod['quantity'] == 0:
                                del cart[index]
                            request.session['cart'] = cart
                            #return HttpResponseRedirect(form.cleaned_data['redirect_path'])
                            return HttpResponseRedirect('cart')

                    cart.append(item)
                    request.session['cart'] = cart
                # redirect to a new URL:
                #return HttpResponseRedirect(form.cleaned_data['redirect_path'])
                return HttpResponseRedirect('cart')
            else:
                print("###### INVALID #####")
    else:
        return HttpResponseRedirect("/sani_optika/login")

def cart(request):
    items = []
    total = 0
    for item in request.session['cart']:
        product = Product.objects.get(id=item['product_id'])
        total += product.price*item['quantity']
        items.append(product)

    user = User.objects.get(username=request.session['username'])

    template = loader.get_template('sani_optika/cart.html')
    context = {
        'cart': items,
        'total': total,
        'coupons': user.coupons,
        'totalWithCoupons': total-user.coupons
    }
    return HttpResponse(template.render(context, request))

def make_order(request):
    if 'username' in request.session:
        if request.method == 'POST':

            user = User.objects.get(username=request.session['username'])
            order = Order.objects.create(user=user)

            total = 0

            for item in request.session['cart']:
                product = Product.objects.get(id=item['product_id'])
                productOrder = ProductOrder.objects.create(
                    product=product, order=order, quantity=item['quantity'])
                total += product.price*item['quantity']

            if user.coupons > 0:
                totalBeforeCoupons = total
                total = total-user.coupons
                user.coupons = totalBeforeCoupons*0.05
            else:
                user.coupons = total*0.05
            user.save()

            order.total = total
            order.save()

            request.session['cart'] = []

            return HttpResponseRedirect('/sani_optika')

    else:
        return HttpResponseRedirect("/sani_optika/login")

def my_purchases(request):
    user = User.objects.get(username=request.session['username'])
    orders = Order.objects.filter(user=user)

    purchases = []
    for index, order in enumerate(orders):
        orderDict = model_to_dict(order, fields=[field.name for field in order._meta.fields])
        purchases.append(orderDict)
        items = []
        productOrders = ProductOrder.objects.filter(order=order)
        for item in productOrders:
            items.append(item)
        purchases[index]['items'] = items

    template = loader.get_template('sani_optika/myPurchases.html')
    context = {
        'purchases': purchases
    }
    return HttpResponse(template.render(context, request))

def review(request, id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            text = form.cleaned_data['text']
            file = form.cleaned_data['file']

            handle_uploaded_file(request.FILES['file'], file.name)

            product = Product.objects.get(id=id)
            user = User.objects.get(username=request.session['username'])
            Review.objects.create(path=file.name, text=text, product=product, user=user)

            # redirect to a new URL:
            return HttpResponseRedirect('/sani_optika')
        else:
            print("###### INVALID #####")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewForm()
        product = Product.objects.get(id=id)

    return render(request, 'sani_optika/review.html', {'form': form, 'product': product})

def make_appointment(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FinalAppointmentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            slot_id = form.cleaned_data['slot_id']

            user = User.objects.get(username=request.session['username'])
            slot = LocationSlot.objects.get(id=slot_id)

            slot.user = user
            slot.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/sani_optika')
        else:
            print("###### INVALID #####")

def find_slots(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            location_id = form.cleaned_data['location_id']
            date = form.cleaned_data['date']

            location = Location.objects.get(id=location_id)

            slots = LocationSlot.objects.filter(location=location, date=date, user=None)

            return render(request, 'sani_optika/make_appointment.html', {'slots': slots})
        else:
            print("INVAAAAAAAAAALID")
    else:
        form = AppointmentForm()
        locations = Location.objects.all()
        
    return render(request, 'sani_optika/find_slots.html', {'form': form, 'locations': locations})

def wish_list(request):
    if request.method == 'POST':
        form = WishListForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            product_id = form.cleaned_data['product_id']

            product = Product.objects.get(id=product_id)
            user = User.objects.get(username=request.session['username'])
            
            WishList.objects.create(user=user, product=product)

            return HttpResponseRedirect('/sani_optika')
        else:
            print("INVAAAAAAAAAALID")
    else:
        user = User.objects.get(username=request.session['username'])
        wish_list = WishList.objects.filter(user=user)
        
    return render(request, 'sani_optika/wish_list.html', {'wish_list': wish_list})

def rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            rating = form.cleaned_data['rating']
            product_id = form.cleaned_data['product_id']

            product = Product.objects.get(id=product_id)
            user = User.objects.get(username=request.session['username'])

            alreadyRated = StarRating.objects.filter(user=user, product=product)

            if alreadyRated.count() == 1:
                return HttpResponseRedirect('/sani_optika')    
            
            StarRating.objects.create(user=user, product=product, stars=rating)

            ratings = StarRating.objects.filter(product=product)

            total = 0
            for rating in ratings:
                total += rating.stars
            
            product.rating = total/ratings.count()
            product.save()
            
            return HttpResponseRedirect('/sani_optika')
        else:
            print("INVAAAAAAAAAALID")
    else:
        user = User.objects.get(username=request.session['username'])
        wish_list = WishList.objects.filter(user=user)
        
    return render(request, 'sani_optika/wish_list.html', {'wish_list': wish_list})
