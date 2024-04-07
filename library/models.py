from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USERTYPE_CHOICES = [
        ('student', 'Student'),
        ('librarian', 'Librarian')
    ]
    usertype = models.CharField(max_length=20, choices=USERTYPE_CHOICES, default='student')
    book_count = models.PositiveIntegerField(default=0)

class Book(models.Model):
    name = models.CharField(max_length=100)
    total = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    lastest_return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.lastest_return_date:
            self.lastest_return_date = None
        super().save(*args, **kwargs)


class Query(models.Model):
    student_username = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    query_for = models.CharField(max_length=100,default="Borrow")


class BorrowedBook(models.Model):
    student = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_renewable = models.BooleanField(default=True)
    in_return_state = models.BooleanField(default=False)

    def __str__(self):
        return f'Student: {self.student.username}, Book: {self.book_name}'

class History(models.Model):
    student = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    renewed = models.BooleanField(default=False)

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     no_of_books_borrowed = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return self.name

# class BookDetails(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     borrowed_date = models.DateField(default=timezone.now)
#     is_renewable = models.BooleanField(default=True)
#     return_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.book.name} - {self.student.name}"

#     def is_overdue(self):
#         if self.return_date:
#             return timezone.now().date() > self.return_date
#         return False
    

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     copies_available = models.PositiveIntegerField(default=0)
    
#     def __str__(self):
#         return self.title
    
#     def available_copies(self):
#         return self.copies_available - self.borrowed_books.count()





# class Student(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     borrowed_books = models.ManyToManyField('BorrowedBook', related_name='borrowers')

#     def __str__(self):
#         return self.user.username

#     def currently_borrowed_books(self):
#         return self.borrowed_books.filter(returned=False)

#     def borrow_limit_reached(self):
#         return self.currently_borrowed_books().count() >= 10

# class Librarian(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username

# class BorrowedBook(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
#     borrower = models.ForeignKey(Student, on_delete=models.CASCADE)
#     borrowed_date = models.DateField(default=timezone.now)
#     return_date = models.DateField()
#     returned = models.BooleanField(default=False)
#     renewed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.book.title} - Borrowed by {self.borrower.user.username}"

#     def renew(self):
#         if not self.renewed:
#             self.renewed = True
#             self.return_date += timezone.timedelta(days=30)
#             self.save()

#     @property
#     def overdue(self):
#         return not self.returned and timezone.now() > self.return_date
