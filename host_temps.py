

from pyVim.connect import SmartConnect, Disconnect
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

try:
    c = SmartConnect(host='vcenter.lab.local', user='root', pwd='Passw0rd')
    print('Valid certificate\n')
except:
    c = SmartConnect(host='vcenter.lab.local', user='root', pwd='Passw0rd', sslContext=s)
    print('Invalid or untrusted certificate\n')

host = c.content.searchIndex.FindByDnsName(None,'esx1.lab.local',False)
health = host.runtime.healthSystemRuntime.systemHealthInfo.numericSensorInfo

print('Hostname: ' + host.name)
print('Type: ' + host.hardware.systemInfo.model)
print('Getting temperature sensor data...\n')

for i in health:
    if i.sensorType == 'temperature':
        temp=i.currentReading/100
        print(i.name + ' ' + str(temp) + ' ' + i.baseUnits)

Disconnect(c)