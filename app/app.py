import json
from model import Digital_clone
from flask import Flask, request, jsonify


app = Flask(__name__, static_url_path="")


digital_clone = Digital_copy()


@app.route("/predict", methods=['POST'])
def predict():
    data = request.get_json(force=True)

    input = data['input']
    temperature = data['temperature']

    output = digital_clone.generate(text, temperature)
    return jsonify({"output": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
