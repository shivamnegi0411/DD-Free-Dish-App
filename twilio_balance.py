from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = 'AC4c9bfc6f4103167c9f3b877fa6a17ef9'
auth_token = 'e54483ea0c5268452daf8dab376fdfd7'

# Create a Twilio client
client = Client(account_sid, auth_token)

main_account = client.api.accounts(account_sid).fetch()
balance = main_account.balance

print(f"Your Twilio account balance is: {balance}")
