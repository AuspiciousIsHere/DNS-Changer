import configparser
import os
import requests
import time
import webbrowser
import subprocess
import threading
import os.path
import platform
from configparser import ConfigParser
from customtkinter import *
from PIL import Image, ImageTk
import dns.resolver
import sys
from urllib.request import urlretrieve
from urllib import error

OS = platform.system()
status = False
# <editor-fold desc="DNS functions and info">

def MultiT():
    T1 = threading.Thread(target=get_ping)
    T1.start()


Number_Of_Tries = 0
flag = False

# Updating the Temporay DNS/Downloading the Configuration if doesnt exist.
def download_file(url):
    global Number_Of_Tries
    Number_Of_Tries += 1
    if Number_Of_Tries == 3:
        global flag
        flag = True
    else:
        try:
            urlretrieve(url, filename = "Configurations.ini")
        except error.URLError:
            download_file(url)


ignoreflag = False
username = 'AuspiciousIsHere'
repository = 'Update'
branch = 'main'
file_path = 'Configurations.ini'
url = f'https://raw.githubusercontent.com/{username}/{repository}/{branch}/{file_path}'

# The domains that need to be checked.
if OS == "Windows":
    Domain1 = "https://open.spotify.com"
    Domain2 = "https://chatgpt.com"
    Domain3 = "https://gemini.google.com"

# The DNS Servers.
SpotifyDNS = ["10.202.10.11"]
AntiDNS = ["10.202.10.202", "10.202.10.102"]
TemporaryDNS =['','']
items_list = []

def make_request(url):
    try:
        response = requests.get(url, timeout = 1)
        return response
    except:
        return None

custom_dns_path = "dns.ini"
# a flag that tells us this is the first time this function is being called so that the next time, it wont do most of the work
isinitial = True
def get_custom_dns():
    global items_list
    global isinitial
    configure = ConfigParser()
    configure.read(custom_dns_path)
    if isinitial:
        file_exist = os.path.isfile(custom_dns_path)

        if not file_exist:
            open(custom_dns_path, 'x')

        
        items_list = configure.sections()
        isinitial = False
    else:
        items_list = configure.sections()
        option_menu.configure(values=items_list)

get_custom_dns()

# a function to save the custom DNS
def save_custom_dns(prefered, alternative):
    open(custom_dns_path, 'a')
    configure = ConfigParser()
    configure.add_section(str(len(items_list) + 1))
    items_list.append(str(len(items_list) + 1))
    if prefered == "" and alternative == "":
        if app_language == "persian":
            custom_app_log_text_box.configure(text="!هر دو دی ان اس نمی تواند خالی باشد", font=("Arial Bold", 16))
        else:
            custom_app_log_text_box.configure(text="CANT SAVE TWO EMPTY DNSs!")
        return
    configure.set(str(len(items_list)), "Address1", prefered)
    configure.set(str(len(items_list)), "Address2", alternative)

    # Save to files
    with open(custom_dns_path, 'a') as w_configure:
        configure.write(w_configure)
    if app_language == "persian":
        custom_app_log_text_box.configure(text="!دی ان اس ها ذخیره شدند", font=("Arial Bold", 16))    
    else:
        custom_app_log_text_box.configure(text="SAVE COMPLETED!")

# creaitng a function to set the Entries Texts according to the chosen DNS
def call_back(chosen_option):
    global preferred_dns_text
    global alternate_dns_text
    configure = ConfigParser()
    configure.read(custom_dns_path)
    preferred_dns_text.set(configure.get(chosen_option, "Address1"))
    alternate_dns_text.set(configure.get(chosen_option, "Address2"))
    
    preferred_dns_text_box.configure(textvariable = preferred_dns_text)
    alternate_dns_text_box.configure(textvariable = alternate_dns_text)

def is_connected_to_network():
    status = subprocess.getstatusoutput("ping -n 1 8.8.8.8")
    if status[0] == 0 and not status[1].__contains__("unreachable"):
        return True
    return False

# Windows App status
if OS == "Windows":
    status = is_connected_to_network()

# Update the status
def update_status():
    global status
    while(True):
        time.sleep(5.0)
        if OS == "Windows":
            status = is_connected_to_network()
        elif OS == "Linux":
            # on Linux it doesnt matter if you are connected or not connected to a network for the program to work!
            # it just always works since it doesnt check if a DNS is valid or not!
            status = True
        update_status_label(status)

status_thread = threading.Thread(target=update_status, daemon = True)
status_thread.start()

# Update the status label
def update_status_label(status):
    if status == True:
        status_label_text = "Online"
        status_label_text_color = "#00896f"
    else:
        status_label_text = "Offline"
        status_label_text_color = "#c34a36"

    status_label.configure(text=status_label_text, text_color=status_label_text_color)

def get_dns_servers():
    if OS == 'Windows':
        dns_resolver = dns.resolver.Resolver()
        return dns_resolver._nameservers
    elif OS == 'Linux':
        output = subprocess.getstatusoutput(['sudo nmcli', 'dev', 'show', '|','grep','DNS'])[1]
        if output.__contains__('servers: '):
            connection_details = output.split('servers: ')[1].split('\n')[0].split(' ')
            if connection_details:
                return connection_details
        else:
            return ['8.8.8.8', '8.8.4.4']


def get_current_dns_servers():
    temp = get_dns_servers()
    alldnsservers = ''
    for each in temp:
        alldnsservers +="\n"+ each
    if app_language == "english":
        other_services_app_log_text_box.configure(text = "Your Current DNS Servers Are:\n" +  alldnsservers, font= ("Arial", 14))
    if app_language == "persian":
        other_services_app_log_text_box.configure(text = ":های فعلی شما DNS\n" +  alldnsservers, font= ("Arial", 14))


def get_current_dns_servers_ping():
    alldnsserverspings = ''
    if OS == "Windows":
        if status:
            temp = get_dns_servers()
            for each in temp:
                output = subprocess.getstatusoutput(f"ping -n 1 {each}")[1]
                alldnsserverspings += "\n"+output.split("Average =")[1]
            if app_language == "persian":
                other_services_app_log_text_box.configure(text = ":های فعلی شما DNS تاخیر\n" +  alldnsserverspings, font= ("Arial", 14))
            if app_language == "english":
                other_services_app_log_text_box.configure(text = "Your Current DNS Servers Ping Are:\n" +  alldnsserverspings, font= ("Arial", 14))
    if OS == "Linux":
        temp = get_dns_servers()
        for each in temp:
            output = subprocess.getstatusoutput(f"sudo ping -c 1 {each}")[1]
            alldnsserverspings += "\n"+output.split("time=")[1].split("ms")[0] + "ms"
        if app_language == "english":
            other_services_app_log_text_box.configure(text = "Your Current DNS Servers Ping Are:\n" +  alldnsserverspings, font= ("Arial", 14))

def connected_network():
    output = subprocess.getstatusoutput(["sudo nmcli", "dev", "show", "|","grep","DNS"])[1]
    return output.split(' connected to ')[1].split('\n')[0]

def Get_Ping(DNS1,DNS2):
    status1 = 1
    status2 = 1
    report = ''
    if OS == 'Windows':
        if status:
            if DNS1 != '':
                status1, output1 = subprocess.getstatusoutput("ping -n 1 " + DNS1)
            if DNS2 != '':
                status2, output2 = subprocess.getstatusoutput("ping -n 1 " + DNS2)
            if DNS1 != '' and status1 != 1:
                report += "PING1 =" + output1.split("Average =")[1] + "\n"
            if DNS2 != '' and status2 != 1:
                report += "PING2 =" + output2.split("Average =")[1] + "\n"
            custom_app_log_text_box.configure(text = report)
            if DNS1 == '' and DNS2 == '':
                if app_language == "english":
                    report = "Please Enter Atleast One DNS And Then Try Again!"
                elif app_language == "persian":
                    report = "!لطفا ابتدا حداقل یک دی ان اس وارد کنید"
                custom_app_log_text_box.configure(text = report, font= ("Arial", 14))
    elif OS == 'Linux':
        if DNS1 != '':
            status1, output1 = subprocess.getstatusoutput("sudo ping -c 1 " + DNS1)
        if DNS2 != '':
            status2, output2 = subprocess.getstatusoutput("sudo ping -c 1 " + DNS2)
        if DNS1 != '' and status1 != 1:
            report += "PING =" + output1.split('time=')[1].split('ms')[0] + "ms\n"
        if DNS2 != '' and status2 != 1:
            report += "PING =" + output2.split('time=')[1].split('ms')[0] + "ms\n"
        custom_app_log_text_box.configure(text = report, font= (0, 14))
        if DNS1 == '' and DNS2 == '':
            if app_language == "english":
                report = "Please Enter Atleast One DNS And Then Try Again!"
            custom_app_log_text_box.configure(text = report, font= (0, 14))

if OS == 'Linux':
    subprocess.run(["sudo","nmcli","connection", "modify", connected_network(), "ipv4.ignore-auto-dns", "yes"])
elif OS == 'Windows':
      currently_connected_network_adapter = subprocess.getstatusoutput("netsh interface show interface")[1].split("Connected")[1].split("\n")[0].split("        ")[1]

def SetCustomDNS(DNS1, DNS2):
    status1 = 1
    status2 = 1
    if OS == 'Windows':
        if status:
            if DNS1 != '':
                status1 = subprocess.getstatusoutput("ping -n 1 " + DNS1)[0]
            if DNS2 != '':
                status2 = subprocess.getstatusoutput("ping -n 1 " + DNS2)[0]
            if  DNS1 != '' and status1 != 1:
                process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {DNS1}', creationflags=subprocess.CREATE_NO_WINDOW)
                process.wait()
            if DNS2 != '' and status2 != 1:
                subprocess.Popen(f'netsh interface ip add dns "{currently_connected_network_adapter}" {DNS2} index = 2', creationflags=subprocess.CREATE_NO_WINDOW)
            if (status1 != 1 and status2 != 1) or (status1 != 1 and DNS2 == '') or (status2 != 1 and DNS1 == ''):
                if app_language == "english":
                    custom_app_log_text_box.configure(text= "Custom DNS Is Set!", font=("Arial", 14))
                elif app_language == "persian":
                    custom_app_log_text_box.configure(text= "!دی ان اس مورد نظر اعمال شد", font=("Arial", 14))
            else:
                if app_language == "english":
                    custom_app_log_text_box.configure(text= "One Or Both DNS(s) Are Wrong Or Down!", font = ("Arial", 14))
                elif app_language == "persian":
                    custom_app_log_text_box.configure(text= "!یک یا هر دو دی ان اس اشتباه یا در دسترس نیستند", font= ("Arial", 14))

    elif OS == 'Linux':
        temp = DNS1 + " " + DNS2
        subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', temp])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        if app_language == "english":
                custom_app_log_text_box.configure(text= "Custom DNS Is Set! Your Network Automatically Restarted To Apply The Changes!", font=(0, 14))

def SetSpotifyDNS():
    if OS == 'Windows':
        if status:
            subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {SpotifyDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
            output = subprocess.getstatusoutput(f"ping -n 1 {SpotifyDNS[0]}")[1]
            if app_language == "english":
                app_log_text_box.configure(text="SPOTIFY DNS ACTIVATED!\n DNS1 PING = " + output.split('Average =')[1], font=("Arial", 14))
            if app_language == "persian":
                app_log_text_box.configure(text="!اسپاتیفای فعال شد DNS\n DNS1 PING = " + output.split('Average =')[1], font=("Arial", 16))

    elif OS == 'Linux':
        subprocess.run(["sudo","nmcli", 'con', 'mod', connected_network(), 'ipv4.dns', f'{SpotifyDNS[0]}'])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        app_log_text_box.configure(text = "SPOTIFY DNS ACTIVATED! Your Network Restarted Automatically To Apply The Changes!", font=(0, 14))


def DefaultDNS():
    if OS == 'Windows':
        subprocess.Popen(f'netsh interface ip set dnsservers "{currently_connected_network_adapter}" source=dhcp', creationflags=subprocess.CREATE_NO_WINDOW)
        if app_language == "english":
            other_services_app_log_text_box.configure(text = "DEFAULT DNS IS APPLIED!", font= ("Arial", 14))
        elif app_language == "persian":
            other_services_app_log_text_box.configure(text = "!پیش فرض اعمال شد DNS", font= ("Arial", 14))
    elif OS == 'Linux':
        subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', '8.8.8.8 8.8.4.4'])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        other_services_app_log_text_box.configure(text = "DEFAULT DNS IS APPLIED! Your Network Restarted Automatically To Apply The Changes!", font= ("Arial", 14))

def SetAnti():
    if OS == 'Windows':
        if status:
            process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {AntiDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait()
            subprocess.Popen(f'netsh interface ip add dns "{currently_connected_network_adapter}" {AntiDNS[1]} index = 2', creationflags=subprocess.CREATE_NO_WINDOW)
            output1 = subprocess.getstatusoutput("ping -n 1 " + f"{AntiDNS[0]}")[1]
            output2 = subprocess.getstatusoutput("ping -n 1 " + f"{AntiDNS[1]}")[1]
            if app_language == "english":
                app_log_text_box.configure(text = "ANTI-PROHIBITION DNS ACTIVATED!\n DNS1 PING = " + output1.split('Average =')[1] + "\nDNS2 PING = " + output2.split("Average = ")[1])
            elif app_language == "persian":
                app_log_text_box.configure(text="!ضد تحریم فعال شد DNS\n DNS1 PING = " + output1.split('Average =')[1] + "\nDNS2 PING = " + output2.split("Average = ")[1])
    if OS == 'Linux':
        subprocess.run(["sudo","nmcli", 'con', 'mod', connected_network(), 'ipv4.dns', f'{AntiDNS[0]} {AntiDNS[1]}'])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        app_log_text_box.configure(text = "ANTI-PROHIBITION DNS ACTIVATED! Your Network Restarted Automatically To Apply The Changes!", font= ("Arial", 14))


def SetTemporary():
    if ignoreflag:
        if app_language == "english":
            app_log_text_box.configure(text = "YOU'RE OFFLINE OR THIS DNS IS NOT AVAILABLE FOR YOUR ISP!")
        elif app_language == "persian":
            app_log_text_box.configure(text = "!با اینترنت شما قابل دسترسی نمی باشد DNS این")

    elif OS == 'Windows' and ignoreflag == False:
        if status:
            process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {TemporaryDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait()
            output = subprocess.getstatusoutput("ping -n 1 " + f"{TemporaryDNS[0]}")[1]

            if app_language == "english":
                app_log_text_box.configure(text = "TEMPORARY DNS ACTIVATED!\n DNS1 PING = " + output.split('Average =')[1])
            if app_language == "persian":
                app_log_text_box.configure(text="!موقت فعال شد DNS\n DNS1 PING = " + output.split('Average =')[1])

    elif OS == 'Linux' and ignoreflag == False:
        subprocess.run(["sudo","nmcli", 'con', 'mod', connected_network(), 'ipv4.dns', f'{TemporaryDNS[0]}'])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        app_log_text_box.configure(text = "TEMPORARY DNS ACTIVATED! Your Network Restarted Automatically To Apply The Changes!")
        

def Manage(func):
    threading.Thread(target= func).start()


def Test_DNS(custom_url_flag = False, url = ""):
    if not custom_url_flag:
        if OS == "Windows":
            response1 = make_request(Domain1)
            response2 = make_request(Domain2)
            response3 = make_request(Domain3)
        return [CIP(response1), CIP(response2), CIP(response3)]
    else:
        if url != "":
            if not url.__contains__("https://"):
                url = "https://" + url
            response = make_request(url)
            return CIP(response)

def Test_All():
    checkmark_img_data = Image.open("Images/Checkmark.png")
    checkmark_img = CTkImage(dark_image=checkmark_img_data,
                         light_image=checkmark_img_data, size=(20, 20))

    d1s1.configure(image = red_cross_img)
    d1s2.configure(image = red_cross_img)
    d1s3.configure(image = red_cross_img)
    d2s1.configure(image = red_cross_img)
    d2s2.configure(image = red_cross_img)
    d2s3.configure(image = red_cross_img)
    d3s1.configure(image = red_cross_img)
    d3s2.configure(image = red_cross_img)
    d3s3.configure(image = red_cross_img)
    Previous = get_dns_servers()

    if OS == "Windows":
        flag = status

    if OS == 'Windows' and flag:
        process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {SpotifyDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()
        SDNS = Test_DNS()

    if OS == 'Windows' and flag:
        process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {AntiDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()
        process = subprocess.Popen(f'netsh interface ip add dns "{currently_connected_network_adapter}" {AntiDNS[1]} index = 2', creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()
        ADNS = Test_DNS()


    if ignoreflag != True and OS == 'Windows':
        process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {TemporaryDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
        process.wait()
        TDNS = Test_DNS()

    if len(Previous) == 0:
        if OS == "Windows" and status:
            process = subprocess.Popen('netsh interface ip set dnsservers "{currently_connected_network_adapter}" source=dhcp', creationflags=subprocess.CREATE_NO_WINDOW)

    if len(Previous) >= 1:
        if OS == "Windows" and status:
            process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {Previous[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait()

    if len(Previous) == 2:
        if OS == "Windows" and status:
            process = subprocess.Popen(f'netsh interface ip add dns "{currently_connected_network_adapter}" {Previous[1]} index = 2', creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait()

    if OS == "Windows" and status:
        if SDNS[0] == True:
            d1s1.configure(image = checkmark_img)
        if SDNS[1] == True:
            d1s2.configure(image = checkmark_img)
        if SDNS[2] == True:
            d1s3.configure(image = checkmark_img)
        if ADNS[0] == True:
            d2s1.configure(image = checkmark_img)
        if ADNS[1] == True:
            d2s2.configure(image = checkmark_img)
        if ADNS[2] == True:
            d2s3.configure(image = checkmark_img)
        if ignoreflag != True:
            if TDNS[0] == True:
                d3s1.configure(image = checkmark_img)
            if TDNS[1] == True:
                d3s2.configure(image = checkmark_img)
            if TDNS[2] == True:
                d3s3.configure(image = checkmark_img)


def CIP(response):
    if response == None:
        return False
    if response != None:
        #print(response.text)
        if response.status_code == 400:
            return False
        elif response.text.__contains__("Forbidden") or response.text.__contains__("Unable") or response.text.__contains__("permission"):
            return False
        return True

# </editor-fold>

class AnimatedGif:
    def __init__(self, root, label, gif_file, restart=True, show_last_frame=False, break_gif_cycle=False):
        self.root = root
        self.gif_file = gif_file
        self.label = label
        self.frames = self.get_gif_frames(self.gif_file)
        self.restart = restart
        self.show_last_frame = show_last_frame
        self.break_gif_cycle = break_gif_cycle

    def play_gif(self):
        total_delay = 100
        frame_delay = 35

        for frame in self.frames:
            self.root.after(total_delay, self.next_frame, frame)
            total_delay += frame_delay

        # Give the frame variable the last frame of gif
        # (in order to if the user want to end the gif and show the last frame after one cycle)
        frame = self.frames[-1]

        self.root.after(total_delay, self.next_frame, frame, self.restart)


    def next_frame(self, next_frame_prop, restart=False):
        if restart:
            try:
                self.label.configure()
            except:
                #print("next frame error1")
                return

            self.root.after(1, self.play_gif)
            return

        try:
            if self.break_gif_cycle:
                return
            self.label.configure(image=next_frame_prop)

        except:
            print("next frame error2")
            return

    @staticmethod
    def get_gif_frames(gif):
        with Image.open(gif) as opened_gif:
            index = 0
            frames = []
            while True:
                try:
                    opened_gif.seek(index)
                    frame = ImageTk.PhotoImage(opened_gif)
                    frames.append(frame)
                except EOFError:
                    break

                index += 1

            return frames


# Settings file path
settings_path = "settings.ini"

# <editor-fold desc="UI Methods">


def get_app_settings():
    file_exist = os.path.isfile(settings_path)

    if not file_exist:
        create_new_ini_file(settings_path)

    configure = ConfigParser()
    configure.read(settings_path)
    theme = configure.get("Settings", "Theme")
    language = configure.get("Settings", "Language")
    terms = configure.get("Settings", "Terms")
    return theme, language, terms

def create_new_ini_file(path):
    open(path, 'x')
    configure = ConfigParser()
    configure.add_section("Settings")
    configure.set("Settings", "Theme", "light")
    configure.set("Settings", "Language", "english")
    configure.set("Settings", "Terms", "False")

    # Save to file
    with open(path, 'w') as w_configure:
        configure.write(w_configure)


def load_actual_application_async():
    # Create a method that load the main page of the application to run on another thread
    def load_widgets():
        global ignoreflag
        if status:
            before = time.time()
            download_file(url)
            aafter = time.time()
            global flag
            if flag != True:
                if (aafter - before) < 3.0:
                    time.sleep(3 - (aafter - before))
                global TemporaryDNS
                configur = ConfigParser()
                configur.read("Configurations.ini")
                try:
                    TemporaryDNS[0]= configur.get("Temporary", "address1")
                    TemporaryDNS[1]= configur.get("Temporary", "address2")
                except configparser.NoSectionError:
                    TemporaryDNS[0]= configur.get("Temporary", "address1")
                    TemporaryDNS[1]= configur.get("Temporary", "address2")
                CheckDNS()
            else:
                ignoreflag = True
        else:
            ignoreflag = True
            time.sleep(3.0)

        global app_main_label_animated_gif
        global animated_gif
        app_main_label_animated_gif.break_gif_cycle = True
        animated_gif.break_gif_cycle = True
        loading_frame.grid_forget()
        app.rowconfigure(1, weight=1)
        app.rowconfigure(0, weight=0)

        small_buttons_frame.grid(row=0, column=0, sticky=E + W)
        buttons_frame.grid(row=1, column=0, sticky=E + W + N + S)

    # Create a new thread
    new_thread = threading.Thread(target=load_widgets, daemon= True)
    # Start the Thread
    new_thread.start()


def get_ping():
    global get_ping_wait_flag
    # If the flag is false we can't go through the waiting process because it's already started
    if get_ping_wait_flag:

        # Make the flag false, so it's prevent the application to show two gif at the same time
        get_ping_wait_flag = False

        please_wait_frame = CTkFrame(master=get_ping_frame, fg_color="transparent", height=200, width=300)

        wait_gif_label = CTkLabel(master=please_wait_frame, text="")

        please_wait_label = CTkLabel(master=please_wait_frame, text="Please wait...")
        please_wait_label.grid(row=1)

        if app_language == "persian":
            please_wait_label.configure(text="...کنید صبر لطفا")

        # Make the frame visible
        please_wait_frame.grid(row=6, column=0, columnspan=6, pady=(20, 0))

        wait_gif_label.grid(row=0)

        if app_theme == 'light':
            wait_animated_gif = AnimatedGif(please_wait_frame, wait_gif_label, "Images/LightTheme Loading Spin.gif")

        else:
            wait_animated_gif = AnimatedGif(please_wait_frame, wait_gif_label, "Images/DarkTheme Loading Spin.gif")

        wait_animated_gif.break_gif_cycle = False
        wait_animated_gif.play_gif()

        def actual_get_ping():
            global get_ping_wait_flag
            Test_All()
            # destroy the 'please wait' frame
            time.sleep(1.0)
            wait_animated_gif.break_gif_cycle = True
            please_wait_frame.destroy()

            # Make the flag ture, so we can show the gif again
            get_ping_wait_flag = True

        new_thread = threading.Thread(target=actual_get_ping)
        new_thread.start()


def start_custom_url_test():
    global test_custom_url_wait_flag

    # If the flag is false we can't go through the waiting process because it's already started
    if not test_custom_url_wait_flag:
        return

    # Make the flag false, so it's prevent the application to show two gif at the same time
    test_custom_url_wait_flag = False

    custom_url_please_wait_frame_father = CTkFrame(master=custom_url_test_frame, fg_color="transparent",
                                                   corner_radius=0, height=200, width=300)
    custom_url_please_wait_frame = CTkFrame(master=custom_url_please_wait_frame_father, fg_color="transparent",
                                            corner_radius=0, height=200, width=300)

    custom_url_wait_gif_label = CTkLabel(master=custom_url_please_wait_frame, text="")

    custom_url_please_wait_label = CTkLabel(master=custom_url_please_wait_frame, text="Please wait...")
    custom_url_please_wait_label.grid(row=1)

    if app_language == "persian":
        custom_url_please_wait_label.configure(text="...کنید صبر لطفا")

    custom_url_wait_gif_label.grid(row=0)

    if app_theme == 'light':
        custom_url_wait_animated_gif = AnimatedGif(custom_url_please_wait_frame,
                                                   custom_url_wait_gif_label,
                                                   "Images/LightTheme Loading Spin.gif")

    else:
        custom_url_wait_animated_gif = AnimatedGif(custom_url_please_wait_frame,
                                                   custom_url_wait_gif_label,
                                                   "Images/DarkTheme Loading Spin.gif")

    custom_url_please_wait_frame.pack()

    if app_language == "persian":
        custom_url_please_wait_label.configure(text="...کنید صبر لطفا")
    else:
        custom_url_please_wait_label.configure(text="Please wait...")

    custom_url_wait_animated_gif.break_gif_cycle = False
    custom_url_wait_animated_gif.play_gif()
    custom_url_please_wait_frame_father.grid(row=3, column=0, sticky=W + E + S + N, padx=10, pady=(30, 0))

    def actual_start_custom_url_test():
        try:
            # TODO: do the desired things to test the url with DNSs
            # text_box name: custom_url_text_box
            # name of red cross images:
            # spotify_custom_url_success_flag
            # anti_pro_custom_url_success_flag
            # temp_dns_custom_url_success_flag
            checkmark_img_data = Image.open("Images/Checkmark.png")
            checkmark_img = CTkImage(dark_image=checkmark_img_data,
                         light_image=checkmark_img_data, size=(20, 20))

            spotify_custom_url_success_flag.configure(image = red_cross_img)
            anti_pro_custom_url_success_flag.configure(image = red_cross_img)
            temp_dns_custom_url_success_flag.configure(image = red_cross_img)


            Previous = get_dns_servers()
            if OS == "Windows" and status:
                process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {SpotifyDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
                process.wait()
                SDNS = Test_DNS(True, url= custom_url_text_box.get())
            
            if OS == "Linux":
                subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', f'{SpotifyDNS[0]}'])
                subprocess.getstatusoutput("sudo nmcli networking off")
                subprocess.getstatusoutput("sudo nmcli networking on")
                time.sleep(3)
                SDNS = Test_DNS(True, url= custom_url_text_box.get())
            
            if OS == 'Windows' and status:
                process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {AntiDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
                process.wait()
                process = subprocess.Popen(f'netsh interface ip add dns "{currently_connected_network_adapter}" {AntiDNS[1]} index = 2', creationflags=subprocess.CREATE_NO_WINDOW)
                process.wait()
                ADNS = Test_DNS(True, url= custom_url_text_box.get())

            if OS == "Linux":
                subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', f'{AntiDNS[0]} {AntiDNS[1]}'])
                subprocess.getstatusoutput("sudo nmcli networking off")
                subprocess.getstatusoutput("sudo nmcli networking on")
                time.sleep(3)
                ADNS = Test_DNS(True, url= custom_url_text_box.get())

            if ignoreflag != True and OS == "Windows":
                process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {TemporaryDNS[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
                process.wait()
                TDNS = Test_DNS(True, url= custom_url_text_box.get())


            if OS == "Linux" and ignoreflag != True:
                subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', f'{AntiDNS[0]} {AntiDNS[1]}'])
                subprocess.getstatusoutput("sudo nmcli networking off")
                subprocess.getstatusoutput("sudo nmcli networking on")
                time.sleep(3)
                TDNS = Test_DNS(True, url= custom_url_text_box.get())
            


            elif OS == "Windows":
                TDNS = False
            if len(Previous) == 0:
                if OS == "Windows" and status:
                    process = subprocess.Popen('netsh interface ip set dnsservers "{currently_connected_network_adapter}" source=dhcp', creationflags=subprocess.CREATE_NO_WINDOW)
                elif OS == "Linux":
                    subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', '8.8.8.8 8.8.4.4'])
            if len(Previous) >= 1:
                if OS == "Windows" and status:
                    process = subprocess.Popen(f'netsh interface ip set dns "{currently_connected_network_adapter}" static {Previous[0]}', creationflags=subprocess.CREATE_NO_WINDOW)
                    process.wait()
                elif OS == "Linux" and len(Previous) == 1:
                    subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', f'{Previous[0]}'])
            if len(Previous) == 2:
                if OS == "Windows" and status:
                    process = subprocess.Popen(f'netsh interface ip add dns "{currently_connected_network_adapter}" {Previous[1]} index = 2', creationflags=subprocess.CREATE_NO_WINDOW)
                    process.wait()
                elif OS == "Linux":
                    subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', f'{Previous[0]} {Previous[1]}'])
            if OS == "Linux":
                subprocess.getstatusoutput("sudo nmcli networking off")
                subprocess.getstatusoutput("sudo nmcli networking on")

            if OS == "Windows" and status or OS == "Linux":
                if SDNS:
                    spotify_custom_url_success_flag.configure(image = checkmark_img)
                if ADNS:
                    anti_pro_custom_url_success_flag.configure(image = checkmark_img)
                if TDNS:
                    temp_dns_custom_url_success_flag.configure(image = checkmark_img)
                
            time.sleep(1)
            custom_url_wait_animated_gif.break_gif_cycle = True
            custom_url_please_wait_frame.destroy()

        finally:
            global test_custom_url_wait_flag
            test_custom_url_wait_flag = True

    test_custom_url_thread = threading.Thread(target=actual_start_custom_url_test)
    test_custom_url_thread.start()


def open_url(url):
    webbrowser.open_new(url)


def go_to_other_services():
    buttons_frame.grid_forget()
    small_buttons_frame.grid_forget()

    app.rowconfigure(1, weight=0)
    app.rowconfigure(0, weight=1)

    other_services_frame.grid(row=0, column=0, sticky=W+E+N+S)


def go_to_about_us():
    buttons_frame.grid_forget()
    small_buttons_frame.grid_forget()
    about_us_frame.grid(sticky=W+E+N+S)


def go_to_get_ping():
    if OS == "Linux":
        other_services_app_log_text_box.configure(text = "This Feature is not available in Linux yet!", font = ("Arial", 18))
        return
    other_services_frame.grid_forget()
    get_ping_frame.grid(row=0, column=0, sticky=W+E+N+S)


def go_to_apply_custom_dns():
    other_services_frame.grid_forget()
    apply_custom_dns_frame.grid(row=0, column=0, sticky=W + E + N + S)


def go_to_home_page_from_other_services():
    other_services_frame.grid_forget()

    app.rowconfigure(1, weight=1)
    app.rowconfigure(0, weight=0)

    small_buttons_frame.grid(row=0, column=0, sticky=E + W)
    buttons_frame.grid(row=1, column=0, sticky=E + W + N + S)


def go_to_settings():
    buttons_frame.grid_forget()
    small_buttons_frame.grid_forget()

    settings_frame.grid(row=0, column=0, sticky=E+W)


def go_to_home_from_settings():
    settings_frame.grid_forget()

    small_buttons_frame.grid(row=0, column=0, sticky=E+W)
    buttons_frame.grid(row=1, column=0, sticky=E+W+N+S)


def go_to_home_from_about_us():
    about_us_frame.grid_forget()

    small_buttons_frame.grid(row=0, column=0, sticky=E + W)
    buttons_frame.grid(row=1, column=0, sticky=E + W + N + S)


def go_to_other_services_page_from_get_ping():
    get_ping_frame.grid_forget()
    other_services_frame.grid(row=0, column=0, sticky=W+E+N+S)


def go_to_other_services_page_from_apply_custom_dns():
    apply_custom_dns_frame.grid_forget()
    other_services_frame.grid(row=0, column=0, sticky=W + E + N + S)


def go_to_custom_url():
    other_services_frame.grid_forget()
    custom_url_test_frame.grid(row=0, column=0, sticky=W + E + N + S)
    other_services_frame.grid(row=0, column=0, sticky=W+E+N+S)


def go_to_get_ping_from_custom_url():
    custom_url_test_frame.grid_forget()
    other_services_frame.grid(row=0, column=0, sticky=W+E+N+S)


def set_app_theme(theme, write_to_file=False):
    global app_theme
    app_theme = theme
    set_appearance_mode(theme)

    if write_to_file:
        configure = ConfigParser()
        configure.read(settings_path)

        def write_to_file():
            configure.set('Settings', 'Theme', theme)
            with open(settings_path, 'w') as w_configure:
                configure.write(w_configure)

        if configure.get('Settings', 'Theme') != theme:
            write_to_file()

    global bold_text_color
    global icon_button_hover_color

    # If desired theme is light...
    if theme == 'light':
        # Set the text color to black
        bold_text_color = "#242424"
        icon_button_hover_color = "#C4C4C4"
        anti_pro_btn.configure(hover_color="#FFEFE2")
        spotify_btn.configure(hover_color="#E2FFDf")
        temporarily_dns_btn.configure(hover_color="#FFF6BC")
        if terms_of_service != "True":
            quit_button.configure(hover_color="#FFF4A9")
    # If the desired theme is dark...
    else:
        # Set the text color to white
        bold_text_color = "#ebebeb"
        icon_button_hover_color = "#4A4A4A"
        anti_pro_btn.configure(hover_color="#4E3724")
        spotify_btn.configure(hover_color="#254722")
        temporarily_dns_btn.configure(hover_color="#5E5416")
        if terms_of_service != "True":
            quit_button.configure(hover_color="#534800")

    if terms_of_service != "True":
        quit_button.configure(text_color=bold_text_color)

    # Change the text color of buttons
    spotify_btn.configure(text_color=bold_text_color)
    anti_pro_btn.configure(text_color=bold_text_color)
    temporarily_dns_btn.configure(text_color=bold_text_color)
    other_services_btn.configure(text_color=bold_text_color)

    # Change the hover color of transparent bg buttons
    other_services_btn.configure(hover_color=icon_button_hover_color)
    about_us_btn.configure(hover_color=icon_button_hover_color)
    settings_btn.configure(hover_color=icon_button_hover_color)
    go_to_home_page_from_settings_btn.configure(hover_color=icon_button_hover_color)
    go_to_home_page_from_about_us_btn.configure(hover_color=icon_button_hover_color)
    go_to_home_page_from_other_services_btn.configure(hover_color=icon_button_hover_color)
    go_to_other_services_page_from_get_ping_btn.configure(hover_color=icon_button_hover_color)
    go_to_other_services_page_from_apply_custom_dns_btn.configure(hover_color=icon_button_hover_color)
    go_to_get_ping_from_custom_url_btn.configure(hover_color=icon_button_hover_color)


def set_app_language(language, write_to_file=False):
    global app_language
    app_language = language

    if write_to_file:
        configure = ConfigParser()
        configure.read(settings_path)

        def write_to_file():
            configure.set('Settings', 'Language', language)
            with open(settings_path, 'w') as w_configure:
                configure.write(w_configure)

        if configure.get('Settings', 'Language') != language:
            write_to_file()

    if language == 'persian':

        # <editor-fold desc="terms_page">
        if terms_of_service != "True":
            terms_of_services_label.configure(text="خط مشی برنامه", font = ("Arial", 16))
            terms_of_services_label.grid_forget()
            terms_of_services_label.grid(row=1, column=0, sticky=E, padx=20, pady=(15, 0))

            terms_label_button1.configure(text="اینجا", font = ("Arial", 16))
            terms_label_button1.grid_forget()
            terms_label_button1.grid(row=3, column=0, pady=(5, 0), sticky=E)
            terms_label_button2.configure(text="اینجا", font = ("Arial", 16))
            terms_label_button2.grid_forget()
            terms_label_button2.grid(row=9, column=0, pady=(5, 0), sticky=E)

            terms_label1.configure(text="این یک برنامه رایگان ساخته شده توسط\n @I_AM_AUSPICIOUS و @lurixed \n(نام کاربری تلگرام) می باشد و هرگونه استفاده تجاری از این نرم افزار خلاف اهداف ما است", justify=RIGHT, font = ("Arial", 16))
            terms_label2.configure(text="این نرم افزار تنها یک تغییر دهنده دی ان اس است و ما هیچ مسئولیتی در قبال مشکلات پیش آمده توسط سرور های دی ان اس نداریم", justify=RIGHT, font = ("Arial", 16))
            terms_label3.configure(text="این برنامه یک نرم افزار متن باز می باشد شما می توانید کد برنامه را مشاهده کنید در", justify=RIGHT, font = ("Arial", 16))
            terms_label4.configure(text="فایل های مربوط به این برنامه را به هیچ عنوان از منبعی به جز گیت هاب برنامه دانلود نکنید", justify=RIGHT, font = ("Arial", 16))
            terms_label5.configure(text="سه دی ان اس در این برنامه برای رفع تحریم های اعمال شده توسط کشور های دیگر بر ایران استفاده شده است که عبارتند از\n"
                                        "Spotify DNS: Radar Game\n"
                                        "Anti-Prohibition DNS: 403 online\n"
                                        "Temporary DNS: Shelter (ممکن است تغییر کند)", justify=RIGHT, font = ("Arial", 16))
            terms_label6.configure(text="ما مالک هیچکدام از دی ان اس های ذکر شده نیستیم، شما می توانید با جستجوی نام هر کدام از دی ان اس ها وبسایت مربوطه را مشاهده کنید", justify=RIGHT, font = ("Arial", 16))
            terms_label7.configure(text="دی ان اس های ذکر شده فقط در کشور ایران قابل استفاده می باشند، اگر شما در کشور دیگری از این برنامه استفاده می کنید ممکن است دی ان اس ها برای شما کار نکنند", justify=RIGHT, font = ("Arial", 16))
            terms_label8.configure(text="این برنامه نیازمند دسترسی ادمین برای ساختن فایل، دانلود فایل و اجرای دستورات می باشد، فایل دانلود شده را می توانید مشاهده کنید در", justify=RIGHT)
            terms_label9.configure(text="استفاده می شود Temporarily DNS که برای به روز کردن", justify=RIGHT, font = ("Arial", 16))

            agreement_check_box.configure(text="شرایط را خوانده و می پذیرم", font = ("Arial", 16))
            continue_button.configure(text="ادامه", font = ("Arial", 18))
            quit_button.configure(text="خروج", font = ("Arial", 18))

        # </editor-fold>

        # <editor-fold desc="loading page">
        loading_label.configure(text="... در حال بارگیری", font = ("Arial", 18))
        made_label.configure(text="@I_AM_AUSPICIOUS : توسعه نرم افزاری", font = ("Arial", 18))
        design_label.configure(text="@lurixed : طراح گرافیکی", font = ("Arial", 18))
        # </editor-fold>

        # <editor-fold desc="main page">
        spotify_btn.configure(text="DNS اسپاتیفای", font = ("Arial", 18))
        anti_pro_btn.configure(text="DNS ضد تحریم", font = ("Arial", 18))
        temporarily_dns_btn.configure(text="DNS موقت", font = ("Arial", 18))
        dns_changer_label.configure(text="DNS تغییر دهنده", font=("Arial", 24))
        other_services_btn.configure(text="... سایر خدمات", font = ("Arial", 20))
        app_log_label.configure(text="لاگ برنامه", font = ("Arial", 18))
        # </editor-fold>

        # <editor-fold desc="settings page">

        settings_label.configure(text="تنظیمات برنامه", font = ("Arial Bold", 24))
        settings_label.grid_forget()
        settings_label.grid(row=1, column=0, sticky=E, padx=20)

        appearance_label.configure(text="ظاهری", font = ("Arial Bold", 24))
        appearance_label.grid_forget()
        appearance_label.grid(row=2, column=0, sticky=E, padx=20, pady=(40, 0))

        app_theme_label.configure(text="تم برنامه", font = ("Arial", 18))
        app_theme_label.grid_forget()
        app_theme_label.grid(row=0, column=0, sticky=E, padx=30, pady=(10, 0))

        app_theme_desc_label.configure(text="حالت برنامه را انتخاب کنید", font = ("Arial", 14))
        app_theme_desc_label.grid_forget()
        app_theme_desc_label.grid(row=1, column=0, sticky=E, padx=30, pady=(0, 2))

        expand_collapse_app_theme_btn.grid_forget()
        expand_collapse_app_theme_btn.grid(row=0, column=0, rowspan=2, sticky=W, padx=15)

        dark_radio.configure(text="")
        if is_app_theme_expanded:
            dark_radio.grid_forget()
            dark_radio.grid(row=2, column=0, sticky=E, padx=0, pady=(10, 5))
            dark_radio_label.grid(row=2, column=0, sticky=E, padx=(0, 110), pady=(10, 5))

        light_radio.configure(text="")
        if is_app_theme_expanded:
            light_radio.grid_forget()
            light_radio.grid(row=3, column=0, sticky=E, padx=0, pady=(0, 10))
            light_radio_label.grid(row=3, column=0, sticky=E, padx=(0, 110), pady=(0, 10))

        language_label.configure(text="زبان", font = ("Arial", 18))
        language_label.grid_forget()
        language_label.grid(row=0, column=0, sticky=E, padx=30, pady=(10, 0))

        language_desc_label.configure(text="زبان برنامه را انتخاب کنید", font = ("Arial", 14))
        language_desc_label.grid_forget()
        language_desc_label.grid(row=1, column=0, sticky=E, padx=30, pady=(0, 2))

        expand_collapse_app_language_btn.grid_forget()
        expand_collapse_app_language_btn.grid(row=0, column=0, rowspan=2, sticky=W, padx=15)

        persian_radio.configure(text="")
        if is_app_language_expanded:
            persian_radio.grid_forget()
            persian_radio.grid(row=2, column=0, sticky=E, padx=0, pady=(10, 5))
            persian_radio_label.grid(row=2, column=0, sticky=E, padx=(0, 110), pady=(10, 5))

        english_radio.configure(text="")
        if is_app_language_expanded:
            english_radio.grid_forget()
            english_radio.grid(row=3, column=0, sticky=E, padx=0, pady=(0, 10))
            english_radio_label.grid(row=3, column=0, sticky=E, padx=(0, 110), pady=(0, 10))

        # </editor-fold>

        # <editor-fold desc="about page">
        language_radio_var.set("persian")
        about_label.configure(text=":درباره", font = ("Arial", 24))
        about_label.grid_forget()
        about_label.grid(row=1, column=0, sticky=E, padx=20)

        developer_label.configure(text=":توسئه نرم افزاری", font = ("Arial", 18))
        developer_label.grid_forget()
        developer_label.grid(row=2, column=0, sticky=E, padx=20, pady=(20, 0))

        developer_email_label.configure(text=":ایمیل توسئه دهنده", font = ("Arial", 18))
        developer_email_label.grid_forget()
        developer_email_label.grid(row=4, column=0, sticky=E, padx=20, pady=(20, 0))

        designer_label.configure(text=":طراح گرافیکی", font = ("Arial", 18))
        designer_label.grid_forget()
        designer_label.grid(row=6, column=0, sticky=E, padx=20, pady=(20, 0))
        
        github_label.configure(text=":گیت هاب", font = ("Arial", 18))
        github_label.grid(row=8, column=0, sticky=E, padx=20, pady=(20, 0))

        line1_about_label.configure(text="در صورت بروز هرگونه مشکلی با ما ارتباط برقرار کنید", font = ("Arial", 14))
        line1_about_label.grid_forget()
        line1_about_label.grid(row=10, column=0, sticky=E, padx=20, pady=(40, 0))

        line2_about_label.configure(text="با استفاده از راه های ارتباطی بالا می توانید با ما ارتباط برقرار کنید", font = ("Arial", 14))
        line2_about_label.grid_forget()
        line2_about_label.grid(row=11, column=0, sticky=E, padx=20)

        # </editor-fold>

        # <editor-fold desc="other services page">
        get_ping_btn.configure(text="تست کردن دی ان اس ها", font = ("Arial", 20))
        get_current_dns_ping_btn.configure(text="فعلی DNS گرفتن تاخیر", font = ("Arial", 20))
        get_current_dns_server_btn.configure(text=" فعلی DNS گرفتن سرور ", font = ("Arial", 20))
        apply_custom_dns.configure(text="دلخواه DNS اعمال", font = ("Arial", 20))
        apply_default_dns.configure(text="پیش فرض DNS اعمال", font = ("Arial", 20))
        # </editor-fold>

        # <editor-fold desc="get ping page">

        actual_get_ping_btn.configure(text="شروع تست", font=("Arial Bold", 16))
        go_to_custom_url_test_btn.configure(text="آدرس دلخواه", font=("Arial Bold", 16))

        # </editor-fold>

        # <editor-fold desc="custom url test page">

        custom_url_text_box_label.configure(text="آدرس", font=("Arial Bold", 16))
        actual_custom_url_test_btn.configure(text="شروع تست", font=("Arial Bold", 16))

        # </editor-fold>

        # <editor-fold desc="apply custom dns page">

        preferred_dns_label.configure(text=" دی ان اس اولیه ", font=("Arial Bold", 16))
        example_preferred_dns_label.configure(text="(مثال: 1.1.1.1 یا 1.0.0.1)", font=("Arial", 12))
        preferred_dns_label.grid_forget()
        preferred_dns_label.grid(row=0, column=1)
        example_preferred_dns_label.grid_forget()
        example_preferred_dns_label.grid(row=0, column=0)
        preferred_dns_label_frame.grid_forget()
        preferred_dns_label_frame.grid(row=1, column=0, padx=10, pady=(20, 0), sticky=E)

        alternate_dns_label.configure(text="دی ان اس ثانویه ", font=("Arial Bold", 16))
        alternate_dns_label.grid_forget()
        alternate_dns_label.grid(row=3, column=0, padx=10, sticky=E, pady=(20, 0))

        actual_apply_custom_dns_btn.configure(text="اعمال دی ان اس", font=("Arial Bold", 16))

        get_custom_dns_ping_btn.configure(text="گرفتن تاخیر", font=("Arial Bold", 16))
        save_dns.configure(text="DNS ذخیره", font=("Arial Bold", 16))
        option_menu.configure(font=("Arial Bold", 16))
        chosen_option.set("انتخاب کنید")

        # </editor-fold>

    else:
        # <editor-fold desc="terms page">
        if terms_of_service != "True":
            terms_of_services_label.configure(text="Terms of services:")
            terms_of_services_label.grid_forget()
            terms_of_services_label.grid(row=1, column=0, sticky=W, padx=20, pady=(15, 0))

            terms_label_button1.configure(text="Here", font = ("Arial", 14))
            terms_label_button1.grid_forget()
            terms_label_button1.grid(row=3, column=0, pady=(5, 0), sticky=W)
            terms_label_button2.configure(text="Here", font = ("Arial", 14))
            terms_label_button2.grid_forget()
            terms_label_button2.grid(row=9, column=0, pady=(5, 0), sticky=W)

            terms_label1.configure(text="* This is a Free Program "
                                        "made by @I_AM_AUSPICIOUS and "
                                        "designed by @lurixed "
                                        "(on telegram) and any "
                                        "commercial use is against"
                                        " our intentions!",
                                   justify=LEFT)
            terms_label2.configure(
                text="* This app is just a"
                     " DNS changer and we "
                     "are not responsible "
                     "of any problem caused "
                     "by the DNS servers!",
                justify=LEFT)
            terms_label3.configure(
                text="* This program is"
                     " Open-source and you "
                     "can find the code at: ",
                justify=LEFT)
            terms_label4.configure(
                text="* Don’t download any file "
                     "related to this program "
                     "from any other sources!",
                justify=LEFT)
            terms_label5.configure(
                text="* There are Three DNSs being "
                     "used in this Program to bypass "
                     "the prohibitions caused by other "
                     "countries over Iran and the names are:\n"
                     "Spotify DNS: Radar Game\n"
                     "Anti-Prohibition DNS: 403 online\n"
                     "Temporary DNS: Shelter (might change)",
                justify=LEFT)
            terms_label6.configure(
                text="* We do not own any of these "
                     "DNS servers and you can"
                     " find their websites by "
                     "searching each name!",
                justify=LEFT)
            terms_label7.configure(
                text="* The Three mentioned DNSs"
                     " above will only work in Iran "
                     "so if you are in other countries,"
                     " none of the mentioned DNSs "
                     "are guaranteed to work!",
                justify=LEFT)
            terms_label8.configure(
                text="* This Program needs Administrator "
                     "privilege (makes command execution) "
                     "in order to work and makes .ini files "
                     "to configure and downloads a file located "
                     "at: ",
                justify=LEFT)
            terms_label9.configure(text="to update the Temporary DNS!", justify=LEFT)

            agreement_check_box.configure(text="I have read and accept the Agreement.")
            continue_button.configure(text="Continue")
            quit_button.configure(text="Quit")

        # </editor-fold>

        # <editor-fold desc="loading page">
        loading_label.configure(text="Loading...", font = ("Arial", 18))
        made_label.configure(text="Made by: I_AM_AUSPICIOUS", font = ("Arial", 16))
        design_label.configure(text="Design: @lurixed", font = ("Arial", 16))
        # </editor-fold>

        # <editor-fold desc="main page">
        spotify_btn.configure(text="Spotify DNS")
        anti_pro_btn.configure(text="Anti Prohibition DNS")
        temporarily_dns_btn.configure(text= "Temporary DNS")
        dns_changer_label.configure(text="DNS Changer", font = ("Arial Narrow", 24))
        other_services_btn.configure(text="Other Services ...", font = ("Arial", 20))
        app_log_label.configure(text="App Log")
        # </editor-fold>

        # <editor-fold desc="settings page">
        language_radio_var.set("english")
        settings_label.configure(text="Settings")
        settings_label.grid_forget()
        settings_label.grid(row=1, column=0, sticky=W, padx=20)

        appearance_label.configure(text="Appearance")
        appearance_label.grid_forget()
        appearance_label.grid(row=2, column=0, sticky=W, padx=20, pady=(40, 0))

        app_theme_label.configure(text="App Theme")
        app_theme_label.grid_forget()
        app_theme_label.grid(row=0, column=0, sticky=W, padx=30, pady=(10, 0))

        app_theme_desc_label.configure(text="Select which app theme to display")
        app_theme_desc_label.grid_forget()
        app_theme_desc_label.grid(row=1, column=0, sticky=W, padx=30, pady=(0, 2))

        expand_collapse_app_theme_btn.grid_forget()
        expand_collapse_app_theme_btn.grid(row=0, column=0, rowspan=2, sticky=E, padx=15)

        dark_radio.configure(text="Dark")
        if is_app_theme_expanded:
            dark_radio.grid_forget()
            dark_radio_label.grid_forget()
            dark_radio.grid(row=2, column=0, sticky=W, padx=40, pady=(10, 5))

        light_radio.configure(text="Light")
        if is_app_theme_expanded:
            light_radio.grid_forget()
            light_radio_label.grid_forget()
            light_radio.grid(row=3, column=0, sticky=W, padx=40, pady=(0, 10))

        language_label.configure(text="Language")
        language_label.grid_forget()
        language_label.grid(row=0, column=0, sticky=W, padx=30, pady=(10, 0))

        language_desc_label.configure(text="Select the application language")
        language_desc_label.grid_forget()
        language_desc_label.grid(row=1, column=0, sticky=W, padx=30, pady=(0, 2))

        expand_collapse_app_language_btn.grid_forget()
        expand_collapse_app_language_btn.grid(row=0, column=0, rowspan=2, sticky=E, padx=15)

        persian_radio.configure(text="Persian (فارسی)")
        if is_app_language_expanded:
            persian_radio.grid_forget()
            persian_radio_label.grid_forget()
            persian_radio.grid(row=2, column=0, sticky=W, padx=40, pady=(10, 5))

        english_radio.configure(text="English")
        if is_app_language_expanded:
            english_radio.grid_forget()
            english_radio_label.grid_forget()
            english_radio.grid(row=3, column=0, sticky=W, padx=40, pady=(0, 10))

        # </editor-fold>

        # <editor-fold desc="about page">
        about_label.configure(text="About:", font = ("Arial", 24))
        about_label.grid_forget()
        about_label.grid(row=1, column=0, sticky=W, padx=20)

        developer_label.configure(text="Developer:")
        developer_label.grid_forget()
        developer_label.grid(row=2, column=0, sticky=W, padx=20, pady=(20, 0))

        developer_email_label.configure(text="Developer's email:")
        developer_email_label.grid_forget()
        developer_email_label.grid(row=4, column=0, sticky=W, padx=20, pady=(10, 0))

        designer_label.configure(text="Designer:")
        designer_label.grid_forget()
        designer_label.grid(row=6, column=0, sticky=W, padx=20, pady=(20, 0))

        github_label.configure(text="Github:")
        github_label.grid(row=8, column=0, sticky=W, padx=20, pady=(20, 0))

        line1_about_label.configure(text="Contact us if you encountered any unexpected error.")
        line1_about_label.grid_forget()
        line1_about_label.grid(row=10, column=0, sticky=W, padx=20, pady=(40, 0))

        line2_about_label.configure(text="Feel free to ask any question.")
        line2_about_label.grid_forget()
        line2_about_label.grid(row=11, column=0, sticky=W, padx=20)
        # </editor-fold>

        # <editor-fold desc="other services page">
        get_ping_btn.configure(text="Test DNS(s)")
        get_current_dns_ping_btn.configure(text="Get current DNS ping")
        get_current_dns_server_btn.configure(text="Get current DNS server")
        apply_custom_dns.configure(text="Apply custom DNS")
        apply_default_dns.configure(text="Apply default DNS")
        # </editor-fold>

        # <editor-fold desc="get ping page">

        actual_get_ping_btn.configure(text="Start Testing", font=("Arial", 14))
        go_to_custom_url_test_btn.configure(text="Custom URL", font=("Arial", 14))

        # </editor-fold>

        # <editor-fold desc="custom url test page">

        custom_url_text_box_label.configure(text="URL:", font=("Arial", 14))
        actual_custom_url_test_btn.configure(text="Start Testing", font=("Arial", 14))

        # </editor-fold>

        # <editor-fold desc="apply custom dns page">

        preferred_dns_label.configure(text="Preferred DNS ")
        example_preferred_dns_label.configure(text="(Example: 1.1.1.1 or 1.0.0.1)")
        preferred_dns_label.grid_forget()
        preferred_dns_label.grid(row=0, column=0)
        example_preferred_dns_label.grid_forget()
        example_preferred_dns_label.grid(row=0, column=1)
        preferred_dns_label_frame.grid_forget()
        preferred_dns_label_frame.grid(row=1, column=0, padx=10, pady=(20, 0), sticky=W)

        alternate_dns_label.configure(text="Alternate DNS")
        alternate_dns_label.grid_forget()
        alternate_dns_label.grid(row=3, column=0, padx=10, sticky=W, pady=(20, 0))

        actual_apply_custom_dns_btn.configure(text="Apply DNS", font=("Arial", 14))

        get_custom_dns_ping_btn.configure(text="Get ping", font=("Arial", 14))

        option_menu.configure(font=("Arial", 14))
        chosen_option.set("Select A DNS")
        save_dns.configure(text="Save DNS", font=("Arial", 14))

        # </editor-fold>


def set_app_terms():
    global terms_of_service
    terms_of_service = 'True'
    configure = ConfigParser()
    configure.read(settings_path)

    def write_to_file():
        configure.set('Settings', 'Terms', "True")
        with open(settings_path, 'w') as w_configure:
            configure.write(w_configure)

    if configure.get('Settings', 'Terms') != terms_of_service:
        write_to_file()

    terms_frame.destroy()
    opening()


# </editor-fold>

# <editor-fold desc="Data">

# Set the application theme and language right before the mainloop so all the elements are created
# In the set_app_theme() and set_app_language() method we change some properties of the app elements
# If we do that before all the elements are created we will get error
app_theme, app_language, terms_of_service = get_app_settings()

# Flag that indicating if the app theme box is expanded
is_app_theme_expanded = False

# Flag that indicating if the app language box is expanded
is_app_language_expanded = False

# The hex value of the hover color for the transparent bg buttons
icon_button_hover_color = "#C4C4C4"

# Color of the texts
bold_text_color = "#505050"

# Application main label
light_app_main_label_data = Image.open("Images/Light Auspicious Main Label.png")
dark_app_main_label_data = Image.open("Images/Dark Auspicious Main Label.png")
auspicious_main_label = CTkImage(dark_image=dark_app_main_label_data,
                                 light_image=light_app_main_label_data, size=(250, 45))

# Red cross icon
red_cross_img_data = Image.open("Images/Red Cross Icon.png")
red_cross_img = CTkImage(dark_image=red_cross_img_data,
                         light_image=red_cross_img_data, size=(20, 20))

# Spotify icon
spotify_logo_img_data = Image.open("Images/Spotify Icon.png")
spotify_logo_img = CTkImage(dark_image=spotify_logo_img_data,
                            light_image=spotify_logo_img_data, size=(30, 30))

# Anti-Prohibition icon
anti_prohibition_img_data = Image.open("Images/Key with Bg.png")
anti_prohibition_img = CTkImage(dark_image=anti_prohibition_img_data,
                                light_image=anti_prohibition_img_data, size=(30, 30))

# Network Icon
network_img_data = Image.open("Images/Network Icon.png")
network_img = CTkImage(dark_image=network_img_data,
                       light_image=network_img_data, size=(30, 30))

# Telegram icon
telegram_img_data = Image.open("Images/Telegram Logo.png")
telegram_img = CTkImage(dark_image=telegram_img_data, light_image=telegram_img_data, size=(40, 40))

# Mail Icon
mail_img_data = Image.open("Images/Mail Icon.png")
mail_img = CTkImage(dark_image=mail_img_data, light_image=mail_img_data, size=(40, 40))

# About us icon
about_us_img_data_light = Image.open("Images/About Us Icon.png")
about_us_img_data_dark = Image.open("Images/About Us Dark Theme.png")
about_us_img = CTkImage(dark_image=about_us_img_data_dark, light_image=about_us_img_data_light, size=(30, 30))

# Settings icon
settings_img_data_light = Image.open("Images/Cog Icon.png")
settings_img_data_dark = Image.open("Images/Cog Icon Dark Theme.png")
settings_img = CTkImage(dark_image=settings_img_data_dark, light_image=settings_img_data_light, size=(30, 30))

# Arrow icon
arrow_img_data_light = Image.open("Images/Arrow Icon.png")
arrow_img_data_dark = Image.open("Images/Arrow Icon Dark Theme.png")
arrow_img = CTkImage(dark_image=arrow_img_data_dark, light_image=arrow_img_data_light)

# App log icon
light_app_log_img_data = Image.open("Images/LightTheme Log Icon.png")
dark_app_log_img_data = Image.open("Images/DarkTheme Log Icon.png")
app_log_img = CTkImage(dark_image=dark_app_log_img_data, light_image=light_app_log_img_data, size=(40, 40))

# Expand icon
light_expand_icon_img_data = Image.open("Images/LightTheme Expand Icon.png")
dark_expand_icon_img_data = Image.open("Images/DarkTheme Expand Icon.png")
expand_icon_img = CTkImage(dark_image=dark_expand_icon_img_data, light_image=light_expand_icon_img_data, size=(15, 15))

# Collapse icon
light_collapse_icon_img_data = Image.open("Images/LightTheme Collapse Icon.png")
dark_collapse_icon_img_data = Image.open("Images/DarkTheme Collapse Icon.png")
collapse_icon_img = CTkImage(dark_image=dark_collapse_icon_img_data, light_image=light_collapse_icon_img_data, size=(15, 15))

# Test DNS icon
test_dns_img_data = Image.open("Images/Test DNS Icon.png")
test_dns_img = CTkImage(dark_image=test_dns_img_data, light_image=test_dns_img_data, size=(30, 30))

# Custom DNS icon
custom_dns_img_data = Image.open("Images/Custom DNS Icon.png")
custom_dns_img = CTkImage(dark_image=custom_dns_img_data, light_image=custom_dns_img_data, size=(30, 30))

# Default DNS icon
default_dns_img_data = Image.open("Images/Default DNS Icon.png")
default_dns_img = CTkImage(dark_image=default_dns_img_data, light_image=default_dns_img_data, size=(30, 30))

# DNS server icon
dns_server_img_data = Image.open("Images/DNS Server Icon.png")
dns_server_img = CTkImage(dark_image=dns_server_img_data, light_image=dns_server_img_data, size=(30, 30))

# Get ping icon
get_ping_img_data = Image.open("Images/Get Ping Icon.png")
get_ping_img = CTkImage(dark_image=get_ping_img_data, light_image=get_ping_img_data, size=(35, 30))

# Github icon
github_img_data = Image.open("Images/Github Icon.png")
github_img = CTkImage(dark_image=github_img_data, light_image=github_img_data, size=(40, 40))

# </editor-fold>

app = CTk()
app.title("Auspicious")
app.geometry('400x620')

if OS == 'Linux':
    app.wm_iconbitmap()
elif OS == 'Windows':
    app.wm_iconbitmap("Images/icon.ico")


# Set the application theme and language right before the mainloop so all the elements are created
# In the set_app_theme() and set_app_language() method we change some properties of the app elements
# If we do that before all the elements are created we will get error
app.resizable(False, False)

# <editor-fold desc="terms_frame">

terms_frame = CTkFrame(master=app, fg_color="transparent", corner_radius=0)
terms_frame.columnconfigure(0, weight=1)
terms_frame.rowconfigure(2, weight=1)

agreement_app_label_frame = CTkFrame(master=terms_frame, fg_color="transparent", corner_radius=0)
CTkLabel(master=agreement_app_label_frame,
         text="Auspicious",
         font=("Arial Bold", 28)).grid(row=0, column=0)
CTkLabel(master=agreement_app_label_frame,
         text="DNS Changer",
         font=("Arial Narrow", 14)).grid(row=0, column=1, padx=(5, 0))


def choice_picker(choice):
    if choice == 'Persian(فارسی)':
        fixed_choice = "persian"
    else:
        fixed_choice = "english"
    set_app_language(fixed_choice, True)


combo_default_value = StringVar()

if OS == "Windows":
    languages = ['Persian(فارسی)', 'English(انگلیسی)']
    if app_language == "persian":
        combo_default_value.set(languages[0])
    else:
        combo_default_value.set(languages[1])

elif OS == "Linux":
    languages = ['English']
    combo_default_value.set(languages[0])

terms_language_combo = CTkComboBox(master=agreement_app_label_frame,
                                   values=languages,
                                   variable=combo_default_value,
                                   command=choice_picker)
terms_language_combo.grid(row=0, column=2, padx=5)

agreement_app_label_frame.grid(row=0, column=0, sticky=W+E, padx=20, pady=(20, 0))

terms_of_services_label = CTkLabel(master=terms_frame,
                                   text="Terms of services:",
                                   font=("Arial", 22))
terms_of_services_label.grid(row=1, column=0, sticky=W, padx=20, pady=(15, 0))

scrollable_frame = CTkScrollableFrame(master=terms_frame, fg_color="transparent", corner_radius=0)

terms_label1 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* This is a Free Program "
                             "made by @Auspicious and "
                             "designed by @lurixed "
                             "(on telegram) and any "
                             "commercial use is against"
                             " our intentions!")
terms_label1.grid(row=0, column=0, padx=7)

terms_label2 = CTkLabel(master=scrollable_frame,
                         wraplength=340,
                         justify=LEFT,
                         font=("Arial", 16),
                         text="* This app is just a"
                              " DNS changer and we "
                              "are not responsible "
                              "of any problem caused "
                              "by the DNS servers!")
terms_label2.grid(row=1, column=0, pady=(15, 0))

terms_label3 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* This program is"
                             " Open-source and you "
                             "can find the code at: ")
terms_label3.grid(row=2, column=0, pady=(15, 0))

terms_label_button1 = CTkButton(master=scrollable_frame,
                                fg_color="#F3D300",
                                hover_color="#796900",
                                text_color="#242424",
                                font=("Arial", 12),
                                command=lambda: open_url("https://github.com/AuspiciousIsHere/DNS-Changer"),
                                text="Here")
terms_label_button1.grid(row=3, column=0, pady=(5, 0), sticky=W)

terms_label4 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* Don’t download any file "
                             "related to this program "
                             "from any other sources!")
terms_label4.grid(row=4, column=0, pady=(15, 0))

terms_label5 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* There are Three DNSs being "
                             "used in this Program to bypass "
                             "the prohibitions caused by other "
                             "countries over Iran and the names are:\n"
                             "Spotify DNS: Radar Game\n"
                             "Anti-Prohibition DNS: 403 online\n"
                             "Temporary DNS: Shelter (might change)")
terms_label5.grid(row=5, column=0, pady=(15, 0))

terms_label6 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* We do not own any of these "
                              "DNS servers and you can"
                              " find their websites by "
                              "searching each name!")
terms_label6.grid(row=6, column=0, pady=(15, 0))

terms_label7 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* The Three mentioned DNSs"
                             " above will only work in Iran "
                             "so if you are in other countries,"
                             " none of the mentioned DNSs "
                             "are guaranteed to work!")
terms_label7.grid(row=7, column=0, pady=(15, 0))

terms_label8 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="* This Program needs Administrator "
                             "privilege (makes command execution) "
                             "in order to work and makes .ini files "
                             "to configure and downloads a file located "
                             "at: ")
terms_label8.grid(row=8, column=0, pady=(15, 0))

terms_label_button2 = CTkButton(master=scrollable_frame,
                                fg_color="#F3D300",
                                hover_color="#796900",
                                text_color="#242424",
                                font=("Arial", 12),
                                command=lambda:open_url("https://github.com/AuspiciousIsHere/Update"),
                                text="Here")
terms_label_button2.grid(row=9, column=0, pady=(5, 0), sticky=W)

terms_label9 = CTkLabel(master=scrollable_frame,
                        wraplength=340,
                        justify=LEFT,
                        font=("Arial", 16),
                        text="to update the Temporary DNS!")
terms_label9.grid(row=10, column=0, pady=(10, 0), sticky=W)


scrollable_frame.grid(row=2, column=0, sticky=W+E+N+S, padx=20, pady=20)

agreement_buttons_frame = CTkFrame(master=terms_frame, fg_color="transparent", corner_radius=0)
agreement_buttons_frame.columnconfigure(0, weight=1)

check_box_var = StringVar()
check_box_var.set("False")


def check_event():
    global check_box_var
    if check_box_var.get() == "True":
        continue_button.configure(state=NORMAL, fg_color="#F3D300")
    else:
        continue_button.configure(state=DISABLED, fg_color="#796900")


agreement_check_box = CTkCheckBox(master=agreement_buttons_frame,
                                  variable=check_box_var,
                                  onvalue="True",
                                  offvalue="False",
                                  checkmark_color="#242424",
                                  fg_color="#F3D300",
                                  hover_color="#534800",
                                  command=check_event,
                                  text="I have read and accept the Agreement.", font = ("Arial", 16))
agreement_check_box.grid(row=0, column=0, sticky=W)


continue_button = CTkButton(master=agreement_buttons_frame,
                            text="Continue",
                            height=40,
                            fg_color="#796900",
                            hover_color="#796900",
                            state=DISABLED,
                            command=set_app_terms,
                            text_color="#242424",
                            font=("Arial Bold", 18))
continue_button.grid(row=1, column=0, sticky=W+E, padx=0, pady=(5, 0))

quit_button = CTkButton(master=agreement_buttons_frame,
                        text="Quit",
                        height=40,
                        fg_color="transparent",
                        hover_color="#534800",
                        border_width=3,
                        border_color="#F3D300",
                        command=sys.exit,
                        font=("Arial Bold", 18))
quit_button.grid(row=2, column=0, sticky=W+E, padx=0, pady=(10, 0))

agreement_buttons_frame.grid(row=3, column=0, sticky=W+E, padx=20, pady=(0, 15))

# </editor-fold>

# <editor-fold desc="loading_frame">

# The loading page
loading_frame = CTkFrame(master=app, fg_color="transparent", corner_radius=0)

loading_frame.rowconfigure(0, weight=2)
loading_frame.rowconfigure(1, weight=1)
loading_frame.columnconfigure(0, weight=1)

# The frame that contains the loading animations
label_frame = CTkFrame(master=loading_frame, fg_color="transparent")

# The label that contains the app's main-label
app_main_label = CTkLabel(master=label_frame, text="", fg_color="transparent")
app_main_label.pack()

if app_theme == 'light':
    app_main_label_animated_gif = AnimatedGif(app, app_main_label,
                                              "Images/LightTheme Auspicious Label.gif",
                                              restart=False, show_last_frame=True)

else:
    app_main_label_animated_gif = AnimatedGif(app, app_main_label,
                                              "Images/DarkTheme Auspicious Label.gif",
                                              restart=False, show_last_frame=True)


# The label that contains the loading gif
gif_label = CTkLabel(master=label_frame, text="")
gif_label.pack(pady=(100, 0))

if app_theme == 'light':
    animated_gif = AnimatedGif(app, gif_label, "Images/LightTheme Loading Spin.gif")

else:
    animated_gif = AnimatedGif(app, gif_label, "Images/DarkTheme Loading Spin.gif")

# Loading Label
loading_label = CTkLabel(master=label_frame, text="Loading...", font=("Arial Narrow", 18))
loading_label.pack()

label_frame.grid(row=0, column=0, pady=(0, 0))

# The frame that contains the app and developer and designer label on loading
app_label_frame = CTkFrame(master=loading_frame, fg_color="transparent")

CTkLabel(master=app_label_frame, text="DNS Changer", font=("Arial Bold", 32)).grid(row=1, column=0, pady=(0, 0))

made_label = CTkLabel(master=app_label_frame, text="Made by: @I_AM_AUSPICIOUS",
                      font=("Arial Narrow", 18), fg_color="transparent")
made_label.grid(row=2, column=0, pady=(0, 0))
design_label = CTkLabel(master=app_label_frame, text="Design by: @lurixed",
                        font=("Arial Narrow", 18), fg_color="transparent")
design_label.grid(row=3, column=0, pady=(0, 0))

app_label_frame.grid(row=1, column=0, pady=(0, 30))

# </editor-fold>

# <editor-fold desc="small_buttons_frame (first page frame, row 0)">

# The frame that contains the setting and about us buttons
small_buttons_frame = CTkFrame(master=app, height=60, fg_color="transparent", border_width=0, corner_radius=0)
small_buttons_frame.rowconfigure(0, weight=1)
small_buttons_frame.columnconfigure(0, weight=1)


about_us_btn = CTkButton(master=small_buttons_frame, height=50, width=50, image=about_us_img, command=go_to_about_us,
                         corner_radius=20, text="", fg_color="transparent", hover_color=icon_button_hover_color)
about_us_btn.grid(row=0, column=0, sticky=W, padx=20, pady=20)

settings_btn = CTkButton(master=small_buttons_frame, height=50, width=50, image=settings_img,
                         corner_radius=20, text="", command=go_to_settings,
                         fg_color="transparent", hover_color=icon_button_hover_color)
settings_btn.grid(row=0, column=0, sticky=E, padx=20, pady=20)

# App Status
if status == True:
    status_label_text = "Online"
    status_label_text_color = "#00896f"
else:
    status_label_text = "Offline"
    status_label_text_color = "#c34a36"

status_label = CTkLabel(master=small_buttons_frame, text=status_label_text, font=("Arial Narrow", 24), fg_color="transparent", text_color=status_label_text_color)
status_label.grid(row=0, column=0, padx=20, pady=20)


# small_buttons_frame.grid(row=0, column=0, sticky=W+E)

# </editor-fold>

# <editor-fold desc="buttons_frame (first page frame, row 1)">

# The frame that contains the buttons
buttons_frame = CTkFrame(master=app, fg_color="transparent", border_width=0, corner_radius=0)

# App Label
CTkLabel(master=buttons_frame, image=auspicious_main_label, text="").pack(pady=(5, 0))

dns_changer_label = CTkLabel(master=buttons_frame, text="DNS Changer", font=("Arial Narrow", 24))
dns_changer_label.pack(pady=(2, 0))

# Spotify DNS button
spotify_btn = CTkButton(master=buttons_frame, height=60, width=260, image=spotify_logo_img, text="Spotify DNS",
                        text_color=bold_text_color,
                        font=("Arial", 20), fg_color="transparent", border_color="#1DD460", border_width=5,
                        hover_color="#E2FFDf", corner_radius=20, command=lambda:Manage(SetSpotifyDNS))
spotify_btn.pack(pady=(30, 0))

# Anti-Prohibition DNS button
anti_pro_btn = CTkButton(master=buttons_frame, height=60, width=260,
                         image=anti_prohibition_img, text="Anti Prohibition DNS",
                         text_color=bold_text_color,
                         font=("Arial", 17), fg_color="transparent", border_color="#F77E16",
                         border_width=5, hover_color="#FFEFE2", corner_radius=20, command=lambda:Manage(SetAnti))
anti_pro_btn.pack(pady=(10, 0))

temporarily_dns_btn = CTkButton(master=buttons_frame, height=60, width=260,
                                image=network_img, text="Temporarily DNS",
                                text_color=bold_text_color,
                                font=("Arial", 17), fg_color="transparent", border_color="#FFDD00",
                                border_width=5, hover_color="#FFF6BC", corner_radius=20, command= lambda:Manage(SetTemporary))
temporarily_dns_btn.pack(pady=(10, 0))

# Other services button
other_services_btn = CTkButton(master=buttons_frame, height=35, text="Other Services...", font=("Arial", 20),
                               text_color=bold_text_color, command=go_to_other_services,
                               fg_color="transparent", hover_color=icon_button_hover_color)
other_services_btn.pack(pady=(20, 0))

log_frame = CTkFrame(master=buttons_frame, fg_color="transparent")

log_frame.rowconfigure(1, weight=1)
log_frame.columnconfigure(0, weight=1)

app_log_text_box_frame = CTkFrame(master=log_frame, width=380, border_width=2, fg_color="transparent")

app_log_text_box_frame.rowconfigure(0, weight=1)
app_log_text_box_frame.columnconfigure(0, weight=1)

app_log_text_box = CTkLabel(master=app_log_text_box_frame, font=("Arial", 14),
                            text='',
                            width=380, height=100,
                            corner_radius=99,
                            fg_color="transparent",
                            wraplength=300, justify=CENTER)
app_log_text_box.grid(row=0, column=0, sticky=W+E+N+S, pady=(20, 2), padx=2)

app_log_text_box_frame.grid(row=1, column=0, sticky=E+W+N+S, pady=(28, 0))

CTkLabel(master=log_frame, text="", image=app_log_img,
         fg_color="transparent").grid(row=1, column=0, sticky=W+N, padx=(10, 0))

app_log_label = CTkLabel(master=log_frame, font=("Arial", 16),
                         text="App Log", fg_color="transparent")
app_log_label.grid(row=1, column=0, sticky=W+N, padx=(55, 0))

log_frame.pack(padx=10, pady=10)

# buttons_frame.grid(row=1, column=0, sticky=E+W+N+S)

# </editor-fold>

# <editor-fold desc="other_services_frame">

other_services_frame = CTkFrame(master=app, corner_radius=0, fg_color="transparent")

# The frame that contains the go back button
top_frame = CTkFrame(master=other_services_frame, corner_radius=0, fg_color="transparent")

go_to_home_page_from_other_services_btn = CTkButton(master=top_frame, height=50, width=50, image=arrow_img,
                                                    corner_radius=20, text="", fg_color="transparent",
                                                    command=go_to_home_page_from_other_services,
                                                    hover_color=icon_button_hover_color)
go_to_home_page_from_other_services_btn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

top_frame.grid(row=0, column=0, sticky=W+E)


middle_frame = CTkFrame(master=other_services_frame, corner_radius=0, fg_color="transparent")

middle_frame.columnconfigure(0, weight=1)


get_ping_btn_frame = CTkFrame(master=middle_frame, corner_radius=0, fg_color="transparent")
get_ping_btn_frame.columnconfigure(1, weight=1)

go_to_get_ping_btn = CTkButton(master=get_ping_btn_frame,
                                fg_color="#F3D300",
                                hover_color="#796900",
                                corner_radius=10,
                                height=50,
                                width=50,
                                command=go_to_get_ping,
                                text="",
                                image=test_dns_img,
                                font=("Arial", 18))
go_to_get_ping_btn.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))

CTkFrame(master=get_ping_btn_frame,
         fg_color="transparent",
         height=50,
         border_width=3,
         corner_radius=18,
         border_color="#D8BB00").grid(row=0, column=1, sticky=W+E, padx=20, pady=(20, 0))
get_ping_btn = CTkLabel(master=get_ping_btn_frame,
                        fg_color="transparent",
                        height=40,
                        text="Test DNS(s)",
                        font=("Arial", 18))
get_ping_btn.grid(row=0, column=1, padx=20, pady=(20, 0))

get_ping_btn_frame.grid(row=0, column=0, sticky=W+E)


get_current_dns_ping_btn_frame = CTkFrame(master=middle_frame, corner_radius=0, fg_color="transparent")
get_current_dns_ping_btn_frame.columnconfigure(0, weight=1)

actual_get_current_dns_ping_btn = CTkButton(master=get_current_dns_ping_btn_frame,
                                            width=50,
                                            height=50,
                                            corner_radius=10,
                                            text="",
                                            fg_color="#F3D300",
                                            hover_color="#796900",
                                            image=get_ping_img,
                                            font=("Arial", 18),
                                            command= lambda: threading.Thread(target=get_current_dns_servers_ping).start())
actual_get_current_dns_ping_btn.grid(row=0, column=1, sticky=E, padx=(0, 20), pady=(20, 0))

CTkFrame(master=get_current_dns_ping_btn_frame,
         height=50,
         corner_radius=18,
         fg_color="transparent",
         border_width=3,
         border_color="#D8BB00").grid(row=0, column=0, padx=20, pady=(20, 0), sticky=W+E)
get_current_dns_ping_btn = CTkLabel(master=get_current_dns_ping_btn_frame,
                                    text="Get current DNS ping",
                                    font=("Arial", 18))
get_current_dns_ping_btn.grid(row=0, column=0, padx=20, pady=(20, 0))

get_current_dns_ping_btn_frame.grid(row=1, column=0, sticky=W+E)


get_current_dns_server_btn_frame = CTkFrame(master=middle_frame, corner_radius=0, fg_color="transparent")
get_current_dns_server_btn_frame.columnconfigure(1, weight=1)

actual_get_current_dns_server_btn = CTkButton(master=get_current_dns_server_btn_frame,
                                              height=50,
                                              width=50,
                                              corner_radius=10,
                                              text="",
                                              fg_color="#F3D300",
                                              hover_color="#796900",
                                              image=dns_server_img,
                                              font=("Arial", 18), command=get_current_dns_servers)
actual_get_current_dns_server_btn.grid(row=0, column=0, sticky=W, padx=(20, 0), pady=(20, 0))

CTkFrame(master=get_current_dns_server_btn_frame,
         height=50,
         corner_radius=18,
         fg_color="transparent",
         border_width=3,
         border_color="#D8BB00").grid(row=0, column=1, sticky=W+E, padx=20, pady=(20, 0))
get_current_dns_server_btn = CTkLabel(master=get_current_dns_server_btn_frame,
                                      text="Get current DNS server",
                                      font=("Arial", 18))
get_current_dns_server_btn.grid(row=0, column=1, padx=20, pady=(20, 0))

get_current_dns_server_btn_frame.grid(row=2, column=0, sticky=W+E)


apply_custom_dns_btn_frame = CTkFrame(master=middle_frame, corner_radius=0, fg_color="transparent")
apply_custom_dns_btn_frame.columnconfigure(0, weight=1)

actual_apply_custom_dns = CTkButton(master=apply_custom_dns_btn_frame,
                                    height=50,
                                    width=50,
                                    command=go_to_apply_custom_dns,
                                    corner_radius=10,
                                    text="",
                                    fg_color="#F3D300",
                                    hover_color="#796900",
                                    image=custom_dns_img,
                                    font=("Arial", 18))
actual_apply_custom_dns.grid(row=3, column=1, sticky=E, padx=(0, 20), pady=(20, 0))

CTkFrame(master=apply_custom_dns_btn_frame,
         height=50,
         corner_radius=18,
         fg_color="transparent",
         border_width=3,
         border_color="#D8BB00").grid(row=3, column=0, sticky=E+W, padx=20, pady=(20, 0))
apply_custom_dns = CTkLabel(master=apply_custom_dns_btn_frame,
                            text="Apply custom DNS",
                            font=("Arial", 18))
apply_custom_dns.grid(row=3, column=0, padx=20, pady=(20, 0))

apply_custom_dns_btn_frame.grid(row=3, column=0, sticky=W+E)


apply_default_dns_btn_frame = CTkFrame(master=middle_frame, corner_radius=0, fg_color="transparent")
apply_default_dns_btn_frame.columnconfigure(1, weight=1)

actual_apply_default_dns = CTkButton(master=apply_default_dns_btn_frame,
                                     height=50,
                                     width=50,
                                     corner_radius=10,
                                     text="",
                                     fg_color="#F3D300",
                                     hover_color="#796900",
                                     image=default_dns_img,
                                     font=("Arial", 18),
                                     command=DefaultDNS)
actual_apply_default_dns.grid(row=4, column=0, sticky=W, padx=(20, 0), pady=(20, 0))

CTkFrame(master=apply_default_dns_btn_frame,
         height=50,
         corner_radius=18,
         fg_color="transparent",
         border_width=3,
         border_color="#D8BB00").grid(row=4, column=1, sticky=W+E, padx=20, pady=(20, 0))
apply_default_dns = CTkLabel(master=apply_default_dns_btn_frame,
                             text="Apply default DNS",
                             font=("Arial", 18))
apply_default_dns.grid(row=4, column=1, padx=20, pady=(20, 0))

apply_default_dns_btn_frame.grid(row=4, column=0, sticky=W+E)

middle_frame.grid(row=1, column=0, sticky=W+E+S+N)


bottom_frame = CTkFrame(master=other_services_frame, corner_radius=0, fg_color="transparent")

bottom_frame.columnconfigure(0, weight=1)

# other_services_text_box = CTkTextbox(master=bottom_frame,
#                                      border_width=2, state=DISABLED, fg_color="transparent")
# other_services_text_box.grid(row=6, column=0, sticky=W+E, padx=20, pady=(0, 20))
# 
# other_services_app_log_label = CTkLabel(master=bottom_frame,
#                                 wraplength=300, justify=CENTER, text='', fg_color="transparent")
# 
# other_services_app_log_label.grid(row=6, column=0, padx=20, pady=(30, 20))

other_services_log_frame = CTkFrame(master=bottom_frame, fg_color="transparent")
other_services_log_frame.rowconfigure(1, weight=1)
other_services_log_frame.columnconfigure(0, weight=1)

other_services_app_log_text_box_frame = CTkFrame(master=other_services_log_frame, width=380, border_width=2, fg_color="transparent")

other_services_app_log_text_box_frame.rowconfigure(0, weight=1)
other_services_app_log_text_box_frame.columnconfigure(0, weight=1)

other_services_app_log_text_box = CTkLabel(master=other_services_app_log_text_box_frame, font=("Arial", 14),
                                           text='',
                                           width=380, height=100,
                                           corner_radius=99,
                                           fg_color="transparent",
                                           wraplength=280,
                                           justify=CENTER)
other_services_app_log_text_box.grid(row=0, column=0, sticky=W+E+N+S, pady=(20, 2), padx=2)

other_services_app_log_text_box_frame.grid(row=1, column=0, sticky=E+W+N+S, pady=(28, 0))

CTkLabel(master=other_services_log_frame, text="", image=app_log_img,
         fg_color="transparent").grid(row=1, column=0, sticky=W+N, padx=(10, 0))

other_services_app_log_label = CTkLabel(master=other_services_log_frame, font=("Arial", 16),
                                        text="App Log", fg_color="transparent")
other_services_app_log_label.grid(row=1, column=0, sticky=W+N, padx=(55, 0))

other_services_log_frame.grid(row=6, column=0, padx=10, pady=10, sticky=S)

bottom_frame.grid(row=6, column=0, pady=(30, 0), sticky=W+E)

# </editor-fold>

# <editor-fold desc="settings_frame">

# The frame that contains the settings page
settings_frame = CTkFrame(master=app, fg_color="transparent", border_width=0, corner_radius=0)

# Go to home page button
go_to_home_page_from_settings_btn = CTkButton(master=settings_frame, height=50, width=50, image=arrow_img,
                                              corner_radius=20, text="", fg_color="transparent",
                                              command=go_to_home_from_settings,
                                              hover_color=icon_button_hover_color)
go_to_home_page_from_settings_btn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

# Settings label
settings_label = CTkLabel(master=settings_frame, text="Settings",
                          font=("Arial Bold", 32))
settings_label.grid(row=1, column=0, sticky=W, padx=20)

# Appearance label
appearance_label = CTkLabel(master=settings_frame, text="Appearance",
                            font=("Arial", 24))
appearance_label.grid(row=2, column=0, sticky=W, padx=20, pady=(40, 0))

app_theme_frame = CTkFrame(master=settings_frame, border_width=2)
app_theme_frame.columnconfigure(0, weight=1)

# App theme label
app_theme_label = CTkLabel(master=app_theme_frame, text="App Theme",
                           font=("Arial", 18))
app_theme_label.grid(row=0, column=0, sticky=W, padx=30, pady=(10, 0))

app_theme_desc_label = CTkLabel(master=app_theme_frame, text="Select which app theme to display",
                                font=("Arial", 13))
app_theme_desc_label.grid(row=1, column=0, sticky=W, padx=30, pady=(0, 2))

# Set the current value of the radio buttons (which one is currently selected)
radio_var = StringVar()
radio_var.set(app_theme)

# Dark theme radio button
dark_radio = CTkRadioButton(master=app_theme_frame, text="Dark",
                            fg_color="#C4A300",
                            hover_color="#796900",
                            variable=radio_var, value='dark',
                            command=lambda: set_app_theme('dark', True),
                            font=("Arial", 16))

dark_radio_label = CTkLabel(master=app_theme_frame, text="تیره", font=("Arial", 16))

# Light theme radio button
light_radio = CTkRadioButton(master=app_theme_frame, text="Light",
                             fg_color="#C4A300",
                             hover_color="#796900",
                             variable=radio_var, value="light",
                             command=lambda: set_app_theme('light', True),
                             font=("Arial", 16))

light_radio_label = CTkLabel(master=app_theme_frame, text="روشن", font=("Arial", 16))


def expand_app_theme():
    global is_app_theme_expanded
    is_app_theme_expanded = True

    if app_language == "persian":
        dark_radio.grid(row=2, column=0, sticky=E, padx=0, pady=(10, 5))
        dark_radio_label.grid(row=2, column=0, sticky=E, padx=(0, 110), pady=(10, 5))
        light_radio.grid(row=3, column=0, sticky=E, padx=0, pady=(0, 10))
        light_radio_label.grid(row=3, column=0, sticky=E, padx=(0, 110), pady=(0, 10))

    else:
        light_radio.grid(row=3, column=0, sticky=W, padx=40, pady=(0, 10))
        dark_radio.grid(row=2, column=0, sticky=W, padx=40, pady=(10, 5))

    expand_collapse_app_theme_btn.configure(command=collapse_app_theme)
    expand_collapse_app_theme_btn.configure(image=collapse_icon_img)


def collapse_app_theme():
    global is_app_theme_expanded
    is_app_theme_expanded = False
    light_radio.grid_forget()
    light_radio_label.grid_forget()
    dark_radio.grid_forget()
    dark_radio_label.grid_forget()
    expand_collapse_app_theme_btn.configure(command=expand_app_theme)
    expand_collapse_app_theme_btn.configure(image=expand_icon_img)


expand_collapse_app_theme_btn = CTkButton(master=app_theme_frame, image=expand_icon_img,
                                          width=20, command=expand_app_theme,
                                          text="", fg_color="transparent", hover=False)
expand_collapse_app_theme_btn.grid(row=0, column=0, rowspan=2, sticky=E, padx=15)

app_theme_frame.grid(row=3, column=0, sticky=W+E, padx=20, pady=(10, 0))


app_language_frame = CTkFrame(master=settings_frame, border_width=2)
app_language_frame.columnconfigure(0, weight=1)

# Language label
language_label = CTkLabel(master=app_language_frame, text="Language",
                          font=("Arial", 18))
language_label.grid(row=0, column=0, sticky=W, padx=30, pady=(10, 0))

language_desc_label = CTkLabel(master=app_language_frame, text="Select the application language",
                               font=("Arial", 13))
language_desc_label.grid(row=1, column=0, sticky=W, padx=30, pady=(0, 2))

# Set the current value of the radio buttons (which one is currently selected)
language_radio_var = StringVar()
language_radio_var.set(app_language)


# Persian language radio button
persian_radio = CTkRadioButton(master=app_language_frame, text="Persian (فارسی)",
                               fg_color="#C4A300",
                               hover_color="#796900",
                               variable=language_radio_var, value='persian',
                               command=lambda: set_app_language("persian", True),
                               font=("Arial", 16))
if OS == "Linux":
    persian_radio.configure(state = "disabled")

persian_radio_label = CTkLabel(master=app_language_frame, text="فارسی", font=("Arial", 16))

# English language radio button
english_radio = CTkRadioButton(master=app_language_frame, text="English",
                               fg_color="#C4A300",
                               hover_color="#796900",
                               variable=language_radio_var, value="english",
                               command=lambda: set_app_language("english", True),
                               font=("Arial", 16))

english_radio_label = CTkLabel(master=app_language_frame, text="انگلیسی(English)", font=("Arial", 16))


def expand_app_language():
    global is_app_language_expanded
    is_app_language_expanded = True

    if app_language == "persian":
        english_radio.grid(row=3, column=0, sticky=E, padx=0, pady=(0, 10))
        english_radio_label.grid(row=3, column=0, sticky=E, padx=(0, 110), pady=(0, 10))
        persian_radio.grid(row=2, column=0, sticky=E, padx=0, pady=(10, 5))
        persian_radio_label.grid(row=2, column=0, sticky=E, padx=(0, 110), pady=(10, 5))

    else:
        english_radio.grid(row=3, column=0, sticky=W, padx=40, pady=(0, 10))
        persian_radio.grid(row=2, column=0, sticky=W, padx=40, pady=(10, 5))

    expand_collapse_app_language_btn.configure(command=collapse_app_language)
    expand_collapse_app_language_btn.configure(image=collapse_icon_img)


def collapse_app_language():
    global is_app_language_expanded
    is_app_language_expanded = False
    english_radio.grid_forget()
    english_radio_label.grid_forget()
    persian_radio.grid_forget()
    persian_radio_label.grid_forget()
    expand_collapse_app_language_btn.configure(command=expand_app_language)
    expand_collapse_app_language_btn.configure(image=expand_icon_img)


expand_collapse_app_language_btn = CTkButton(master=app_language_frame, image=expand_icon_img,
                                             width=20, command=expand_app_language,
                                             text="", fg_color="transparent", hover=False)
expand_collapse_app_language_btn.grid(row=0, column=0, rowspan=2, sticky=E, padx=15)

app_language_frame.grid(row=4, column=0, sticky=W+E, padx=20, pady=(10, 0))

# </editor-fold>

# <editor-fold desc="about_us_frame">

about_us_frame = CTkFrame(master=app, fg_color="transparent", corner_radius=0)

# Go to home page button
go_to_home_page_from_about_us_btn = CTkButton(master=about_us_frame, height=50, width=50, image=arrow_img,
                                              corner_radius=20, text="", fg_color="transparent",
                                              command=go_to_home_from_about_us,
                                              hover_color=icon_button_hover_color)
go_to_home_page_from_about_us_btn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

about_label = CTkLabel(master=about_us_frame, text="About:",
                       font=("Arial Bold", 30), wraplength=400)
about_label.grid(row=1, column=0, sticky=W, padx=20)

developer_label = CTkLabel(master=about_us_frame, text="Developer:", font=("Arial", 16))
developer_label.grid(row=2, column=0, sticky=W, padx=20, pady=(20, 0))
CTkButton(master=about_us_frame, image=telegram_img, text="@I_AM_AUSPICIOUS",
          fg_color="#F3D300", hover_color="#796900",
          text_color="#242424",
          font=("Arial Bold", 18), command=lambda: open_url("https://t.me/I_AM_AUSPICIOUS"),
          anchor="w").grid(row=3, column=0, sticky=W+E, padx=20)

developer_email_label = CTkLabel(master=about_us_frame, text="Developer's email:", font=("Arial", 16))
developer_email_label.grid(row=4, column=0, sticky=W, padx=20, pady=(10, 0))
CTkButton(master=about_us_frame, image=mail_img, text="auspicious818@yahoo.com",
          fg_color="#F3D300", hover_color="#796900",
          text_color="#242424",
          font=("Arial Bold", 18),
          anchor="w").grid(row=5, column=0, sticky=W+E, padx=20)

designer_label = CTkLabel(master=about_us_frame, text="Designer:", font=("Arial", 16))
designer_label.grid(row=6, column=0, sticky=W, padx=20, pady=(20, 0))
CTkButton(master=about_us_frame, image=telegram_img,
          fg_color="#F3D300", hover_color="#796900",
          text_color="#242424",
          text="@lurixed", font=("Arial Bold", 18), anchor="w",
          command=lambda: open_url("https://t.me/lurixed")).grid(row=7, column=0, sticky=W+E, padx=20)

github_label = CTkLabel(master=about_us_frame, text="Github", font=("Arial", 16))
github_label.grid(row=8, column=0, sticky=W, padx=20, pady=(20, 0))
CTkButton(master=about_us_frame, image=github_img, text="AuspiciousIsHere/DNS-Changer",
          fg_color="#F3D300", hover_color="#796900",
          text_color="#242424",
          font=("Arial Bold", 18), command=lambda: open_url("https://github.com/AuspiciousIsHere/DNS-Changer"),
          anchor="w").grid(row=9, column=0, sticky=W+E, padx=20)

line1_about_label = CTkLabel(master=about_us_frame, text="Contact us if you encountered any unexpected error.",
                             font=("Arial Bold", 13), wraplength=400)
line1_about_label.grid(row=10, column=0, sticky=W, padx=20, pady=(0, 0))
line2_about_label = CTkLabel(master=about_us_frame, text="Feel free to ask any question.",
                             font=("Arial Bold", 13), wraplength=400)
line2_about_label.grid(row=11, column=0, sticky=W, padx=20)

# </editor-fold>

# <editor-fold desc="get_ping_frame">

get_ping_frame = CTkFrame(master=app, fg_color="transparent", corner_radius=0)

get_ping_frame.columnconfigure(0, weight=1)
get_ping_frame.columnconfigure(1, weight=1)
get_ping_frame.columnconfigure(2, weight=1)

go_to_other_services_page_from_get_ping_btn = CTkButton(master=get_ping_frame,
                                                        height=50, width=50, image=arrow_img,
                                                        corner_radius=20, text="", fg_color="transparent",
                                                        command=go_to_other_services_page_from_get_ping,
                                                        hover_color=icon_button_hover_color)
go_to_other_services_page_from_get_ping_btn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

# The text must be " " because of a bug in library
CTkButton(master=get_ping_frame,
          image=spotify_logo_img,
          text=" ",
          fg_color="transparent",
          hover=False,
          height=50,
          width=50).grid(row=2, column=0, sticky=W, padx=2, pady=(0, 10))
CTkButton(master=get_ping_frame,
          image=anti_prohibition_img,
          text=" ",
          fg_color="transparent",
          hover=False,
          height=50,
          width=50).grid(row=3, column=0, sticky=W, padx=2, pady=(0, 10))
CTkButton(master=get_ping_frame,
          image=network_img, text=" ",
          fg_color="transparent",
          hover=False,
          height=50,
          width=50).grid(row=4, column=0, sticky=W, padx=2, pady=(0, 10))

CTkLabel(master=get_ping_frame,
         text="Spotify",
         font=("Arial", 12),
         fg_color="transparent",
         height=50,
         width=50).grid(row=1, column=1, sticky=W, padx=5)
CTkLabel(master=get_ping_frame,
         text="Chat GPT",
         font=("Arial", 12),
         fg_color="transparent",
         height=50,
         width=50).grid(row=1, column=2, sticky=W, padx=5)
CTkLabel(master=get_ping_frame,
         text="Gemini",
         font=("Arial", 12),
         fg_color="transparent",
         height=50,
         width=50).grid(row=1, column=3, sticky=W, padx=5)


# d1s1: d = DNS, s = Site (DNS1 Site1)
d1s1 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d1s1.grid(row=2, column=1, padx=5)
d1s2 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d1s2.grid(row=2, column=2, padx=5)
d1s3 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d1s3.grid(row=2, column=3, padx=5)

d2s1 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d2s1.grid(row=3, column=1, padx=5)
d2s2 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d2s2.grid(row=3, column=2, padx=5)
d2s3 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d2s3.grid(row=3, column=3, padx=5)

d3s1 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d3s1.grid(row=4, column=1, padx=5)
d3s2 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d3s2.grid(row=4, column=2, padx=5)
d3s3 = CTkLabel(master=get_ping_frame, text="", image=red_cross_img)
d3s3.grid(row=4, column=3, padx=5)

test_dns_buttons_frame = CTkFrame(master=get_ping_frame, fg_color="transparent", corner_radius=0)
test_dns_buttons_frame.columnconfigure(0, weight=1)
test_dns_buttons_frame.columnconfigure(0, weight=1)

actual_get_ping_btn = CTkButton(master=test_dns_buttons_frame,
                                fg_color="#F3D300",
                                hover_color="#796900",
                                text_color="#242424",
                                text="Start Testing",
                                command=MultiT)
actual_get_ping_btn.grid(row=0, column=0, padx=(0, 20))

go_to_custom_url_test_btn = CTkButton(master=test_dns_buttons_frame,
                                      fg_color="#F3D300",
                                      hover_color="#796900",
                                      text_color="#242424",
                                      text="Custom URL",
                                      command=go_to_custom_url)
go_to_custom_url_test_btn.grid(row=0, column=1)

test_dns_buttons_frame.grid(row=5, columnspan=6, pady=(30, 0))


# The flag indicating if the waiting process (showing gif) is already started or not
# Prevent the application to show two waiting gif at the same time
get_ping_wait_flag = True


# </editor-fold>

# <editor-fold desc="custom_url_test_frame">

custom_url_test_frame = CTkFrame(master=app, fg_color="transparent", corner_radius=0)
custom_url_test_frame.columnconfigure(0, weight=1)
custom_url_test_frame.rowconfigure(3, weight=1)

go_to_get_ping_from_custom_url_btn = CTkButton(master=custom_url_test_frame,
                                               height=50, width=50, image=arrow_img,
                                               corner_radius=20, text="", fg_color="transparent",
                                               command=go_to_get_ping_from_custom_url,
                                               hover_color=icon_button_hover_color)
go_to_get_ping_from_custom_url_btn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

custom_url_text_box_frame = CTkFrame(master=custom_url_test_frame, fg_color="transparent", corner_radius=0)
custom_url_text_box_frame.columnconfigure(0, weight=1)

custom_url_text_box_label = CTkLabel(master=custom_url_text_box_frame, text="URL:")
custom_url_text_box_label.grid(row=0, column=0, sticky=W)

custom_url_text_box = CTkEntry(master=custom_url_text_box_frame, placeholder_text="https://...", height=45)
custom_url_text_box.grid(row=1, column=0, sticky=W+E)

custom_url_text_box_frame.grid(row=1, column=0, sticky=W+E, padx=10, pady=(20, 0))


biggest_frame = CTkFrame(master=custom_url_test_frame, fg_color="transparent", corner_radius=0)
middle_big_frame = CTkFrame(master=biggest_frame, fg_color="transparent", corner_radius=0)

middle_big_frame.rowconfigure(0, weight=1)
middle_big_frame.columnconfigure(0, weight=1)
middle_big_frame.columnconfigure(1, weight=1)
middle_big_frame.columnconfigure(2, weight=1)

custom_spotify_icon = CTkImage(dark_image=spotify_logo_img_data, light_image=spotify_logo_img_data, size=(50, 50))
custom_anti_pro_icon = CTkImage(dark_image=anti_prohibition_img_data, light_image=anti_prohibition_img_data, size=(50, 50))
custom_temp_dns_icon = CTkImage(dark_image=network_img_data, light_image=network_img_data, size=(50, 50))

# The frame that contains the spotify icon
frame1 = CTkFrame(master=middle_big_frame, fg_color="transparent", corner_radius=0)
frame1.columnconfigure(0, weight=1)
CTkLabel(master=frame1, text="", image=custom_spotify_icon).pack(pady=(0, 25))
spotify_custom_url_success_flag = CTkLabel(master=frame1, text="", image=red_cross_img)
spotify_custom_url_success_flag.pack()
frame1.grid(row=0, column=0)

# The frame that contains the anti-pro icon
frame2 = CTkFrame(master=middle_big_frame, fg_color="transparent", corner_radius=0)
CTkLabel(master=frame2, text="", image=custom_anti_pro_icon).pack(pady=(0, 25))
anti_pro_custom_url_success_flag = CTkLabel(master=frame2, text="", image=red_cross_img)
anti_pro_custom_url_success_flag.pack()
frame2.grid(row=0, column=1, padx=70)

# The frame that contains the temporary DNS icon
frame3 = CTkFrame(master=middle_big_frame, fg_color="transparent", corner_radius=0)
CTkLabel(master=frame3, text="", image=custom_temp_dns_icon).pack(pady=(0, 25))
temp_dns_custom_url_success_flag = CTkLabel(master=frame3, text="", image=red_cross_img)
temp_dns_custom_url_success_flag.pack()
frame3.grid(row=0, column=2)

middle_big_frame.pack()
biggest_frame.grid(row=2, column=0, sticky=W+E, padx=10, pady=(40, 0))


actual_custom_url_test_btn = CTkButton(master=custom_url_test_frame,
                                       height=45,
                                       width=210,
                                       fg_color="#F3D300",
                                       hover_color="#796900",
                                       text_color="#242424",
                                       text="Start Testing",
                                       command=start_custom_url_test)
actual_custom_url_test_btn.grid(row=4, column=0, pady=(20, 30))

# The flag indicating if the waiting process (showing gif) is already started or not
# Prevent the application to show two waiting gif at the same time
test_custom_url_wait_flag = True

# </editor-fold>

# <editor-fold desc="apply_custom_dns_frame">

apply_custom_dns_frame = CTkFrame(master=app, fg_color="transparent", corner_radius=0)

apply_custom_dns_frame.columnconfigure(0, weight=1)

go_to_other_services_page_from_apply_custom_dns_btn = CTkButton(master=apply_custom_dns_frame,
                                                                height=50, width=50, image=arrow_img,
                                                                corner_radius=20, text="", fg_color="transparent",
                                                                command=go_to_other_services_page_from_apply_custom_dns,
                                                                hover_color=icon_button_hover_color)
go_to_other_services_page_from_apply_custom_dns_btn.grid(row=0, column=0, sticky=W, padx=10, pady=10)

preferred_dns_label_frame = CTkFrame(master=apply_custom_dns_frame, fg_color="transparent", corner_radius=0)
preferred_dns_label = CTkLabel(master=preferred_dns_label_frame,
                               text="Preferred DNS",
                               font=("Arial Bold", 18))
preferred_dns_label.grid(row=0, column=0)
example_preferred_dns_label = CTkLabel(master=preferred_dns_label_frame,
                                       text=" (Example: 1.1.1.1 or 1.0.0.1)",
                                       font=("Arial", 12))
example_preferred_dns_label.grid(row=0, column=1)
preferred_dns_label_frame.grid(row=1, column=0, padx=10, pady=(20, 0), sticky=W)

preferred_dns_text = StringVar()
preferred_dns_text_box = CTkEntry(master=apply_custom_dns_frame, height=40,
                                  textvariable=preferred_dns_text, font=("Arial", 14))
preferred_dns_text_box.grid(row=2, column=0, sticky=W+E, padx=10)

alternate_dns_label = CTkLabel(master=apply_custom_dns_frame,
                               text="Alternate DNS",
                               font=("Arial Bold", 18))
alternate_dns_label.grid(row=3, column=0, padx=10, sticky=W, pady=(20, 0))

alternate_dns_text = StringVar()
alternate_dns_text_box = CTkEntry(master=apply_custom_dns_frame, height=40,
                                  textvariable=alternate_dns_text, font=("Arial", 14))
alternate_dns_text_box.grid(row=4, column=0, sticky=W+E, padx=10)

acd_buttons_frame = CTkFrame(master=apply_custom_dns_frame, fg_color="transparent", corner_radius=0)
acd_buttons_frame.columnconfigure(0, weight=1)
acd_buttons_frame.columnconfigure(1, weight=1)

actual_apply_custom_dns_btn = CTkButton(master=acd_buttons_frame,
                                        fg_color="#F3D300",
                                        hover_color="#796900",
                                        text_color="#242424",
                                        text="Apply DNS",
                                        command=lambda: SetCustomDNS(preferred_dns_text_box.get(),
                                                                     alternate_dns_text_box.get()))
actual_apply_custom_dns_btn.grid(row=0, column=0, sticky=W + E, padx=10)

get_custom_dns_ping_btn = CTkButton(master=acd_buttons_frame,
                                    text="Get ping",
                                    fg_color="#F3D300",
                                    hover_color="#796900",
                                    text_color="#242424",
                                    command=lambda: threading.Thread(Get_Ping(preferred_dns_text_box.get(),
                                                                              alternate_dns_text_box.get())).start())
get_custom_dns_ping_btn.grid(row=0, column=1, sticky=W + E, padx=10)

acd_buttons_frame.grid(row=5, column=0, pady=(50, 0))

apply_custom_dns_frame.rowconfigure(6, weight=1)

# The button to save the custom DNS
save_dns = CTkButton(master=acd_buttons_frame, text="Save Custom DNS",font=("Arial", 14),
                                    fg_color="#F3D300",
                                    hover_color="#796900",
                                    text_color="#242424",
                                    command=lambda: [save_custom_dns(preferred_dns_text_box.get(),
                                                                              alternate_dns_text_box.get()), get_custom_dns()])

save_dns.grid(row=1, column=0, sticky=W + E, padx=10, pady = 20)

# The option menu so user can choose which DNS they want
chosen_option = StringVar()
fontt = None
if app_language == "persian":
    chosen_option.set("انتخاب کنید")
    fontt = ("Arial Bold", 14)
else:
    chosen_option.set("Select a DNS")
    fontt = ("Arial", 14)

option_menu = CTkOptionMenu(master=acd_buttons_frame,font=fontt,
                                    fg_color="#F3D300",
                                    text_color="#242424",
                                    values=items_list,
                                    button_color="#F3D300",
                                    button_hover_color="#796900",
                                    variable=chosen_option,
                                    anchor=CENTER,
                                    dropdown_fg_color="#CCB204",
                                    dropdown_hover_color="#796900",
                                    dropdown_text_color="#242424",
                                    dropdown_font=("Arial", 14),
                                    command=call_back)

option_menu.grid(row=1, column=1, sticky=W + E, padx=10, pady = 20)


custom_log_frame = CTkFrame(master=apply_custom_dns_frame, fg_color="transparent")
custom_log_frame.rowconfigure(1, weight=1)
custom_log_frame.columnconfigure(0, weight=1)

custom_app_log_text_box_frame = CTkFrame(master=custom_log_frame, width=380, border_width=2, fg_color="transparent")

custom_app_log_text_box_frame.rowconfigure(0, weight=1)
custom_app_log_text_box_frame.columnconfigure(0, weight=1)

custom_app_log_text_box = CTkLabel(master=custom_app_log_text_box_frame, font=("Arial", 14),
                                   text='',
                                   width=380, height=100,
                                   corner_radius=99,
                                   fg_color="transparent",
                                   wraplength=280,
                                   justify=CENTER)
custom_app_log_text_box.grid(row=0, column=0, sticky=W+E+N+S, pady=(20, 2), padx=2)

custom_app_log_text_box_frame.grid(row=1, column=0, sticky=E+W+N+S, pady=(28, 0))

CTkLabel(master=custom_log_frame, text="", image=app_log_img,
         fg_color="transparent").grid(row=1, column=0, sticky=W+N, padx=(10, 0))

custom_app_log_label = CTkLabel(master=custom_log_frame, font=("Arial", 16),
                                text="App Log", fg_color="transparent")
custom_app_log_label.grid(row=1, column=0, sticky=W+N, padx=(55, 0))

custom_log_frame.grid(row=6, column=0, padx=10, pady=10, sticky=S)

# </editor-fold>

app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

settings_frame.columnconfigure(0, weight=1)
about_us_frame.columnconfigure(0, weight=1)
other_services_frame.columnconfigure(0, weight=1)


def CheckDNS():
    global ignoreflag
    global TemporaryDNS
    if OS == "Windows":
        output = subprocess.getstatusoutput("ping -n 1 " + f"{TemporaryDNS[0]}")[1]
        if output.__contains__("Request timed out"):
            output = subprocess.getstatusoutput("ping -n 1 " + f"{TemporaryDNS[1]}")[1]
            if output.__contains__("Request timed out"):
                ignoreflag = True
            else:
                TemporaryDNS[0] = TemporaryDNS[1]

    elif OS == "Linux":
        output = subprocess.getstatusoutput(f"sudo ping -c 1 {TemporaryDNS[0]}")[1]
        if output.__contains__("0 received"):
            output = subprocess.getstatusoutput(f"sudo ping -c 1 {TemporaryDNS[1]}")[1]
            if output.__contains__("0 received"):
                ignoreflag = True
            else:
                TemporaryDNS[0] = TemporaryDNS[1]


# Set the application theme and language right before the mainloop so all the elements are created


# In the set_app_theme() and set_app_language() method we change some properties of the app elements
# if we do that before all the elements are created we will get error
set_app_theme(app_theme)
set_app_language(app_language)

def opening():
    # Play the gif just before the loading frame is displayed
    app_main_label_animated_gif.play_gif()
    animated_gif.play_gif()
    # Display the loading frame
    loading_frame.grid(row=0, column=0, sticky=W + E + N + S)
    # Load the main page of the application (close the loading page)
    app.after(100, load_actual_application_async)


if terms_of_service == 'False':
    terms_frame.grid(row=0, column=0, sticky=W + E + S + N)

else:
    terms_frame.grid_forget()
    opening()

app.mainloop()
