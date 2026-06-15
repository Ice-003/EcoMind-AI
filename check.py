import google.generativeai as genai

genai.configure(api_key="AIzaSyAaaS7YSTiid8FgW8ABQbrRn-orhSQwK0E")

for m in genai.list_models():
    print(m.name)