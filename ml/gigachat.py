from gigachat import GigaChat
import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': '4f8f3727-d5ca-49cf-80fb-8dc249bbce86',
  'Authorization': 'Basic <Authorization key>'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

giga = GigaChat(
   credentials="ключ_авторизации",
)

response = giga.get_token()

print(response)
