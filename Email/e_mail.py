## email microservice will email the recepient and return the customer's email in the function when it is completed.
# inputs required: customer email, customer name (optional)
# receiver of AMPQ direct msg from create_account.py


# to create an account, user has to use facebook. email is therefore already VERIFIED and does not need further verification that the email exists in this microservice.


# this microservice uses SMTP_SSL() to send emails.
# Documentation: https://realpython.com/python-send-email/
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
import os
# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

import amqp_setup

monitorBindingKey='try.email'

def receiveAcountDetails():
    amqp_setup.check_setup()
        
    queue_name = 'email'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an accounts details by " + __file__)
    processAccountDetails(json.loads(body))
    print() # print a new line feed

def processAccountDetails(account):
    print("Sending an email to the customer:")
    print("Account variable", account)
    # print("Account data", account["data"])
    port = 465  # For SSL
    if account["email_action"]=="1":
      sender_email = "cocktailogy.esd@gmail.com"
      sender_p = "cockt4ilogy!"
      
      receiver_email = account["email"]

      message = MIMEMultipart("alternative")
      message["Subject"] = "Welcome to the Cocktailogy family!"
      message["From"] = sender_email
      message["To"] = receiver_email

      # TODO: replace # with our deployed app login page
      html = f"""\
      <html>
        <body>
        <b>Hi {account['account_name']}!</b><br>
        We are so happy to see you join our family! &#128513;<br>
        Feel free to scroll through our page to check out our drinks after loggin in <a href="https://localhost:9000">here</a>. <br><br>
          </p>
          Warmest Regards,<br>
          Cocktailogy Development Team
        </body>
      </html>
      """
      # Turn these into plain/html MIMEText objects
      part2 = MIMEText(html, "html")
      # Add HTML/plain-text parts to MIMEMultipart message
      message.attach(part2)
      # Create a secure SSL context
      context = ssl.create_default_context()

      # !! do not store email password in code. Use Input to let user type in their password when running the script
      with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
          server.login(sender_email, sender_p)
          server.sendmail(sender_email, receiver_email, message.as_string())

      print("Email has been sent to the customer that their account has been successfully created.")
      
    elif account["email_action"] == "2":
      sender_email = "cocktailogy.esd@gmail.com"
      sender_p = "cockt4ilogy!"
      
      receiver_email = account["email"]
      print("account : ",account)
      print("account name: ",account['account_name'])

      message = MIMEMultipart("alternative")
      message["Subject"] = "Cocktailology pickup order not fulfilled"
      message["From"] = sender_email
      message["To"] = receiver_email

      # TODO: replace # with our deployed app login page
      html = f"""\
      <html>
        <body>
        <b>Hi {account['account_name']},</b><br>
        We are sorry to inform you that we have no more stock for your order items. Our inventory is low, we will let you know when the stock is replenished!<br> Click
        <a href="https://localhost:9000">here</a> to see more drinks!<br><br>
          </p>
          Warmest Regards,<br>
          Cocktailogy Development Team
        </body>
      </html>
      """
      # Turn these into plain/html MIMEText objects
      part2 = MIMEText(html, "html")
      # Add HTML/plain-text parts to MIMEMultipart message
      message.attach(part2)
      # Create a secure SSL context
      context = ssl.create_default_context()

      # !! do not store email password in code. Use Input to let user type in their password when running the script
      with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
          server.login(sender_email, sender_p)
          server.sendmail(sender_email, receiver_email, message.as_string())

      print("Email has been sent to the customer that their account has been successfully created.")
    else:
      print(account, "action not 1")


if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveAcountDetails()
