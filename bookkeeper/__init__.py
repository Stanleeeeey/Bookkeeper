from bookkeeper.database.database import Database
from bookkeeper.api import API
from bookkeeper.desktop import DesktopApp


app = DesktopApp()
app.run()

#api = API(db)
#api.run()