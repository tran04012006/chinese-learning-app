import google.generativeai as genai

genai.configure(api_key="AIzaSyBU8FsGS4Dm9Bi7CPslztYY04WV6O0cVz4")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Model Name: {m.name}") # Đây là ID bạn cần điền vào code

