# module for business logic
from database import DataBaseManger

# create an instance for for the DataBaseManager class
db = DataBaseManger('bookmarks.db')


class CreateBookmarksTableCommand:

    def __init__(self):
        pass

    def execute(self):
        db.create_table('bookmarks',
                        {
                            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                            'title': 'TEXT NOT NULL',
                            'url': 'TEXT NOT NULL',
                            'notes': 'TEXT',
                            'date added': 'TEXT NOT NULL'
                        })

