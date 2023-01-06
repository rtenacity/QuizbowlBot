import requests
from requests.structures import CaseInsensitiveDict

url = "http://qbreader.org/api/query"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{"questionType":"tossup", "searchType":"tossup"}'


resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
