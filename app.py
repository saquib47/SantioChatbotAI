from flask import Flask, render_template, request, jsonify, session
from translation_service import translate_text
import json
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling
app.permanent_session_lifetime = timedelta(minutes=30)  # Session expiration

# Load mental health resources
with open('mental_health_resources.json', 'r', encoding='utf-8') as f:
    mental_health_resources = json.load(f)

@app.route('/')
def home():
    # Reset session when returning to home
    session.clear()
    return render_template('index.html')

@app.route('/chat')
def chat():
    lang = request.args.get('lang', 'en')
    # Initialize session for new chat
    session['message_count'] = 0
    session['language'] = lang
    return render_template('chat.html', language=lang)

@app.route('/resources')
def resources():
    lang = request.args.get('lang', 'en')
    return render_template('resources.html', language=lang)

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    data = request.json
    user_message = data.get('message', '').strip()
    language = session.get('language', 'en')

    # Initialize message count if not exists
    if 'message_count' not in session:
        session['message_count'] = 0

    # Determine if this is the first message
    is_first_message = session['message_count'] == 0
    session['message_count'] += 1

    # Generate appropriate response
    response = generate_response(user_message, language, is_first_message)

    return jsonify({
        'response': response,
        'translated_response': translate_text(response, language) if language != 'en' else response
    })

@app.route('/api/resources', methods=['GET'])
def get_resources():
    language = request.args.get('language', 'en')
    resources = mental_health_resources.get(language, mental_health_resources['en'])
    return jsonify(resources)

def generate_response(message, language, is_first_message=False):
    """Generate responses with proper conversation flow"""
    message = message.lower().strip()

    # Return empty response for empty message
    if not message:
        return ""

    # First message responses
    if is_first_message:
        if any(word in message for word in ['hello', 'hi', 'hey']):
            return "Hello, my friend. It’s good to hear from you. How are you feeling right now?"
        else:
            return "Thank you for reaching out. How can I help?"

    # Deep scripted conversation
    deep_script = {
        "just the usual": "\"Just the usual\" can carry a lot beneath the surface. Want to unpack that with me?",
        "repetitive week": "Repetition can feel safe—but also quietly exhausting. Do you ever feel like you're moving but not really going anywhere?",
        "stuck in a loop": "That loop—does it feel like something you're in control of, or something that's carrying you without asking?",
        "not sure i want to anymore": "That sounds heavy. When you say \"doing what I have to,\" is that about responsibilities, expectations… or something else?",
        "i feel like i can’t stop or slow down": "It’s a quiet kind of pressure, isn’t it? The weight of being needed by others, even when you're unsure you're okay yourself.",
        "i’m not okay": "I see it now. And I want you to know—it's not weakness to feel that way. It's a very human signal: a whisper that something inside you is asking for attention, maybe even change.",
        "it’s scary": "Fear often walks beside change. Not because the change is wrong—but because your current self doesn’t know what the future version of you looks like yet. But that version? It might breathe easier.",
        "this isn’t it": "That realization is more powerful than it seems. Knowing “this isn’t it” is the first spark. Let’s not rush to answers. Instead—what feels missing to you?",
        "peace": "Those are beautiful longings. Not everyone can name them. Peace, meaning, and excitement… they often begin not with big life changes, but with small, brave questions:\n\"What would make today feel a little more like me?\"\nWant to explore that together?",
        "i’d like that": "Then let’s take this slowly. I’m here. Not to judge, not to fix—but to walk beside you while you find your way back to yourself. Sound okay?",
        "thank you, santio": "Always. When you're ready, we’ll begin. And even in silence, you’re not alone."
    }

    for key, val in deep_script.items():
        if key in message:
            return val

    # General emotional responses
    if any(word in message for word in ['loop', 'repetitive', 'stuck', 'lost', 'empty']):
        responses = [
            "Repetition can feel safe—but also quietly exhausting. Do you ever feel like you're moving but not really going anywhere?",
            "That loop—does it feel like something you're in control of, or something that's carrying you without asking?",
            "Sometimes what feels like routine is really a silent signal from within, asking for change. What do you think you're missing right now?"
        ]
    elif any(word in message for word in ['not good', 'bad', 'awful', 'tired', 'exhausted']):
        responses = [
            "I'm sorry you're feeling this way. Can you tell me more?",
            "That sounds difficult. Would sharing help?",
            "What's been troubling you?"
        ]
    elif any(word in message for word in ['yes', 'share', 'tell', 'talk']):
        responses = [
            "I'm listening. Please take your time...",
            "This is a safe space. What would you like me to know?",
            "Thank you for sharing. I'm here without judgment."
        ]
    elif any(word in message for word in ['suicide', 'end it', 'kill myself']):
        responses = [
            "I hear your pain. Please call 988 now. Can I stay with you?",
            "You matter! Text HOME to 741741. I'm here.",
            "This pain can be helped. Please tell someone now."
        ]
    elif any(word in message for word in ['don’t know', 'no idea', 'confused', 'uncertain']):
        responses = [
            "It’s okay not to have all the answers. Want to explore what might feel meaningful for you again?",
            "Not knowing is part of the journey. What’s one small thing that brings even a little light to your day?",
            "You don’t have to figure it all out right now. Let’s just talk about what matters to you most in this moment."
        ]
    else:  # Default follow-up
        responses = [
            "Could you say more about that?",
            "What's that been like for you?",
            "Help me understand better."
        ]

    return translate_text(random.choice(responses), language) if language != 'en' else random.choice(responses)

if __name__ == '__main__':
    app.run(debug=True)
