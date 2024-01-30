<h1 align="center">Django Multi Role Authentication 👋</h1>

This project shows how i implemented multi-role authentication in django django rest framework.

## USE CASE:
The system has four different portals(admin,patient,staff, support) which requires users have respective roles in order to log in.
A user can have multiple roles.
To login, a seperate endpoint is provided for each portal where the role is checked and user authenticated. This returns a jwt token. 
For eg. 
admins login using `/admin/auth/login`
staff login using `/staff/auth/login`



## Install and Run

1. Get the source code on to your machine via git.

    ```shell
    git clone https://github.com/ElijahAhianyo/django-multi-role-auth.git && cd django-multi-role-auth
    ```

2. Create virtual environment and install dependencies
```sh
#using virtual environment
python3 -m venv .virtualenv
#activate virtual environment
source ./.virtualenv/bin/activate
#install dependencies
pip install -r requirements.txt
```

3. Migrate and run application
```sh
cd app
python manage.py migrate
python manage.py runserver
```



## TO-DO:
- Add unit tests
- enforce static typing

#   Rotas que funcionaram
```
http://localhost:8000/users
```

corpo

```
{
 "email": "novousuario@example.com",
 "mobile": "+123456789",
 "role": [
   {"display": "patient"},
   {"display": "staff"}
 ],
 "password": "senha123"
}
```

resposta
```
{
	"id": 1,
	"email": "novousuario@example.com",
	"mobile": "+123456789",
	"role": [
		{
			"id": 1,
			"display": "patient"
		},
		{
			"id": 2,
			"display": "staff"
		}
	]
}
```


Vamos mostrar como você pode acessar cada uma das rotas no Postman. Certifique-se de ter o Postman instalado em seu sistema.

### 1. Criar Permissão para uma Função (Role):

#### Rota:
- **Método:** POST
- **URL:** `http://seu-domínio/api/create-permission-for-role/`

#### Dados da Solicitação (corpo da requisição):
```json
{
  "role": {
    "display": "novarole",
    "created_at": "2024-01-01T00:00:00Z",  // Preencha com a data desejada
    "modified_at": "2024-01-01T00:00:00Z"  // Preencha com a data desejada
  },
  "permission": {
    "codename": "novapermissao",
    "name": "Nova Permissao",
    "created_at": "2024-01-01T00:00:00Z",  // Preencha com a data desejada
    "modified_at": "2024-01-01T00:00:00Z"  // Preencha com a data desejada
  }
}
```

```json
{
  "role": {
    "display": "patient"
  },
  "permission": {
    "codename": "patient",
    "name": "Nova Permissao",
    "roles": [1]
  }
}
```

### 2. Associar uma Permissão Existente a uma Função Existente:

#### Rota:
- **Método:** POST
- **URL:** `http://seu-domínio/api/assign-permission-to-role/`

#### Dados da Solicitação (corpo da requisição):
```json
{
  "role_id": 1,  // Substitua pelo ID da função existente
  "permission_id": 1  // Substitua pelo ID da permissão existente
}
```

Lembre-se de substituir os valores das datas, IDs, etc., pelos valores específicos do seu sistema. Esses são exemplos genéricos. Certifique-se de que seu servidor Django esteja em execução e acessível a partir do Postman.

Depois de configurar os dados da solicitação, clique em "Send" no Postman para fazer a solicitação. Certifique-se de verificar as respostas para garantir que tudo tenha sido processado corretamente.

Esses são exemplos básicos, e você pode ajustar conforme necessário para atender às suas necessidades específicas.

# /////////////////////////////////////////////////////
Para implementar a função `funcpermission` que verifica se o usuário possui uma permissão específica com base no `codename` da permissão, você pode adicionar o seguinte código à sua aplicação. Vou criar um exemplo de como implementar isso:

1. **Modifique a sua model `User` para incluir a função:**

```python
# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone


class UserManager(BaseUserManager):
    # ... (seu código existente)

class User(AbstractBaseUser, PermissionsMixin):
    # ... (seu código existente)

    @property
    def permissions_codenames(self):
        return list(self.role.values_list('permissions__codename', flat=True))
```

A função `permissions_codenames` retorna uma lista de todos os codenames das permissões associadas ao usuário.

2. **Crie uma função utilitária em algum lugar do seu código:**

```python
# utils/permissions.py

def funcpermission(user, codename):
    return codename in user.permissions_codenames
```

3. **Use a função `funcpermission` em suas views:**

```python
# authentication/views.py

from utils.permissions import funcpermission

class SomeView(APIView):
    def some_method(self, request):
        codename = 'read'  # Substitua isso pelo codename desejado
        if funcpermission(request.user, codename):
            # O usuário possui a permissão, continue com a lógica da view
            return Response({"message": "Usuário tem permissão para acessar esta visualização."})
        else:
            # O usuário não possui a permissão, retorne uma resposta de não autorizado
            return Response({"message": "Usuário não tem permissão para acessar esta visualização."}, status=status.HTTP_403_FORBIDDEN)
```

Essencialmente, a função `funcpermission` verifica se o `codename` da permissão está presente na lista de codenames das permissões associadas ao usuário. Certifique-se de adaptar o código de acordo com a estrutura real do seu projeto, ajustando os imports e as referências de caminho conforme necessário.