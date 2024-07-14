import flask
import os
import colorama
import secrets
<<<<<<< HEAD
=======

>>>>>>> 4e405b300223ae048bf69f9e9eccc4b7aeff6c38
import json
from rag_model import rag_model
from vector_db_manager import vector_db_manager

cfg = dict()
with open(os.path.join(os.path.dirname(__file__),"config.json"),"r") as f:
    cfg = json.loads(f)

model_name = cfg["model_name"]
<<<<<<< HEAD
=======

>>>>>>> 4e405b300223ae048bf69f9e9eccc4b7aeff6c38

model = None
db_manager = None

app = flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
app.secret_key = cfg["flask_secret_key"]
<<<<<<< HEAD
=======

>>>>>>> 4e405b300223ae048bf69f9e9eccc4b7aeff6c38

def get_val(d,key,default):
    if key in d:
        return d[key]
    return default

@app.route("/")
def base():
    return flask.send_from_directory("../client/dist", "index.html")

@app.route("/<path:path>")
def home(path):
    return flask.send_from_directory("../client/dist", path)

@app.route("/chat-completion", methods=["POST"])
def chat_completion():
    data = flask.request.json

    if "chat_history" not in data:
        return flask.jsonify({"error": "No chat history provided"}), 400
    
    chat_history = data["chat_history"]

    max_new_tokens = get_val(data,"max_new_tokens",10)
    incomplete_message = get_val(data,"incomplete_message",False)
    temperature = get_val(data,"temperature",0.1)

    model_message,incomplete_message = model.make_prediction(chat_history,incomplete_message,max_new_tokens,temperature)

    return flask.jsonify({"response": model_message,"incomplete_message":incomplete_message})

@app.route("/context-retrieval", methods=["POST"])
def context_retrieval():
    data = flask.request.json
    user_id = flask.session.get("user_id",-1)
    print(f"{user_id} context retrieval")

    if "query" not in data:
        return flask.jsonify({"error": "No query provided"}), 400
    
    query = data["query"]

    top_k = get_val(data,"top_k",5)

    context = db_manager.get_context_as_text(user_id,query,top_k)

    return flask.jsonify({"context": context})

@app.route("/open-session", methods=["POST"])
def open_session():
    user_id = secrets.token_urlsafe(16)
    flask.session["user_id"] = user_id
    print(f"{user_id} open")
    return flask.jsonify({"success": True})

@app.route("/close-session", methods=["POST"])
def close_session():
    print(f"{flask.session.get('user_id')} close")
    os.system(f"rm -r {os.path.dirname(__file__)}/../uploads/{flask.session.get('user_id',-1)}")
    flask.session.pop("user_id",None)
    return flask.jsonify({"success": True})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in flask.request.files:
        return flask.jsonify({"error": "No file part"})
    file = flask.request.files["file"]
    
    if file.filename == "":
        return flask.jsonify({"error": "No file selected"})
    if file:
        user_id = str(flask.session.get("user_id",-1))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], user_id, file.filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

        db_manager.add_user_store(user_id,[filepath])
        return flask.jsonify({"success": True, "filepath": filepath})

    return flask.jsonify({"error": "Something went wrong"}), 500

if __name__ == "__main__":
    model = rag_model(model_name)
    db_manager = vector_db_manager()
    app.run(host="0.0.0.0",port=2137)

    print("\r",end="")
    print(colorama.Fore.GREEN + "Wiping file cache...")
    print(colorama.Style.RESET_ALL,end="")

    os.system(f"rm -r {os.path.dirname(__file__)}/../uploads && mkdir {os.path.dirname(__file__)}/../uploads")

    print(colorama.Fore.GREEN + "Shutting down...")
    print(colorama.Style.RESET_ALL,end="")

    model.unload()

    print(colorama.Fore.GREEN + "Done")
    print(colorama.Style.RESET_ALL,end="")