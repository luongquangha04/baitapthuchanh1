import smtplib
import imaplib
import email
from email.mime.text import MIMEText

# Đọc dữ liệu từ tệp
with open('email_credentials.txt', 'r') as f:
    lines = f.readlines()
    sender_email = lines[0].strip()
    app_password = lines[1].strip()

with open('recipient.txt', 'r') as f:
    recipient_email = f.read().strip()

with open('email_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

with open('email_filter.txt', 'r') as f:
    filter_sender = f.read().strip()

# Gửi email
msg = MIMEText(content)
msg['Subject'] = 'Thử nghiệm gửi email từ Python'
msg['From'] = sender_email
msg['To'] = recipient_email

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)
    print("✅ Email đã được gửi đến", recipient_email)

# Nhận email
with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
    mail.login(sender_email, app_password)
    mail.select('inbox')
    result, data = mail.search(None, f'FROM "{filter_sender}"')
    ids = data[0].split()

    if ids:
        latest_email_id = ids[-1]
        result, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        print("📥 Đã nhận được email:")
        print("Tiêu đề:", msg['Subject'])

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    print("Nội dung:", part.get_payload(decode=True).decode())
                    break
        else:
            print("Nội dung:", msg.get_payload(decode=True).decode())
    else:
        print("❌ Không có email nào phù hợp.")
        import smtplib
import imaplib
import email
from email.mime.text import MIMEText

# Bước 1: Đọc thông tin tài khoản Gmail từ tệp
with open('email_credentials.txt', 'r') as file:
    account_info = file.readlines()
    email_address = account_info[0].strip()
    app_password = account_info[1].strip()

# Bước 2: Đọc nội dung email, người nhận, và tiêu chí lọc
with open('email_content.txt', 'r') as file:
    email_content = file.read()

with open('recipient.txt', 'r') as file:
    recipient_email = file.read().strip()

with open('email_filter.txt', 'r') as file:
    filter_sender = file.read().strip()

# Bước 3: Gửi email qua SMTP
msg = MIMEText(email_content)
msg['Subject'] = 'Email Tự Động'
msg['From'] = email_address
msg['To'] = recipient_email

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(email_address, app_password)
    server.send_message(msg)
    print("✅ Email đã được gửi thành công.")

# Bước 4: Nhận email từ hộp thư đến qua IMAP
with imaplib.IMAP4_SSL('imap.gmail.com') as server:
    server.login(email_address, app_password)
    server.select('INBOX')

    # Tìm email từ người gửi cụ thể
    _, data = server.search(None, f'FROM "{filter_sender}"')
    for num in data[0].split():
        _, msg_data = server.fetch(num, '(RFC822)')
        email_msg = email.message_from_bytes(msg_data[0][1])
        subject = email_msg['subject']
        print(f"📬 Tiêu đề email nhận được: {subject}")
        
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == 'text/plain':
                    print("📄 Nội dung:")
                    print(part.get_payload(decode=True).decode())
                    break
        else:
            print("📄 Nội dung:")
            print(email_msg.get_payload(decode=True).decode())
        break  # Chỉ đọc 1 email đầu tiên