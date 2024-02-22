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