import requests
from datetime import datetime, timedelta
import time

#import json

notifyUrl = 'http://192.168.1.245:1880/chompy?vt={}&dt={}'
exitUrl = 'http://192.168.1.245:1880/chomped?code={}'
url = "https://mychart.montagehealth.org/mychart/OpenScheduling/OpenScheduling/GetScheduleDays?noCache=0.5941451357342415"

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
  '__requestverificationtoken': 'ZxK_Hp3oLpLxV-GpkD3dkIdKWkj1wWmn_8l3Kiq55sw67Dk0NgjClW64pTYlOftMEjhha5zRIkJ4iFXwAfHCaIbzHDg1',
  'cookie': 'MyChart_Session=x1ghxkbnrqwy3zxp2kagchdh; __RequestVerificationToken_L215Y2hhcnQ1=vO7R6XEGJDDE-VtpoLfTOuGbbGiCs9fgi6Dvh2ah1ZzacApkVknp6Wo82fa-rHh31rBKfnUbmnlt0J33ZkJoGdqm9iQ1; MyChartLocale=en-US; .WPCOOKIE4mychart=F709A55A157E5939BA87E0044F15D57A1E54665B68735CAE90E711838C1EBAEA1C5226FBF6B16CBAFA8722D59F0B15CE3D7BB6D77002F5C85CBB221030B13674A4889B23E466276D8ACE8AF8926121E27099DF66C3048AD2D22144DA3F0C8CF699BE0C41477873B0FE540789B99D98964185128523F8C67970EB0A368F85F58CE241E76D12B3318AB9ACD53EAE6764EE534EF016FD6CA3F0BF9E536120DCB67CAAC615B768D6857AFD473AC042F2F6F338DCF45DCAE7D6A823D9A6C8D2D4B269B4E34501F2E9EEBEADA3E4141FB3FAA6C7B3ADCA67E65C24B79B64EB84D3F02FBF4D5C51CF505B2266BAC75DADFE3A668C90FD04; MYCPERS=3456111626.47873.0000; __zlcmid=13PjvO2BxHaDO3a; MyChartLocale=en-US; MYCPERS=3456111626.47873.0000'
}

vts = {
"117741": "Pfizer",
"117744": "Pfizer Standby",
"1171006": "Moderna",
"1171007": "Moderna Standby",
"1171008": "Janssen",
"1171009": "Janssen Standby"
}

notifyCount = 0;

requests.request("GET", exitUrl.format(58))

while notifyCount < 50 :
    for vt, name in vts.items():
        print("Name: " + name)
        #print("vt: " + vt)
        currDt = datetime.now() - timedelta(hours=7) #Convert UTC to PST
        for week in range(1,6):
            fmtDt = currDt.strftime("%Y-%m-%d")

            payload={'view': 'grouped',
            'specList': '246',
            'vtList': vt,
            'start': fmtDt,
            'filters': '{"Providers":{},"Departments":{},"DaysOfWeek":{},"TimesOfDay":"both"}'}

            response = requests.request("POST", url, headers=headers, data=payload)
            if(response.status_code != 200):
                requests.request("GET", exitUrl.format(response.status_code))
                sys.exit(response.status_code)
            #print(response)
            resp = response.json()
            #print(resp)

            if(resp.get("AllDays")):
                print(" - Week of:" + fmtDt + ": Available!")
                notifyCount += 1
                requests.request("GET", notifyUrl.format(name, fmtDt))
            else:
                print(" - Week of:" + fmtDt + ": None")

            currDt = currDt + timedelta(weeks=1)

    time.sleep(1800) #check every 30 mins
