from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_id = len(users) + 1
    new_user = {"id": new_id, "name": data.get("name")}
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)