import csv
import requests
import json
import sys
import uuid
import json
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# run using python3 importpsk_v11.py


def readfile():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%m-%d-%Y")
    print ("Reading CSV file", end = "")
    with open(SZKEYFILE, mode="r", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        result = {}
        for row in reader:
            key = row.pop("Passphrase")
            result[key] = row
            row["uuid"] = "SZ2CP-"+timestampStr+"-"+str(uuid.uuid4())
            print (".", end = "")
    print (" ")
    return result

def getcptoken(username, password):
    #print ("Getting API token")
    url = "https://"+CPFQDN+"/admin/publicApi/token"
    body = {"userName":username, "password":password}
    response = requests.post(url, json=body, verify=False)
    token = response.json()['token']
    return token

def createdpsks(olddpsk):
    url = "https://"+CPFQDN+"/admin/publicApi/dpskPools/"+CPDPSKGUID+"/dpsks"
    for key in olddpsk:
        token = getcptoken(CPUSER, CPPASSWORD)
        print ('Creating EDPSK '+key+" ", end = "")
        uuid = olddpsk[key]["uuid"]
        VLAN = olddpsk[key]["VLAN ID"]
        name = olddpsk[key]["User Name"]
        cpheaders = {"Content-Type":"application/json", "Authorization":token}
        body = {"name":uuid, "passphrase":key, "vlanid":VLAN, "thirdPartyId":name}
        response = requests.post(url, headers=cpheaders, json=body, verify=False)
        
        
        if response.status_code == 201:
            print("Key Created - " + name + " " +key)
        elif response.status_code == 409:
            
            json_data = json.loads(response.text)
    

            print("Error creating key: " +json_data['message'])

        
    print (" ")
    return

def main(argv):
    if len(sys.argv) == 6:
     CPFQDN = sys.argv[1]
     CPUSER = sys.argv[2]
     CPPASSWORD = sys.argv[3]
     SZKEYFILE = sys.argv[4]
     CPDPSKGUID = sys.argv[5]
     szkeys = readfile()
     createdpsks (szkeys)
     return
    else:
        print("Please supply the following information: \n\n Cloudpath Server Address \n Cloudpath Username \n Cloudpath Password \n CSV File Name \n Cloudpath DPSK GUID")
        print("\n Example: python3 importdpsk.py myserver.com joe@ruckus.com password123 keyfile.csv AccountDpskPool-d989b726-383f-4384-8916-03cef08d6f36 \n\n")

if __name__ == "__main__":
        main(sys.argv[1:])
