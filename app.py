from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import messaging, credentials

app = Flask(__name__)

# Initialiser Firebase Admin SDK
cred = credentials.Certificate('path_to_firebase_adminsdk.json')  # Bruk filbanen til Firebase Admin SDK JSON
firebase_admin.initialize_app(cred)

# Midlertidig lagring av abonnenter (FCM tokens)
subscribers = {}

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    token = data.get('token')
    flight_number = data.get('flight_number')

    if token and flight_number:
        # Lagre brukernes token sammen med valgt flightnummer
        subscribers[token] = flight_number
        return jsonify({'message': 'Subscribed successfully'}), 200
    else:
        return jsonify({'error': 'Missing token or flight number'}), 400

def send_push_notification(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        response = messaging.send(message)
        print(f'Successfully sent message to {token}:', response)
    except Exception as e:
        print(f'Error sending message to {token}:', str(e))

# Funksjon for å sende varsel når et fly lander
@app.route('/notify_landing', methods=['POST'])
def notify_landing():
    data = request.json
    flight_number = data.get('flight_number')
    notification_message = f'Fly {flight_number} har landet!'

    # Send varsler til alle abonnenter for dette flyet
    for token, subscribed_flight in subscribers.items():
        if subscribed_flight == flight_number:
            send_push_notification(token, "Flystatus", notification_message)

    return jsonify({'message': 'Notifications sent'}), 200

if __name__ == '__main__':
    app.run(debug=True)
