# views.py
# authentication/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsStaffOrReadOnly, IsSupportOrReadOnly, IsPatientOrReadOnly

# ...
from rest_auth.views import LoginView
from rest_framework.response import Response
from users.models import Roles,User
from authentication.exceptions import AuthenticationError
from rest_framework_simplejwt.tokens import RefreshToken
from abc import ABC, abstractmethod

"""
class CustomLoginView(LoginView):
    def get_response(self):
        data = super().get_response().data
        user = self.serializer.validated_data['user']
        data['role'] = user.role.display
        return Response(data)
"""


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = request.user.role.all()

        if roles.exists():  # Verifica se o usuário tem pelo menos uma função
            role_display_messages = [
                f"Você tem permissão como {role.display}."
                for role in roles
            ]
            return Response({"message": " ".join(role_display_messages)})
        else:
            return Response({"message": "Usuário não tem permissão para acessar esta visualização."}, status=status.HTTP_403_FORBIDDEN)


class LoginBaseClass(ABC,LoginView):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    @abstractmethod
    def login(self):
        pass

    def get_response(self):
        data = {}
        
        refresh = self.get_token(self.user)
        # generate access and refresh tokens 
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return Response(data)

    



class CustomLoginView(LoginBaseClass):

    def login(self):
        try:
            self.user = self.serializer.validated_data['user']
            # Coloque aqui a lógica específica do seu login
            # (por exemplo, verificar papéis, fazer outras verificações)
            return self.user
        except Roles.DoesNotExist:
            raise AuthenticationError

    def get_response(self):
        data = super().get_response().data
        print("validated_data:", self.serializer.validated_data)  # Adicione esta linha para verificar
        user = self.serializer.validated_data.get('user')

        if user:
            roles_display = [role.display for role in user.role.all()]
            data['roles'] = roles_display

        access_token = self.serializer.validated_data.get('access')
        if access_token:
            data['jwt_token'] = str(access_token)

        return Response(data)











class StaffLoginView(LoginBaseClass):

    def login(self):
        try:
            self.user = self.serializer.validated_data['user']
            # check if user has practitioner among its roles
            self.user.role.get(display='staff')
            return self.user
        except Roles.DoesNotExist:
            raise AuthenticationError
            








class PatientLoginView(LoginBaseClass):

    def login(self):
        try:
            self.user = self.serializer.validated_data['user']
            # check if user has patient among its roles
            self.user.role.get(id='patient')
            return self.user
        except Roles.DoesNotExist:
            raise AuthenticationError









class AdminLoginView(LoginBaseClass):

    def login(self):
        try:
            self.user = self.serializer.validated_data['user']
            # check if user is a corporate admin
            self.user.role.get(display='admin')
            return self.user
        except Roles.DoesNotExist:
            raise AuthenticationError







class SupportLoginView(LoginBaseClass):

    def login(self):
        try:
            self.user = self.serializer.validated_data['user']
            self.user.role.get(display='support')
            return self.user
        except Roles.DoesNotExist:
            raise AuthenticationError





class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        # Sua lógica de visualização aqui
        return Response({"message": "Você tem permissão para acessar esta visualização."})



class SupportProtectedView(APIView):
    permission_classes = [IsAuthenticated, IsSupportOrReadOnly]

    def get(self, request):
        # Sua lógica de visualização para suporte aqui
        return Response({"message": "Você tem permissão para acessar esta visualização de suporte."})

# Repita o mesmo padrão para outras views protegidas
# ...

class PatientProtectedView(APIView):
    permission_classes = [IsAuthenticated, IsPatientOrReadOnly]

    def get(self, request):
        # Sua lógica de visualização para pacientes aqui
        return Response({"message": "Você tem permissão para acessar esta visualização de paciente."})

# Repita o mesmo padrão para outras views protegidas
# ...

class AdminProtectedView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        # Sua lógica de visualização para administradores aqui
        return Response({"message": "Você tem permissão para acessar esta visualização de administrador."})

# Repita o mesmo padrão para outras views protegidas
# ...

class StaffProtectedView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def get(self, request):
        # Sua lógica de visualização para staff aqui
        return Response({"message": "Você tem permissão para acessar esta visualização de staff."})
    

# Repita o mesmo padrão para outras views protegidas
# ...


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Realize aqui qualquer lógica de logout necessária
        # Isso pode incluir invalidar tokens, limpar sessões, etc.

        # Exemplo: invalidar o token de atualização
        request.auth.delete()

        return Response({"detail": "Logout bem-sucedido"})