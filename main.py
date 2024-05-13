from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
  organization=os.getenv("OPEN_AI_ORG"),
  api_key=os.getenv("OPEN_AI_PROJ_KEY"),
)

def chatbot_conversation():
    welcome = "Hello! How can I assist you today?"

    # reset_conv()
    print(" quit:\t\t to quit\n reset\t\t to reset\n verdict\t ask the bot to judge on candidate")
    print(f"Assistant: {welcome}")
    while True:
        user_message = input("User: ")
        if user_message.lower() == "quit":
          break
        if user_message.lower() == "reset":
          reset_conv()
          print(f"\nAssistant: {welcome}")
        if user_message.lower() == "verdict":
          response = judge_candidate()
        else:
            # Here you can add the code to get the response from the chatbot
            chatbot_response = get_chat_response(user_message)
            print("Assistant: " + chatbot_response)


   

#1. Send to text to chatgpt

#2. We want to save the chat history to send back and forth for context
def reset_conv():
   """
   Delete all contents of our conversation
   """
   with open('database.json', 'w') as db_file:
        db_file.write('')

def judge_candidate():
  messages = load_messages()
  
  print("Verdict:")
  Request = """-- Das Interview ist abgeschlossen --
  Bewerte den Kandidaten auf seine Tauglichkeit für die Stelle und begründe deine Wahl anhand der Daten.
  """
  #TODO: judge candidate

  return "Accepted"

def get_chat_response(user_message):
  #TODO:add instructions
  messages = load_messages()
  messages.append({"role":"user","content": user_message})
  #print("debug: " + str(messages))

  # Send to openai
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
  )
  parsed_gpt_response = completion.choices[0].message.content
  save_messages(user_message, parsed_gpt_response)

  return parsed_gpt_response

def load_messages():
  # Load the chat history from a file
  messages = [
     {"role": "system", "content": "Du interviewst den Nutzer zu einer Jobbeschreibung und sollst anschließend begründen können ob der Kandidat die benötigten Fähigkeiten für die Rolle besitzt. Stelle kurze und relevante Fragen. Gestallte sie als lockere Konversation."}
  ]
  file = 'database.json'

  empty = os.stat(file).st_size == 0
  if not empty:
    with open(file) as db_file:
      data = json.load(db_file)
      for item in data:
        messages.append(item)
  
  return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)

def get_job_description(file):
   #TODO: import Job.txt and pass it on to chatgpt somehow
   return


chatbot_conversation()