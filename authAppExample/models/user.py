# Models es como una clase abstracta que sirve para representar los modelos de la DB
from django.db import models
# Automatiza una parte de la gestión de usuarios 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# make_hashers ayuda a encriptar constraseñas a través de hash, por ejemplo, recibe una
# contraseña como palabra clave, y a partir de esta genera una contraseña encriptada
from django.contrib.auth.hashers import make_password

# BaseUserManager es una clase que se utiliza para administrar usuarios, es como un
# "administrador general de usuarios", de tal forma que facilita muchas operaciones comunes con usuarios
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('El usuario debe tener un username')
        # El método model es heredado de BaseUserManager, self.model se refiere a esta clase,
        # sería como UserManager.model, aprovechando un método heredado, y el atributo username
        # de la clase (heredado) va a ser igual al username que recibe el método como argumento.
        # Todo sería como: crear un modelo con el nombre de usuario, con la contraseña y guardarlo
        # usando la base de datos por defecto para esta clase (es decir, la que está en el settings.py)
        # gracias a la función save() que es lo que llamamos ORM, se comunica con la DB sin necesidad
        # de escribir SQL, además gestiona automáticamente lo que debe hacer dependiendo el tipo de DB.
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username_, password_):
        user = self.create_user(
            username = username_,
            password = password_
        )
        # La propiedad is_admin es heredada, y por defecto es falsa, así que aquí se convierte en
        # verdadera para indicar que este tipo de usuario es administrador
        user.is_admin = True
        user.save(using=self._db)
        return user

# Se hereda de la clase AbstractBaseUser, que tiene propiedades predeterminadas de un usuario
class User(AbstractBaseUser, PermissionsMixin):
    # models ayuda a gestionar los tipos de datos de los campos en las tablas en la DB,
    # pero nosotros debemos escoger el tipo de dato más adecuado, también podemos definir las
    # propiedades de cada campo, por ejemplo el nombre (de la columna) o si es llave primaria o si es unico
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Username', max_length=20, unique=True)
    password = models.CharField('Password', max_length=256)
    name = models.CharField('Nombre', max_length=250)
    email = models.EmailField('Email', max_length=100)

    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        # La contraseña será cifrada con la función make_password, que hará el cifrado con una operación
        # de hashing a partir de la contraseña original y una palabra clave (some_salt), 
        # esta contraseña cifrada será la que se guarde en la base de datos, siendo ilegible
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)

        objects = UserManager()
        USERNAME_FIELD = 'username'