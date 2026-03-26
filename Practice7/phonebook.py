# phonebook.py
import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_contact(first_name, last_name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
        (first_name, last_name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename='contacts.csv'):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
                (row['first_name'], row['last_name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()

def get_contacts_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM contacts WHERE first_name ILIKE %s OR last_name ILIKE %s",
        (f"%{name}%", f"%{name}%")
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def update_contact(old_name, new_name=None, new_phone=None):
    conn = get_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET first_name=%s WHERE first_name=%s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE contacts SET phone=%s WHERE first_name=%s", (new_phone, old_name))
    conn.commit()
    cur.close()
    conn.close()

def delete_contact(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()
    if name:
        cur.execute("DELETE FROM contacts WHERE first_name=%s", (name,))
    if phone:
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()

# Консольдік меню
def menu():
    create_table()
    while True:
        print("\n--- PhoneBook ---")
        print("1. Контакт қосу")
        print("2. CSV-тен импорт")
        print("3. Контактілерді іздеу")
        print("4. Контакт жаңарту")
        print("5. Контакт өшіру")
        print("6. Шығу")
        choice = input("Таңдаңыз (1-6): ")

        if choice == "1":
            first = input("Аты: ")
            last = input("Тегі: ")
            phone = input("Телефон: ")
            insert_contact(first, last, phone)
            print("Контакт қосылды!")
        elif choice == "2":
            insert_from_csv()
            print("CSV импортталды!")
        elif choice == "3":
            name = input("Іздеу үшін аты немесе тегі: ")
            results = get_contacts_by_name(name)
            for r in results:
                print(f"ID:{r[0]} | {r[1]} {r[2]} | {r[3]}")
        elif choice == "4":
            old = input("Ескі аты: ")
            new_name = input("Жаңа аты (болмаса Enter): ")
            new_phone = input("Жаңа телефон (болмаса Enter): ")
            update_contact(old, new_name or None, new_phone or None)
            print("Контакт жаңартылды!")
        elif choice == "5":
            name = input("Өшіру үшін аты (болмаса Enter): ")
            phone = input("Телефон нөмірі (болмаса Enter): ")
            delete_contact(name or None, phone or None)
            print("Контакт өшірілді!")
        elif choice == "6":
            break
        else:
            print("Қате таңдау!")

if __name__ == "__main__":
    menu()