from django.utils import timezone
from django.shortcuts import render
from borrowings.models import BorrowingRecord
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from borrowings.permissions import IsOwner
from django.db import transaction
from borrowings.serializers import BorrowingSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(
    summary="Borrow a book",
    description="Create a borrowing record for the logged-in user.",
    responses={201: BorrowingSerializer}
)
class BorrowBookView(generics.CreateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Show my borrowings",
    description="Retrieve a list of borrowing records for the logged-in user.",
    responses={200: BorrowingSerializer(many=True)}
)
class MyBorrowsView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowingRecord.objects.filter(user=self.request.user)


@extend_schema(
    summary="Return a borrowed book",
    description="Mark a borrowing record as returned and update book availability.",
    responses={200: BorrowingSerializer}
)
class ReturnBookView(generics.UpdateAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = BorrowingRecord.objects.all()

    def perform_update(self, serializer):
        borrowing = serializer.instance
        if not borrowing.is_returned:
            with transaction.atomic():
                borrowing.is_returned = True
                borrowing.return_date = timezone.now()
                borrowing.book.available_copies = min(
                    borrowing.book.available_copies + 1,
                    borrowing.book.total_copies
                )
                borrowing.book.save()
                borrowing.save()
