import mysql.connector


def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Swapnith@07",
        database="library"
    )


def close_database_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_users_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def register_user(username, password, role):
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO users (username, password, role) VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (username, password, role))
    connection.commit()
    close_database_connection(connection, cursor)


def authenticate_user(username, password):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM users WHERE username = %s AND password = %s
    """
    cursor.execute(select_query, (username, password))
    user = cursor.fetchone()

    close_database_connection(connection, cursor)
    return user


def get_user_details(username):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM users WHERE username = %s
    """
    cursor.execute(select_query, (username,))
    user_details = cursor.fetchone()

    close_database_connection(connection, cursor)
    return user_details


def create_books_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            genre VARCHAR(255) NOT NULL,
            publication_year INT,
            isbn VARCHAR(20) UNIQUE
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def add_book(title, author, genre, publication_year, isbn):
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO books (title, author, genre, publication_year, isbn) VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (title, author,
                   genre, publication_year, isbn))
    connection.commit()
    close_database_connection(connection, cursor)


def get_all_books():
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books
    """
    cursor.execute(select_query)
    books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return books


def delete_book(book_name, isbn_number):
    connection = get_database_connection()
    cursor = connection.cursor()

    delete_query = """
        DELETE FROM books WHERE title = %s AND isbn = %s
    """
    cursor.execute(delete_query, (book_name, isbn_number))
    connection.commit()
    close_database_connection(connection, cursor)


def check_book_existence(book_name, isbn_number):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books WHERE title = %s AND isbn = %s
    """
    cursor.execute(select_query, (book_name, isbn_number))
    book = cursor.fetchone()

    close_database_connection(connection, cursor)
    return bool(book)


def get_all_guest_users():
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM users WHERE role = 'guest'
    """
    cursor.execute(select_query)
    guest_users = cursor.fetchall()

    close_database_connection(connection, cursor)
    return guest_users


def create_issued_books_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS issued_books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_name VARCHAR(255) NOT NULL,
            isbn_number VARCHAR(20) NOT NULL,
            due_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def issue_book(user_id, book_name, isbn_number, due_date):
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO issued_books (user_id, book_name, isbn_number, due_date) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (user_id, book_name, isbn_number, due_date))
    connection.commit()
    close_database_connection(connection, cursor)


def get_issued_books():
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT ib.book_name, ib.isbn_number, ib.due_date, u.username
        FROM issued_books ib
        INNER JOIN users u ON ib.user_id = u.id
    """
    cursor.execute(select_query)
    issued_books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return issued_books


def return_book(book_name, isbn_number, username):
    connection = get_database_connection()
    cursor = connection.cursor()

    delete_query = """
        DELETE FROM issued_books WHERE book_name = %s AND isbn_number = %s AND user_id = (
            SELECT id FROM users WHERE username = %s
        )
    """
    cursor.execute(delete_query, (book_name, isbn_number, username))
    connection.commit()
    close_database_connection(connection, cursor)


def search_books_by_name(query):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books WHERE title LIKE %s
    """
    cursor.execute(select_query, (f"%{query}%",))
    books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return books


def search_books_by_author(query):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books WHERE author LIKE %s
    """
    cursor.execute(select_query, (f"%{query}%",))
    books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return books


def search_books_by_genre(query):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books WHERE genre LIKE %s
    """
    cursor.execute(select_query, (f"%{query}%",))
    books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return books


def search_books_by_isbn(query):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books WHERE isbn LIKE %s
    """
    cursor.execute(select_query, (f"%{query}%",))
    books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return books


def search_books_by_publication_year(query):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM books WHERE publication_year LIKE %s
    """
    cursor.execute(select_query, (f"%{query}%",))
    books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return books


def get_borrowing_history(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT book_name, isbn_number, due_date
        FROM issued_books
        WHERE id = %s
    """
    cursor.execute(select_query, (user_id,))
    borrowing_history = cursor.fetchall()

    close_database_connection(connection, cursor)
    return borrowing_history
