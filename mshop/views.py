from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, Category, Customer, Order
from django.contrib.auth.hashers import make_password, check_password





def index(request):
    categories = Category.get_all_categories()
    # print('you are' , request.session.get('email'))
    return render(request, "shop/index.html", {'categories': categories})


def about(request):
    return render(request, "shop/about.html")



def contact(request):
    return HttpResponse("about")



def productpage(request):
    if(request.method == 'POST'):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        print(product)
        cart = request.session.get('cart')
        
        # CART FUNCTIONALITY
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        # print(request.session['cart'])
        # ///////////////
        
        categoryid = request.GET.get('category')
        products = Product.get_all_products_byId(categoryid)
        email = request.session.get('email')
        if categoryid:
            catid = Category.get_all_categories_byid(categoryid)
        return render(request, "shop/productpage.html", {'products': products, 'catid': catid})
   
   
    else:
        categories = Category.get_all_categories()
        # print('you are' , request.session.get('email'))
        

        categoryid = request.GET.get('category')
        products = Product.get_all_products_byId(categoryid)
    
    

        if categoryid:
            catid = Category.get_all_categories_byid(categoryid)
    

        return render(request, "shop/productpage.html", {'products': products, 'categories': categories, 'catid': catid})
    
    
    
    
    
    
   


        
    


def search(request):
    return HttpResponse("about")


def checkout(request):
    return HttpResponse("about")


def tracker(request):
    return HttpResponse("about")


def account(request):
    if request.method == 'GET':
        return render(request, "shop/account.html")
    else:
        postdata = request.POST
        firstname = postdata.get('firstname')
        lastname = postdata.get('lastname')
        phone = postdata.get('phone')
        email = postdata.get('email')
        password = postdata.get('password')

        values = {'firstname': firstname,
                  'lastname': lastname,
                  'phone': phone,
                  'email': email}

        customer = Customer(first_name=firstname,
                            last_name=lastname,
                            phone=phone,
                            email=email,
                            password=password)

        # ERROR VALIDATIONS
       
        error = None
        if not firstname:
            error = 'First Name required'
        elif not lastname:
            error = 'Last Name required'
        elif not phone:
            error = 'Phone Number required'
       
        elif not email:
            error = "Email required"
        elif not password:
            error = "Password required"
        elif customer.emailexist():
            error = 'Email Address Already Found'

        if not error:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('MegaShop')
        else:
            return render(request, 'shop/account.html', {'error': error, 'values': values})




def login(request):
    if request.method == 'GET':
        return render(request, "shop/login.html")
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_byemail(email)
        error = None
        if customer:
            flag = check_password(password , customer.password)
            if flag:
                request.session['customer'] = customer.id
                return redirect('MegaShop')
            else:
                error = 'Email or Password is Invalid'
        else:
            error = 'Email or Password is Invalid'
        
        return render(request, 'shop/login.html', {'error' : error})
    


def logout(request):
    request.session.clear()
    return redirect('login')


def cart(request):
    print(request.session.get('cart'))
    error = None
    if not request.session.get('cart'):
        error = 'Your Cart is empty'
        return render(request, 'shop/cart.html' , {'error' : error})
    ids = list(request.session.get('cart').keys())
    products = Product.get_all_cart_byId(ids)
    # print(products)
    return render(request, 'shop/cart.html', {'products' : products})



def checkout(request):
        if request.method == 'POST':
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            customer = request.session.get('customer')
            cart = request.session.get('cart')
            product = Product.get_all_cart_byId(list(cart.keys()))
            print(address , phone , customer , cart , product)

            for product in product:
                order = Order(customer = Customer(id = customer), 
                              product = product,
                              price = product.price,
                              quantity = cart.get(str(product.id)),
                              address = address,
                              phone = phone
                              )
                
                request.session['cart'] = {}
                order.place_order()


            return redirect('cart')