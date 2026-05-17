import smtplib


content = "whatever"

mail = smtplib.SMTP("smtp.gmail.com" , 587)
mail.ehlo()
mail.starttls()
emailAddress = "laflametoast@gmail.com"
password = "YOUR_EMAIL_PASSWORD"
mail.login(emailAddress , password)
mail.sendmail("fromEmail@gmail.com" , "affan.fareed@gmail.com", content )






