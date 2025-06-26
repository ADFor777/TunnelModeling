import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
from openai import OpenAI

app = Flask(__name__)

GPT_MODEL = "qwen-plus"

load_dotenv('.env')
# 获取环境变量
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=OPENAI_API_KEY,
    # 填写DashScope SDK的base_url
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 全局变量存储对话历史
conversation_history = [
    {
        "role": "assistant",
        "content": """你叫小雨是一个AI助手。你需要与用户进行持续的多轮对话，直到用户明确表示想要结束对话。

对话规则：
1. 请以冷酷，不耐烦的语气回答问题；
2. 如果用户希望你帮他发送一封邮件，如果他没有提供发件人邮箱、收件人邮箱、邮件主题和邮件内容，请提示用户提供这些信息；
3. 如果用户希望你帮他查找某个点距离数据库中最近的点，请提示用户提供目标点的坐标，格式为 [x, y]；
4. 如果用户希望你解析隧道工程参数，请提示用户提供隧道项目的详细描述；
5. 在每轮对话中，保持对话的连贯性，记住之前的对话内容;
6. 如果用户表达以下意图，请结束对话：
   - 明确说"再见"、"拜拜"、"结束对话"等告别语
   - 表达"我要走了"、"对话到此为止"等结束意图
   - 使用"exit"、"quit"等退出命令"""
    }
]


def find_point(target_point, num_data):
    """
    查找距离目标点最近的数据点并可视化

    Args:
        target_point (tuple): 目标点坐标 (x, y)
        num_data (list): 数据点列表，每个元素为 [x, y] 格式

    Returns:
        tuple: 最近点的坐标和图片的base64编码
    """
    # 将数据转换为numpy数组
    data_points = np.array(num_data)
    target = np.array([target_point])

    # 计算所有点到目标点的距离
    distances = cdist(data_points, target)

    # 找到最近点的索引
    nearest_idx = np.argmin(distances)
    nearest_point = data_points[nearest_idx]

    # 创建散点图
    plt.figure(figsize=(10, 8))

    # 绘制数据库中的点（蓝色）
    plt.scatter(data_points[:, 0], data_points[:, 1],
                c='blue', label='Database Point')

    # 绘制目标点（红色）
    plt.scatter(target_point[0], target_point[1],
                c='red', label='Target Point')

    # 绘制最近点（黄色星号）
    plt.scatter(nearest_point[0], nearest_point[1],
                c='yellow', marker='*', s=200, label='Nearest point')

    plt.title('Data Point Distribution Chart')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    # 将图片转换为base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return tuple(nearest_point), image_base64


def parse_tunnel_specification(input_text, strict_mode=False, unit_preference="auto"):
    """
    解析隧道工程参数

    Args:
        input_text (str): 自然语言描述的隧道项目
        strict_mode (bool): 是否启用严格验证模式
        unit_preference (str): 首选单位系统

    Returns:
        dict: 结构化的隧道工程参数
    """
    # 初始化结果字典
    result = {
        "hasTunnelLength": None,
        "hasGeologicalCondition": None,
        "hasHydroCondition": None,
        "hasSoilType": None,
        "tunnelType": None,
        "hasTunnelDiameter": None
    }

    # 简单的关键词匹配和数值提取
    text = input_text.lower()

    # 提取隧道长度
    import re
    length_patterns = [
        r'长度.*?(\d+(?:\.\d+)?)\s*(?:米|m|公里|km)',
        r'(\d+(?:\.\d+)?)\s*(?:米|m|公里|km).*?长',
        r'length.*?(\d+(?:\.\d+)?)\s*(?:m|meter|km|kilometer)',
        r'(\d+(?:\.\d+)?)\s*(?:m|meter|km|kilometer).*?long'
    ]
    for pattern in length_patterns:
        match = re.search(pattern, text)
        if match:
            length_value = float(match.group(1))
            # 如果是公里，转换为米
            if 'km' in match.group(0) or '公里' in match.group(0):
                length_value *= 1000
            result["hasTunnelLength"] = length_value
            break

    # 提取隧道直径
    diameter_patterns = [
        r'直径.*?(\d+(?:\.\d+)?)\s*(?:米|m)',
        r'(\d+(?:\.\d+)?)\s*(?:米|m).*?直径',
        r'diameter.*?(\d+(?:\.\d+)?)\s*(?:m|meter)',
        r'(\d+(?:\.\d+)?)\s*(?:m|meter).*?diameter'
    ]
    for pattern in diameter_patterns:
        match = re.search(pattern, text)
        if match:
            result["hasTunnelDiameter"] = float(match.group(1))
            break

    # 围岩等级判断 - 统一使用罗马数字
    rock_grade_map = {
        "ⅰ": "I", "i": "I", "1": "I", "一": "I",
        "ⅱ": "II", "ii": "II", "2": "II", "二": "II",
        "ⅲ": "III", "iii": "III", "3": "III", "三": "III",
        "ⅳ": "IV", "iv": "IV", "4": "IV", "四": "IV",
        "ⅴ": "V", "v": "V", "5": "V", "五": "V",
        "ⅵ": "VI", "vi": "VI", "6": "VI", "六": "VI"
    }

    for grade_key, grade_value in rock_grade_map.items():
        if f"围岩{grade_key}" in text or f"等级{grade_key}" in text or f"grade {grade_key}" in text:
            result["hasGeologicalCondition"] = grade_value
            break

    # 水文条件判断 - 使用英文值
    if "富水" in text or "water-rich" in text or "rich water" in text:
        result["hasHydroCondition"] = "water-rich"
    elif "干燥" in text or "干旱" in text or "dry" in text:
        result["hasHydroCondition"] = "dry"

    # 土壤类型判断 - 使用英文值
    if "强风化" in text or "强土" in text or "strong soil" in text or "strong rock" in text:
        result["hasSoilType"] = "StrongSoil"
    elif "弱风化" in text or "弱土" in text or "weak soil" in text or "weak rock" in text:
        result["hasSoilType"] = "WeakSoil"
    elif "中等风化" in text or "中等土" in text or "medium soil" in text or "medium rock" in text:
        result["hasSoilType"] = "MediumSoil"

    # 隧道类型判断 - 使用英文值
    if "山岭" in text or "山区" in text or "mountain" in text:
        result["tunnelType"] = "MountainTunnelProject"
    elif "水下" in text or "海底" in text or "underwater" in text or "subsea" in text:
        result["tunnelType"] = "UnderwaterTunnelProject"
    elif "浅埋" in text or "shallow" in text:
        result["tunnelType"] = "ShallowTunnelProject"
    elif "深埋" in text or "deep" in text:
        result["tunnelType"] = "DeepTunnelProject"

    return result


tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            # 因为获取当前时间无需输入参数，因此parameters为空字典
            "parameters": {},
        },
    },
    # 工具2 发送邮件
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to the specified email with the subject and content",
            "parameters": {
                "type": "object",
                "properties": {
                    "FromEmail": {
                        "type": "string",
                        "description": "The email address, eg., rememeber0101@126.com",
                    },
                    "Subject": {
                        "type": "string",
                        "description": "Subject of the email",
                    },
                    "Body": {
                        "type": "string",
                        "description": "The content of the email",
                    },
                    "Recipients": {
                        "type": "string",
                        "description": "The recipients' email addresses",
                    }
                },
                "required": ["FromEmail", "Subject", "Body", "Recipients"],
            },
        }
    },
    # 工具3 查找某点距离数据库中最近的点
    {
        "type": "function",
        "function": {
            "name": "find_point",
            "description": "Find the nearest point in the database to the given coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_point": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "The target point coordinates [x, y]",
                    }
                },
                "required": ["target_point"],
            },
        }
    },
    # 工具4 解析隧道工程参数
    {
        "type": "function",
        "function": {
            "name": "parse_tunnel_specification",
            "description": "Extract and structure tunnel engineering parameters from natural language descriptions",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_text": {
                        "type": "string",
                        "description": "Natural language description of the tunnel project"
                    },
                    "strict_mode": {
                        "type": "boolean",
                        "default": False,
                        "description": "Enable strict validation for parameter values (default: false)"
                    },
                    "unit_preference": {
                        "type": "string",
                        "enum": ["metric", "imperial", "auto"],
                        "default": "auto",
                        "description": "Preferred unit system for numerical values (default: auto)"
                    }
                },
                "required": ["input_text"]
            },
            "returns": {
                "type": "object",
                "properties": {
                    "hasTunnelLength": {
                        "type": "number",
                        "description": "Tunnel length in meters"
                    },
                    "hasGeologicalCondition": {
                        "type": "string",
                        "enum": ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ"],
                        "description": "Surrounding rock grade according to Chinese classification standard"
                    },
                    "hasHydroCondition": {
                        "type": "string",
                        "enum": ["dry", "water-rich"],
                        "description": "Hydrogeological condition category"
                    },
                    "hasSoilType": {
                        "type": "string",
                        "enum": ["Medium Soil", "Strong soil", "WeakSoil"],
                        "description": "Dominant soil or rock type"
                    },
                    "tunnelType": {
                        "type": "string",
                        "enum": ["MountainTunnelProject", "UnderwaterTunnelProject", "ShallowTunnelProject", "DeepTunnelProject"],
                        "description": "Tunnel project type classification"
                    },
                    "hasTunnelDiameter": {
                        "type": "number",
                        "description": "Tunnel diameter in meters (circular tunnels) or hydraulic diameter (non-circular)"
                    }
                }
            }
        }
    }
]

# 查询当前时间的工具。返回结果示例："当前时间：2024-04-15 17:15:18。"


def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def send_email(sender_email, sender_authorization_code, recipient_email, subject, body):
    # 创建 MIMEMultipart 对象
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # 创建 SMTP_SSL 会话
    with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
        server.login(sender_email, sender_authorization_code)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history

    data = request.json
    user_message = data.get('message', '')

    # 检查用户是否想要结束对话
    if user_message.lower() in ['再见', '拜拜', '结束对话', 'exit', 'quit', '我要走了', '对话到此为止']:
        return jsonify({
            'response': '哼~我也不是很想和你聊天，再见！',
            'end_conversation': True
        })

    conversation_history.append({"role": "user", "content": user_message})

    response = chat_completion_request(
        messages=conversation_history,
        tools=tools
    )

    if content := response.choices[0].message.content:
        conversation_history.append({"role": "assistant", "content": content})
        return jsonify({
            'response': content,
            'end_conversation': False
        })
    else:
        fn_name = response.choices[0].message.tool_calls[0].function.name
        fn_args = response.choices[0].message.tool_calls[0].function.arguments

        if fn_name == "send_email":
            try:
                args = json.loads(fn_args)
                response = {
                    'response': f"邮件内容如下：\n发件人: {args['FromEmail']}\n收件人: {args['Recipients']}\n主题: {args['Subject']}\n内容: {args['Body']}\n\n请确认是否发送？",
                    'end_conversation': False,
                    'action': 'confirm_email',
                    'email_data': args
                }
                return jsonify(response)
            except Exception as e:
                return jsonify({
                    'response': f"发送邮件时出错：{str(e)}",
                    'end_conversation': False
                })
        elif fn_name == "find_point":
            try:
                args = json.loads(fn_args)
                target_point = tuple(args['target_point'])
                nearest_point, image_base64 = find_point(
                    target_point, num_data)
                response = f"距离点{target_point}最近的点是{nearest_point}。"
                conversation_history.append(
                    {"role": "assistant", "content": response})
                return jsonify({
                    'response': response,
                    'end_conversation': False,
                    'image': image_base64
                })
            except Exception as e:
                return jsonify({
                    'response': f"查找最近点时出错：{str(e)}",
                    'end_conversation': False
                })
        elif fn_name == "get_current_time":
            try:
                now_time = get_current_time()
                response = f"函数输出信息：{now_time}"
                print(f"【AI】: {response}")
                conversation_history.append(
                    {"role": "assistant", "content": response})
                # 返回当前时间
                return jsonify({
                    'response': response,
                    'end_conversation': False,
                })

            except Exception as e:
                print(f"查找时间出错：{e}")
                conversation_history.append(
                    {"role": "assistant", "content": "抱歉，无法查找当前时间！"})
                return jsonify(response)
        elif fn_name == "parse_tunnel_specification":
            try:
                args = json.loads(fn_args)
                input_text = args['input_text']
                strict_mode = args.get('strict_mode', False)
                unit_preference = args.get('unit_preference', 'auto')

                # 调用隧道参数解析函数
                tunnel_params = parse_tunnel_specification(input_text, strict_mode, unit_preference)

                # 生成时间戳作为文件名的一部分
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                json_filename = f"tunnel_parameters_{timestamp}.json"

                # 保存为JSON文件
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(tunnel_params, f, indent=2, ensure_ascii=False)

                # 格式化输出结果（中文显示）
                response = f"隧道工程参数解析结果已保存为 {json_filename}：\n"
                param_found = False
                for key, value in tunnel_params.items():
                    if value is not None:
                        param_found = True
                        if key == "hasTunnelLength":
                            response += f"隧道长度 (hasTunnelLength): {value} 米\n"
                        elif key == "hasGeologicalCondition":
                            response += f"围岩等级 (hasGeologicalCondition): {value}\n"
                        elif key == "hasHydroCondition":
                            response += f"水文条件 (hasHydroCondition): {value}\n"
                        elif key == "hasSoilType":
                            response += f"土壤类型 (hasSoilType): {value}\n"
                        elif key == "tunnelType":
                            response += f"隧道类型 (tunnelType): {value}\n"
                        elif key == "hasTunnelDiameter":
                            response += f"隧道直径 (hasTunnelDiameter): {value} 米\n"

                if not param_found:
                    response = "抱歉，无法从描述中提取到有效的隧道工程参数。请提供更详细的信息。"
                else:
                    # 获取文件绝对路径
                    json_path = os.path.abspath(json_filename)
                    response += f"文件绝对路径：{json_path}\n"

                conversation_history.append(
                    {"role": "assistant", "content": response})
                return jsonify({
                    'response': response,
                    'end_conversation': False
                })
            except Exception as e:
                print(f"解析隧道参数时出错：{e}")
                conversation_history.append(
                    {"role": "assistant", "content": "抱歉，解析隧道参数时出现错误！"})
                return jsonify({
                    'response': "抱歉，解析隧道参数时出现错误！",
                    'end_conversation': False
                })


@app.route('/send_email', methods=['POST'])
def send_email_route():
    data = request.json
    try:
        send_email(
            sender_email=data["FromEmail"],
            sender_authorization_code=AUTHORIZATION_CODE,
            recipient_email=data["Recipients"],
            subject=data["Subject"],
            body=data["Body"]
        )
        return jsonify({
            'response': "邮件已发送，还需要什么帮助吗？",
            'end_conversation': False
        })
    except Exception as e:
        return jsonify({
            'response': f"发送邮件时出错：{str(e)}",
            'end_conversation': False
        })


if __name__ == "__main__":
    # 读取num_data.json文件
    with open('num_data.json', 'r', encoding='utf-8') as f:
        num_data = json.load(f)
    app.run(debug=True)