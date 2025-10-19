from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class SignUpService:
    """
    Service class for managing user sign-up operations.
    """

    def _ensure_default_groups(self):
        Group.objects.get_or_create(name='reader')
        Group.objects.get_or_create(name='writer')

    def create_user(self, *, username: str, password: str, first_name: str = "", last_name: str = ""):
        """
        Creates a Django auth User, and assigns the 'reader' group to it.
        Args:
            username (str): The desired username for the new user.
            password (str): The desired password for the new user.
            first_name (str, optional): The first name of the user. Defaults to "".
            last_name (str, optional): The last name of the user. Defaults to "".
        Returns:
            User: The created Django auth User instance.
        """

        User = get_user_model()
        self._ensure_default_groups()
        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        reader = Group.objects.get(name='reader')
        new_user.groups.add(reader)
        return new_user
