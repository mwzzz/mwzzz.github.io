from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/receive', methods=['POST'])
def handle_raw():
    raw_data = request.data
    try:
        data = request.get_json(force=True)  # 强制解析为 JSON
        print(data)
        # name = data.get('name')
        # age = data.get('age')

        response = {
            "message": "Raw data received and parsed as JSON",
            # "received_name": name,
            # "received_age": age
        }
    except Exception as e:
        response = {
            "message": "Raw data received but could not parse as JSON",
            "raw_data": raw_data.decode('utf-8')
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)