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

monitorBindingKey='create.success'

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
    print(account)
    port = 465  # For SSL
    sender_email = "cocktailogy.esd@gmail.com"
    sender_p = input("Type your password and press enter: ")
    # sender_p = "cockt4ilogy!"

    # TODO: replace with customers email
    receiver_email = "andrea.yap.2020@smu.edu.sg"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Welcome to the Cocktailogy family!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # TODO: replace # with our deployed app login page
    html = """\
    <html>
      <body>
      <b>Hi there!</b><br>
      We are so happy to see you join our family! &#128513;<br>
      Feel free to scroll through our page to check out our drinks <a href="#">here</a>. <br><br>
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


if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveAcountDetails()
