from django.urls import path
from borrowings.views import BorrowBookView, MyBorrowsView, ReturnBookView


urlpatterns = [
    path("borrow/", BorrowBookView.as_view()),
    path("my-borrows/", MyBorrowsView.as_view()),
    path("return/<int:pk>/", ReturnBookView.as_view()),
]