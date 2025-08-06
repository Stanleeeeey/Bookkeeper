from bookkeeper.database.database import Database
from bookkeeper.database import Library, User
from bookkeeper.desktop.utils import render_page, get_arg
from flask import render_template, request, redirect
from bookkeeper.desktop.settings import get_setting, set_setting




def landing_page():
    return render_page("launch.html")

def home(db : Database):

    user = get_setting("user-id")
    if user: 

        return render_page("home.html", user = db.get_user_by_id(user).value, libraries = db.get_libraries_by_user(user))
    return redirect("/create-main-user")


def create_main_user_page(db : Database):
    if request.method == "GET":
        return render_page("forms/main-user.html")
    elif request.method == "POST":
        user_id = db.add_user(User(name = request.form.get("name"), surname = request.form.get("surname")))
        set_setting("user-id", user_id.value)
        return redirect("/home")

def create_library( db: Database):

    if request.method == "GET":
        return render_page("forms/library.html")
    else:

        db.add_library(Library(name = request.form.get("name"), user_id = get_setting("user-id")))
        return redirect("/home")
    
def library(id: int, db : Database):
    print(db.get_books_by_library(id))
    return render_page("library.html", library_id = id, books = db.get_books_by_library(id))