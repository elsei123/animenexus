import requests


def send_email_via_emailjs(name, email, message):
    url = "https://api.emailjs.com/api/v1.0/email/send"
    payload = {
        "service_id": "your_service_id",
        "template_id": "your_template_id",
        "user_id": "your_api_key",
        "template_params": {"name": name, "email": email, "message": message},
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print(f"Error sending email: {response.status_code} - {response.text}")
        return False
