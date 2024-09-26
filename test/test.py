from flask import Flask, request, jsonify, make_response
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    # filename='app.log',  # 指定日志文件名
    # filemode='a',        # 追加模式
    # format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

app = Flask(__name__)


@app.route('/receive', methods=['POST'])
def receive_data():
    # 获取请求中的 JSON 数据
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    # 检查是否成功获取到 JSON 数据
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    print(data)

    # 验证数据
    # if 'name' not in data or 'age' not in data:
    #     return jsonify({"error": "Missing required fields: name and/or age"}), 400

    # 提取数据
    # name = data.get('name')
    # age = data.get('age')

    # 记录接收到的数据
    # logging.info(f"Received data: Name: {name}, Age: {age}")

    # 返回响应
    response = {
        "message": "Data received successfully",
        # "received_name": name,
        # "received_age": age
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)