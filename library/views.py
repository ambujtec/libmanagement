import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from library.models import CustomUser, Book, Query, BorrowedBook, History
from library.authentication import CustomAuthBackend
from datetime import datetime, timedelta



customauth = CustomAuthBackend()


def index(request):
    books = Book.objects.all()
    is_librarian = False
    is_student = False
    user_id = 0
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        # print(user.usertype)\
        user_id = user.id
        print(user_id)
        if user.usertype == 'librarian':
            is_librarian = True
        elif user.usertype == "student":
            is_student = True
    
    return render(request, 'index.html', {'books': books, 'is_librarian': is_librarian, 'is_student': is_student, 'userid': user_id})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usertype = request.POST.get('usertype')
        try:
            user = CustomUser.objects.create_user(username=username, password=password, usertype=usertype)
        except:
            error_message = "Username is already registered. Choose a different username"
            return render(request, 'signup.html', {'message': error_message})
        print(user)
        user.user_type=usertype

        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'signup.html')    


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usertype = request.POST['usertype']
        print(usertype)
        user = customauth.authenticate(request, username=username, password=password, usertype=usertype)
        if user is not None:
            login(request, user)
            # if usertype == "librarian":
            return redirect('index')
            # else:
            #     return redirect('login')
        else:
            error_message = "Invalid username, password, or user type."
            return render(request, 'login.html', {'message': error_message})
    else:
        return render(request, 'login.html')
    

# from .forms import BookForm

# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')  # Redirect to the library catalog page after adding the book
#     else:
#         form = BookForm()
#     return render(request, 'add_book.html', {'form': form})

def add_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        total = int(request.POST.get('total'))
        if request.POST.get('available_copies'):
            available = int(request.POST.get('available_copies'))
        else :
            available = 0
        # first_book_return_date = request.POST.get('first_book_return_date')
        # copies = int(request.POST.get('copies'))

        book = Book.objects.create(
            name=name,
            total=total,
            available=available,
            # lastest_return_date=first_book_return_date,
        )
        return redirect('index')
    return render(request, 'add_book.html')


def update_book(request, book_id):
    print(book_id,"===")
    book = get_object_or_404(Book, id=book_id)
    print(book)
    if request.method == 'POST':
        name = request.POST.get('name')
        total = int(request.POST.get('total'))
        is_available = request.POST.get('is_available')
        print(is_available)
        available = int(request.POST.get('available_copies'))
        first_book_return_date = request.POST.get('first_book_return_date')
        if is_available == 'true':
            first_book_return_date == None
        else :
            available = 0
        book.name = name
        book.total = total
        book.available = available
        book.lastest_return_date = first_book_return_date

        book.save()
        
        return redirect('index')
    return render(request, 'update_book.html', {'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('index')
    return render(request, 'delete_book.html', {'book': book})



def borrow_book(request, book_id, user_id):
    try:
        book = get_object_or_404(Book, pk=book_id)
        user = get_object_or_404(CustomUser, pk=user_id)
        already_borrowed = BorrowedBook.objects.filter(book_name=book.name)
        already_queried = Query.objects.filter(student_username = user).filter(book_name = book.name)
        # if already_borrowed or already_queried:
        #     return JsonResponse({"message": f'You Already queried or own this book!'})
        if user.book_count == 10:
            return JsonResponse({"message": f'You reached the limit of borrowing Book!'})
        
        count = user.book_count
        user.book_count = count + 1
        available_books = book.available
        book.available = available_books - 1
        if book.available == 0:
            book.lastest_return_date = datetime.now() + timedelta(days=30)
        book.save()
        user.save()
        query = Query.objects.create(student_username=user.username, book_name=book.name, is_approved=False, query_for = 'Borrow')
        return JsonResponse({"message": f'Book "{book.name}" Sent for Confirmation from Librarian!'})

    except Exception as e:
        return HttpResponseBadRequest("Failed to borrow book")
    

def query_list(request):
    queries = Query.objects.all()
    context = {'queries': queries}
    return render(request, 'query_list.html', context)

        # stu = BorrowedBook.objects.create(student=user.username, book_name=book.name, borrowed_date = datetime.now(),return_date = datetime.now() + timedelta(days=30), is_renewable = True)
    # stu = History.objects.create(student=user.username, book_name=book.name, borrowed_date = datetime.now(),return_date = datetime.now() + timedelta(days=30), renewed = True)

def stud_books(request):
    user = request.user
    user_id = user.id
    borrowed_books = BorrowedBook.objects.filter(student=user)
    
    context = {'borrowed_books': borrowed_books,'student_id': user_id}
    return render(request, 'stud_book.html', context)


def student_history_view(request):
    
    student_history = History.objects.filter(student=request.user)
    return render(request, 'student_history.html', {'borrowed_books': student_history})

def renew_book(request, book_id):
    try:
        borrowed_book = get_object_or_404(BorrowedBook, id=book_id, student=request.user)
        # query = Query.objects.create(student_username=request.user, book_name=borrowed_book.book_name, is_approved=False, query_for='Renew')
        borrowed_book.is_renewable = False
        if not borrowed_book:
            return JsonResponse({'error': 'Book cannot be renewed'}, status=400)
        
        borrowed_book.return_date = borrowed_book.return_date + timedelta(days=30)
        borrowed_book.save()
        
        return JsonResponse({'message': 'Book Renewed Successfull'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def return_book(request, book_id):
    try:
        borrowed_book = get_object_or_404(BorrowedBook, id=book_id,student =request.user)
        borrowed_book.in_return_state = True
        borrowed_book.save()
        query = Query.objects.create(student_username=request.user, book_name=borrowed_book.book_name, is_approved=False, query_for='Return')
        return JsonResponse({'message': 'Return request sent successfully to librarian'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def handle_query(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print(data)
        action = data.get('action')
        query_id = data.get('queryId')
        student = data.get('studentName')
        book = data.get('bookName')
        query_for = data.get('queryFor')
        print(action)
        query = Query.objects.filter(id = query_id)
        if action == 'approve':
            message = f'Query {query_id} approved successfully!'
            if query_for == 'Borrow':
                book_added = BorrowedBook.objects.create(student=student, book_name=book, borrowed_date = datetime.now(), return_date = datetime.now() + timedelta(days=30), is_renewable = True)
            elif query_for == 'Return':
                book_for_return = BorrowedBook.objects.filter(book_name = book, student_username = student)
                book_for_return.delete()

        elif action == 'reject':
            message = f'Query {query_id} rejected successfully!'

        query.delete()
        return JsonResponse({'message': message})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def history_view(request):
    return render(request, 'history.html')