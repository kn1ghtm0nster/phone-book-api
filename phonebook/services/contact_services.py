import structlog
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from phonebook.models import Contact, PhoneNumber

logger = structlog.get_logger(__name__)


class ContactService:
    """
    Service class for managing contacts
    and their associated phone numbers.
    """

    def _check_name_exists(self, full_name: str) -> bool:
        """
        Verifies if a contact with the given full name already exists.
        Args:
            full_name (str): The full name to check.
        Returns:
            bool: True if a contact with the given name exists, False otherwise.
        """
        return Contact.objects.filter(full_name=full_name).exists()

    def _check_phone_number_exists(self, phone_number: str) -> bool:
        """
        Verifies if a phone number already exists in the database.
        Args:
            phone_number (str): The phone number to check.
        Returns:
            bool: True if the phone number exists, False otherwise.
        """
        return PhoneNumber.objects.filter(phone_number=phone_number).exists()

    def create_new_contact(self, name: str, phone_number: str) -> dict[str, str]:
        """
        Creates a new contact and associates a phone number with it.

        Args:
            name (str): The full name of the contact.
            phone_number (str): The phone number to associate with the contact.
        Returns:
            dict[str, str]: A dictionary containing the contact's name and phone number.
        """

        new_contact = Contact.objects.create(full_name=name)

        PhoneNumber.objects.create(
            phone_number=phone_number,
            contact=new_contact
        )

        logger.info('contact_service.created',
                    contact_name=new_contact.full_name)

        return {
            'name': new_contact.full_name,
            'phone_number': phone_number
        }

    def retrieve_all_contacts(self) -> list[dict[str, str | None]]:
        """
        Retrieves all contacts from the database.

        Returns:
            list[dict[str, str | None]]: A list of dictionaries representing all contacts.
        """
        qs = (
            Contact.objects
            .select_related("phone_number")
            .only("full_name", "id", "phone_number__phone_number")
        )

        results: list[dict[str, str | None]] = []
        for c in qs:
            try:
                number_obj = c.phone_number  # reverse OneToOne; may not exist
                number = number_obj.phone_number if number_obj else None
            except ObjectDoesNotExist:
                number = None
            results.append({"name": c.full_name, "phone_number": number})

        logger.info('contact_service.retrieve_all', count=len(results))

        return results

    def delete_contact(self, name: str | None = None, phone_number: str | None = None) -> None:
        """
        Deletes a contact based on the provided name or phone number.

        - If both are provided, name takes precedence.
        - Raises Http404 if the target record does not exist.
        - Raises ValueError if neither identifier is provided.
        """
        if name:
            contact = get_object_or_404(Contact, full_name=name)
            contact.delete()
            logger.info('contact_service.deleted', contact_name=name)
            return

        if phone_number:
            pn = get_object_or_404(PhoneNumber, phone_number=phone_number)
            # One-to-one; deleting the contact will cascade-delete the phone record
            pn.contact.delete()
            logger.info('contact_service.deleted',
                        contact_name=pn.contact.full_name)
            return

        raise ValueError("Either 'name' or 'phone_number' must be provided.")
