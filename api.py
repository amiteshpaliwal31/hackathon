from flask import Flask, jsonify
import random, datetime

app = Flask(__name__)

@app.route("/traffic")
def traffic():
    data = {
        "North": {"vehicles": random.randint(10, 40)},
        "South": {"vehicles": random.randint(5, 35)},
        "East": {"vehicles": random.randint(8, 45)},
        "West": {"vehicles": random.randint(6, 30)},
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)
