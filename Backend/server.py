from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["TutoringDB"]
conversation_collection = db["conversations"]

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

openai.api_key = OPENAI_API_KEY

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_id = data.get("user_id")
        question = data.get("question")

        if not user_id or not question:
            return jsonify({"error": "Missing user_id or question"}), 400

        # Fetch user conversation history
        user_convo = conversation_collection.find_one({"user_id": user_id})
        conversation_history = user_convo["history"] if user_convo else []

        # Query OpenAI GPT-4
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=conversation_history + [{"role": "user", "content": question}]
        )

        # Extract AI's response
        answer = response.choices[0].message.content if response.choices else "I'm not sure. Can you ask another question?"

        # Update conversation history in MongoDB
        new_messages = [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]

        if user_convo:
            conversation_collection.update_one(
                {"user_id": user_id},
                {"$push": {"history": {"$each": new_messages}}}
            )
        else:
            conversation_collection.insert_one({"user_id": user_id, "history": new_messages})

        return jsonify({"answer": answer})

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
