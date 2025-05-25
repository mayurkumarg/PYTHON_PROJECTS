import smtplib
from email.mime.text import MIMEText

CORRECT_PASSWORD = "1234"
SENDER_EMAIL = "Type here senders Email"
SENDER_PASSWORD = "Senders Gmail password"
RECIPIENT_EMAIL = "Type here recievers Email"

DEVICE_STATUS = {
    "lights": "off",
    "thermostat": "idle",
    "door": "locked"
}

def send_alert_email(subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        msg = MIMEText(body)
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def toggle_device(device):
    if device in DEVICE_STATUS:
        DEVICE_STATUS[device] = "off" if DEVICE_STATUS[device] == "on" else "on"
        print(f"{device.capitalize()} is now {DEVICE_STATUS[device]}.")
    else:
        print(f"Device '{device}' not recognized.")

def control_smart_home():
    print("\n<========== SMART HOME CONTROL PANEL ==========>")
    print("Available devices: lights, thermostat, door")
    print("Commands: 'toggle <device>' or 'exit'")
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "exit":
            print("Exiting Smart Home Control Panel.")
            break
        elif command.startswith("toggle "):
            toggle_device(command.split(" ")[1])
        else:
            print("Invalid command. Try again.")

def attempt_login():
    attempts = 0
    while attempts < 2:
        entered_password = input("Enter the password: ").strip()
        if entered_password == CORRECT_PASSWORD:
            print("Access granted! Welcome to your smart home.")
            DEVICE_STATUS["door"] = "unlocked"
            control_smart_home()
            break
        else:
            attempts += 1
            print(f"Incorrect password! You have {2 - attempts} attempt(s) left.")
            if attempts == 2:
                send_alert_email("Smart Home Security Alert", "SECURITY ALERT !!!! ☠  ☠.\n\nSOMEONE TRIED TO ACCESS THE SMART HOME CONTROLL")
                print("Alert sent to your email.")
                DEVICE_STATUS["door"] = "locked"

def main():
    print("<========== SMART HOME SECURITY SYSTEM ==========>")
    print("Welcome! Please enter your password to access the system.")
    attempt_login()

if _name_ == "_main_":
    main()