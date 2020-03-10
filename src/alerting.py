from twilio.rest import Client

def get_message(changed):
    separator = "\n"
    message = separator.join(changed)
    return message

def send(message, account_sid, auth_token, from_num, to_num):
    print(f"Sending a message to {to_num}:\n--------\n{message}\n-------")
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=to_num, 
        from_=from_num,
        body=message)