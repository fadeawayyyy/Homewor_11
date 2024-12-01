import os
import json
import csv
import datetime
import pandas as pd
from unicodedata import category

NOTES_FILE = 'notes.json'
TASKS_FILE = 'tasks.json'
CONTACTS_FILE = 'contacts.json'
FINANCE_FILE = 'finance.json'


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        save_data(file_path, default_data)
        return default_data
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp


class Task:
    def __init__(self, task_id, title, description, done=False, priority="Низкий", due_date=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date


class Contact:
    def __init__(self, contact_id, name, phone=None, email=None):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email


class FinanceRecord:
    def __init__(self, record_id, amount, category, date=None, description=None):
        self.record_id = record_id
        self.amount = amount
        self.category = category
        self.date = date or datetime.datetime.now().strftime("%d-%m-%Y")
        self.description = description


class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        data = load_data(NOTES_FILE, [])
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.__dict__ for note in self.notes]
        save_data(NOTES_FILE, data)

    def add_note(self, title, content):
        note_id = max([note.note_id for note in self.notes], default=0) + 1
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена")

    def list_notes(self):
        if not self.notes:
            print("Список заметок пуст")
            return
        for note in self.notes:
            print(f"{note.note_id}. {note.title} (дата: {note.timestamp})")

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    def view_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f"Заголовок: {note.title}")
            print(f"Содержимое: {note.content}")
            print(f"Дата создания / изменения: {note.timestamp}")
        else:
            print("Заметка не найдена.")

    def edit_note(self, note_id, new_title, new_content):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print("Заметка успешно обновлена.")
        else:
            print("Заметка не найдена.")

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print("Заметка успешно удалена.")
        else:
            print("Заметка не найдена.")

    def import_notes_from_csv(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                self.add_note(row['title'], row['content'])
            print("Заметки успешно импортированы из CSV.")
        except Exception as e:
            print(f"Ошибка при импорте заметок: {e}")

    def export_notes_to_csv(self, csv_file):
        data = [{'id': note.note_id, 'title': note.title, 'content': note.content} for note in self.notes]
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        print("Заметки успешно экспортированы в CSV.")


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data(TASKS_FILE, [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data(TASKS_FILE, data)

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def add_task(self, title, description="", priority="Низкий", due_date=None):
        task_id = max([task.task_id for task in self.tasks], default=0) + 1
        new_task = Task(task_id=task_id,
                        title=title,
                        description=description,
                        priority=priority,
                        due_date=due_date)

        if due_date is None:
            new_task.due_date = datetime.datetime.now().strftime("%d-%m-%Y")

        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача успешно добавлена.")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
            return

        for task in self.tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(f"{task.task_id}. {task.title} - {status} (Приоритет: {task.priority},"
                  f" Срок: {task.due_date})")

    def mark_task_as_done(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print("Задача отмечена как выполненная.")
        else:
            print("Задача не найдена.")

    def edit_task(self, task_id, new_title=None, new_description=None, new_priority=None, new_due_date=None):
        task = self.get_task_by_id(task_id)
        if task:
            if new_title is not None:
                task.title = new_title
            if new_description is not None:
                task.description = new_description
            if new_priority is not None:
                task.priority = new_priority
            if new_due_date is not None:
                task.due_date = new_due_date
            self.save_tasks()
            print("Задача успешно обновлена.")
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Задача успешно удалена.")
        else:
            print("Задача не найдена.")

    def import_tasks_from_csv(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                self.add_task(row['title'], row['description'], row['priority'], row['due_date'])
            print("Задачи успешно импортированы из CSV.")
        except Exception as e:
            print(f"Ошибка при импорте задач: {e}")

    def export_tasks_to_csv(self, csv_file):
        data = [{'id': task.task_id,
                 'title': task.title,
                 'description': task.description,
                 'done': task.done,
                 'priority': task.priority,
                 'due_date': task.due_date} for task in self.tasks]


class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        data = load_data(CONTACTS_FILE, [])
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.__dict__ for contact in self.contacts]
        save_data(CONTACTS_FILE, data)

    def add_contact(self, name, phone=None, email=None):
        contact_id = max([contact.contact_id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id=contact_id, name=name, phone=phone, email=email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Контакт успешно добавлен.")

    def list_contacts(self):
        if not self.contacts:
            print("Список контактов пуст.")
            return
        for contact in self.contacts:
            print(f"{contact.contact_id}. {contact.name} (Телефон: {contact.phone}, Email: {contact.email})")

    def get_contact_by_name(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

    def get_contact_by_phone(self, phone):
        for contact in self.contacts:
            if contact.phone == phone:
                return contact
        return None

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                return contact
        return None

    def edit_contact(self, contact_id, new_name=None, new_phone=None, new_email=None):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            if new_name is not None:
                contact.name = new_name
            if new_phone is not None:
                contact.phone = new_phone
            if new_email is not None:
                contact.email = new_email
            self.save_contacts()
            print("Контакт успешно обновлен.")
        else:
            print("Контакт не найден.")

    def delete_contact(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print("Контакт успешно удален.")
        else:
            print("Контакт не найден.")

    def import_contacts_from_csv(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                self.add_contact(row['name'], row['phone'], row['email'])
            print("Контакты успешно импортированы из CSV.")
        except Exception as e:
            print(f"Ошибка при импорте контактов: {e}")

    def export_contacts_to_csv(self, csv_file):
        data = [{'id': contact.contact_id,
                 'name': contact.name,
                 'phone': contact.phone,
                 'email': contact.email} for contact in self.contacts]



class FinanceManager:
    def __init__(self):
        self.records = []
        self.load_finance_records()

    def load_finance_records(self):
        data = load_data(FINANCE_FILE, [])
        self.records = [FinanceRecord(**record) for record in data]

    def save_finance_records(self):
        data = [record.__dict__ for record in self.records]
        save_data(FINANCE_FILE, data)

    def get_record_by_id(self, record_id):
        for record in self.records:
            if record.record_id == record_id:
                return record
        return

    def add_finance_record(self, amount, category, date=None, description=None):
        record_id = max([record.record_id for record in self.records], default=0) + 1
        new_record = FinanceRecord(record_id=record_id,
                                   amount=amount,
                                   category=category,
                                   date=date,
                                   description=description)
        self.records.append(new_record)
        self.save_finance_records()
        print("Финансовая запись успешно добавлена.")

    def view_filtered_records(self, start_date=None, end_date=None, category=None):
        filtered_records = self.records
        if start_date or end_date:
            filtered_records = [
                record for record in filtered_records
                if (not start_date or record.date >= start_date) and
                   (not end_date or record.date <= end_date)
            ]
        if category:
            filtered_records = [
                record for record in filtered_records
                if record.category.lower() == category.lower()
            ]
        if not filtered_records:
            print("Нет записей, соответствующих заданным критериям.")
            return

        print("Отфильтрованные записи:")
        for record in filtered_records:
            print(f"{record.record_id}. {record.category} - {record.amount} (Дата: {record.date})")

    def generate_report(self, start_date=None, end_date=None):
        filtered_records = [
            record for record in self.records
            if (not start_date or record.date >= start_date) and
               (not end_date or record.date <= end_date)
        ]

        total_income = sum(record.amount for record in filtered_records if record.amount > 0)
        total_expense = sum(record.amount for record in filtered_records if record.amount < 0)

        print(f"Отчет за период с {start_date} по {end_date}:")
        print(f"Общий доход: {total_income}")
        print(f"Общие расходы: {total_expense}")
        print(f"Баланс: {total_income + total_expense}")

    def delete_finance_record(self, record_id):
        record = self.get_record_by_id(record_id)
        if record:
            self.records.remove(record)
            self.save_finance_records()
            print("Финансовая запись успешно удалена.")
        else:
            print("Финансовая запись не найдена.")

    def import_finance_records_from_csv(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                amount = float(row['amount'])
                category = row['category']
                date = row['date']
                description = row['description']
                self.add_finance_record(amount, category, date, description)
            print("Финансовые записи успешно импортированы из CSV.")
        except Exception as e:
            print(f"Ошибка при импорте финансовых записей: {e}")

    def export_finance_records_to_csv(self, csv_file):
        data = [{'id': record.record_id,
                 'amount': record.amount,
                 'category': record.category,
                 'date': record.date,
                 'description': record.description} for record in self.records]


def notes_menu():
    manager = NoteManager()
    while True:
        print("\nУправление заметками:")
        print("1. Добавить новую заметку")
        print("2. Посмотреть список заметок")
        print("3. Просмотреть заметку по ID")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Экспорт заметок в CSV")
        print("7. Импорт заметок из CSV")
        print("8. Назад")

        user_choice = int(input("Введите номер действия: "))

        if user_choice == 1:
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            manager.add_note(title, title)

        elif user_choice == 2:
            manager.list_notes()

        elif user_choice == 3:
            try:
                note_ID = int(input("Введите ID заметки: "))
                manager.view_note(note_ID)
            except ValueError:
                print("Заметка с таким ID не найдена")

        elif user_choice == 4:
            try:
                note_ID = int(input("Введите ID заметки для редактирования: "))
                new_title = input("Введите новый заголовок: ")
                new_content = input("Введите новое содержимое: ")
                manager.edit_note(note_ID, new_title, new_content)
            except ValueError:
                print("Заметка с таким ID не найдена")

        elif user_choice == 5:
            try:
                note_ID = int(input("Введите ID заметки для удаления: "))
                manager.delete_note(note_ID)
            except ValueError:
                print("Заметка с таким ID не найдена")

        elif user_choice == 6:
            csv_file = input("Введите имя CSV-файла для экспорта: ")
            manager.export_notes_to_csv(csv_file)

        elif user_choice == 7:
            csv_file = input("Введите имя CSV-файла для импорта: ")
            manager.import_notes_from_csv(csv_file)

        elif user_choice == 8:
            break
        else:
            print("Нет такого варианта ответа. Попробуйте ещё раз.")


def tasks_menu():
    manager = TaskManager()
    while True:
        print("\nУправление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Экспорт задач в CSV")
        print("7. Импорт задач из CSV")
        print("8. Назад")

        user_choice = int(input("Введите номер действия: "))

        if user_choice == 1:
            title = input("Введите заголовок задачи: ")
            description = input("Введите описание задачи: ")
            priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
            due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
            manager.add_task(title, description, priority, due_date)

        elif user_choice == 2:
            manager.list_tasks()

        elif user_choice == 3:
            try:
                task_ID = int(input("Введите ID задачи для отметки как выполненной: "))
                manager.mark_task_as_done(task_ID)
            except ValueError:
                print("")

        elif user_choice == 4:
            try:
                task_ID = int(input("Введите ID задачи для редактирования: "))
                new_title = input("Введите новый заголовок (оставьте пустым для пропуска): ") or None
                new_description = input("Введите новое описание (оставьте пустым для пропуска): ") or None
                new_priority = input("Выберите новый приоритет (оставьте пустым для пропуска): ") or None
                new_due_date = input("Введите новый срок выполнения (оставьте пустым для пропуска): ") or None
                manager.edit_task(task_ID, new_title=new_title, new_description=new_description,
                                  new_priority=new_priority, new_due_date=new_due_date)
            except ValueError:
                print("")

        elif user_choice == 5:
            try:
                task_ID = int(input("Введите ID задачи для удаления: "))
                manager.delete_task(task_ID)
            except ValueError:
                print("")

        elif user_choice == 6:
            csv_file = input("Введите имя CSV-файла для экспорта задач:")
            manager.export_tasks_to_csv(csv_file)

        elif user_choice == 7:
            csv_file = input('Импортируйте задачи из файла:')
            manager.import_tasks_from_csv(csv_file)

        elif user_choice == 8:
            break
        else:
            print("Нет такого варианта ответа. Попробуйте ещё раз.")


def contacts_menu():
    manager = ContactManager()
    while True:
        print("\nУправление контактами:")
        print("1. Добавить новый контакт")
        print("2. Найти контакта по номеру телефона")
        print("3. Найти контакта по имени")
        print("4. Редактировать контакт")
        print("5. Удалить контакт")
        print("6. Экспорт контактов в CSV")
        print("7. Импорт контактов из CSV")
        print("8. Назад")
        user_choice = int(input("Введите номер действия: "))
        if user_choice == 1:
            name = input("Введите имя контакта: ")
            phone = input("Введите номер телефона контакта: ")
            email = input("Введите адрес электронной почты: ")
            manager.add_contact(name, phone, email)
        elif user_choice == 2:
            phone = input("Введите номер телефона для поиска: ")
            contact = manager.get_contact_by_phone(phone)
            if contact:
                print(f"Найден контакт: {contact.name} (Телефон: {contact.phone}, Email: {contact.email})")
            else:
                print("Контакт не найден.")

        elif user_choice == 3:
            name = input("Введите имя для поиска: ")
            contact = manager.get_contact_by_name(name)
            if contact:
                print(f"Найден контакт: {contact.name} (Телефон: {contact.phone}, Email: {contact.email})")
            else:
                print("Контакт не найден.")

        elif user_choice == 4:
            try:
                contact_id = int(input("Введите ID контакта для редактирования: "))
                new_name = input("Введите новое имя (оставьте пустым для пропуска): ") or None
                new_phone = input("Введите новый номер телефона (оставьте пустым для пропуска): ") or None
                new_email = input("Введите новый адрес электронной почты (оставьте пустым для пропуска): ") or None
                manager.edit_contact(contact_id, new_name, new_phone, new_email)
            except ValueError:
                print("Некорректный ввод ID.")

        elif user_choice == 5:
            try:
                target_contact_id = int(input("Введите ID контакта для удаления: "))
                manager.delete_contact(target_contact_id)
            except ValueError:
                print("Некорректный ввод ID.")

        elif user_choice == 6:
            csv_file = input("Введите имя CSV-файла для экспорта: ")
            manager.export_contacts_to_csv(csv_file)

        elif user_choice == 7:
            csv_file = input("Введите имя CSV-файла для импорта: ")
            manager.import_contacts_from_csv(csv_file)

        elif user_choice == 8:
            break
        else:
            print("Нет такого варианта ответа. Попробуйте ещё раз.")



def finance_menu():
    manager = FinanceManager()
    while True:
        print("\nУправление контактами:")
        print("1. Добавить новую финансовую запись")
        print("2. Найти запись по ID")
        print("3. Просмотреть записи с фильтрацией по дате")
        print("4. Просмотреть записи с фильтрацией по категории")
        print("5. Сгенерировать отчёт за определённый период")
        print("6. Экспорт финансовых записей в CSV")
        print("7. Импорт финансовых записей из CSV")
        print("8. Назад")
        user_choice = int(input("Введите номер действия: "))
        if user_choice == 1:
            amount = float(input("Введите сумму операции"
                               " (положительное число для доходов, отрицательное для расходов): "))
            category = input("Введите категорию операции "
                             "(например, «Еда», «Транспорт», «Зарплата»): ")
            date = input("Введите дату операции в формате 'ДД-ММ-ГГГГ': ")
            description = input("Введите описание операции: ")
            manager.add_finance_record(amount, category, date, description)
        elif user_choice == 2:
            target_id = int(input("Введите ID записи, которую хотите просмотреть: "))
            target_record = manager.get_record_by_id(target_id)
            if target_record:
                print(f"Информация об операции с ID {target_id}:\n"
                      f"{target_record.category}")
            else:
                print("Запись с таким ID не найдена. Попробуйте ещё раз.")
        elif user_choice == 3:
            start_target_date = input("Введите дату начала периода в формате 'ДД-ММ-ГГГГ' или пустую строку (тогда выведется с самого начала): ")
            end_target_date = input("Введите дату конца периода в формате 'ДД-ММ-ГГГГ' или пустую строку (тогда выведется до самого конца): ")
            if start_target_date <= end_target_date:
                manager.view_filtered_records(start_target_date, end_target_date)
            else:
                print("Дата начало не может быть больше даты конца. Попробуйте ещё раз")
        elif user_choice == 4:
            try:
                target_category = input("Введите категорию трат: ")
                manager.view_filtered_records(target_category)
            except ValueError:
                print("--")

        elif user_choice == 5:
            if start_target_date <= end_target_date:
                start_target_date = input("Введите дату начала периода в формате 'ДД-ММ-ГГГГ' или пустую строку (тогда выведется с самого начала): ")
                end_target_date = input("Введите дату конца периода в формате 'ДД-ММ-ГГГГ' или пустую строку (тогда выведется до самого конца): ")
                manager.generate_report(start_target_date, end_target_date)
            else:
                print("Дата начало не может быть больше даты конца. Попробуйте ещё раз")
        elif user_choice == 6:
            csv_file = input("Введите имя CSV-файла для экспорта: ")
            manager.export_finance_records_to_csv(csv_file)
        elif user_choice == 7:
            csv_file = input("Введите имя CSV-файла для импорта")
            manager.import_finance_records_from_csv(csv_file)
        elif user_choice == 8:
            break
        else:
            print("Нет такого варианта ответа. Попробуйте ещё раз.")


def calculator():
    while True:
        expression = input("\nВведите выражение для вычисления (или 'выход' для выхода): ")
        if expression.lower() == "выход":
            break
        try:
            result = eval(expression)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка: {e}")


def main_menu():
    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        user_choice = int(input())
        if user_choice == 1:
            notes_menu()
        elif user_choice == 2:
            tasks_menu()
        elif user_choice == 3:
            contacts_menu()
        elif user_choice == 4:
            finance_menu()
        elif user_choice == 5:
            calculator()
        elif user_choice == 6:
            break


if __name__ == '__main__':
    main_menu()
