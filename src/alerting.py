from twilio.rest import Client

def send(changed, account_sid, auth_token, from_num, to_num):
    client = Client(account_sid, auth_token)
    for change in changed:
        print(f"Sending a message to {to_num}: {change}")
        client.messages.create(
            to=to_num, 
            from_=from_num,
            body=change)