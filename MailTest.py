import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

fromaddr = "ceragioli.arnaud@hotmail.com"
toaddr = "ceragioli.arnaud@hotmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test"

body = "YOUR MESSAGE HERE"
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('ceragioli.arnaud@hotmail.com', 587)
server.starttls()
server.login(fromaddr, "Zeusse1996")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()