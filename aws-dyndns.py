import socket, re, boto3, urllib3, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dns')
parser.add_argument('--id')
args = parser.parse_args()

dnsname =  args.dns 
zoneid = args.id 


print('DNS recored: ' + dnsname)
print('ZONE ID: ' + zoneid)
 
url = 'http://ipecho.net/plain'


http = urllib3.PoolManager()
r = http.request('GET', url)

#old_ip = socket.gethostbyname(dnsname)
new_ip = re.sub("(b|')", "", str(r.data))


client = boto3.client('route53')

print('INFO: Changing dns recorded ' + dnsname + ' to ' + new_ip)


client.change_resource_record_sets(
HostedZoneId = zoneid,

ChangeBatch = {
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

