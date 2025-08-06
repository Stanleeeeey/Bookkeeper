from bookkeeper.database.database import Database
from bookkeeper.api import API
from bookkeeper.desktop import DesktopApp

db = Database()
#db.add_book(Book(title = "1984", edition = 1, status = 1, author_id = 1, library_id = 1))

app = DesktopApp()
app.run()

#api = API(db)
#api.run()