import requests
import json

# url = 'https://www.gtabase.com/media/com_jamegafilter/en_gb/1.json'
# response = requests.request("GET", url)
# data = response.json()
# name = "Schlagen GT"
# # for x in data:
# #     thedata = data[x]['attr']
# #     print("Name: " + data[x]['name'] + " " + x)
# #     print(thedata["ct1"]['title'][0] + ": " + thedata["ct1"]['frontend_value'][0])
# #     try:
# #         print(thedata["ct2"]['title'][0] + ": " + thedata["ct2"]['frontend_value'][0])
# #     except:
# #         pass
# #     print(thedata["ct32"]['title'][0] + ": " + thedata["ct32"]['frontend_value'])
# #     print(thedata["ct33"]['title'][0] + ": " + thedata["ct33"]['frontend_value'])
# #     try:
# #         print(thedata["ct34"]['title'][0] + ": " + thedata["ct34"]['frontend_value'][0])
# #     except:
# #         pass
# #     try:
# #         print(thedata["ct35"]['title'][0] + ": " + thedata["ct35"]['frontend_value'][0])
# #     except:
# #         pass
# #     print(thedata["ct6"]['title'][0] + ": " + thedata["ct6"]['frontend_value'])
# #     print(thedata["ct7"]['title'][0] + ": " + thedata["ct7"]['frontend_value'])
# #     print(thedata["ct8"]['title'][0] + ": " + thedata["ct8"]['frontend_value'])
# #     print(thedata["ct9"]['title'][0] + ": " + thedata["ct9"]['frontend_value'])
# #     print(thedata["ct10"]['title'][0] + ": " + thedata["ct10"]['frontend_value'])
# #     try:
# #         print(thedata["ct72"]['title'][0] + ": " + thedata["ct10"]['frontend_value'])
# #     except:
# #         pass
# #     try:
# #         print(thedata["ct132"]['title'][0] + ": " + thedata["ct132"]['frontend_value'])
# #     except:
# #         pass

# for x in data:
#     if data[x]['name'] == name:
#         thedata = data[x]['attr']
#         print("Name: " + data[x]['name'] + " " + x)
#         for y in thedata:
#             # print(print(y))
#             data1 = thedata[y]['title']
#             data2 = thedata[y]['frontend_value']
#             if isinstance(data1, list):
#                 data1 = data1[0]
#             if isinstance(data2, list):
#                 data2 = data2[0] 
#             print(data1 + ": " + str(data2))

# data = {'footer': {'text': 'Posted by Łilson#4971'}, 'thumbnail': {'url': 'http://www.buygosleep.com/wp-content/uploads/2016/01/Car-Icon.png', 'proxy_url': 'https://images-ext-2.discordapp.net/external/GGWTBmj9QaL4AvGbWsE_VZN4Q7KJaFEPHcpo_LXtTY0/http/www.buygosleep.com/wp-content/uploads/2016/01/Car-Icon.png', 'width': 0, 'height': 0}, 'author': {'name': 'Mike Willson', 'icon_url': 'https://cdn.discordapp.com/avatars/216551246457339904/18e64f56a7b58a2f6317482328f437c3.webp?size=1024', 'proxy_icon_url': 'https://images-ext-2.discordapp.net/external/CDL-5EF-MwRRiPdVIjVuCnooJMGHRR-olqh6rF34FGM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/216551246457339904/18e64f56a7b58a2f6317482328f437c3.webp'}, 'fields': [{'name': 'Vehicle Name', 'value': 'Novak (SUV)', 'inline': True}, {'name': 'Price', 'value': '$ 409,500', 'inline': True}, {'name': 'Preferred to be contacted by', 'value': 'email', 'inline': True}, {'name': 'Phone Number', 'value': '2359272', 'inline': True}, {'name': 'Discord', 'value': '<@216551246457339904>', 'inline': True}, {'name': 'Remarks', 'value': 'Bazinga', 'inline': True}], 'color': 16711680, 'type': 'rich'}

# for x in data['fields']:
#     if x['name'] == 'Discord':
#         print(x['value'])

url = "https://api.eclipse-rp.net/auth/login"
payload = """{"username":"minin0la","password":"Mnnl1480@ecrp"}"""
headers = {
'Accept': 'application/json, text/plain, */*',
'DNT': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'Content-Type': 'application/json;charset=UTF-8'
}
response = requests.request("POST", url, headers=headers, data = payload)
result_token = response.json()['token']
url = "https://api.eclipse-rp.net/basic/vehicledealerships"
payload = {}
headers = {
'Accept': 'application/json, text/plain, */*',
'DNT': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'token': str(result_token)
}
stocks = []
response = requests.request("GET", url, headers=headers, data = payload)
data = response.json()
data = data['dealerships']
for x in data:
    if x['Name'] == 'Motorsport':
        for y in x['VehicleStocks']:
            if y['v']['Stock'] != 0:
                stocks.append(y['v'])
    if x['Name'] == 'DownTownBoats':
        for y in x['VehicleStocks']:
            if y['v']['Stock'] != 0:
                stocks.append(y['v'])
classlist = [x['Class'] for x in stocks]
classlist = list(dict.fromkeys(classlist))
for x in classlist:
    for y in stocks:
        if y['Class'] == x:
            print(y['Name'])
# print(classlist)