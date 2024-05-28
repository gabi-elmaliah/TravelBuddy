import os 





def get_project_root():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def get_database_path():
    project_root = get_project_root()
    return os.path.join(project_root, 'instance', 'database.db')


