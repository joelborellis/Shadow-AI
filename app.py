import json
import os
import logging
import requests
import openai
from flask import Flask, Response, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH", False)
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", 5)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", "true")
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")

# AOAI Integration Settings these are in the app service Configuration setting in Azure
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE")
AZURE_OPENAI_TOP_P = os.environ.get("AZURE_OPENAI_TOP_P")
AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS")
AZURE_OPENAI_STOP_SEQUENCE = os.environ.get("AZURE_OPENAI_STOP_SEQUENCE")
AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get("AZURE_OPENAI_SYSTEM_MESSAGE")
AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION")
AZURE_OPENAI_STREAM = os.environ.get("AZURE_OPENAI_STREAM", "true")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_OPENAI_MODEL_NAME") # Name of the model, e.g. 'gpt-35-turbo' or 'gpt-4'

SHOULD_STREAM = True if AZURE_OPENAI_STREAM.lower() == "true" else False

def is_chat_model():
    if 'gpt-35' in AZURE_OPENAI_MODEL_NAME.lower():
        return True
    return False

def should_use_data():
    if AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX and AZURE_SEARCH_KEY:
        return True
    return False

def prepare_body_headers_with_data(request):
    request_messages = request.json["messages"]
    print(request_messages)

    #with open('promp.json', 'w') as fp:
                #fp.write(json.dumps(request_messages))
                
    body = {
        "messages": request_messages,
        "temperature": float(AZURE_OPENAI_TEMPERATURE),
        "max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
        "top_p": float(AZURE_OPENAI_TOP_P),
        "stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
        "stream": SHOULD_STREAM,
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": f'https://{AZURE_SEARCH_SERVICE}.search.windows.net',
                    "key": AZURE_SEARCH_KEY,
                    "indexName": AZURE_SEARCH_INDEX,
                    "fieldsMapping": {
                        "contentField": AZURE_SEARCH_CONTENT_COLUMNS.split("|") if AZURE_SEARCH_CONTENT_COLUMNS else [],
                        "titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
                        "urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
                        "filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None
                    },
                    "inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
                    "topNDocuments": AZURE_SEARCH_TOP_K,
                    "queryType": "semantic" if AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" else "simple",
                    "semanticConfiguration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
                    "roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE
                }
            }
        ]
    }

    chatgpt_url = f'https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}'
    if is_chat_model():
        chatgpt_url += f'/chat/completions?api-version=2023-03-15-preview'
    else:
        chatgpt_url += f'/completions?api-version=2023-03-15-preview'

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY,
        "chatgpt_url": chatgpt_url,
        "chatgpt_key": AZURE_OPENAI_KEY,
        "x-ms-useragent": "ShadowSeller/1.0.0"
    }
    return body, headers

def stream_with_data(body, headers, endpoint):    
    s = requests.Session()
    response = {
        "id": "",
        "model": "",
        "created": 0,
        "object": "",
        "choices": [{
            "messages": []
        }]
    }
    try:
        print(endpoint)
        print(headers)
        with s.post(endpoint, json=body, headers=headers, stream=True) as r:
            collected_messages = []
            for line in r.iter_lines(chunk_size=10):
                if line:
                    lineJson = json.loads(line.lstrip(b"data:").decode("utf-8"))                    
                    if "error" in lineJson:
                        yield json.dumps(lineJson).replace("\n", "\\n") + "\n"
                    response["id"] = lineJson["id"]
                    response["model"] = lineJson["model"]
                    response["created"] = lineJson["created"]
                    response["object"] = lineJson["object"]
                    
                    role = lineJson["choices"][0]["messages"][0]["delta"].get("role")    
                    if role == "tool":
                        response["choices"][0]["messages"].append(lineJson["choices"][0]["messages"][0]["delta"])
                    elif role == "assistant": 
                        response["choices"][0]["messages"].append({
                            "role": "assistant",
                            "content": ""
                        })
                    else:
                        deltaText = lineJson["choices"][0]["messages"][0]["delta"]["content"]
                        if deltaText != "[DONE]":
                            response["choices"][0]["messages"][1]["content"] += deltaText              
                    yield json.dumps(response).replace("\n", "\\n") + "\n"
                                    
                            
    except Exception as e:
        print(json.dumps(str(e)))
        yield json.dumps({"error": str(e)}).replace("\n", "\\n") + "\n"

def conversation_with_data(request):
    body, headers = prepare_body_headers_with_data(request)
    endpoint = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"

    if not SHOULD_STREAM:
        r = requests.post(endpoint, headers=headers, json=body)
        status_code = r.status_code
        r = r.json()

        return Response(json.dumps(r).replace("\n", "\\n"), status=status_code)
    else:
        if request.method == "POST":
            return Response(stream_with_data(body, headers, endpoint), mimetype="text/event-stream")
        else:
            return Response(None, mimetype='text/event-stream')

def stream_without_data(response):
    responseText = ""
    for line in response:
        deltaText = line["choices"][0]["delta"].get('content')
        if deltaText and deltaText != "[DONE]":
            responseText += deltaText

        response_obj = {
            "id": line["id"],
            "model": line["model"],
            "created": line["created"],
            "object": line["object"],
            "choices": [{
                "messages": [{
                    "role": "assistant",
                    "content": responseText
                }]
            }]
        }
        yield json.dumps(response_obj).replace("\n", "\\n") + "\n"

def conversation_without_data(request):
    openai.api_type = "azure"
    openai.api_base = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
    openai.api_version = AZURE_OPENAI_PREVIEW_API_VERSION
    openai.api_key = AZURE_OPENAI_KEY

    request_messages = request.json["messages"]
    messages = [
        {
            "role": "system",
            "content": AZURE_OPENAI_SYSTEM_MESSAGE
        }
    ]

    for message in request_messages:
        messages.append({
            "role": message["role"] ,
            "content": message["content"]
        })

    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_MODEL,
        messages = messages,
        temperature=float(AZURE_OPENAI_TEMPERATURE),
        max_tokens=int(AZURE_OPENAI_MAX_TOKENS),
        top_p=float(AZURE_OPENAI_TOP_P),
        stop=AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
        stream=SHOULD_STREAM
    )

    if not SHOULD_STREAM:
        response_obj = {
            "id": response,
            "model": response.model,
            "created": response.created,
            "object": response.object,
            "choices": [{
                "messages": [{
                    "role": "assistant",
                    "content": response.choices[0].message.content
                }]
            }]
        }

        return jsonify(response_obj), 200
    else:
        if request.method == "POST":
            return Response(stream_without_data(response), mimetype='text/event-stream')
        else:
            return Response(None, mimetype='text/event-stream')

def get_user_history(request):
    
    selected = request.json["user"]
    print(selected)
    
    response_obj = [
  [
    { "role": "user", "content": "good afternoon" },
    {
      "role": "assistant",
      "content": "Good afternoon! How can I assist you today?"
    },
    { "role": "user", "content": "can you help with an upcoming sales call" },
    {
      "role": "assistant",
      "content": "Of course! I can definitely help you with your upcoming sales call. What specific aspect of the sales call would you like assistance with? Are you looking for tips on building rapport, handling objections, or closing the deal? Let me know so I can provide you with the most relevant information."
    },
    { "role": "user", "content": "i need to create an aganda" },
    {
      "role": "assistant",
      "content": "When creating an agenda for your sales call, it's important to consider the key elements that will help you effectively communicate your message and achieve your objectives. Here are some steps you can follow to create a comprehensive agenda:\n\n1. Introduction: Start the call by introducing yourself and establishing rapport with the prospect. Make sure to create a positive and engaging atmosphere.\n\n2. Purpose of the Call: Clearly state the purpose of the call and what you hope to achieve. This will help set expectations and keep the conversation focused.\n\n3. Agenda Overview: Provide a brief overview of the topics you will cover during the call. This will give the prospect an idea of what to expect and help them prepare any questions or concerns they may have.\n\n4. Background and Needs Discovery: Spend some time understanding the prospect's background, challenges, and needs. Ask open-ended questions to encourage them to share relevant information.\n\n5. Value Proposition: Present your value proposition and explain how your product or service can address the prospect's specific needs and challenges. Highlight the unique benefits and advantages you offer.\n\n6. Product or Service Demonstration: If applicable, provide a demonstration of your product or service to showcase its features and functionality. Tailor the demonstration to address the prospect's specific pain points.\n\n7. Addressing Objections: Anticipate and address any potential objections or concerns the prospect may have. Be prepared with persuasive responses and examples that demonstrate how your offering can overcome those objections.\n\n8. Pricing and Terms: Discuss pricing options and any relevant terms or conditions. Be transparent and provide clear explanations to ensure the prospect understands the value they will receive.\n\n9. Next Steps: Outline the next steps in the sales process, such as scheduling a follow-up call, providing additional information, or arranging a product trial. Clearly communicate the actions you expect from both parties.\n\n10. Closing Remarks: End the call on a positive note, expressing gratitude for the prospect's time and interest. Reiterate your commitment to supporting their needs and offer any additional assistance they may require.\n\nRemember, the agenda should be flexible and adaptable to the prospect's specific situation and needs. Be prepared to adjust the agenda based on their responses and engagement during the call.\n\n[doc1], [doc2], and [doc3] provide valuable insights and strategies for creating an effective sales call agenda. You can refer to these documents for more detailed information and examples.\n\nLet me know if there's anything else I can assist you with!"
    }
  ],
  [
    { "role": "user", "content": "good afternoon" },
    {
      "role": "assistant",
      "content": "Good afternoon! How can I assist you today?"
    }
  ],
  [
    { "role": "user", "content": "hey i need help with an upcoming call" },
    {
      "role": "assistant",
      "content": "Sure, I'm happy to help, lets figure out how we can create an agenda"
    }
  ]
]
    return Response(json.dumps(response_obj), mimetype="application/json", status=200)

@app.route("/conversation", methods=["GET", "POST"])
def conversation():
    try:
        use_data = should_use_data()
        if use_data:
            return conversation_with_data(request)
        else:
            return conversation_without_data(request)
    except Exception as e:
        logging.exception("Exception in /conversation")
        return jsonify({"error": str(e)}), 500
    
@app.route("/selecthistory", methods=["GET", "POST"])
def getchathistory():
    try:
        #res = get_user_history(request)
        #print("response:  ", res.get_data().decode("utf-8"))
        return get_user_history(request)
    except Exception as e:
        logging.exception("Exception in /selecthistory")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)