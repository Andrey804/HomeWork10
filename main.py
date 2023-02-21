import sys, re
from collections import UserDict


class UserNameError(Exception):
    pass


class UserNumberError(Exception):
    pass


class UserChangingNumberError(Exception):
    pass


class UserNewNumberError(Exception):
    pass


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return f"Contact with name: '{record.name.value}'" + \
               (f", and phone number: '{record.phones[-1].value}'" if record.is_entered_phone is not False else "") + \
               f" - has been successfully added!"

    def phone_user(self, name_or_phone):
        for name, contact in self.data.items():
            if name_or_phone == name:
                return f"{name} -> " + \
                       ', '.join([phone.value for phone in contact.phones] if len(contact.phones) > 0 else
                                 ['No phone numbers'])

            for contact_phone in contact.phones:
                if name_or_phone == contact_phone.value:
                    return f"{name} -> " + \
                           ', '.join([phone.value for phone in contact.phones] if len(contact.phones) > 0 else
                                     ['No phone numbers'])
        return f"Contacts with this data: {name_or_phone} - not found!"

    def show_all(self):

        if not bool(self.data):
            return "Address book is empty!"

        longest_name = max([len(names) for names in self.data])

        return "\n".join([f"{str(contact.name.value):<{longest_name}} -> " +
                          (", ".join([i.value for i in contact.phones] if len(contact.phones) > 0
                                     else ['No phone numbers']))
                          for contact in self.data.values()])


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.is_entered_phone = False
        self.phones = []

        self.user_contacts_values = address_book.data.get(self.name.value)
        if self.user_contacts_values is not None:
            self.phones = self.user_contacts_values.phones

    def add_new_phone(self, phone):
        if bool(phone) is not False:

            for contact in address_book.values():
                for contact_phone in contact.phones:
                    if phone == contact_phone.value:
                        return f"In a contact with the name: '{contact.name.value}', the phone number: '{phone}'" \
                               f" - has been already exists!"

            self.is_entered_phone = True
            self.phones.append(Phone(phone))

        else:
            if self.name.value in address_book:
                return f"Contact with name: '{self.name.value}' - has been already created!"

    def change_phone(self, phone, new_phone):
        for phones in self.phones:
            if phones.value == phone:
                id_remove_phone = self.phones.index(phones)
                self.phones.remove(phones)
                self.phones.insert(id_remove_phone, Phone(new_phone))
                return f"In the contact with the name: '{self.name.value}'" \
                       f" - the phone number: '{phone}' was successfully changed to '{new_phone}'!"
        return f"In contact with name: '{self.name.value}', phone number: '{phone}' - not found!"

    def remove_phone(self, phone):
        for phones in self.phones:
            if phones.value == phone:
                self.phones.remove(phones)
                return f"In the contact with name: '{self.name.value}'" \
                       f" - phone: '{phone}' has been successfully removed!"
        return f"In contact with name: '{self.name.value}', phone number: '{phone}' - not found!"


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


# основна функція, яка працює з користувачем, приймає та виводить інформацію
def main():
    entered_str = None

    while True:
        entered_str = input("Hello!\n>>>") if entered_str is None else input(">>>")
        key = None

        for i in dict_of_keys.keys():
            if re.match(i, entered_str.lower()):
                key = i
                entered_str = entered_str.lower().removeprefix(key).removeprefix(" ").capitalize()
                break

        print(handler(key, entered_str))


# функція-декоратор, яка перевіряє строку, введену користувачем, на винятки
def input_error(func):
    def wrappers(key, entered_str):
        try:
            return func(key, entered_str)

        except KeyError:
            return "I don't understand what you want from me!\n" \
                   "(An invalid command was entered. To see existing commands, type <help> or <info>)"

        except UserNameError:
            return "You entered the invalid name!\n" \
                   "(The name must begin with a Latin letter, have no spaces, " \
                   "and be separated from the command by one space)"

        except UserNumberError:
            return "You entered the invalid number!\n" \
                   "(The phone number should look like this: 380888888888, and be separated from the name by one space)"

        except UserChangingNumberError:
            return "You entered the invalid changing number!\n" \
                   "(The phone number should look like this: 380888888888, and be separated from the name by one space)"

        except UserNewNumberError:
            return "You entered the invalid new number!\n" \
                   "(The phone number should look like this: 380888888888, " \
                   "and be separated from the changing number by one space)"
    return wrappers


# функція, яка працює з введеною користувачем строкою
@input_error
def handler(key, entered_str):
    if key == "add" or key == "remove":
        if re.match(r"[a-zA-Z]+", entered_str) is None:
            raise UserNameError()
        if re.match(r"\w+ \+?\d{12}|\w+$", entered_str) is None:
            raise UserNumberError()
        name, phone, other = re.split(" ", entered_str + "  ", maxsplit=2)
        phone = phone.removeprefix("+")
        return dict_of_keys[key](name, phone)

    elif key == "change":
        if re.match(r"[a-zA-Z]\w+", entered_str) is None:
            raise UserNameError()
        if re.match(r"[a-zA-Z]\w+ \+?\d{12}", entered_str) is None:
            raise UserChangingNumberError()
        if re.match(r"[a-zA-Z]\w+ \+?\d{12} \+?\d{12}", entered_str) is None:
            raise UserNewNumberError()
        name, phone, new_phone, other = re.split(" ", entered_str + " ", maxsplit=3)
        phone = phone.removeprefix("+")
        new_phone = new_phone.removeprefix("+")
        return dict_of_keys[key](name, phone, new_phone)

    elif key == "phone":
        if re.match(r"[a-zA-Z]\w+|\+?\d{12}", entered_str) is None:
            raise UserNameError()
        name_or_phone, other = re.split(" ", entered_str + " ", maxsplit=1)
        return dict_of_keys[key](name_or_phone)

    elif key == "delete":
        if re.match(r"[a-zA-Z]\w+", entered_str) is None:
            raise UserNameError()
        name, other = re.split(" ", entered_str + " ", maxsplit=1)
        return dict_of_keys[key](name)

    return dict_of_keys[key]()


# бот виводить у консоль привітання
def hello(*args, **kwargs):
    return "How can I help you?"


# бот зберігає в пам'яті новий контакт або додає номер до існуючого
def add(name, phone):
    record = Record(name)
    is_skipping_add = record.add_new_phone(phone)
    if bool(is_skipping_add):
        return is_skipping_add
    return address_book.add_record(record)


# бот змінює номер існуючого контакту
def change(name, phone, new_phone):
    if name in address_book:
        return address_book[name].change_phone(phone, new_phone)
    else:
        return f"Contact name: '{name}' - not found!"


# бот змінює номер існуючого контакту
def remove_phone(name, phone):
    if name in address_book:
        return address_book[name].remove_phone(phone)
    else:
        return f"Contact name: '{name}' - not found!"


# бот видаляє існуючий контакт
def delete_user(name):
    if name in address_book:
        del address_book[name]
        return f"Contact with name: '{name}' - has been successfully deleted!"
    else:
        return f"Contact name: '{name}' - not found!"


# бот виводить у консоль номер телефону для зазначеного контакту
def phone_user(name_or_phone):
    return address_book.phone_user(name_or_phone)


# бот виводить у консоль список всіх контактів
def show_all(*args, **kwargs):
    return address_book.show_all()


# бот виводить у консоль список всіх команд
def info(*args, **kwargs):
    longest_keys = 0
    for i in dict_of_description.keys():
        if len(i) > longest_keys:
            longest_keys = len(i)
    return "All existing keys:\n\n" \
           "!!! WARNING: THERE SHOULD BE ONLY ONE SPACE BETWEEN ALL WORDS " \
           "AND THE NAME MUST CONTAIN ONLY LATIN LETTERS !!!\n\n" + \
           "\n".join([f"{f'<{key}>':<{longest_keys + 2}} -> " +
                      f"\n{r'    ':_>{longest_keys + 6}}".join(desc)
                      for key, desc in dict_of_description.items()])


# бот віходить із програми
def close(*args, **kwargs):
    sys.exit("Good bye!")


# словник з усіма командами
dict_of_keys = {
    "hello": hello,
    "hi": hello,
    "add": add,
    "change": change,
    "remove": remove_phone,
    "delete": delete_user,
    "phone": phone_user,
    "show all": show_all,
    "info": info,
    "help": info,
    "good bye": close,
    "close": close,
    "exit": close,
    "no": close
}

# словник з описом усіх команд
dict_of_description = {
    "hello": ["Greetings command", "(Need only one command)"],
    "hi": ["Greetings command", "(Need only one command)"],
    "add": ["Command to add a new contact or another number to an existing one",
            "(After the command, write the name of the new contact, and then the phone number of the "
            "form '380888888888'. If you do not add a phone number, the contact will only be created with the "
            "name you specified. If a contact with this name exists, the specified number will be added to it)"],
    "change": ["Command to change the number of an existing contact",
               "(After the command, write the name of the existing contact, then the number you want to change "
               "and then the phone number in the form '380888888888')"],
    "remove": ["Command to remove the number of an existing contact",
               "(After the command, write the name of the existing contact and then the phone number in the "
               "form '380888888888' that you want to remove)"],
    "delete": ["Command to delete an existing contact",
               "(After the command, write the name of the contact you want to delete)"],
    "phone": ["Command to display information about an existing contact",
              "(After the command, write the name of the existing contact whose information you want to know)"],
    "show all": ["Command to display all contacts", "(Need only one command)"],
    "info": ["A helper command that shows all possible commands and their descriptions", "(Need only one command)"],
    "help": ["A helper command that shows all possible commands and their descriptions", "(Need only one command)"],
    "good bye": ["Program exit command", "(Need only one command)"],
    "close": ["Program exit command", "(Need only one command)"],
    "exit": ["Program exit command", "(Need only one command)"],
    "no": ["Program exit command", "(Need only one command)"]
}

# запуск програми
if __name__ == "__main__":
    address_book = AddressBook()
    print("\n-- To see existing commands, type <help> or <info> --\n")
    add('Andrey', "380818888888")
    add('Mary', "380717777777")
    add('Sasha', "380616666666")
    add('Ivan', "")
    add('Maksim', "380515555555")
    main()
