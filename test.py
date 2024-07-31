import requests
import json

url = "
params = {
    "user_id": "123456",
    "message_type": "email"
}

response = requests.get(url, params=params)
data = response.json()

messages = data["messages"]
for message in messages:
    subject = message["subject"]
    content = message["content"]
    # 进行消息处理操作
    print(subject)
    print(content)