import sys

from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from managers.database_manager import DatabaseManager

if __name__ == '__main__':
    database_manager = DatabaseManager()
    database_manager.create_database()
    database_manager.create_cities()
    database_manager.create_users()
    database_manager.create_tours()
