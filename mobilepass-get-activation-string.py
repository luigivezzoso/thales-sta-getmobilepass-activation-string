import requests
from bs4 import BeautifulSoup
import lxml

banner = """

 ___                    __ ___             __                                _                                                   __                 
  | |_   _. |  _   _   (_   |  /\    __   /__  _ _|_   |\/|  _  |_  o |  _  |_) _.  _  _    /\   _ _|_ o     _. _|_ o  _  ._    (_ _|_ ._ o ._   _  
  | | | (_| | (/_ _>   __)  | /--\        \_| (/_ |_   |  | (_) |_) | | (/_ |  (_| _> _>   /--\ (_  |_ | \/ (_|  |_ | (_) | |   __) |_ |  | | | (_| 
                                                                                                                                                 _| 

 """

print(banner)

# SOAP request URL

API_URL = "https://cloud.eu.safenetid.com/bsidca/BSIDCA.asmx"

# structured XML

# headers
headers_auth = {
	'Host': 'cloud.eu.safenetid.com',
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept-Encoding':'gzip,deflate',
    'SOAPAction':'http://www.cryptocard.com/blackshield/Connect',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.5.5 (Java/16.0.1)'

}

# headers
headers_token = {
	'Host': 'cloud.eu.safenetid.com',
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept-Encoding':'gzip,deflate',
    'SOAPAction':'http://www.cryptocard.com/blackshield/GetMobilePASSProvisioningActivationCode',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.5.5 (Java/16.0.1)'

}

company = 'Umbrella Corp'
username = input("STA Operator Email: ")  # Enter STA Tenant Operator Email
passcode = input("STA Operator OTP: ")  # Enter STA Tenant Operator OTP
print()
user = input("Provisioned User: ")  # Enter the username of user of which we want retrieve MobilePass activation string
taskid = input("Provisioning TaskID: ")  # Enter the TaskID of the enrolled token



mobilepass_payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:blac="http://www.cryptocard.com/blackshield/">
   <soapenv:Header/>
   <soapenv:Body>
      <blac:GetMobilePASSProvisioningActivationCode>
         <!--Optional:-->
         <blac:userName>"""+ user + """</blac:userName>
         <blac:taskID>""" + taskid + """</blac:taskID>
         <!--Optional:-->
         <blac:organization>"""+company+"""</blac:organization>
      </blac:GetMobilePASSProvisioningActivationCode>
   </soapenv:Body>
</soapenv:Envelope>"""


auth_payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:blac="http://www.cryptocard.com/blackshield/">
   <soapenv:Header/>
   <soapenv:Body>
      <blac:Connect>
         <!--Optional:-->
         <blac:OperatorEmail>""" + username +"""</blac:OperatorEmail>
         <!--Optional:-->
         <blac:OTP>""" + passcode + """</blac:OTP>
         <!--Optional:-->
         <blac:validationCode>?</blac:validationCode>
      </blac:Connect>
   </soapenv:Body>
</soapenv:Envelope>"""


# Creating a Session Object

api_session = requests.Session()
api_session.headers.update(headers_auth)
api_session.auth = ('username','pass')

response = api_session.post(API_URL,headers=headers_auth,data=auth_payload)



soup = BeautifulSoup(response.text,'xml')
auth_result = soup.find('ConnectResult')
print('Authentication Status: ' + auth_result.text)
api_session.headers.update(headers_token)
response = api_session.post(API_URL,headers=headers_token,data=mobilepass_payload)
#print(response.text)



soup = BeautifulSoup(response.text,'xml')
activationString_result = soup.find('GetMobilePASSProvisioningActivationCodeResponse')
print('Activation String: ' + activationString_result.text)






