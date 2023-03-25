import amino
import secmail
from time import sleep
from requests import get
from random import randint
from pywebio.input import *
from pywebio.output import *
from names import get_last_name
from pywebio import start_server, config

def generator():
    def get_verification_code(sec_mail: secmail.SecMail, email: str):
        sleep(3)
        verify_messageID = sec_mail.get_messages(email=email).id
        verification_link = sec_mail.read_message(
            email, verify_messageID[0]).htmlBody.split('"')[13]
        put_table([
              ["Verification code", put_image(src=verification_link)]
          ])

    def save_account(email: str, password: str, device_id: str):
        with open("accounts.txt", "a") as accounts:
            accounts.write(f"{email}:{password}:{device_id}\n")
            accounts.close()


    def generate_device_id():
        return amino.lib.util.helpers.generate_device_id()


    def auto_register():
        sec_mail = secmail.SecMail()
        password = input("Password for all accounts", required=True, placeholder="Password", type=PASSWORD)
        while True:
            client = amino.Client(deviceId=generate_device_id())
            try:
                nickname = get_last_name()
                email = sec_mail.generate_email()
                device_id = client.device_id
                put_table([
                        ["Account"],
                        ["Email", email],
                        ["Password", password],
                        ["deviceID", device_id]
                ])
                client.request_verify_code(email=email)
                get_verification_code(sec_mail=sec_mail, email=email)
                verification_code = input(
                    "Verification code",
                    required=True,
                    placeholder="Verification code")
                client.register(
                    nickname=nickname,
                    email=email,
                    password=password,
                    verificationCode=verification_code,
                    deviceId=device_id)
                save_account(email=email, password=password, device_id=device_id)
                put_success(f"{email} is registered and saved in accounts.txt!")
            except Exception as e:
                put_error(e)


    @config(theme="minty", title="AminoAutoRegWeb")
    def main():
        popup(title="🍻Welcome", content="AminoAutoRegWeb - by zeviel;")
        put_link(
            name="Script Author",
            url="https://github.com/zeviel",
            new_window=True)
        auto_register()


    start_server(main, debug=True, port=randint(1000, 8000), cdn=False)
    