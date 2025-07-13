from django.db import models

# Create your models here.
class Borrowing(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_extended = models.BooleanField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


    def __str__(self):
        return f"{str(self.user)} - {str(self.book)}"
        