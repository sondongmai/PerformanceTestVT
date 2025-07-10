from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/user", methods=["POST"])
def create_user():
    _ = request.json
    return Response(status=201)

if __name__ == "__main__":
    # Tắt debug + bật threaded để xử lý song song
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)