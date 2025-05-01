import google.generativeai as genai

genai.configure(api_key="your key")

models = genai.list_models()
for m in models:
    print(m.name)


# Create your test
#AIzaSyBEgbo2MIsVWSu4vbRaOwipmU7bBmZiY08
