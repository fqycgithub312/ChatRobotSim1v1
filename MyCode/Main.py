"""
摘要：调用大模型，去自动调用函数
"""
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import random

load_dotenv()
base_url = os.getenv("base_url1")
key = os.getenv("key1")
model = os.getenv("model1")

# base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# model = "qwen3.7-plus"
# # base_url="http://localhost:11434/v1"
# # model="deepseek-r1:1.5b" # 本地大模型
# key = ""
## ==========================================================================
##sim1>>调用大模型进行对话
# def myfunc1(a,b):
#     # 计算两数之和
#     y=a+b
#     return y
# def myfunc2(n):
#     # 计算n的阶乘
#     y=1
#     for ind in range(1,n+1):
#         y=y*ind
#     return y
# def myfunc3():
#     print(f"啥也不用计算呢！")
# MyFuncs={
#     "myfunc1":{
#         "function":myfunc1,
#         "description":"a+b"
#     },
#     "myfunc2": {
#         "function": myfunc2,
#         "description": "计算阶乘"
#     },
#     "myfunc3":{
#         "function":myfunc3,
#         "description":"打印一行字符串！"
#     },
# }
# systemcontent="""
# 你是一个智能助手，现在我有三个函数可以调用，现在你要根据我的提问句子，自行判断调用哪个函数，传入什么参数。补充要求和信息如下：
# ### 意图识别
# (1)如果用户的问题里面含有方程，你要先解方程，然后再算
# ### 函数名称与功能
# (1)myfunc1(a,b):计算a,b两数的和返回结果
# (2)myfunc2(n):计算整数n的阶乘结果
# (3)myfunc3():打印一行文字
# ### 输出内容要求
# (1)你的输出内容要包含应该调用的函数的名字以及参数列表
# (2)你要根据自己的推理，识别出用户的意图，比如用户说计算五减去9,你应该判断出要调用函数myfunc1(a=5,b=-9)
# (3)你必须用标准的json格式给我输出回复信息,例如{"funcname":"myfunc1","args":[5,-9]}，不要带有Markdown的渲染符号哦
# """
# usercontent="""
# a=8,b=9,计算加法
# """
#
# client=OpenAI(
#     base_url=base_url,
#     api_key=key,
# )
# res=client.chat.completions.create(
#     model=model,
#     messages=[
#         {"role":"system","content":systemcontent},
#         {"role":"user","content":usercontent},
#     ]
# )
# # var1=res.model_dump_json()# 先转换成json
# var1=res.to_dict()# 先转换成字典？
# var2=var1.get("choices","Error!")[0];
# var3=var2.get("message","No message!").get("content","No content!")
# print(f"var3>>\n{var3}")
# info=json.loads(var3)# 转换成字典格式
# print(f"data>>\n{info}")
# func_name=info.get('funcname')
# func_selected=MyFuncs.get(info.get("funcname","No function!")).get("function")# 获取函数对象
# args=info.get("args","No arg!");
# print(f"被调用的函数是：{func_name}\n")
# print(f"函数参数是：{args}\n")
# value=func_selected(*args)
# print(f"执行结果为：{value}")
##==============================================================
##sim2>>调用大模型流式输出文本
# systemcontent="""
# 你是一个百科全书的超级大脑
# """
# usercontent="""
# 你好，介绍你自己。
# """
#
# client=OpenAI(
#     base_url=base_url,
#     api_key=key,
# )
# res=client.chat.completions.create(
#     model=model,
#     messages=[
#         {"role":"system","content":systemcontent},
#         {"role":"user","content":usercontent},
#     ],
#     stream=True,
# )
# for chunk in res:
#     var1=chunk.model_dump_json()# 先转换成json
#     dic1=json.loads(var1)
#     # print(dic1)
#     # print(f"=" * 35)
#     var2 = dic1.get("choices")[0]
#     if (var2 is not None) :
#         var3=var2.get("delta").get("reasoning_content")
#         if (var3 is not None):
#             print(f"当前段落为：\n{var3}",end="",flush=True)
#             print(f"="*35)
## ===============================================================
## sim0611_1>>调用大模型进行流式输出
# client=OpenAI(
#     base_url=base_url,
#     api_key=key,
# )
# systemcontent="""
# 你是一个脾气嚣张的家伙
# """
# usercontent="""
# 你好，介绍你自己。
# """
# res=client.chat.completions.create(
#     model=model,
#     messages=[
#         {"role":"system","content":systemcontent},
#         {"role":"user","content":usercontent},
#     ],
#     stream=True,
# )
# text_all=""
# ind=1
#
# for chunk in res:
#
#     if (chunk.choices) and (chunk.choices[0].delta.content is not None):
#         text=chunk.choices[0].delta.content
#         if (text is not None) and (text!= ""):
#             # python 的代码里面，if(A) 与if (A is not None)有什么区别？
#             text_all=text_all+text
#             print(f"{text}",end="",flush=True)
#             # print(f"="*35)
#     ind=ind+1
#
# # for chunk in res:
# #     # 检查 choices 是否存在且非空
# #     if chunk.choices and chunk.choices[0].delta.content is not None:
# #         print(chunk.choices[0].delta.content, end="", flush=True)
# print(f"完整文本\n{text_all}")
## ==========================================================
# sim0611>>与大模型进行有多轮有记忆的对话
# client=OpenAI(
#     base_url=base_url,
#     api_key=key,
# )
# systemcontent="""
# 你是一个问答助手
# """
# usercontent="""
# 你好，介绍你自己。
# """
# messages = [
#     {"role": "system", "content": systemcontent},
#     {"role": "user", "content": "你好！"},
# ]
# print(f"{type(messages)}")
# text_all=""
# ind=1
# N=50;# 对话的交互次数
# while (ind<N):
#     print(f"第ind={ind}次对话内容：")
#     usercontent_new=str(input("请输入你的问题：\n"))
#     print(f"{usercontent_new}")
#     messages_new={
#         "role":"user",
#         "content":usercontent_new,
#         }
#     # messages_new=list(messages_new)
#     print(f"nmessages_new>>\n{messages_new}")
#     messages.append(messages_new)
#     # print(f"m>>{messages}")
#     res = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         stream=True,
#         max_tokens=100,
#     )
#     print(f"开始输出AI回答>>\n"+34*"=")
#     for chunk in res:
#         if (chunk.choices) and (chunk.choices[0].delta.content is not None):
#             print(f"{chunk.choices[0].delta.content}",end="",flush=True)
#     print(f"\n")
#     ind=ind+1
## ==================================================================
# sim0612_v1仿真与大模型进行工具调用
# from openai import OpenAI
# import json
# import os
# import random
#
# # 初始化客户端
# client = OpenAI(
#     # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key=key,
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# # 模拟用户问题
# USER_QUESTION = "北京天气咋样"
# # 定义工具列表
# tools = [
#     {
#         "type": "function",
#         "name": "get_current_weather",
#         "description": "当你想查询指定城市的天气时非常有用。",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "城市或县区，比如北京市、杭州市、余杭区等。",
#                 }
#             },
#             "required": ["location"],
#         },
#     }
# ]
#
#
# # 模拟天气查询工具
# def get_current_weather(arguments):
#     # 这里传递的参数是包含地理位置的字典？
#     weather_conditions = ["晴天", "多云", "雨天"]
#     random_weather = random.choice(weather_conditions)
#     location = arguments["location"]
#     return f"{location}今天是{random_weather}。"
#
#
# # 封装模型响应函数
# def get_response(input_data):
#     response = client.responses.create(
#         model=model,
#         input=input_data,#这个参数里面有用户的提示词
#         tools=tools,
#         # max_output_tokens=200,
#     )
#     return response
#
#
# # 维护对话上下文
# conversation = [{"role": "user", "content": USER_QUESTION}]
#
# response = get_response(conversation) # 在这里调用了大模型推理
# # response里面是什么内容？
# print(f"datatype of response>>\n{type(response)}")
# # function_calls = [item for item in response.output if item.type == "function_call"]
# function_calls=[]# 记录下被调用的工具的信息
# # print(f"response>>\n{response}")
# for item in response.output:
#     if item.type=="function_call":
#         function_calls.append(item)
#
# # 如果不需要调用工具，直接输出内容
# if not function_calls:
#     print(f"助手最终回复：{response.output_text}")
# else:
#     # 进入工具调用循环
#     while function_calls:
#         for fc in function_calls:
#             func_name = fc.name # 获取函数名字
#             arguments = json.loads(fc.arguments) # 获取函数参数
#             print(f"正在调用工具 [{func_name}]，参数：{arguments}")
#             # 执行工具
#             tool_result = get_current_weather(arguments)
#             #上面这行代码有问题？调用工具怎么是指定的呢？不应该是大模型自己判断得到的吗？
#
#             print(f"工具返回：{tool_result}")
#             # 将工具调用和结果成对追加到上下文中
#             conversation.append(
#                 {
#                     "type": "function_call",
#                     "name": fc.name,
#                     "arguments": fc.arguments,
#                     "call_id": fc.call_id,
#                 }
#             )
#             conversation.append(
#                 {
#                     "type": "function_call_output",
#                     "call_id": fc.call_id,
#                     "output": tool_result,
#                 }
#             )
#         # 携带完整上下文再次调用模型
#         response = get_response(conversation)
#         function_calls = []
#         for item in response.output:
#             if item.type == "function_call":
#                 function_calls.append(item)
#
#     print(f"助手最终回复：{response.output_text}")

## =====================================================================
sim0612>>仿真openai调用工具和函数

初始化客户端
client = OpenAI(
    api_key=key,
    base_url=base_url,
)


# 1. 定义工具函数
def get_weather(city: str) -> str:
    """模拟查询天气"""
    weather_data = {
        "北京": "晴天,25°C,东南风3级",
        "上海": "阴天,22°C,东风2级",
        "广州": "多云,28°C,南风2级"
    }
    return weather_data.get(city, f"{city}:天气数据暂不可用")


def get_flight_price(origin: str, destination: str) -> str:
    """模拟查询机票价格"""
    if origin == "北京" and destination == "上海":
        return "经济舱 500元, 公务舱 1200元"
    elif origin == "上海" and destination == "广州":
        return "经济舱 450元, 公务舱 1000元"
    else:
        return f"{origin}到{destination}:暂未查询到航班信息"


def makePPT(fpath: str) -> str:
    print(f"完成ppt制作！")
    return (f"所有的ppt都已经搞定！")


# 2. 工具描述（告诉模型可以调用哪些函数）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_price",
            "description": "查询两个城市之间的机票价格",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "出发城市"},
                    "destination": {"type": "string", "description": "到达城市"}
                },
                "required": ["origin", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "makePPT",
            "description": "整理文档",
            "parameters": {
                "type": "object",
                "properties": {
                    "fpath": {"type": "string", "description": "文件路径"}
                },
                "required": ["fpath"]
            }
        }
    }
]

# 3. 工具分发映射
tool_map = {
    "get_weather": get_weather,
    "get_flight_price": get_flight_price,
    "makePPT": makePPT,
}


# 4. Agent主循环
def run_agent(user_input: str):
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以根据用户问题调用工具获取信息。"},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    msg = response.choices[0].message
    # print(f"msg>>\n{msg}")
    print(f"=" * 35, "\n")
    # 无工具调用，直接返回
    if not msg.tool_calls:
        return msg.content

    # 执行工具调用并获取结果
    messages.append(msg)
    for tc in msg.tool_calls:
        print(f"当前tc>>\n{tc}")
        print(f"=" * 35)
        fn_name = tc.function.name  # 获取工具的名称
        fn_args = json.loads(tc.function.arguments)  # 获取调用参数，转换成字典形式
        result = tool_map[fn_name](**fn_args)
        print(f"-" * 35)
        print(f"调用工具：{fn_name}")
        print(f"传入参数：{fn_args}")
        print(f"返回结果：{result}")
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": result  # 工具调用的返回结果添加到聊天记录里面
        })

    # 将工具结果交给模型生成最终回答
    final_response = client.chat.completions.create(
        model=model,
        messages=messages
    )  # 把工具返回的结果也带入到大模型对话里面，一起输入给大模型，重新返回回答
    return final_response.choices[0].message.content


# 5. 运行示例
if __name__ == "__main__":
    # # 测试1：查询天气
    # result1 = run_agent("北京今天天气怎么样？")
    # print(f"[最终回答] {result1}\n")
    #
    # # 测试2：查询机票价格
    # result2 = run_agent("从北京到上海的机票多少钱？")
    # print(f"[最终回答] {result2}\n")

    # 测试3：组合查询（可能同时调用两个工具）
    result3 = run_agent("我想从北京去上海去汇报一个电脑C盘的PPT，查一下北京的天气和机票价格")
    print(f"[最终回答] {result3}")
## ====================================================================
# sim0613>>仿真大模型自主决策调用工具


# client = OpenAI(
#     base_url=base_url,
#     api_key=key,
# )  # 需要设置 OPENAI_API_KEY 环境变量
#
#
# # ========== 模拟工具实现（含查询不到信息的默认返回） ==========
# def download_document(url: str) -> str:
#     if random.random() < 0.2:  # 模拟 20% 概率下载失败
#         return f"[模拟] 未能从 {url} 下载到任何文档，请检查链接是否有效"
#     return f"[模拟] 已从 {url} 下载文档"
#
#
# def query_weather(city: str) -> str:
#     supported_cities = ["北京", "上海", "深圳", "广州"]
#     if city not in supported_cities:
#         return f"[模拟] 暂未收录「{city}」的天气数据，无法查询到相关信息"
#     return f"[模拟] {city} 今日天气：晴 25°C"
#
#
# def query_train_ticket(from_city: str, to_city: str, date: str) -> str:
#     if random.random() < 0.78:  # 模拟 30% 概率无票
#         return f"[模拟] {date} 从 {from_city} 到 {to_city} 暂未查询到可用车次"
#     return f"[模拟] {date} 从 {from_city} 到 {to_city} 的车票：G123 次有票"
#
#
# def organize_ppt(topic: str) -> str:
#     if not topic or len(topic) < 2:
#         return "[模拟] 主题过于模糊，未能整理出有效的 PPT 内容"
#     return f"[模拟] 已整理关于「{topic}」的 PPT 大纲"
#
#
# # 工具名 -> 函数映射
# TOOLS_MAP = {
#     "download_document": download_document,
#     "query_weather": query_weather,
#     "query_train_ticket": query_train_ticket,
#     "organize_ppt": organize_ppt,
# }
#
# # ========== 工具定义（给大模型看的 schema） ==========
# TOOL_SCHEMAS = [
#     {
#         "type": "function",
#         "function": {
#             "name": "download_document",
#             "description": "从指定 URL 下载文档",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"url": {"type": "string", "description": "文档 URL"}},
#                 "required": ["url"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "query_weather",
#             "description": "查询指定城市的天气",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"city": {"type": "string", "description": "城市名"}},
#                 "required": ["city"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "query_train_ticket",
#             "description": "查询指定日期和起止城市的火车票",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "from_city": {"type": "string"},
#                     "to_city": {"type": "string"},
#                     "date": {"type": "string", "description": "格式 YYYY-MM-DD"},
#                 },
#                 "required": ["from_city", "to_city", "date"],
#             },
#         },
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "organize_ppt",
#             "description": "根据主题整理 PPT 大纲",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"topic": {"type": "string", "description": "PPT 主题"}},
#                 "required": ["topic"],
#             },
#         },
#     },
# ]
#
#
# def chat(user_query: str) -> str:
#     messages = [{"role": "user", "content": user_query}]
#
#     # 最多进行 5 轮工具调用，防止死循环
#     for ind in range(5):
#         response = client.chat.completions.create(
#             model=model,
#             messages=messages,
#             tools=TOOL_SCHEMAS,
#             tool_choice="auto",
#         )
#         msg = response.choices[0].message
#         messages.append(msg)
#
#         # 模型不想调用工具了，直接返回答案
#         if not msg.tool_calls:
#             return msg.content
#
#         # 依次执行每个工具调用，并把结果塞回消息
#         for tc in msg.tool_calls:
#             func = TOOLS_MAP.get(tc.function.name)
#             args = json.loads(tc.function.arguments)
#             print(f"当前tc:\n{func}")
#             print(f"=" * 35)
#             print(f"调用工具>>{tc.function.name}")
#             print(f"传入参数>>{tc.function.arguments}")
#             if func:
#                 result = func(**args)
#             else:
#                 result = f"未知工具：{tc.function.name}"
#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": tc.id,
#                 "content": result,
#             })
#
#     return "超出最大工具调用次数"
# # 测试大模型响应
# user_input = "我要去北京汇报一下AI文献，我的文件还缺少一点资料，出门要不要带伞？顺便看看从上海到杭州 2026-06-15 的车票"
# response = chat(user_input)
# print(f"大模型最终返回结果：\n{response}")

## =====================================================================================
# sim0614>>仿真调用DeepSeek大模型对话
base_url = os.getenv("base_url3")
key = os.getenv("key3")
model = "deepseek-v4-flash"

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(
    api_key=key,
    base_url=base_url
)
messages = [
    {"role": "system",
     "content": "知识库，收纳了很多小说的文本"
     },
    {"role": "user",
     "content": "把三国演义小说文本流式输出，中间不要省略，换一章的时候，输出“=====================”加以区分段落"
     }
]
response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=50000,
    temperature=1.5,
    stream=True,
)
for chunk in response:
    text = chunk.choices[0].delta.content
    if chunk.choices[0] and (text is not None):
        print(f"{text}", end="", flush=False)
print(f"\n回答完毕！")

## ============================================================================

