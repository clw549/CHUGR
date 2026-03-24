from langchain_community.chat_models import ChatLiteLLM
import langchain.messages as lcm
import tkinter as tk
from git import Repo
import os

MEMORY_FILE = "memory.txt"

PROMPT_STR = "What would you like to say? "
LLM_MODEL = "Meta-Llama-3.1-70B-Instruct-quantized"
llm = ChatLiteLLM(
    model=f"litellm_proxy/{LLM_MODEL}",
    api_key=#TODO: make new way to not hard code api key
    ,
    api_base="https://llm-api.cyverse.ai/v1")

# print (llm.invoke("Hello, world!"))

def prompt_engineer(prompt, memory):
  message = [
    lcm.SystemMessage(memory),
    lcm.HumanMessage(prompt)
  ]
  return message

def delete_memory():
  with open(MEMORY_FILE, 'w') as file:
    file.write("Contextual information: \"You\" are the previous responses you (the LLM) have given, wrapped in brakets []. User is the users prompts wrapped also in brakets []. Please do not wrap your own responses in brackets, thank you!\n")

def update_memory_box():
  with open(MEMORY_FILE, 'r') as file:
    text = file.read()
    print(text)
    replace_text(text, memory_text)

def send_prompt():
  prompt = user_prompt.get("1.0", tk.END)
  print(prompt)
  user_message.config(text=prompt, wraplength=screen.winfo_width())
  with open(MEMORY_FILE, "r") as file:
    text = file.read()
  message = prompt_engineer(prompt, text)
  reply = llm.invoke(message)
  replace_text(reply.content, text_display)
  user_prompt.delete("1.0", tk.END)
  with open(MEMORY_FILE, "a") as file:
    file.write(f"User: [{prompt}]")
    file.write(f"You: [{reply.content}]")
  print(reply.content)
  
  return reply

def replace_text(new_text, text_displayer : tk.Text):
  text_displayer.config(state=tk.NORMAL)
  text_displayer.delete("1.0", tk.END)
  text_displayer.insert("1.0", new_text)
  text_displayer.config(state=tk.DISABLED)

def get_repo():
  repo_url = github_url.get("1.0", "1.0 lineend")
  Repo.clone_from(repo_url, "current_repo")
  return

def search_for(file_path = "./current_repo/README.md"):
  search_strs = search_text.get("1.0", "1.0 lineend").split(sep=",")
  print(search_strs)
  print(file_path)

  if ".git" not in file_path:
      try:
          with open(file_path, 'r', encoding='utf-8') as file:
              lines = file.readlines()
              for line in lines: 
                for word in search_strs:
                  if line.find(word) != -1:
                    print(line)
      except UnicodeDecodeError:
          print(f"Skipping binary file: {file_path}")
    

# Gets a list of files, opens more dirs recursively
# finally searches files by keywords given
def find_files(current_dir = "current_repo"):
  for root, dirs, files in os.walk("current_repo"):
    for filename in files:
        filepath = os.path.join(root, filename)
        search_for(filepath)
  print(root)
  print(dirs)
  print(files)



screen = tk.Tk()

chat_frame = tk.Frame(screen)
chat_frame.pack(side=tk.LEFT,fill='both', expand=True, padx=10, pady=10)

memory_frame = tk.Frame(screen)
memory_frame.config()
memory_frame.pack(side=tk.LEFT,fill='both', expand=True, padx=10, pady=10)

mem_scroll = tk.Scrollbar(memory_frame)
memory_text = tk.Text(memory_frame, wrap=tk.WORD, yscrollcommand=mem_scroll.set, state=tk.DISABLED)
mem_scroll.config(command=memory_text.yview)
memory_text.pack()

delete_memory_button = tk.Button(memory_frame, text="delete memory", command=delete_memory, justify=tk.LEFT)
delete_memory_button.pack()

update_memory_button = tk.Button(memory_frame, text="update memory", command=update_memory_box, justify=tk.LEFT)
update_memory_button.pack()

#github things
github_url = tk.Text(memory_frame, wrap=tk.WORD, height=1)
github_url.pack()
github_submit_btn = tk.Button(memory_frame, text="get repo", command = get_repo, justify=tk.LEFT)
github_submit_btn.pack()

#searching things
search_text = tk.Text(memory_frame, wrap=tk.WORD, height=1)
search_btn = tk.Button(memory_frame, text="search word", command = find_files, justify=tk.LEFT)
search_text.pack()
search_btn.pack()


frame = tk.Frame(chat_frame)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_display = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, state=tk.DISABLED)
text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#attatch scrollbar to text
scrollbar.config(command=text_display.yview)

screen.title("Ciaran LLM testing window")
screen.configure(background="light green")
screen.minsize(100, 100)
send_button = tk.Button(chat_frame, text="send", command=send_prompt, justify=tk.LEFT)

#to display updatable text
reply_label = tk.Label(chat_frame, text="Hello, World!")
reply_label.pack()
#show user input
user_message = tk.Label(chat_frame)
user_message.pack()
#get user input
prompt_frame = tk.Frame(chat_frame)
prompt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
prompt_scroll = tk.Scrollbar(prompt_frame)
user_prompt = tk.Text(prompt_frame, width=70, height=5, yscrollcommand=prompt_scroll.set)
prompt_scroll.config(command=user_prompt.yview)
user_prompt.pack(expand=True)

send_button.pack()

screen.mainloop()
