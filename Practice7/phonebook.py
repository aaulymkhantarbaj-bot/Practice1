# phonebook.py
import csv
import os
from connect import get_connection

CSV_FILE = "contacts.csv"

# Егер CSV файл жоқ болса, оны жасаймыз
def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["name","phone"])
            writer.writeheader()
            # Мысал үшін бірнеше жазба қосуға болады
            writer.writerow({"name":"Alice","phone":"87012345678"})
            writer.writerow({"name":"Bob","phone":"87771234567"})
            writer.writerow({"name":"Charlie","phone":"87098765432"})
        print(f"{CSV_FILE} файлы жасалды.")

# Кесте жасау
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Кесте дайын.")

# CSV файлдан деректер енгізу
def import_from_csv(file_path=CSV_FILE):
    ensure_csv_exists()  # Файл бар екеніне көз жеткіземіз
    conn = get_connection()
    cur = conn.cursor()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()
    print("CSV файлдан деректер импортталды.")

# Консольдан деректер енгізу
def add_contact():
    name = input("Аты: ")
    phone = input("Телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт қосылды.")

# Контакт жаңарту
def update_contact():
    id = input("Жаңартқыңыз келетін контакт ID: ")
    new_name = input("Жаңа аты (қалдыру үшін Enter): ")
    new_phone = input("Жаңа телефон (қалдыру үшін Enter): ")
    
    conn = get_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET name = %s WHERE id = %s", (new_name, id))
    if new_phone:
        cur.execute("UPDATE contacts SET phone = %s WHERE id = %s", (new_phone, id))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт жаңартылды.")

# Контакт іздеу
def search_contacts():
    keyword = input("Іздеу сөзін енгізіңіз (аты немесе телефоны): ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, phone FROM contacts WHERE name ILIKE %s OR phone ILIKE %s",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Контакт жою
def delete_contact():
    id = input("Жою үшін контакт ID: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт жойылды.")

# Мәзір
def menu():
    while True:
        print("\n--- PhoneBook ---")
        print("1. Контакт қосу (консольдан)")
        print("2. CSV файлдан импорт")
        print("3. Контакт жаңарту")
        print("4. Контакт іздеу")
        print("5. Контакт жою")
        print("6. Шығу")
        choice = input("Таңдауыңыз: ")
        if choice == '1':
            add_contact()
        elif choice == '2':
            import_from_csv()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            break
        else:
            print("Қате таңдау.")

if __name__ == "__main__":
    create_table()
    ensure_csv_exists()  # Бағдарлама басталғанда файл бар екеніне көз жеткіземіз
    menu()