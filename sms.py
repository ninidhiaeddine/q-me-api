from twilio.rest import Client

# for production:
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']

# for debugging:
ACCOUNT_SID = 'AC2b63d459a65cf3fc84bbb19613c1ed24'
AUTH_TOKEN = '7c8577bca245bf9aab66b4fd85d8146f'
client = Client(ACCOUNT_SID, AUTH_TOKEN)
FROM = '+15039665752'


def send_sms(to_phone_number, message_body):
    """
    Sends an SMS message to the specified destination phone number.
    Incurs 0.1$ from the Twilio account.
    """
    message = client.messages \
                    .create(
                        body=message_body,
                        from_=FROM,
                        to=to_phone_number
                    )
    print("An SMS message has been sent to '{}'. Message SID={}".format(
        to_phone_number, message.sid))
