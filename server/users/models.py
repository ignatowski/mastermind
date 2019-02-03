from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    """A user object."""

    def __str__(self) -> str:
        """String representation of a User object."""
        return self.email
