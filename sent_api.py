import requests

url = "http://api.meaningcloud.com/sentiment-2.1"

payload = "key=YOUR_KEY_VALUE&lang=en&txt=YOUR_TXT_VALUE&txtf=plain&url=YOUR_URL_VALUE&doc=YOUR_DOC_VALUE"
headers = {'content-type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
