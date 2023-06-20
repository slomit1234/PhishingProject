# PhishingProject
Maabadat Hatkafa - Phishing Project

We submitted the following files:

1.Phishing.py - Sends the Pishing mail.

2.Create_attachment.py - copy attachment to another file.

3.Attachment.py - get all the user info and send it to 1.2.3.4 (using DNS Tunneling).

4.a.html - the lure (the email)

Requirements:
* python
* scapy
* smtplib
* email MIME
* requests

Testing:

1.Run Phishing.py:

<img width="678" alt="image" src="https://github.com/slomit1234/PhishingProject/assets/42152443/7ffeab2f-6e73-4318-befb-5b530d9e4f8d">

Here you can see that the mail sent to the victim (in this case slomitas@gmail.com)

<img width="910" alt="image" src="https://github.com/slomit1234/PhishingProject/assets/42152443/edd046a3-2afa-41b2-86b7-d81e9c5a0c2f">

2. now if we download and press(run) the attachment of the mail, it will run attachment.py

* please notice that the attachment.py needs to run as admin (to read the password file)
* Capture.pcap is attached
* for convenience purposes, the endpoint of the DNS tunnel is 1.2.3.4

attachment.py - on Windows system:
<img width="937" alt="image" src="https://github.com/slomit1234/PhishingProject/assets/42152443/f9404376-92f1-49a6-81e2-d8f9d2a6b19a">

attachment.py - on Linux system:
<img width="850" alt="image" src="https://github.com/slomit1234/PhishingProject/assets/42152443/bbfab04c-173e-4bdc-b255-6b7af3cdac83">
