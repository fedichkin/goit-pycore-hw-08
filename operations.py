from functools import wraps
from address_book import AddressBook, Record


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'Not enough arguments for command {e}'
        except IndexError as e:
            return f'Enter name for get phone {e}'
        except KeyError as e:
            return f'There is not contact {e}'
        except Exception as e:
            return e

    return inner


@input_error
def add_contact(args: list, contacts: AddressBook):
    name, phone = args
    message = 'Contact updated'

    record = contacts.find(name)
    if not record:
        record = Record(name)
        contacts.add_record(record)
        message = 'Contact added'

    record.add_phone(phone)

    return message


@input_error
def change_contact(args: list, contacts: AddressBook):
    name, old_phone, phone = args

    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, phone)
    else:
        return 'Contact not found'

    return f'Phone of contact "{name}" changed'


@input_error
def get_phone(args: list, contacts: AddressBook):
    name = args[0]

    record = contacts.find(name)

    if not record:
        return f'Contact not found'

    return record.phones


@input_error
def add_birthday(args: list, contacts: AddressBook):
    name, birthday = args

    record = contacts.find(name)

    if not record:
        return f'Contact not found'

    record.add_birthday(birthday)

    return f'Added birthday for contact {name}'


@input_error
def show_birthday(args: list, contacts: AddressBook):
    name = args[0]

    record = contacts.find(name)

    if not record:
        return f'Contact not found'

    return record.birthday.get_birthday_str()


@input_error
def birthdays(contacts: AddressBook):
    return contacts.get_upcoming_birthdays()
