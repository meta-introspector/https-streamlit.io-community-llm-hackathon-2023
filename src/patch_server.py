import streamlit.web.server.server
import inspect
import os.path
target = "backups"
#st.write(inspect.getsourcefile(streamlit.web.server.server))
INJECT="""
import streamlit.web.server.inject
"""

def patch_server():
    #copy a backup of server code
    target = inspect.getsourcefile(streamlit.web.server.server)
    inject_target = target.replace("/server.py","/inject.py",)
    backups = "backups"
    backup  = os.path.join(backups,"server_old.py")
    inject_source  = os.path.join(backups,"inject.py")
    if not os.path.exists(backup):
        with open(backup,"w") as fo:
            with open(target,"r") as fi:
                fo.write(fi.read())
    # patch the file
    with open(backup,"r") as fi:
        with open(target,"w") as fo:
            fo.write(fi.read())
            fo.write(INJECT)
            
    # write the injection target, safer
    with open(inject_target,"w") as fo:
        with open(inject_source,"r") as fi:
            fo.write(fi.read())
