from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

notes = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/status")
def status():
    return render_template("status.html")

@app.route("/health", methods=["GET"])
def health():
    return "Backend is healthy", 200

@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Note text is required"}), 400

    note = {
        "id": len(notes) + 1,
        "text": data["text"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(note)
    return jsonify({"message": "Note added", "note": note})

@app.route("/notes/clear", methods=["POST"])
def clear_notes():
    notes.clear()
    return jsonify({"message": "All notes cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
