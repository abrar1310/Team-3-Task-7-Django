from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book
from .serializers import BookSerializer
from rest_framework.permissions import AllowAny, IsAdminUser

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return[IsAdminUser()]

