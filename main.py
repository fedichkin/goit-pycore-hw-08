from operations import add_contact, change_contact, get_phone, add_birthday, birthdays, show_birthday
from address_book import AddressBook
import pickle


def save_data(contacts: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(contacts, f)


def load_data(filename="addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def main():
    contacts = load_data()
    print('Welcome to the assistant bot!')

    while True:
        user_input = input('Enter a command: ')

        try:
            command, *args = parse_input(user_input)
        except ValueError:
            print('Enter command and arguments')
            continue

        if command in ['close', 'exit']:
            save_data(contacts)
            print('Good bye!')
            break

        match command:
            case 'hello':
                print('How can I help you?')
            case 'add':
                print(add_contact(args, contacts))
            case 'change':
                print(change_contact(args, contacts))
            case 'phone':
                print(get_phone(args, contacts))
            case 'all':
                for name in contacts:
                    print(contacts[name])
            case 'add-birthday':
                print(add_birthday(args, contacts))
            case 'show-birthday':
                print(show_birthday(args, contacts))
            case 'birthdays':
                print(birthdays(contacts))
            case _:
                print('Invalid command.')


if __name__ == "__main__":
    main()
