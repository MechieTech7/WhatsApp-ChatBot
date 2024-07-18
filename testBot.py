import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@app.route("/send_message", methods=['GET'])
def send_message():
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Twilio WhatsApp Sandbox number
        body='Your Yummy Cupcakes Company order of 1 dozen frosted cupcakes has shipped and should be delivered on July 10, 2019. Details: http://www.yummycupcakes.com/',
        to='whatsapp:+919597774733'  # Your phone number in international format
    )
    return f"Message sent with SID: {message.sid}"

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    if 'hello' in incoming_msg:
        msg.body("Hi there! Welcome to Binare Cloud Kitchen. How can I assist you today? You can say 'Menu', 'Book a Table', or 'Contact'.")
    elif 'menu' in incoming_msg:
        msg.body("Here is our menu: 1. Pizza 2. Pasta 3. Salads 4. Desserts. To order, please reply with the item number.")
    elif 'book a table' in incoming_msg:
        msg.body("Sure, I can help with that. Please provide the date and time for your reservation.")
    elif 'contact' in incoming_msg:
        msg.body("You can reach us at 9597774733 or visit us at [Restaurant Address].")
    else:
        msg.body("I'm sorry, I didn't understand that. Can you please rephrase?")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
