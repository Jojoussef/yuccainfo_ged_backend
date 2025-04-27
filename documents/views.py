from django.shortcuts import render
from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
import pytesseract
from .permissions import IsAdminOrOwner
from rest_framework.permissions import DjangoModelPermissions
from PIL import Image
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .apps import DocumentsConfig
from django.contrib.auth.models import Group


#********* Document classifier **********
CANDIDATE_LABELS = ["invoice", "contract","letter", "report", "other", "receipt", "memo", "email", "presentation"]

def classify_document(text): 
    labels = CANDIDATE_LABELS
    result = DocumentsConfig.classifier(text, candidate_labels=labels)
    return result['labels'][0] if result['scores'][0] > 0.5 else "other"

#********* ViewSets **********

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        DjangoModelPermissions,  # checks group perms (add, change, delete, view)
        IsAdminOrOwner
    ]

    def perform_create(self, serializer):
        document = serializer.save()
        if document.file:
            if document.file.name.endswith(('png', 'jpg', 'jpeg', 'pdf')):
                image = Image.open(document.file)
                text = pytesseract.image_to_string(image)
                document.extracted_text = text
                
                # Predict document category
                if text:
                    category_name = classify_document(text)
                    # Get or create a category with this name
                    document.doc_type = category_name
                    category, created = Category.objects.get_or_create(name=category_name)
                    document.category = category
                
                document.save()
                
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists():
            return Document.objects.all()
        return Document.objects.filter(owner=user)


# ********* Registration **********

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email    = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error':'Username taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the user
        user = User.objects.create_user(username, email, password)
        
        # Add user to 'User' permission group
        user_group, created = Group.objects.get_or_create(name='User')
        user.groups.add(user_group)
        
        return Response({'message':'User created successfully'}, status=status.HTTP_201_CREATED)
    
    
# ********* Logout **********

class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response