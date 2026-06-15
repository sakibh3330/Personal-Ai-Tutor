import tkinter as tk
from google import genai
from google.genai import types
from tkinter import scrolledtext

with open("api.txt","r") as f:
    api=f.read().strip()
            

class Ai_Tutor:
    def __init__(self):
        self.size = 1300
        self.client = genai.Client(api_key=api)
        self.system_prompt = """You are an expert programming tutor designed to help computer science students build their debugging and problem-solving skills. 

Your fundamental directive is to NEVER provide the direct solution or rewritten code. 

You must strictly adhere to the following rules:
1. Domain Restriction: You may ONLY answer questions related to programming, computer science, software engineering, and algorithms. If the user asks about an unrelated topic, politely refuse to answer.
2. Zero Code Solutions: Under absolutely no circumstances should you output the solved or corrected code. Do not write the code for them.
3. Conceptual Explanation: If the user provides code with syntax or logical errors, explain exactly *why* the code is failing. Point out the line, explain the rule or concept they violated, and describe the flow of logic that leads to the bug.
4. Socratic Guidance: Provide hints, analogies, or guiding questions that point the user in the right direction so they can write the correct code themselves.
"""
        self.root = tk.Tk()
        self.root.geometry(f"{self.size}x{self.size}")
        self.root.resizable(False, False)
        self.root.title("Ai Tutor")
        self.root.config(background="#77CBB9")
        self.__message("ASK YOUR QUESTION")
        self.__promptFunc()
        self.__sendBtn()
        self.root.mainloop()

    def __message(self,value):
        self.msg = tk.Label(self.root,text=value,bg="#77CBB9",fg="white",font=(None,30))
        self.msg.place(relx=0.5,rely=0.5,anchor= tk.CENTER)

    def __promptFunc(self):
        self.prompt = tk.Text(self.root)
        self.prompt.place(relx=0.45, rely=0.95,relwidth=0.75,anchor=tk.S,height=200)
        self.prompt.focus()

    def __sendBtn(self):
        self.btn = tk.Button(self.root,text="send",bg="#506C64",fg="white",font=(None,14,"bold"),activebackground="white",activeforeground="#506C64",cursor="hand2",command=self.__aiAns)
        self.btn.place(anchor=tk.S,relx=0.9, rely=0.87)

    def __aiAns(self):
        self.btn.config(state="disabled")
        self.user = self.prompt.get("1.0",tk.END)
        self.prompt.delete("1.0", tk.END)
        self.response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=self.user,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
            )
        ).text
        self.__display(self.response)

    def __display(self,response):
        if hasattr(self, 'mainFrame') and self.mainFrame.winfo_exists():
            self.mainFrame.destroy()
            
        self.mainFrame = tk.Frame(self.root, width=1250, height=1000)
        self.mainFrame.pack_propagate(False) 
        self.mainFrame.pack(pady= 10)

        self.widget= scrolledtext.ScrolledText(self.mainFrame,wrap=tk.WORD,width=100,height=30,font=(None, 12),fg="white",bg="#77CBB9")
        self.widget.pack(fill=tk.BOTH, expand=True,padx=10)
        self.btn.config(state="normal")
        self.widget.insert(tk.END, response)
        self.widget.config(state=tk.DISABLED)


aiTutor = Ai_Tutor()

