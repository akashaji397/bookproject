from django.shortcuts import render,redirect
from .models import Book
from . forms import AuthorForm,BookForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from authenticationapp . models import loginTable,UserProfile


# Create your views here.
def listBook(request):
    user_name=request.session['username']
    books = Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_page)

    return render(request, 'admin_step/listbook.html', {'user_name':user_name,'books': books,'page':page})


def detailsview(request,book_id):
    user_name=request.session['username']
    book=Book.objects.get(id=book_id)
    return render(request,'admin_step/detailsview.html',{'user_name':user_name,'book':book})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

def updatebook(request, book_id):
    user_name=request.session['username']
    # Use get_object_or_404 for better error handling
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            form.save()
            return redirect('listBook')  # Redirect to the homepage or another appropriate page
    else:
        form = BookForm(instance=book)  # Initialize the form with the current book instance

    # Render the form for GET requests
    return render(request, 'admin_step/updatebook.html', {'user_name':user_name,'form': form, 'book': book})

def deletebook(request,book_id):
    user_name=request.session['username']
    book=Book.objects.get(id=book_id)
    if request.method=='POST':
        book.delete()
        return redirect('listBook')
    return render(request,'admin_step/deletebook.html',{'user_name':user_name,'book':book})

def createBook(request):
    user_name=request.session['username']
    books=Book.objects.all()
    if request.method=='POST':
        form=BookForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('listBook')
            
    else:
        form=BookForm()
    return render(request,'admin_step/book.html',{'user_name':user_name,'form':form,'books':books})


def CreateAuthor(request):
    user_name=request.session['username']
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listBook')  # Redirect to another view after successful form submission
    else:
        form = AuthorForm()

    return render(request, 'admin_step/author.html', {'user_name':user_name,'form': form})  # Ensure this line is executed



def index(request):
    user_name=request.session['username']
    return render(request,'admin_step/base.html',{'user_name':user_name})

from django.db.models import Q

def Search_Book(request):
    user_name = request.session.get('username', 'Guest')  # Use a default value if username isn't set
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
        # Assuming 'author' is a ForeignKey pointing to an Author model
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)  # Access the name field of the author
        )
        context['books'] = books
        context['query'] = query  # Update query in context

    return render(request, 'admin_step/search.html', context)



def admin_view(request):
    
    user_name=request.session['username']
    return render(request,'admin_step/admin_view.html',{'user_name':user_name})


