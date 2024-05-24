#   Este ee o filtro que queremos melhorar

```bash
    ROLE_CHOICES = (
        ('patient', 'PATIENT'),
        ('staff', 'STAFF'),
        ('support', 'SUPPORT'),
        ('admin', 'ADMIN'),
    )
```

Para filtrar os dados que já existem na tabela `Roles` e usar esses valores para definir `ROLE_CHOICES` dinamicamente, você pode fazer isso de duas formas principais:

1. **Carregar as opções dinamicamente durante a inicialização do modelo**.
2. **Usar uma abordagem personalizada para definir as opções de escolha na inicialização do aplicativo**.

### 1. Carregar as opções dinamicamente durante a inicialização do modelo

Você pode sobrescrever o método `__init__` do seu modelo para carregar as escolhas dinamicamente da base de dados. Aqui está um exemplo de como fazer isso:

```python
from django.db import models

class Roles(models.Model):
    display = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_role_choices():
        roles = Roles.objects.all().values_list('display', 'display')
        return [(role[0], role[1].upper()) for role in roles]

    def __str__(self):
        return self.display


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'mobile'
    email = models.EmailField('email', blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(unique=True, validators=[phone_regex], max_length=17)
    role = models.ManyToManyField('Roles', related_name='user_role', blank=True)
    objects = UserManager()

    def __unicode__(self):
        return self.email

    @classmethod
    def add_role(cls, current_user, current_role):
        current_user.role.add(current_role)

    @classmethod
    def remove_role(cls, current_user, current_role):
        current_user.role.remove(current_role)

    @property
    def permissions_codenames(self):
        return list(self.role.values_list('permissions__codename', flat=True))
```

### 2. Usar uma abordagem personalizada para definir as opções de escolha na inicialização do aplicativo

Outra abordagem é definir `ROLE_CHOICES` quando o Django inicializa, carregando as opções diretamente da base de dados no arquivo `apps.py` da sua aplicação.

#### Passo 1: Criar um sinal de inicialização em `apps.py`

```python
from django.apps import AppConfig
from django.db.models.signals import post_migrate

def set_role_choices(sender, **kwargs):
    from .models import Roles
    Roles.ROLE_CHOICES = Roles.get_role_choices()

class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        post_migrate.connect(set_role_choices, sender=self)
```

#### Passo 2: Atualizar `__init__.py` do seu aplicativo

Certifique-se de que o `AppConfig` personalizado seja usado em `__init__.py` do seu aplicativo.

```python
default_app_config = 'myapp.apps.MyAppConfig'
```

Com essa abordagem, você define dinamicamente `ROLE_CHOICES` durante a inicialização do aplicativo. Isso garante que as escolhas sejam sempre atualizadas com base nos dados atuais da base de dados.