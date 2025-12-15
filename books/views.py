from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book
from .serializers import BookSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view


# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="List all books",
        description="Retrieve a list of all books in the library.",
        responses={200: BookSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Get book details",
        description="Retrieve details of a specific book by ID.",
    ),
    create=extend_schema(
        summary="Create a new book",
        description="Add a new book to the library.",
    ),
    update=extend_schema(
        summary="Update a book",
        description="Update all fields of a specific book.",
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Update some fields of a specific book.",
    ),
    destroy=extend_schema(
        summary="Delete a book",
        description="Remove a book from the library.",
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return[IsAdminUser()]

