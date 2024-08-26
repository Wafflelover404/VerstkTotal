import requests
import re

def send(request, hf_token):
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {hf_token}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def replace_assistant(strin):
        e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
        e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
        return e.strip()

    prompt = f"""
        <|system|>
        Assistant is an expert in coding. He is specialized in frontend web development. He has to help user with his
        </s>
        <|user|>
        {request}
        </s>
        <|assistant|>
        """
    
    for _ in range(10):
        try:
            response = query({
                "inputs": prompt,
                "parameters": {"max_new_tokens": 8000, "use_cache": False, "max_time": 120.0},
                "options": {"wait_for_model": True}
            })
            full_response = replace_assistant(response[0]["generated_text"])
            return full_response
        except Exception as e:
            print(e)
            continue
    
    return "Error"