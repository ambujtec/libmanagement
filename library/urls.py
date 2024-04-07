
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('add_book/', views.add_book, name='add_book'),
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('borrow_book/<int:book_id>/<int:user_id>', views.borrow_book, name='borrow_book'),
    path('queries/', views.query_list, name='query_list'),
    path('stud_books/', views.stud_books, name='stud_books'),
    path('stud_history/', views.student_history_view, name='student_history'),
    path('renew_book/<int:book_id>/', views.renew_book, name='renew_book'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('handle_query/', views.handle_query, name='handle_query'),
    path('history/', views.history_view, name='history'),
]
