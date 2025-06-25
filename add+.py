import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
from openai import OpenAI


GPT_MODEL = "qwen-plus"

load_dotenv()
# 获取环境变量
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUTHORIZATION_CODE = os.getenv("AUTHORIZATION_CODE")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def find_point(target_point, num_data):
    """
    查找距离目标点最近的数据点并可视化

    Args:
        target_point (tuple): 目标点坐标 (x, y)
        num_data (list): 数据点列表，每个元素为 [x, y] 格式

    Returns:
        tuple: 最近点的坐标
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
    plt.scatter(data_points[:, 0], data_points[:, 1], c='blue', label='Database Point')

    # 绘制目标点（红色）
    plt.scatter(target_point[0], target_point[1], c='red', label='Target Point')

    # 绘制最近点（黄色星号）
    plt.scatter(nearest_point[0], nearest_point[1],
                c='yellow', marker='*', s=200, label='Nearest point')

    plt.title('Data Point Distribution Chart')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)

    # 保存图片
    plt.savefig('nearest_point.png')
    plt.close()

    return tuple(nearest_point)


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
                        "description": "The email address, eg., xiaoyu@163.com",
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
                        "description": "The recipients' email addresses,eg., chuyu@hust.com",
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


# 查询当前时间的工具
def get_current_time():
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
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
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
        server.login(sender_email, sender_authorization_code)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)


def main():
    # 读取num_data.json文件
    with open('num_data.json', 'r', encoding='utf-8') as f:
        num_data = json.load(f)
    messages = [
        {
            "role": "assistant",
            "content": """你叫ADFOR是一个AI助手。你需要与用户进行持续的多轮对话，直到用户明确表示想要结束对话。

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

    while True:
        msg = input("【You】: ")
        messages.append({"role": "user", "content": msg})

        # 检查用户是否想要结束对话
        if msg.lower() in ['再见', '拜拜', '结束对话', 'exit', 'quit', '我要走了', '对话到此为止']:
            print("\n哼~我也不是很想和你聊天，再见！")
            break

        response = chat_completion_request(
            messages=messages,
            tools=tools
        )
        if content := response.choices[0].message.content:
            print(f"【AI】: {content}")
            messages.append({"role": "assistant", "content": content})
        else:
            fn_name = response.choices[0].message.tool_calls[0].function.name
            fn_args = response.choices[0].message.tool_calls[0].function.arguments

            if fn_name == "send_email":
                try:
                    args = json.loads(fn_args)
                    print("【AI】: 邮件内容如下：")
                    print(f"发件人: {args['FromEmail']}")
                    print(f"收件人: {args['Recipients']}")
                    print(f"主题: {args['Subject']}")
                    print(f"内容: {args['Body']}")

                    confirm = input("AI: 确认发送邮件吗？ (yes/no): ").strip().lower()
                    if confirm == "yes":
                        send_email(
                            sender_email=args["FromEmail"],
                            sender_authorization_code=AUTHORIZATION_CODE,
                            recipient_email=args["Recipients"],
                            subject=args["Subject"],
                            body=args["Body"],
                        )
                        print("邮件已发送，还需要什么帮助吗？")
                        messages.append(
                            {"role": "assistant", "content": "邮件已发送，还需要什么帮助吗？"})
                    else:
                        print("邮件发送已取消，还需要什么帮助吗？")
                        messages.append(
                            {"role": "assistant", "content": "邮件发送已取消，还需要什么帮助吗？"})
                except Exception as e:
                    print(f"发送邮件时出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，功能异常！"})
            elif fn_name == "find_point":
                try:
                    args = json.loads(fn_args)
                    target_point = tuple(args['target_point'])
                    nearest_point = find_point(target_point, num_data)
                    response = f"距离点{target_point}最近的点是{nearest_point}。我已经生成了可视化图表，保存在nearest_point.png文件中。"
                    print(f"【AI】: {response}")
                    messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    print(f"查找最近点时出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，查找最近点时出现错误！"})
            elif fn_name == "get_current_time":
                try:
                    now_time = get_current_time()
                    response = f"函数输出信息：{now_time}"
                    print(f"【AI】: {response}")
                    messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    print(f"查找时间出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，无法查找当前时间！"})
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
                        
                        # 询问是否发送到下一个程序
                        send_to_next = input("是否发送到下一个程序？(yes/no): ").strip().lower()
                        if send_to_next == "yes":
                            try:
                                # 使用 subprocess 调用下一个程序并传递文件路径
                                import subprocess
                                result = subprocess.run(
                                    ["python", "next_program.py", json_path],
                                    capture_output=True,
                                    text=True
                                )
                                
                                if result.returncode == 0:
                                    response += f"下一个程序执行成功，输出：\n{result.stdout}"
                                else:
                                    response += f"下一个程序执行失败，错误：\n{result.stderr}"
                                    
                            except FileNotFoundError:
                                response += "错误：未找到下一个程序 (next_program.py)，请确保程序存在。"
                            except Exception as e:
                                response += f"发送到下一个程序时出错：{str(e)}"
                
                    print(f"【AI】: {response}")
                    messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    print(f"解析隧道参数时出错：{e}")
                    messages.append(
                        {"role": "assistant", "content": "抱歉，解析隧道参数时出现错误！"})


if __name__ == "__main__":
    main()