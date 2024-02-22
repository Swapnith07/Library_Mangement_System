import datetime
import streamlit as st
from database import accept_a_request, add_request, create_borrowing_history_table, create_users_table, extend_date, find_book, get_issued_books, get_requests, get_user_requests, get_user_requestss, register_user, authenticate_user, reject_a_request
from database import create_books_table, add_book, get_all_books, delete_book, check_book_existence, get_all_guest_users, get_user_details
from database import create_issued_books_table, issue_book, get_issued_books, return_book
from database import search_books_by_author, search_books_by_genre, search_books_by_isbn, search_books_by_name, get_borrowing_history, create_request_table
from datetime import datetime, timedelta


def user_selection_page():
    st.title("Library Management System")
    create_users_table()
    user_type = st.radio("Select your user type:", [
        "User", "Admin", "Registration"])
    if user_type == "Admin":
        admin_login_page()
    elif user_type == "User":
        guest_login_page()
    elif user_type == "Registration":
        registration_page()


def guest_login_page():
    st.title("User Login")
    username_guest = st.text_input("Username:")
    password_guest = st.text_input("Password:", type="password")

    if st.button("Login as User"):
        if username_guest == "" or password_guest == "":
            st.warning("Username and password cannot be empty.")
        else:
            user_guest = authenticate_user(username_guest, password_guest)

            if user_guest:
                st.success(
                    f"Successfully logged in as " + user_guest[1])
                st.session_state.user_id = 2
                st.session_state.loggedin_id = user_guest[0]

                main_page(st.session_state.user_id)
            else:
                st.error("Invalid username or password. Please try again.")


def admin_login_page():
    st.title("Admin Login")
    username_admin = st.text_input("Username:")
    password_admin = st.text_input("Password:", type="password")

    if st.button("Login"):
        admin_username = "admin"
        admin_password = "123"

        if username_admin == admin_username and password_admin == admin_password:
            st.success(f"Welcome, {admin_username}!")
            st.session_state.user_id = 1
            main_page(st.session_state.user_id)
        else:
            st.error("Invalid username or password. Please try again.")


def registration_page():
    st.title("User Registration")
    new_username = st.text_input("Username:")
    new_password = st.text_input("Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    if st.button("Register"):
        password_validation_result = is_valid_password(new_password)
        if get_user_details(new_username):
            st.warning(
                "Username already exists. Please choose another username.")
        elif new_password == new_username:
            st.warning(
                "Password cannot be the same as the username. Please choose a different password.")
        elif new_password != confirm_password:
            st.warning(
                "Passwords do not match. Please enter the same password in both fields.")
        elif password_validation_result is not True:
            st.warning(password_validation_result)
        else:
            register_user(new_username, new_password, "guest")
            st.success(
                "Registration successful. You can now log in as a guest.")


def is_valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    if not any(char.isalpha() for char in password):
        return "Password must include at least one alphabet character."

    if not any(char.isdigit() for char in password):
        return "Password must include at least one numeric character."

    if not any(char in '@_' for char in password):
        return "Password can have only special characters (@, _) not anything more."

    return True


def main_page(user_id):
    st.title("Library Management System")
    st.sidebar.title("Navigation")

    if user_id == 1:  # Admin
        st.sidebar.subheader("Admin Actions")
        admin_actions = ["Manage Books", "Manage Students", "Requests",
                         "Issue Book", "Return Book", "View Issued Books", "Logout"]
        admin_choice = st.sidebar.selectbox("Select Action", admin_actions)

        if admin_choice == "Manage Books":
            st.sidebar.subheader("Book Actions")
            book_actions = ["Add Book", "View Books",
                            "Delete Book"]
            book_choice = st.sidebar.selectbox(
                "Select Book Action", book_actions)

            if book_choice == "Add Book":
                add_book_page()
            elif book_choice == "View Books":
                view_books_page()
            elif book_choice == "Delete Book":
                delete_book_page()
        elif admin_choice == "Manage Students":
            manage_students_page()
        elif admin_choice == "Requests":
            view_requests()
        elif admin_choice == "Issue Book":
            issue_book_page()
        elif admin_choice == "Return Book":
            return_book_page()
        elif admin_choice == "View Issued Books":
            view_issued_books_page()
        elif admin_choice == "Logout":
            st.session_state.user_id = None
            user_selection_page()

    else:
        st.sidebar.subheader("Guest Actions")
        guest_actions = ["Search Books", "Requested Books",
                         "Borrowing History", "Featured Books", "Logout"]
        guest_choice = st.sidebar.selectbox("Select Action", guest_actions)

        if guest_choice == "Requested Books":
            guest_requested_books_page(st.session_state.loggedin_id)
        elif guest_choice == "Search Books":
            search_books_page()
        elif guest_choice == "Borrowing History":
            borrowing_history_page()
        elif guest_choice == "Featured Books":
            featured_books_page()
        elif guest_choice == "Logout":
            st.session_state.user_id = None
            user_selection_page()


def add_book_page():
    st.title("Add Book")
    title = st.text_input("Title:")
    author = st.text_input("Author:")
    genre = st.text_input("Genre:")
    publication_year = st.text_input("Publication Year:")
    isbn = st.text_input("ISBN:")

    if st.button("Add Book"):
        if title == "" or author == "" or genre == "" or publication_year == "" or isbn == "":
            st.warning(
                "Title, author, genre, publication year, and ISBN cannot be empty.")
        else:
            create_books_table()
            add_book(title, author, genre, publication_year, isbn)
            st.success("Book added successfully.")


def view_books_page():
    st.title("View Books")
    create_books_table()
    books = get_all_books()

    if not books:
        st.info("No books available.")
    else:
        st.write("### Books Information")
        st.table({
            'SNO': [i+1 for i in range(len(books))],
            'BOOK NAME': [book[1] for book in books],
            'Author': [book[2] for book in books],
            'Genre': [book[3] for book in books],
            'Publication Year': [book[4] for book in books],
            'ISBN': [book[5] for book in books]
        })


def delete_book_page():
    st.title("Delete Book")
    book_name = st.text_input("Book Name:")
    isbn_number = st.text_input("ISBN Number:")

    if st.button("Delete Book"):
        if book_name == "" or isbn_number == "":
            st.warning("Book name and ISBN number cannot be empty.")
        else:
            book_exists = check_book_existence(book_name, isbn_number)
            if book_exists:
                delete_book(book_name, isbn_number)
                st.success("Book deleted successfully.")
            else:
                st.error(
                    "Book not found. Please check the book name and ISBN number.")


def manage_students_page():
    st.title("Manage Students")
    create_users_table()
    students = get_all_guest_users()

    if not students:
        st.info("No guest users available.")
    else:
        st.write("### Guest Users Information")
        st.table({
            'SNO': [i + 1 for i in range(len(students))],
            'Username': [user[1] for user in students],
            'Role': [user[3] for user in students]
        })


def issue_book_page():
    st.title("Issue Book")
    student_username = st.text_input("Student Username:")
    book_name = st.text_input("Book Name:")
    isbn_number = st.text_input("ISBN Number:")

    min_date = datetime.now().date()
    max_date = min_date + timedelta(days=3650)
    due_date = st.date_input(
        "Due Date", min_value=min_date, max_value=max_date)

    if st.button("Issue Book"):
        if student_username == "" or book_name == "" or isbn_number == "":
            st.warning(
                "Student username, book name, and ISBN number cannot be empty.")
        else:
            # Check if the student is a guest user
            student = get_user_details(student_username)
            if student and student[3] == 'guest':
                # Check if the book exists and is available for issuance
                book_exists = check_book_existence(book_name, isbn_number)
                if book_exists:
                    # Issue the book
                    issue_book(student[0], book_name, isbn_number,
                               due_date, book_id=book_exists[0])
                    st.success(
                        f"Book '{book_name}' issued to {student_username} with due date {due_date}.")
                else:
                    st.error(
                        "Book not found or not available for issuance. Please check the book name and ISBN number.")
            else:
                st.error(
                    f"User '{student_username}' not found or not a guest user.")


def return_book_page():
    st.title("Return Book")
    username_return = st.text_input("Username:")
    book_name_return = st.text_input("Book Name:")
    isbn_number_return = st.text_input("ISBN Number:")

    if st.button("Return Book"):
        if username_return == "" or book_name_return == "" or isbn_number_return == "":
            st.warning("Username, book name, and ISBN number cannot be empty.")
        else:
            # Check if the book is issued to the specified user
            issued_books = get_issued_books()
            matching_books = [book for book in issued_books if
                              book[0] == book_name_return and book[1] == isbn_number_return and
                              book[3] == username_return]

            if matching_books:
                # Remove the book entry from the issued_books table
                return_book(book_name_return,
                            isbn_number_return, username_return, book_id=matching_books[0][4])
                st.success(f"Book '{book_name_return}' returned successfully.")
            else:
                st.error("Book not found or not issued to the specified user.")


def view_issued_books_page():
    st.title("View Issued Books")
    issued_books = get_issued_books()

    if not issued_books:
        st.info("No books are currently issued to guest users.")
    else:
        st.write("### Issued Books Information")
        st.table({
            'Book Name': [book[0] for book in issued_books],
            'ISBN Number': [book[1] for book in issued_books],
            'Due Date': [book[2] for book in issued_books],
            'Issued To': [book[3] for book in issued_books],
        })


def view_requests():
    st.title("View Requests")
    requests, books = get_requests()
    avl_books = [book[5] for book in books]
    if not requests:
        st.info("No requests available.")
    else:
        st.write("### Requests Information")
        for i, request in enumerate(requests):
            st.write(f"Request {i+1}:")
            st.write(f"Request ID: {request[0]}")
            st.write(f"Book Name: {request[1]}")
            st.write(f"ISBN Number: {request[2]}")
            st.write(f"User ID: {request[3]}")

            if request[4] == "Accepted":
                st.write("Request has already been accepted.")
            elif request[4] == "Rejected":
                st.write("Request has been rejected.")

            elif request[2] in avl_books:
                if request[4] == "Pending":
                    button_key_accept = f"accept_button_{request[0]}"
                    st.button("Accept Request", key=button_key_accept,
                              on_click=accept_request, args=(request[0], request[2]))
                    button_key_reject = f"reject_button_{request[0]}"
                    st.button("Reject Request", key=button_key_reject,
                              on_click=reject_request, args=(request[0],))
                elif request[4] == "Accepted":
                    st.write("Request has already been accepted.")
                elif request[4] == "Rejected":
                    st.write("Request has been rejected.")
            else:
                st.write("Book is not available.")

            st.write(" ---")


def accept_request(request_id, isbn):
    accept_a_request(request_id, isbn)
    st.success("Request accepted successfully.")


def reject_request(request_id):
    reject_a_request(request_id)
    st.success("Request rejected successfully.")


def guest_requested_books_page(user_id):
    st.title("User Requested Books")
    user_requests = get_user_requests(user_id)

    if not user_requests:
        st.info("No requests available.")
    else:
        st.write("### Requests Information")
        st.table({
            'Book Name': [request[1] for request in user_requests],
            'ISBN Number': [request[2] for request in user_requests],
            'Request Status': [request[4] for request in user_requests],
        })


def search_books_page():
    st.title("Search Books")

    search_category = st.selectbox("Select search category:", [
                                   "Book Name", "Author", "Genre", "ISBN"])
    search_query = st.text_input(f"Enter {search_category} to search:")

    if st.button("Search"):
        create_books_table()
        books = search_books(search_category, search_query)
        requests = get_user_requestss(st.session_state.loggedin_id)
        req_books = [book[5] for book in requests]
        
        if not books:
            st.info("No matching books found.")
        else:
            st.write("### Matching Books Information")
            for i, book in enumerate(books):
                st.write(f"#### Book {i + 1}")
                st.write(f"**Book Name:** {book[1]}")
                st.write(f"**Author:** {book[2]}")
                st.write(f"**Genre:** {book[3]}")
                st.write(f"**Publication Year:** {book[4]}")
                st.write(f"**ISBN:** {book[5]}")
                if book[0] in req_books:
                    st.write("This book has alredy been requested")
                else:
                    st.button(f"Request {book[1]}",
                              on_click=req_book, args=(book[5],))


def req_book(isbn):
    book = find_book(isbn)

    if st.session_state.user_id == 2:  # Check if the user is a guest
        requested_books_count = len(
            get_user_requests(st.session_state.loggedin_id))
        request_limit = 3

        if requested_books_count >= request_limit:
            st.warning(
                f"You have already requested {request_limit} books. Please return a book before requesting another.")
        else:
            add_request(book[5], book[1], "Pending",
                        st.session_state.loggedin_id, book[0])
            st.success(f"Request for '{book[1]}' successfully added.")
    else:
        st.error("User not found or not a guest user.")


def search_books(category, query):
    if category == "Book Name":
        return search_books_by_name(query)
    elif category == "Author":
        return search_books_by_author(query)
    elif category == "Genre":
        return search_books_by_genre(query)
    elif category == "ISBN":
        return search_books_by_isbn(query)
    else:
        return []


def can_extend_due_date(due_date):
    current_datetime = datetime.now()
    due_datetime = datetime.combine(
        due_date, datetime.min.time())
    return current_datetime < due_datetime


def borrowing_history_page():
    st.title("Borrowing History")

    if st.session_state.user_id:
        user_id = st.session_state.loggedin_id
        borrowing_history = get_borrowing_history(user_id)
        if not borrowing_history:
            st.info("No borrowing history available.")
        else:
            st.write("### Borrowing History")

            for book in borrowing_history:
                st.write(f"**Book Name:** {book[0]}")
                st.write(f"**ISBN Number:** {book[1]}")
                st.write(f"**Due Date:** {book[2].strftime('%Y-%m-%d')}")
                button_id = f"extend_button_{book[1]}"

                if can_extend_due_date(book[2]):
                    if st.button("Extend Date", button_id, on_click=extend, args=(user_id, book[1])):
                        st.info("Due date extended!")
                else:
                    st.write("Due date cannot be extended.")

                st.write("------")

    else:
        st.warning("User not logged in.")


def extend(user_id, book_id):
    extend_date(user_id, book_id)


def featured_books_page():
    pass


def main():
    st.set_page_config(page_title="app", page_icon="")
    st.sidebar.title("Library Management System")

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id is None:
        user_selection_page()
    elif st.session_state.user_id == 1:
        create_issued_books_table()
        create_borrowing_history_table()
        create_request_table()
        main_page(st.session_state.user_id)
    else:  # Guest
        create_borrowing_history_table()
        main_page(st.session_state.user_id)


if __name__ == "__main__":
    main()
