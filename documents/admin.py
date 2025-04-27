from django.contrib import admin

from django.contrib import admin
from .models import Document, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'category', 'owner', 'uploaded_at')
    list_filter  = ('doc_type', 'category', 'uploaded_at')
    search_fields = ('title', 'extracted_text')
    raw_id_fields = ('owner',)
