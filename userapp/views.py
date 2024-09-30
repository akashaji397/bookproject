from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage
from bookapp .models import Book
from authenticationapp . models import loginTable,UserProfile
from django.db.models import Q
from. models import Cart,CartItem
from django.shortcuts import get_object_or_404
import stripe
from django.urls import reverse
from django.conf import settings

# Create your views here.
def user_view(request):
    user_name=request.session['username']
    books = Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_page)

    return render(request,'user/user_view.html',{'user_name':user_name,'books': books,'page':page})


def user_detail(request, book_id):
    user_name=request.session['username']
    book = Book.objects.get(id=book_id)
    return render(request, 'user/user_detail.html', {'user_name':user_name,'book': book})



from django.shortcuts import render
from django.db.models import Q

def user_search(request):
    user_name = request.session.get('user/username', 'Guest')  # Use a default value if username isn't set
    query = None
    books = []

    # Initialize context
    context = {
        'books': books,
        'query': query,
        'user_name': user_name  # Add user_name to the context
    }

    if 'q' in request.GET:
        query = request.GET.get('q')
        # Correct the filter to remove the unnecessary nested filter
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)  # Access the name field of the author
        )
        context['books'] = books
        context['query'] = query  # Update query in context

    return render(request, 'user/user_search.html', context)



def userbase(request):
    return render(request,'user/userbase.html')


def add_to_cart(request,book_id):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)
    user_profile = get_object_or_404(UserProfile, username=username)
    book=Book.objects.get(id=book_id)

    if book.quantity>0:
        cart,item_created=Cart.objects.get_or_create(user=user_profile)
        cart_item,item_created=CartItem.objects.get_or_create(cart=cart,book=book)
        if not item_created:
            cart_item.quantity+=1
            cart_item.save()

    return redirect('user_cart')


def user_cart(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if no username in session

    user_profile = get_object_or_404(UserProfile, username=username)
    cart, created = Cart.objects.get_or_create(user=user_profile)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    }

    return render(request, 'user/user_cart.html', context)

def increase_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity+=1
        cart_item.save()

    return redirect('user_cart')

def decrease_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()

    return redirect('user_cart')

def remove_from_cart(request,item_id):
    try:
        cart_item=CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass

    return redirect('user_cart')

def create_checkout_session(request):
    cart_items = CartItem.objects.all()

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            line_items = []

            for cart_item in cart_items:
                if cart_item.book:
                    # Correcting the unit_amount and quantity reference
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            # Ensure price is multiplied by 100 and is an integer
                            'unit_amount': int(float(cart_item.book.price) * 100),
                            'product_data': {
                                'name': cart_item.book.title
                            },
                        },
                        # Quantity should come from cart_item, not cart_item.book
                        'quantity': cart_item.quantity  # Use cart_item.quantity if it exists
                    }
                    line_items.append(line_item)

            if line_items:
                # Create a Stripe checkout session with the corrected line items
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),
                )

                # Redirect to Stripe's checkout page
                return redirect(checkout_session.url, code=303)

    return render(request, 'cart_empty.html')  # Optional: handle case where cart is empty








# def create_checkout_session(request):
#     cart_items=CartItem.objects.all()

#     if cart_items:
#         stripe.api_key=settings.STRIPE_SECRET_KEY

#         if request.method=='POST':
#             line_items=[]
#             for cart_item in cart_items:
#                 if cart_item.book:
#                     line_item={
#                         'price_data':{
#                             'currency':'INR',
#                             'unit_amount':int(cart_item.book.price * 100),
#                             'product_data':{
#                                 'name':cart_item.book.title
#                             },
#                         },
#                         'quantity':cart_item.book.quantity
#                     }
#                     line_items.append(line_item)

#             if line_items:

#                 checkout_session=stripe.checkout.Session.create(
#                     payment_method_types=['card'],
#                     line_items=line_items,
#                     mode='payment',
#                     success_url=request.build_absolute_uri(reverse('success')),
#                     cancel_url=request.build_absolute_uri(reverse('cancel'))
#                 )

#             return redirect(checkout_session.url,code=303)
        
def success(request):

    username = request.session.get('username')
    user_profile = get_object_or_404(UserProfile, username=username)
    cart, created = Cart.objects.get_or_create(user=user_profile)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    cart_items=CartItem.objects.all()
    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity>=cart_item.quantity:
            product.quantity-=cart_item.quantity
            product.save()

    cart_item.delete()

    return render(request,'user/success.html',{'total_price': total_price})


def cancel(request):
    return render(request,'user/cancel.html')
