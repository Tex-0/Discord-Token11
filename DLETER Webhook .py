import os
import sys
import time
import json

# Ensure requests is installed
try:
    import requests
except ImportError:
    print("\n[!] Error: 'requests' module not found.")
    print("[!] Please run: pip install requests")
    input("\nPress Enter to exit...")
    sys.exit()

# Setup terminal for ANSI color codes (Windows compatibility)
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# ANSI Color Codes for CMD
R = "\033[31m"  # Red
G = "\033[32m"  # Green
W = "\033[0m"   # White
Y = "\033[33m"  # Yellow
B = "\033[34m"  # Blue

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""{R}
.-%#**%*:...:+**=:....:#*:::+*:...........   .                 
                   . .            ....*%===*#-..:#%**##-....=#=-=*+.......................          
                                  ....-#%##%+...:#%**##-....=#**#=.....-+*+-...............         
                                  ......:#@%#-...:%@%%=...:+#=:-*=....+#*+*#=....:=+=:.......       
                                    .....+%*#%=.:#%##%+:.-**-:::+*-...=#****-...=#+=+*=......      .
                      .    .        .....=%*=*%*#%#***#++#+:::::-*+..:*###+:....**::-++:.....       
     . . ..                         .....-%*==+%%#****##*-:::::::=*=+#***#+...:=###**+:....         
                                   .....:#%%#===*%%%%%#+:::-#%+:::+##****#*--*#+=#+:.......         
 .      .       .        .          ....#%%%%*=======-::::*%#%%+::-*#*****##*=--#*........   .      
          .                         ....=%%%#+=------:::-#%###%#=::-+#####+-::-*#:.....             
          .                       .......-%#+=-----=-::::=%%##%*-:::::::::::=#%%+......             
     .                   .    ...........:%%#*====----::::=%%#-::::::::::::-#%%%#......             
    .               .....................-%*=+*#%%%#*+-::::--::::::::::::::=#%%%*.......            
                    ...........:-=++**###%%%*+======+*#%%%%%#+=---:::::::::-#%*:.......             
     .     ...........:=*#%%%%%%%%%#**++=+++*%%%%%#*+==--:::--=++*##%%%%%%%%%=.........         .   
      .    ......-*%%%%%#####**++++++**#**++==----=++*#%%%#*+=-------:--::-*#-.........             
          ....-#%%#+-:------::::::::::::::--=++*******++-::-+#%%%%%%%%%%%%%%#:.........    .        
         ..:*@%*=-:-+-:::::---==+++++++=--::::.:::::::::::-+*=::-*+-:.....:+##-........             
  .   ....+@%+------:::-=+++++==--:::::::::::::--:::::--=++=:::==::-=-:....:=##-.......             
   .  ...*@#--------+#+-:::::::::-=-::::::::::+=:............:=-::=-:.::.....=##:.........          
     ...:@@+:------*=:-::::::::::==::::::::::-=:................:-::-:.......:+##:........          
   .....+@%-----------:----::::::-+-:::::::::::..:-=+**####*=-:::..............+##-.....   .        
   ...:*@%=:----------=+***+++=:::-:::::::::::-=#%%#++#%%%%%%%%#+-:............:=##=........       .
 ....=%@#----------=%@@%%%%@@@@@#+-::::::::::+%%*-...:+%%%%%%#+*##+::-::.......::+##*-......        
 ..-#@#==+**+++++=-+##%%%%@@@@@@%*++-:::::+%%-.:=*%%%##*****####+:.-+-....:-======*#*-........    
 .-%%+=*+===-----:-----------=+*#%@@%+-:::::-+%%%%#+=-::=+=:....:.....:=+*##**+-..:-==*#*:........  
.:%@*++=**=-+***+=-:-------------+@*-:::::::::-=-::::::::+#%*-::::-=*#%%*+=-=+*%#=:.---*#*......... 
.-@%*+=*+-#@%***#@@#+==**=-------+%*---::::::::::::::::::::=*#%%%%%#*+-::=*=::::*%*:.--:*%+.......  
.=@%*+-*=-=----=--+#%@%%*--:---=#%%+----:::::::::::::::::::::::::::::::-+#%*-::::+#+.--:=##.....    
.-@%*+-*+----=#@+---------:--*#%%+---------:-*%@%#+-+-:::::::::::::-=*#%%*#%%*=::=%+:--:=%#:..      
..*@#*=-++---*@@*---------=*%@@#---------:::::--=%@+-======-:::-=*#%%*=:..+%%##+:##=:=-:*@*.  .     
..:#@*+*+---=%@@@+-----=+++++#%%+--::---=%%%%%#-=%%=:::::::-+*#%%%#-.....=%#=:::=%+:-=-+%%-.        
 ..:#@*--==-+@@@@@#=-----------*%#*++*----------**-:::=*#%@@%*==##:...:=#%%+::::--:=+-+%%-..        
   .-%@+----#@@@%#@@@#+=----:---=*%%%*-------:-=+*##%@@%+=-....=%#-=*#%%%%+::::::---=#%#-...        
   ..+@#=--=#@@%=+%#+#@@@%##*++======+++*##%%@@@%#*@%+.......:*@@@@@*=+%#=::::::::*%@%=...  ...     
   ..:#@+--=%@@#-*@*..-%@*+#%@@@@@@@@%%%@@#=-::....*@+...=*#%@@@@@+:.*@%=::::::::=%%*:..    ...     
     .*@*--=%@@@%@@%:.=%*:.....*@*......%%:........=@@%%@@@@@%++%#:-%@#=------::+%%=......  ...   . 
     .+@#---#@@@@@@@@%@@@%#*+==%@#-----+@@+-=+*#%%@@@@@@@#=:...:#@%@@+---------=%%-............     
     .=%#---#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@%=........*@@#=---------=%@=..... ........    
 . ...=@#---+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*-:..:#%=.....:*@@#=----------+%@=...... .........   
   ...+@#---=%@#%@%*@@@@@@@@@@@@@@@@%#*+=+@#:........=@#:..=%@@#=----------=#@%:..                  
   ...*@*----+%@%@@--@%=.+@#:..-%@*:.....-%#:.........+@%%@@%+------------*%@*..     ..     .       
   ..:#@+-----=#@@#=:=@#::*@+...:##-.. ..:%#-......-*%@@@#+---=+*=-=*#=-*%@#:....    .   .          
   ..:#%=-------=*%@@@@@%##@@%=:-#@*:.:::+@@%##%@@@@%#+----+##+-=*#+-=#@@#:......              .    
   ..-%%=------------=+*#%%%@@@@@@@@@@@@@@@%%##*+=-----=*#*==+##+-=*@@%+.......   .                 
   ..=%#=------=*+--------------------------------=+*#*==+##+--=#@@%*:...         .                .
   ..=@#---=+----+##+=------------=---------==+***+=+*#*=--=*%@@%+:......                 .         
   ..+@#----+*=-----=+*##**++++++********+++=++*#*+=---=+#@@%*-..........     .    .         .      
   ..=%%=-----=*#*+==-----------=====++****+=------=+#%@%#=...........            .                 
   ..:*@#---------==++++++++++++===------------=+*%@%#+:.......    .      . .              .        
     .:*@%=-----------------------------==+*#%@@@%*-....                           ..               
     ...-#@%*+=------------------=++*#%@@%%#*+=:.......                             .     .    .    
     .....:+#%@%%#**++++***##%%@@@%#*+=:..............                     .                   .    
      ...  ...:=+**#######**++=-:..... 
      
                  ---------------------------------
                  {W}     Dr andro Webhook Tool     {R}
                  ---------------------------------
    """
    print(banner)

def loading_animation(task_text):
    sys.stdout.write(f"{W}[{Y}*{W}] {task_text}")
    for _ in range(3):
        time.sleep(0.3)
        sys.stdout.write(f"{Y}.")
        sys.stdout.flush()
    sys.stdout.write(f"{W}\r")

def send_messages():
    print(f"\n{W}[#] Option 1 Selected: Send Webhook Messages")
    url = input(f"{W}[>] Webhook URL: {R}").strip()
    
    if not url or not url.startswith("https://discord.com/api/webhooks/"):
        print(f"\n{W}[{R}!{W}] Error: Invalid Webhook URL.")
        time.sleep(2)
        return

    msg = input(f"{W}[>] Message Content: {R}").strip()
    if not msg:
        print(f"\n{W}[{R}!{W}] Error: Message cannot be empty.")
        time.sleep(2)
        return

    try:
        count = int(input(f"{W}[>] Number of times to send: {R}"))
    except ValueError:
        print(f"\n{W}[{R}!{W}] Error: Please enter a valid number.")
        time.sleep(2)
        return

    loading_animation("Connecting to Webhook")
    
    success_count = 0
    for i in range(count):
        try:
            response = requests.post(url, json={"content": msg})
            if response.status_code in [200, 204]:
                success_count += 1
                print(f"{W}[{G}+{W}] Message {i+1}/{count} sent successfully.")
            else:
                print(f"{W}[{R}-{W}] Failed to send message {i+1}. Code: {response.status_code}")
        except Exception as e:
            print(f"{W}[{R}!{W}] Error: {e}")
        time.sleep(0.3)

    print(f"\n{W}[{G}✓{W}] Finished! Successfully sent {success_count}/{count} messages.")
    input(f"\n{W}Press Enter to return to main menu...")

def delete_webhook():
    print(f"\n{W}[#] Option 2 Selected: Delete Webhook")
    url = input(f"{W}[>] Webhook URL: {R}").strip()
    
    if not url or not url.startswith("https://discord.com/api/webhooks/"):
        print(f"\n{W}[{R}!{W}] Error: Invalid Webhook URL.")
        time.sleep(2)
        return

    loading_animation("Processing request")
    
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            print(f"\n{W}[{G}+{W}] Status: {G}YES{W}, the Webhook has been permanently deleted.")
        elif response.status_code == 404:
            print(f"\n{W}[{R}-{W}] Status: Webhook not found (already deleted or invalid URL).")
        else:
            print(f"\n{W}[{R}!{W}] Failed to delete. Response Code: {response.status_code}")
    except Exception as e:
        print(f"\n{W}[{R}!{W}] Connection Error: {e}")
        
    input(f"\n{W}Press Enter to return to main menu...")

def main():
    while True:
        print_banner()
        print(f"{W}  [1] Send Message(s) via Webhook")
        print(f"  [2] Delete Webhook")
        print(f"  [3] Exit")
        print("-" * 50)
        
        choice = input(f"{W}[>] Choose an option (1-3): {R}").strip()
        
        if choice == '1':
            send_messages()
        elif choice == '2':
            delete_webhook()
        elif choice == '3':
            print(f"\n{G}Thanks for using Dr andro Tool. Goodbye!{W}")
            time.sleep(1)
            break
        else:
            print(f"\n{W}[{R}!{W}] Invalid option! Please choose 1, 2, or 3.")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Forced exit by user.")
        sys.exit()