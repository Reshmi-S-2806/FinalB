import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the URL from the Environment Variable we set in Kubernetes
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # This connects to Supabase using the string in your deployment.yaml
    return psycopg2.connect(DATABASE_URL)

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('message')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Simple search logic: Find an answer that matches the user's question
    cur.execute("SELECT answer FROM chatbot_faqs WHERE question ILIKE %s", (f'%{user_query}%',))
    result = cur.fetchone()
    
    cur.close()
    conn.close()

    if result:
        return jsonify({"response": result[0]})
    else:
        return jsonify({"response": "I'm sorry, I couldn't find information on that. How else can I help?"})
