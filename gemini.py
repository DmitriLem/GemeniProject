from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from datetime import datetime



current_date = datetime(2024, 5, 9)

app = Flask(__name__, template_folder="templates")

print(app.template_folder) 

genai.configure(api_key="AIzaSyAf6xe3xbknUp2DFBMMvZ6cPUPKoKhgUBM")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


convo = model.start_chat(history=[])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form["user_input"].strip()
    if user_input:
        response = convo.send_message(user_input)
        return jsonify({"sender": "AI", "message": response.text})
    else:
        return jsonify({"error": "Empty input"}), 400

if __name__ == "__main__":
    app.run(debug=True)
