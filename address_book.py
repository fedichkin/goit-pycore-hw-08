from collections import UserDict
import re
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Name(Field):
    ...


class Birthday(Field):
    def __init__(self, value: str):
        if re.match(r'^\d{2}.\d{2}.\d{4}$', value) is not None:
            super().__init__(datetime.strptime(value, '%d.%m.%Y').date())
        else:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')

    def get_birthday_str(self):
        return self.value.strftime('%d.%m.%Y')


class Phone(Field):
    def __init__(self, value: str):
        if re.match(r'^\d{10}$', value) is not None:
            super().__init__(value)
        else:
            raise ValueError('Invalid format of phone')


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday = None

    def __str__(self):
        return f'Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}'

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        index_phone = next((index for (index, item) in enumerate(self.phones) if item.value == phone), None)

        if index_phone is not None:
            del self.phones[index_phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        index_phone = next((index for (index, item) in enumerate(self.phones) if item.value == old_phone), None)

        if index_phone is not None:
            self.phones[index_phone] = Phone(new_phone)
        else:
            raise ValueError('Not found phone')

    def find_phone(self, phone: str) -> Phone:
        return next((item for item in self.phones if item.value == phone), None)

    def add_birthday(self, value: str):
        self.birthday = Birthday(value)


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data[name] if name in self.data else None

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)

    @staticmethod
    def __date_to_string(date: datetime):
        return date.strftime('%d.%m.%Y')

    @staticmethod
    def __find_next_weekday(start_date: datetime, weekday: int):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def __adjust_for_weekend(birthday: datetime):
        if birthday.weekday() >= 5:
            return AddressBook.__find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for name in self.data:
            if self.data[name].birthday is None:
                continue

            birthday_this_year = self.data[name].birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = self.data[name].birthday.value.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = AddressBook.__adjust_for_weekend(birthday_this_year)

                congratulation_date_str = AddressBook.__date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date_str})

        return upcoming_birthdays


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    john_record.add_birthday('30.04.2003')
    jane_record.add_birthday('20.05.2003')

    print(book.get_upcoming_birthdays())

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    john.remove_phone("5555555555")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
