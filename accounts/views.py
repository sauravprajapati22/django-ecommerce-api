from django.shortcuts import render
from .serializers import RegisterSerializer,UserSerializer
from .models import User
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    