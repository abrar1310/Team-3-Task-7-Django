from rest_framework import serializers
from borrowings.models import BorrowingRecord


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingRecord
        fields = "__all__"
        read_only_fields = ["user", "borrow_date", "due_date", "is_returned"]
