from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Usuario del gimnasio: inicia sesión con su email."""

    email = models.EmailField(unique=True, verbose_name='Email')
    # Campo extra de la práctica
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Teléfono',
        validators=[RegexValidator(r'^\+?\d{10,15}$', 'Escribe de 10 a 15 dígitos; puede iniciar con +.')],
    )

    USERNAME_FIELD = 'email'
    # El manual deja esta lista vacía, pero entonces "createsuperuser" falla
    # porque el UserManager de Django exige un username.
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
