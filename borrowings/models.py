from datetime import timedelta
from django.db import models, transaction
from django.conf import settings
from books.models import Book
from django.utils import timezone

class BorrowingRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.due_date = timezone.now() + timedelta(days=14)
            if self.book.available_copies <= 0:
                raise ValueError("No copies available")
            with transaction.atomic():
                self.book.available_copies -= 1
                self.book.save()
        super().save(*args, **kwargs)
