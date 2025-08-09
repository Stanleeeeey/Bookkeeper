from bookkeeper.database.DTO import Author, Book
from bookkeeper.database.database import Database
from bookkeeper.database import Library, User
from bookkeeper.desktop.utils import render_page
from flask import Response, request, redirect
from bookkeeper.desktop.settings import Settings, get_setting, set_setting

def landing_page():
    return render_page("launch.html")

def home(db : Database):

    user = get_setting("user-id")
    if user: 

        return render_page("home.html", user = db.get_user_by_id(user).value, libraries = db.get_libraries_by_user(user))
    return redirect("/create-main-user")


def add_main_user(db : Database):
    if request.method == "GET":
        return render_page("forms/main-user.html")
    elif request.method == "POST":
        user_id = db.add_user(User(name = request.form.get("name"), surname = request.form.get("surname")))

        set_setting("user-id", user_id.value)
        return redirect("/home")

def add_user(db : Database):
    if request.method == "GET":
        return render_page("forms/user.html")
    elif request.method == "POST":
        user_id = db.add_user(User(name = request.form.get("name"), surname = request.form.get("surname")))
        return redirect("/manage-users")

def add_library( db: Database):

    if request.method == "GET":
        return render_page("forms/library.html")
    else:

        db.add_library(Library(name = request.form.get("name"), owned_by = get_setting("user-id")))
        return redirect("/home")
    
def library(id: int, db : Database):
    library = db.get_library_by_id(id)
    books = db.get_books_by_library(id).value
    books.sort(key  =lambda x: [x.author.surname, x.title])
    return render_page("library.html", library = db.get_library_by_id(id).value, books= books)

def add_book(id:int, db:Database):
    if request.method == "GET":
        return render_page("forms/book.html", library_id = id, authors = db.get_authors())
    else:
        print(request.form.get("author"))
        
        db.add_book(Book(
            title = request.form.get("title"),
            author_id = request.form.get("author"),
            edition = request.form.get("edition"),
            status = 1, #to be added,
            user_id= get_setting("user-id"),
            library_id = id,

        ))
        return redirect(f"/library/{id}")
    
def add_author(id:int, db:Database):
    if request.method == "GET":
        return render_page("forms/author.html", library_id = id)
    else:
        db.add_author(Author(name = request.form.get("name"), surname = request.form.get("surname")))
        return redirect("/home")
    
def settings():
    if request.method == "GET":
        return render_page("settings.html", settings = Settings())
    
def change_setting():
    setting = request.json.get("setting")
    value = request.json.get("value")
    if setting != None and value != None:
        set_setting(setting, value)

        return Response(status=200)
    else:
        return Response(status=403)
    
def book(id: int, db : Database):
    book = db.get_book_by_id(id).value
    return render_page('book.html', book = book, owned_by = db.get_user_by_id(book.user_id).value)

def author(id: int, db:Database):
    
    return render_page("author.html", author = db.get_author_by_id(id).value, books = db.get_books_by_author_id(id))

def users(db:Database):
    return render_page("users.html", users = db.get_users())

def user(id: int, db:Database):
    return render_page("user.html", user = db.get_user_by_id(id).value, books = db.get_books_by_user_id(id))

def edit_book(id:int, db:Database):
    if request.method == "GET":
        return render_page("forms/edit-book.html", book = db.get_book_by_id(id).value, authors = db.get_authors().value, users = db.get_users().value)
    elif request.method == "POST":
        db.edit_book(id, 
            title = request.form.get("title"),
            author_id = request.form.get("author"),
            edition = request.form.get("edition"),
            status = 1, #to be added,
            user_id= get_setting("user-id"),
            library_id = id,

        )
        return redirect(f"/library/{id}")
    
def edit_user(id: int, db:Database):
    print("halo")
    if request.method == "GET":

        return render_page("forms/edit-user.html", user = db.get_user_by_id(id).value)
    elif request.method == "POST":
        user_id = db.edit_user(id, name = request.form.get("name"), surname = request.form.get("surname"))
        return redirect("/manage-users")
    
def edit_author(id:int, db:Database):
    if request.method == "GET":

        return render_page("forms/edit-author.html", author = db.get_author_by_id(id).value)
    elif request.method == "POST":
        user_id = db.edit_author(id, name = request.form.get("name"), surname = request.form.get("surname"))
        return redirect(f"/author/{id}")
    