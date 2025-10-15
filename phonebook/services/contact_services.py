from phonebook.models import Contact, PhoneNumber


class ContactService:
    """
    Service class for managing contacts
    and their associated phone numbers.
    """

    def create_new_contact(self, full_name: str, phone_numbers: list[str] | str) -> Contact:
        """
        creates a new contact with the given full name and phone number(s).
        Phone numbers can be a single string or a list of strings.

        Args:
            full_name (str): The full name of the contact.
            phone_numbers (list[str] | str): A single phone number or a list of phone numbers.

        Returns:
            Contact: The created Contact instance.
        """
        if isinstance(phone_numbers, str):
            phone_numbers = [phone_numbers]

        contact = Contact.objects.create(full_name=full_name)

        for i, pn in enumerate(phone_numbers):
            PhoneNumber.objects.create(
                phone_number=pn,
                contact=contact,
                is_primary=(i == 0)  # First number is primary
            )

        return contact

    def retrieve_all_contacts(self) -> list[dict[str, str | None]]:
        """
        Retrieves all contacts from the database.

        Returns:
            list[dict[str, str | None]]: A list of dictionaries representing all contacts.
        """
        contacts = Contact.objects.all().prefetch_related("phone_numbers")

        return [
            {
                "name": c.full_name,
                "phone_number": next(
                    (pn.phone_number for pn in c.phone_numbers.all() if pn.is_primary),
                    None
                )
            }
            for c in contacts
        ]
