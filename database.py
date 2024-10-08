from datetime import datetime, timedelta
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
            isbn VARCHAR(20) NOT NULL,
            number_of_copies INT DEFAULT 1,
            UNIQUE KEY isbn_unique (isbn)
    )
    """

    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def add_book(title, author, genre, publication_year, isbn):
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO books (title, author, genre, publication_year, isbn, number_of_copies)
        VALUES (%s, %s, %s, %s, %s, 1)
        ON DUPLICATE KEY UPDATE number_of_copies = number_of_copies + 1
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
    return book


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
            book_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def create_borrowing_history_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
      CREATE TABLE IF NOT EXISTS borrowing_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_name VARCHAR(255) NOT NULL,
            isbn_number VARCHAR(20) NOT NULL,
            due_date DATE NOT NULL,
            CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def issue_book(user_id, book_name, isbn_number, due_date, book_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query_issued_books = """
        INSERT INTO issued_books (user_id, book_name, isbn_number, due_date,book_id) VALUES (%s, %s, %s, %s,%s)
    """
    cursor.execute(insert_query_issued_books,
                   (user_id, book_name, isbn_number, due_date, book_id))

    insert_query_borrowing_history = """
        INSERT INTO borrowing_history (user_id, book_name, isbn_number, due_date) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query_borrowing_history,
                   (user_id, book_name, isbn_number, due_date))

    update_query = """
            UPDATE books
            SET number_of_copies = GREATEST(number_of_copies - 1, 0)
            WHERE isbn = %s
            """
    cursor.execute(update_query, (isbn_number,))

    connection.commit()
    close_database_connection(connection, cursor)


def get_issued_books():
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT ib.book_name, ib.isbn_number, ib.due_date, u.username, ib.book_id
        FROM issued_books ib
        INNER JOIN users u ON ib.user_id = u.id
    """
    cursor.execute(select_query)
    issued_books = cursor.fetchall()

    close_database_connection(connection, cursor)
    return issued_books


def return_book(book_name, isbn_number, username, book_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    delete_query = """
        DELETE FROM issued_books WHERE book_name = %s AND isbn_number = %s AND user_id = (
            SELECT id FROM users WHERE username = %s
        )
    """
    cursor.execute(delete_query, (book_name, isbn_number, username))
    connection.commit()
    change_query = "UPDATE requests SET request_status = 'returned' WHERE book_id = %s"
    cursor.execute(change_query, (book_id,))
    connection.commit()
    update_query = " UPDATE books SET number_of_copies = number_of_copies + 1 WHERE isbn = %s"
    cursor.execute(update_query, (isbn_number,))
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


def get_borrowing_history(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT book_name, isbn_number, due_date
        FROM borrowing_history
        WHERE user_id = %s
    """
    cursor.execute(select_query, (user_id,))
    borrowing_history = cursor.fetchall()

    close_database_connection(connection, cursor)
    return borrowing_history


def create_request_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
       CREATE TABLE IF NOT EXISTS issued_books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                book_name VARCHAR(255) NOT NULL,
                isbn_number VARCHAR(20) NOT NULL,
                due_date DATE NOT NULL,
                book_id INT,
                CONSTRAINT fk_user_id_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (id),
                CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES books (id)
        )
    """

    cursor.execute(create_table_query)
    connection.commit()
    close_database_connection(connection, cursor)


def add_request(isbn_number, book_name, request_status, user_requested, book_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    insert_query = """
      INSERT INTO requests (isbn_number, book_name, request_status,user_requested,book_id) VALUES (%s, %s, %s,%s,%s)"""
    cursor.execute(insert_query, (isbn_number, book_name,
                   request_status, user_requested, book_id))
    connection.commit()
    close_database_connection(connection, cursor)


def find_book(isbn_number):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM books WHERE isbn = %s"
    values = (isbn_number,)

    cursor.execute(query, values)
    book = cursor.fetchone()

    close_database_connection(connection, cursor)
    return book


def get_requests():
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM books WHERE number_of_copies > 0"
    cursor.execute(query)
    books = cursor.fetchall()

    query = "SELECT * FROM requests"
    cursor.execute(query)
    requests = cursor.fetchall()

    close_database_connection(connection, cursor)
    return requests, books


def accept_a_request(request_id, isbn):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "UPDATE requests SET request_status = 'Accepted' WHERE request_id = %s"
    values = (request_id,)
    cursor.execute(query, values)

    update_query = """
        UPDATE books
        SET number_of_copies = GREATEST(number_of_copies - 1, 0)
        WHERE isbn = %s
    """
    cursor.execute(update_query, (isbn,))
    connection.commit()

    query1 = "SELECT * FROM requests WHERE request_id = %s"
    values = (request_id,)
    cursor.execute(query1, values)
    request = cursor.fetchone()
    user_id = int(request[3])
    book_name = request[1]
    book_id = int(request[5])
    isbn_number = int(request[2])
    due_date = datetime.now().date() + timedelta(days=3)

    issue_book(user_id, book_name, isbn_number, due_date, book_id)

    connection.commit()
    close_database_connection(connection, cursor)


def reject_a_request(request_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "UPDATE requests SET request_status = 'Rejected' WHERE request_id = %s"
    values = (request_id,)
    cursor.execute(query, values)

    connection.commit()
    close_database_connection(connection, cursor)


def get_user_requests(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM requests WHERE user_requested = %s"
    values = (user_id,)

    cursor.execute(query, values)
    user_requests = cursor.fetchall()

    close_database_connection(connection, cursor)
    return user_requests


def get_user_requestss(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM requests WHERE user_requested = %s AND request_status IN ('Accepted', 'Pending')"
    values = (user_id,)

    cursor.execute(query, values)
    user_requestss = cursor.fetchall()

    close_database_connection(connection, cursor)
    return user_requestss


def extend_date(user_id, isbn):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "UPDATE borrowing_history SET due_date = DATE_ADD(due_date, INTERVAL 3 DAY) WHERE user_id = %s AND isbn_number = %s"
    values = (user_id, isbn)
    cursor.execute(query, values)

    query2 = "UPDATE issued_books SET due_date = DATE_ADD(due_date, INTERVAL 3 DAY) WHERE user_id = %s AND isbn_number = %s"
    values = (user_id, isbn)
    cursor.execute(query2, values)

    connection.commit()
    close_database_connection(connection, cursor)


def ifcanextend(user_id):
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM requests WHERE user_requested = %s AND request_status = 'returned'"
    values = (user_id,)
    cursor.execute(query, values)
    issued_books = cursor.fetchall()

    return issued_books
