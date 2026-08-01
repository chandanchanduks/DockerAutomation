from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Fake Android Device is running!"

@app.route("/status")
def status():
    return {
        "device": "Android Emulator",
        "wifi": "Connected",
        "battery": 82
    }

app.run(host="0.0.0.0", port=5000)