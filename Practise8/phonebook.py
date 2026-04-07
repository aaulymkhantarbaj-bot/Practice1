from connect import get_connection

conn = get_connection()

if conn:
    cur = conn.cursor()

    print("1 - Search")
    print("2 - Add/Update")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM search_contacts(%s)", (name,))
        print(cur.fetchall())

    elif choice == "2":
        name = input("Name: ")
        phone = input("Phone: ")
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print("Saved!")

    cur.close()
    conn.close()