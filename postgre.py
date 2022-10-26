import psycopg2

self_database = 'datauserinformation'
self_user = 'postgres'
self_password = 'database'


def table_creation(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(60),
            sur_name VARCHAR(60),
            email VARCHAR(60) UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS client_contacts(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES client(id),
            phone VARCHAR(30)
            );           
            """)
        conn.commit()


def new_client(conn, client_name, client_surname, client_email):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO client(name, sur_name, email) VALUES (%s, %s, %s);""",
                    (client_name, client_surname, client_email))
        print(f'Добавлен новый пользователь с именем {client_name}')


def phone_adding(conn, client_id, client_phone):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO client_contacts(client_id, phone) VALUES (%s, %s);""", (client_id, client_phone))
        print(f'Пользователю с id "{client_id}" добавлен телефон - "{client_phone}"')


def client_editor(conn, client_name, client_surname, client_email, client_id):
    with conn.cursor() as cur:
        cur.execute("""UPDATE client SET name = %s, sur_name = %s, email = %s WHERE id = %s;""",
                    (client_name, client_surname, client_email, client_id))
        print(f'Данные пользователя с id "{client_id}" - изменены')


def contacts_remove(conn, contact_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM client_contacts WHERE id=%s;""", (contact_id))
        print(f'Телефоны пользователя с id "{contact_id}" удалены.')


def client_remove(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM client WHERE id=%s;""", (client_id))
        print(f'Пользователь с id "{client_id}" удален.')


def client_search(conn, search):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT name, sur_name, email, phone FROM client c JOIN client_contacts ct ON c.id = ct.client_id WHERE name LIKE '%{search}%' OR sur_name LIKE '%{search}%' OR email LIKE '%{search}%' OR phone LIKE '%{search}%';""")
        return print(f'Данные о пользователе - {cur.fetchall()}')


with psycopg2.connect(database=self_database, user=self_user, password=self_password) as connection:
    try:
        table_creation(connection)
        new_client(connection, 'Илья', 'Иванов', 'ivan@mail.ru')
        new_client(connection, 'Bill', 'Gates', 'billga@mail.ru')
        phone_adding(connection, '1', '+7(800)777-55-11')
        client_editor(connection, "Михаил", "Кулябин", "miha@mail.ru", "1")
        client_search(connection, 'Михаил')
        contacts_remove(connection, '2')
        client_remove(connection, '2')
    except psycopg2.Error as er:
        print(f'ERROR: {er}')
connection.close()