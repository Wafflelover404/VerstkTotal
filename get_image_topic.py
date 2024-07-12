import requests
import re

hf_token = "" # replace with your HuggingFace API key

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()

def replace_assistant(strin):
  e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
  e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
  return e.strip()

def send(prompt):
  for i in range(0, 10):
    try:
      prompt = f"""
          <|system|>
          Assistant is an expert in photography with an experience of 20 years. Assistant is provided with user's request and it's task is to return just 1 word which describes topic for image search. Assistant is allowed to response with one word only and it's absolutely prohibited to respond with more than 1 word.
          </s>
          <|user|>
          {prompt}
          </s>
          <|assistant|>
          """
      response = query({
        "inputs": prompt,
        "parameters": {"max_new_tokens": 8000, "use_cache": False, "max_time": 120.0},
        "options": {"wait_for_model": True}
      })
      full_response = replace_assistant(response[0]["generated_text"])
      return full_response
      break
    except Exception as e:
      print(e)
      pass
  return "Error"

# Get user prompt and optional requested information
