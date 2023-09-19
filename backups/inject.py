#begin inject
from streamlit.web.server.server import Server

server_create_app_backup = Server._create_app
def server_create_app_hack(self):
    app = server_create_app_backup(self)
    print("PATCH",app)
    return app
Server._create_app=server_create_app_hack
