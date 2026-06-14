import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
import random


class StreamChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("大模型流式输出演示")
        self.root.geometry("1000x600")

        # 创建顶部输入区域
        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(input_frame, text="输入消息:").pack(side=tk.LEFT)
        self.input_entry = tk.Entry(input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.bind('<Return>', lambda e: self.start_stream())

        self.send_btn = tk.Button(input_frame, text="发送", command=self.start_stream)
        self.send_btn.pack(side=tk.LEFT, padx=5)

        # 创建消息显示区域
        self.message_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=70,
            height=25,
            font=('Microsoft YaHei', 10)
        )
        self.message_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 配置标签样式
        self.message_area.tag_config('user', foreground='#0066cc', font=('Microsoft YaHei', 10, 'bold'))
        self.message_area.tag_config('assistant', foreground='#333333')
        self.message_area.tag_config('streaming', foreground='#009900')

        # 状态变量
        self.is_streaming = False

    def start_stream(self):
        """开始流式输出"""
        if self.is_streaming:
            return

        user_input = self.input_entry.get().strip()
        if not user_input:
            messagebox.showwarning("提示", "请输入消息")
            return

        self.input_entry.delete(0, tk.END)

        # 显示用户消息
        self.message_area.insert(tk.END, f"用户: {user_input}\n\n", 'user')
        self.message_area.insert(tk.END, "助手: ", 'assistant')

        # 在新线程中启动流式输出
        self.is_streaming = True
        self.send_btn.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.stream_response, args=(user_input,))
        thread.daemon = True
        thread.start()

    def stream_response(self, user_input):
        """模拟大模型的流式输出"""
        # 模拟大模型的响应文本
        response = self.generate_mock_response(user_input)

        # 逐字符流式输出
        for char in response:
            if not self.is_streaming:
                break
            # 使用 after 方法在主线程中更新 UI
            self.root.after(0, self.append_char, char)
            time.sleep(random.uniform(0.02, 0.08))  # 模拟网络延迟

        # 完成输出
        self.root.after(0, self.finish_stream)

    def append_char(self, char):
        """在消息区域追加字符"""
        self.message_area.insert(tk.END, char, 'streaming')
        self.message_area.see(tk.END)  # 自动滚动到底部

    def finish_stream(self):
        """完成流式输出"""
        self.message_area.insert(tk.END, "\n\n")
        self.is_streaming = False
        self.send_btn.config(state=tk.NORMAL)

    def generate_mock_response(self, user_input):
        """生成模拟的大模型响应"""
        responses = [
            f"您好！您的问题是：'{user_input}'。这是一个很好的问题。\n\n让我为您详细解答：\n\n首先，关于您提到的内容，我认为需要从几个方面来分析。第一，我们需要考虑基本概念和背景。第二，实际应用场景也很重要。第三，还需要考虑可能遇到的问题和解决方案。\n\n希望这个回答对您有帮助！如果您还有其他问题，欢迎继续提问。",
            f"收到您的消息：'{user_input}'。\n\n这是一个有趣的话题。让我来为您分析一下：\n\n1. 首先，我们可以从基础开始理解。\n2. 其次，实际应用中需要注意一些细节。\n3. 最后，建议您可以进一步探索相关内容。\n\n如果您需要更详细的信息，请随时告诉我！",
            f"感谢您的提问！关于'{user_input}'，我想分享一些想法：\n\n这是一个值得深入探讨的话题。从多个角度来看，我们都可以获得不同的见解。重要的是要保持开放的心态，不断学习和探索。\n\n希望我的回答能够帮助到您！"
        ]
        return random.choice(responses)


def main():
    root = tk.Tk()
    app = StreamChatWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()