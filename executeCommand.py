import os
from winreg import *
import win32serviceutil
import time
import psutil


if os.name == 'nt':
    os.chdir(r"C:\Program Files\Veritas\NetBackup\wmc\bin\install")
    os.system(r'configureWebServerCerts.bat -addExternalCert -all -certPath c:\eca\cert_chain.der.p7b -privateKeyPath c:\eca\private\key-pkcs8.der -trustStorePath c:\eca\trusted\cacerts.der.p7b')

    aKey = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Veritas\NetBackup\CurrentVersion\Config", 0, KEY_ALL_ACCESS)
    SetValueEx(aKey, 'ECA_CERT_PATH', 0, REG_SZ, 'c:\eca\cert_chain.der.p7b')
    SetValueEx(aKey, 'ECA_TRUST_STORE_PATH', 0, REG_SZ, r'c:\eca\trusted\cacerts.der.p7b')
    SetValueEx(aKey, 'ECA_PRIVATE_KEY_PATH', 0, REG_SZ, 'c:\eca\private\key-pkcs8.der')

    os.chdir(r'C:\Program Files\Veritas\NetBackup\bin')
    os.system('nbcertcmd.exe -enrollCertificate')

    serviceName='NetBackup Web Management Console'
    win32serviceutil.RestartService(serviceName)

    service = psutil.win_service_get(serviceName)
    service = service.as_dict()

    while service['status'] != 'running' :
        print(f"NetBackup Web Management Console service status is  {service['status']}")
        time.sleep(5)
        service = psutil.win_service_get(serviceName)
        service = service.as_dict()

else:
    pass
