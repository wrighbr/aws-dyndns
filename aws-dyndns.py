import socket
import re
import boto3
import urllib3
import argparse
import time
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('--dns')
parser.add_argument('--id')
args = parser.parse_args()


dnsname = args.dns
zoneid = args.id


now = datetime.now()

url = 'http://ipecho.net/plain'


http = urllib3.PoolManager()
r = http.request('GET', url)

new_ip = re.sub("(b|')", "", str(r.data))

client = boto3.client('route53')

zone = client.list_resource_record_sets(
    HostedZoneId=zoneid,
    StartRecordName=dnsname
)

rrs = zone['ResourceRecordSets']
current_ip = rrs[0]['ResourceRecords'][0]['Value']


print(str(now) + ': DNS recored: ' + str(dnsname))
print(str(now) + ': ZONE ID: ' + str(zoneid))
print(str(now) + ': Current IP Address is ' + str(current_ip))

print(str(now) + ': Checking if IP address has changed')

if current_ip != new_ip:
    print(str(now) + ': IP address has changed. Now Changing dns recorded ' +
        str(dnsname) + ' to ' + str(new_ip))

    client.change_resource_record_sets(
                HostedZoneId=zoneid,
                ChangeBatch={
                    "Comment": "Update record to reflect new IP Public address",
                    "Changes": [
                        {
                            "Action": "UPSERT",
                            "ResourceRecordSet": {
                                "Name": dnsname,
                                "Type": "A",
                                "TTL": 60,
                                "ResourceRecords": [
                                    {
                                        "Value": new_ip
                                    }
                                ]
                            }
                        }
                    ]
                }
            )
        
