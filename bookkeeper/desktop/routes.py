"""every endpoint of the application"""
from flask import Response, request, redirect

from bookkeeper.database.database import Database
from bookkeeper.database import Library, User, Author, Book
from bookkeeper.desktop.utils import render_page
from bookkeeper.desktop.settings import Settings, get_setting, set_setting

def launch_page():
    """returns launch page"""

    return render_page("launch.html")

def home_page(db : Database):
    """returns home page with list of libraries"""

    user = get_setting("user-id")
    if user:
        return render_page(
            "home.html",
            user = db.get_user_by_id(user).value,
            libraries = db.get_libraries()
        )
    return redirect("/create-main-user")


def add_main_user_page(db : Database):
    """form for adding main user of the app"""

    if request.method == "GET":
        return render_page("forms/main-user.html")
    elif request.method == "POST":
        user_id = db.add_user(
            User(
                name = request.form.get("name"),
                surname = request.form.get("surname")
            )
        )

        set_setting("user-id", user_id.value)
        return redirect("/home")

def add_user_page(db : Database):
    """add a user form"""

    if request.method == "GET":
        return render_page("forms/user.html")
    elif request.method == "POST":
        db.add_user(
            User(
                name = request.form.get("name"),
                surname = request.form.get("surname")
            )
        )
        return redirect("/manage-users")

def add_library_page( db: Database):
    """add a library form"""

    if request.method == "GET":
        return render_page("forms/library.html")
    else:
        db.add_library(
            Library(
                name = request.form.get("name"),
                owned_by = get_setting("user-id")
        ))

        return redirect("/home")

def library_page(library_id: int, db : Database):
    """returns a page with all the books in the library"""

    print(library_id)

    library = db.get_library_by_id(library_id).value
    books = db.get_books_by_library(library_id).value
    books.sort(key  =lambda x: [x.author.surname, x.title])
    return render_page("library.html", library = library, books= books)

def add_book_page(library_id:int, db:Database):
    """returns a form to add a book"""

    if request.method == "GET":
        return render_page("forms/book.html", library_id = library_id, authors = db.get_authors())
    else:
        print(request.form.get("author"))

        db.add_book(Book(
            title = request.form.get("title"),
            author_id = request.form.get("author"),
            edition = request.form.get("edition"),
            status = 1, #to be added,
            user_id= get_setting("user-id"),
            library_id = library_id,

        ))
        return redirect(f"/library/{library_id}")

def add_author_page(db:Database):
    """Add author, library_id user to return to previous url"""

    if request.method == "GET":
        return render_page("forms/author.html")
    else:
        db.add_author(
            Author(
                name = request.form.get("name"),
                surname = request.form.get("surname")
            )
        )
        return redirect("/home")

def settings_page():
    """returns page to control settings"""

    if request.method == "GET":
        return render_page("settings.html", settings = Settings())

def change_setting():
    """endpoint to change settings without submitting form, accessed by js"""

    setting = request.json.get("setting")
    value = request.json.get("value")
    if setting is not None and value is not None:
        set_setting(setting, value)

        return Response(status=200)
    else:
        return Response(status=403)

def book_page(book_id: int, db : Database):
    """returns a page with book information"""

    book = db.get_book_by_id(book_id).value
    return render_page('book.html', book = book, owned_by = db.get_user_by_id(book.user_id).value)

def author_page(author_id: int, db:Database):
    """returns page with author and all theirs books"""

    return render_page(
        "author.html",
        author = db.get_author_by_id(author_id).value,
        books = db.get_books_by_author_id(author_id)
    )

def users_page(db:Database):
    """returns page with list of all users"""

    return render_page("users.html", users = db.get_users())

def user_page(user_id: int, db:Database):
    """returns user and all books they have"""

    return render_page(
        "user.html",
        user = db.get_user_by_id(user_id).value,
        books = db.get_books_by_user_id(user_id)
    )

def edit_book_page(book_id:int, db:Database):
    """edits book with a given id"""

    if request.method == "GET":

        return render_page(
            "forms/edit-book.html",
            book = db.get_book_by_id(book_id).value,
            authors = db.get_authors().value,
            users = db.get_users().value
        )

    elif request.method == "POST":
        db.edit_book(
            book_id,
            title = request.form.get("title"),
            author_id = request.form.get("author"),
            edition = request.form.get("edition"),
            status = 1, #to be added,
            user_id= get_setting("user-id"),
            library_id = request.form.get("library_id"),
        )
        return redirect(f"/library/{request.form.get('library_id')}")

def edit_user_page(user_id: int, db:Database):
    """edits user with a given user_id"""

    if request.method == "GET":

        return render_page(
            "forms/edit-user.html",
            user = db.get_user_by_id(user_id).value
        )

    elif request.method == "POST":
        db.edit_user(user_id, name = request.form.get("name"), surname = request.form.get("surname"))
        return redirect("/manage-users")

def edit_author_page(author_id:int, db:Database):
    """edits author with a given id"""

    if request.method == "GET":

        return render_page(
            "forms/edit-author.html",
            author = db.get_author_by_id(author_id).value
        )

    elif request.method == "POST":
        db.edit_author(author_id, name = request.form.get("name"), surname = request.form.get("surname"))
        return redirect(f"/author/{author_id}")
