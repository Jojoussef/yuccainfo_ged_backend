from rest_framework import serializers
from .models import Document
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class DocumentSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = Document
        fields = ['id', 'title', 'file',
                  'extracted_text', 'doc_type',
                  'category', 'category_id',
                  'uploaded_at']
