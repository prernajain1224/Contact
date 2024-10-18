from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token 
from .serializers import UserSerializer, ContentSerializer
from .models import Content
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# User registration
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user) 

        return Response({
            "message": "Account created successfully",
            "name": user.username,
            "email": user.email,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login
@csrf_exempt
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "message": "Login successful"
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Add new contact
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_contact(request):
    serializer = ContentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Edit contact
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_contact(request, contact_id):
    content = get_object_or_404(Content, id=contact_id, user=request.user)
    
    if request.method == 'PUT':
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        content.delete()
        return Response({"message": "Contact deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Get all contacts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contacts(request):
    contacts = Content.objects.filter(user=request.user)
    serializer = ContentSerializer(contacts, many=True)
    return Response(serializer.data)

# Get contact by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contact_by_id(request, contact_id):
    content = get_object_or_404(Content, id=contact_id, user=request.user)
    serializer = ContentSerializer(content)
    return Response(serializer.data)
