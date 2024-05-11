import os
from customtkinter import *
import dns.resolver
import subprocess
import ctypes
import platform

set_appearance_mode("dark")
OS = platform.system()

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
            return ['1.1.1.1', '8.8.8.8']

def connected_network():
    output = subprocess.getstatusoutput(["sudo nmcli", "dev", "show", "|","grep","DNS"])[1]
    return output.split(' connected to ')[1].split('\n')[0]

if OS == 'Linux':
    subprocess.run(["sudo","nmcli","connection", "modify", connected_network(), "ipv4.ignore-auto-dns", "yes"])

def get_current_dns_servers():
    dnslist = [None]*3
    i = 0
    for temp in get_dns_servers():
        dnslist[i] = temp
        i += 1
    if (not dnslist.__contains__("10.202.10.202") and not dnslist.__contains__("10.202.10.102")) and not dnslist.__contains__("10.202.10.11"):
        if OS == "Windows":
            if dnslist[2] != None:
                Log(logtext, "CURRENT DNS SERVERS:\n" + "DNS1 = " + dnslist[1] + "\nDNS2 = " + dnslist[2])
            else:
                Log(logtext, "CURRENT DNS SERVERS:\n" + "DNS1 = " + dnslist[1] + "\nDNS2 = " + dnslist[0])
        elif OS == 'Linux':
            if dnslist[1] != None:
                Log(logtext, "CURRENT DNS SERVERS:\n" + "DNS1 = " + dnslist[0] + "\nDNS2 = " + dnslist[1])
            else:
                Log(logtext, "CURRENT DNS SERVERS:\n" + "DNS1 = " + dnslist[0])

    elif (dnslist.__contains__("10.202.10.202") and dnslist.__contains__("10.202.10.102")):
        Log(logtext, "ANTI-PROHIBITION DNS IS ACTIVE!")
    elif dnslist.__contains__("10.202.10.11"):
        Log(logtext, "SPOTIFY DNS IS ACTIVE!")

def get_current_dns_servers_ping():
    if OS == "Windows":
        dnslist = [None]*3
        i = 0
        for temp in get_dns_servers():
            dnslist[i] = temp
            i += 1
        output1 = subprocess.getstatusoutput("ping -n 1 " + dnslist[1])[1]
        if dnslist[2] != None:
            output2 = subprocess.getstatusoutput("ping -n 1 " + dnslist[2])[1]
            Log(logtext, "CURRENT DNS PING:\n" + "DNS1 PING = " + output1.split("Average =")[1] + "\nDNS2 PING = " + output2.split("Average =")[1])
        else:
            Log(logtext, "CURRENT DNS PING:\n" + "DNS1 PING = " + output1.split("Average =")[1])
    elif OS == "Linux":
        dnslist = [None]*3
        i = 0
        for temp in get_dns_servers():
            dnslist[i] = temp
            i += 1
        if dnslist[1] != None:
            output1 = subprocess.getstatusoutput('sudo ping -c 1 ' + dnslist[0])[1]
            output2 = subprocess.getstatusoutput('sudo ping -c 1 ' + dnslist[1])[1]
            Log(logtext, "CURRENT DNS PING:\n" + "DNS1 PING = " + output1.split('time=')[1].split('ms')[0] + "\nDNS2 PING = " + output2.split('time=')[1].split('ms')[0])
        else:
            output1 = subprocess.getstatusoutput('sudo ping -c 1 ' + dnslist[0])[1]
            Log(logtext, "CURRENT DNS PING:\n" + "DNS1 PING = " + output1.split('time=')[1].split('ms')[0])

def get_ping(DNS1,DNS2, temp1, temp2):
    if OS == 'Windows':
        status1, output1 = subprocess.getstatusoutput("ping -n 1 " + DNS1)
        status2, output2 = subprocess.getstatusoutput("ping -n 1 " + DNS2)
        if status1 != 1 and status2 != 1:
            temp1.configure(text = "PING =" + output1.split("Average =")[1])
            temp2.configure(text = "PING =" + output2.split("Average =")[1])
    elif OS == 'Linux':
        status1, output1 = subprocess.getstatusoutput("sudo ping -c 1 " + DNS1)
        status2, output2 = subprocess.getstatusoutput("sudo ping -c 1 " + DNS2)
        if status1 != 1 and status2 != 1:
            temp1.configure(text = "PING =" + output1.split('time=')[1].split('ms')[0])
            temp2.configure(text = "PING =" + output2.split('time=')[1].split('ms')[0])

def is_connected_to_network():
    status = subprocess.getstatusoutput("ping -n 1 8.8.8.8")[0]
    if status == 0:
        return True
    return False

def DefaultDNS():
    if OS == 'Windows':
        os.system('netsh interface ip set dnsservers name="Wi-Fi" source=dhcp')
    elif OS == 'Linux':
        subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', '8.8.8.8 1.1.1.1'])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")

    top = CTkToplevel(root)
    top.title("Report")
    top.focus_force()
    top.resizable(False, False)
    top.geometry("400x100")
    labeltemp = CTkLabel(top, text="The Default DNS Has Been Applied!", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    labeltemp.pack()
    buttemp = CTkButton(top, text = "OK", fg_color = "light blue", command = top.destroy, text_color = "black", font = ('Arial', 14), corner_radius = 100)
    buttemp.pack()
    Log(logtext, "APPLIED DEFAULT DNS!")
    SpotifyDNSStatus(label4)
    AntiDNSStatus(label7)

def SetCustomDNS(DNS1, DNS2):
    if OS == 'Windows':
        status1, output1 = subprocess.getstatusoutput("ping -n 1 " + DNS1)
        status2, output2 = subprocess.getstatusoutput("ping -n 1 " + DNS2)
        if  status1 != 1 and status2 != 1:
            os.system('netsh interface ip set dns "WI-FI" static ' + DNS1)
            os.system('netsh interface ip add dns "WI-FI" ' + DNS2 + ' index = 2')
    elif OS == 'Linux':
        temp = DNS1 + " " + DNS2
        subprocess.run(["sudo","nmcli", 'connection', 'modify', connected_network(), 'ipv4.dns', temp])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
    
    top = CTkToplevel(root)
    top.title("Report")
    top.focus_force()
    top.resizable(False, False)
    top.geometry("400x100")
    labeltemp = CTkLabel(top, text="DNS Changed!", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    labeltemp.pack()
    buttemp = CTkButton(top, text = "OK", fg_color = "light blue", command = top.destroy, text_color = "black", font = ('Arial', 14), corner_radius = 100)
    buttemp.pack()
    if OS == 'Windows':
        Log(logtext, "APPLIED CUSTOM DNS!\n DNS1 PING = " + output1.split('Average =')[1] + "\nDNS2 PING = " + output2.split("Average = ")[1])
    elif OS == 'Linux':
        Log(logtext, "APPLIED CUSTOM DNS!")
    else:
        if OS == 'Windows':
            os.system('netsh interface ip set dnsservers name="Wi-Fi" source=dhcp')
        elif OS == 'Linux':
            DefaultDNS()

        top = CTkToplevel(root)
        top.title("Report")
        top.focus_force()
        top.resizable(False, False)
        top.geometry("400x100")
        labeltemp = CTkLabel(top, text="ERROR! THE DEFAULT DNS IS APPLIED!!", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
        Log(logtext, "ERROR! APPLIED DEFAULT DNS!")
        labeltemp.pack()
        buttemp = CTkButton(top, text = "OK", fg_color = "light blue", command = top.destroy, text_color = "black", font = ('Arial', 14), corner_radius = 100)
        buttemp.pack()
    AntiDNSStatus(label7)
    SpotifyDNSStatus(label4)

def SetSpotifyDNS(temp):
    if OS == 'Windows':
        os.system('netsh interface ip set dns "WI-FI" static 10.202.10.11')
        output = subprocess.getstatusoutput("ping -n 1 10.202.10.11")[1]
        print(output)
        Log(logtext, "SPOTIFY DNS ACTIVATED!\n PING = " + output.split('Average =')[1])
    elif OS == 'Linux':
        subprocess.run(["sudo","nmcli", 'con', 'mod', connected_network(), 'ipv4.dns', "10.202.10.11"])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        Log(logtext, "SPOTIFY DNS ACTIVATED!")
    temp.configure(text = "ACTIVE")
    AntiDNSStatus(label7)

def SetAnti(temp):
    if OS == 'Windows':
        os.system('netsh interface ip set dns "WI-FI" static 10.202.10.202')
        os.system('netsh interface ip add dns "WI-FI" 10.202.10.102 index = 2')
        output1 = subprocess.getstatusoutput("ping -n 1 10.202.10.202")[1]
        output2 = subprocess.getstatusoutput("ping -n 1 10.202.10.102")[1]
        Log(logtext, "ANTI-PROHIBITION DNS ACTIVATED!\n DNS1 PING = " + output1.split('Average =')[1] + "\nDNS2 PING = " + output2.split("Average = ")[1])
    if OS == 'Linux':
        subprocess.run(["sudo","nmcli", 'con', 'mod', connected_network(), 'ipv4.dns', '10.202.10.202 10.202.10.102'])
        subprocess.getstatusoutput("sudo nmcli networking off")
        subprocess.getstatusoutput("sudo nmcli networking on")
        Log(logtext, "ANTI-PROHIBITION DNS ACTIVATED!")
    temp.configure(text = "ACTIVE")
    SpotifyDNSStatus(label4)

def AntiDNSStatus(temp):
    temporary = get_dns_servers()
    if not(temporary.__contains__('10.202.10.202') and temporary.__contains__('10.202.10.102')):
        temp.configure(text = "NOT ACTIVE")
    else:
        temp.configure(text = "ACTIVE")

def InitialAntiStatus():
    temp = get_dns_servers()
    if not (temp.__contains__('10.202.10.202') and temp.__contains__('10.202.10.102')):
        return "NOT ACTIVE"
    else:
        if OS == 'Windows':
            output1 = subprocess.getstatusoutput("ping -n 1 10.202.10.202")[1]
            output2 = subprocess.getstatusoutput("ping -n 1 10.202.10.102")[1]
            Log(logtext, "ANTI-PROHIBITION DNS IS ACTIVE!\n DNS1 PING = " + output1.split('Average =')[1] + "\nDNS2 PING = " + output2.split("Average = ")[1])
        elif OS == 'Linux':
            output1 = subprocess.getstatusoutput("sudo ping -c 1 10.202.10.202")[1]
            output2 = subprocess.getstatusoutput("sudo ping -c 1 10.202.10.102")[1]
            Log(logtext, "ANTI-PROHIBITION DNS IS ACTIVE!\n DNS1 PING = " + output1.split('time=')[1].split('ms')[0] + "\nDNS2 PING = " + output2.split('time=')[1].split('ms')[0])
        return "ACTIVE"

def InitialSpotifyStatus():
    if not get_dns_servers().__contains__('10.202.10.11'):
        return "NOT ACTIVE"
    else:
        if OS == 'Windows':
            output = subprocess.getstatusoutput("ping -n 1 10.202.10.11")[1]
            Log(logtext, "SPOTIFY DNS IS ACTIVE!\n PING = " + output.split('Average =')[1])
        elif OS == 'Linux':
            output = subprocess.getstatusoutput("sudo ping -c 1 10.202.10.11")[1]
            Log(logtext, "SPOTIFY DNS IS ACTIVE!\n PING = " + output.split('time=')[1].split('ms')[0])
        return "ACTIVE"

def SpotifyDNSStatus(temp):
    if not get_dns_servers().__contains__('10.202.10.11'):
        temp.configure(text = "NOT ACTIVE")
    else:
        temp.configure(text = "ACTIVE")

def AboutMe():
    top = CTkToplevel(root)
    top.title("About Me")
    top.resizable(False, False)
    top.focus_force()
    top.geometry("600x100")
    labeltemp = CTkLabel(top, text="Telegram ID: @I_AM_AUSPICIOUS\nEMAIL: auspicious818@yahoo.com", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    labeltemp.pack()
    labeltemp1 = CTkLabel(top, text="CONTACT ME IF YOU ENCOUNTERED ANY UNEXPECTED ERROR.\nFEEL FREE TO ASK ANY QUESTION.", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    labeltemp1.pack()
    buttemp = CTkButton(top, text = "CLOSE", fg_color = "light blue", command = top.destroy, text_color = "black", font = ('Arial', 14), corner_radius = 100)
    buttemp.pack()
 
def Log(temp, Text):
    temp.configure(text = Text)

if (OS == 'Windows' and ctypes.windll.shell32.IsUserAnAdmin() and is_connected_to_network()) or OS == 'Linux':
    root = CTk()
    root.geometry('400x600')
    root.resizable(False, False)
    root.title("Auspicious DNS Changer")
    CurrentDNSButton = CTkButton(root, text = "Get Current\nDNS Server", fg_color = "light blue", command = lambda: get_current_dns_servers(), text_color = "black", font = ('Arial', 13), corner_radius = 100, width = 20)
    CurrentDNSButton.place(x = 290, y = 10)
    label1 = CTkLabel(root, text="Auspicious DNS Changer", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    label2 = CTkLabel(root, text="Made by: Auspicious", fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    label3 = CTkLabel(root, text = "Spotify DNS Status:", fg_color = "green", width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    logtext = CTkLabel(root, text = 'Welcome!', width = 40, text_color = "orange", font = ('Arial', 14), corner_radius = 8)
    label4 = CTkLabel(root, text = InitialSpotifyStatus(), fg_color = "green", width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    button1 = CTkButton(root, text = "Start Spotify DNS", fg_color = "light blue", command = lambda: SetSpotifyDNS(label4), text_color = "black", font = ('Arial', 14), corner_radius = 100)
    label1.pack()
    label2.pack()
    button1.pack()
    label3.pack()
    label4.pack()
    pingbutton = CTkButton(root, text = "Get\nPing", fg_color = "light blue", command = lambda: get_ping(str(dnsentry1.get()), str(dnsentry2.get()), ping1label, ping2label), text_color = "black", font = ('Arial', 14), corner_radius = 100, width = 40)
    label7 = CTkLabel(root, text = InitialAntiStatus(), fg_color = "green", width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    button6 = CTkButton(root, text = "Start Anti-Prohibition DNS", fg_color = "light blue", command = lambda: SetAnti(label7), text_color = "black", font = ('Arial', 14), corner_radius = 100)
    button6.pack()
    label6 = CTkLabel(root, text = "Anti-Prohibition DNS Status:", fg_color = "green", width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    label6.pack()
    label7.pack()
    label5 = CTkLabel(root, text = 'Custom DNS:', fg_color = "orange", width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    label5.pack()
    dnsentry1 = CTkEntry(root,fg_color = 'orange', text_color = 'black', font = ('Arial', 14), corner_radius = 8)
    dnsentry1.place(x = 30, y = 280)
    currentpingbutton = CTkButton(root, text = "Get Current\nDNS Ping", fg_color = "light blue", command = lambda: get_current_dns_servers_ping(), text_color = "black", font = ('Arial', 13), corner_radius = 100, width = 20)
    currentpingbutton.place(x = 13, y = 10)
    pingbutton.place(x = 170, y = 270)
    ping1label = CTkLabel(root, text = 'PING = NOT MEASURED', width = 20, text_color = "orange", font = ('Arial', 10), corner_radius = 100)
    ping1label.place(x = 5, y = 251)
    ping2label = CTkLabel(root, text = 'PING = NOT MEASURED', width = 20, text_color = "orange", font = ('Arial', 10), corner_radius = 100)
    ping2label.place(x = 250, y = 251)
    dnsentry2 = CTkEntry(root,fg_color = 'orange', text_color = 'black', font = ('Arial', 14), corner_radius = 8)
    dnsentry2.place(x = 230, y = 280)
    button2 = CTkButton(root, text = "Apply Custom DNS", fg_color = "light blue", command = lambda: SetCustomDNS(str(dnsentry1.get()), str(dnsentry2.get())), text_color = "black", font = ('Arial', 14), corner_radius = 100)
    button2.place(x = 120, y = 320)
    button3 = CTkButton(root, text = "Close the program", fg_color = "light blue", command = root.destroy, text_color = "black", font = ('Arial', 14), corner_radius = 100, width = 150)
    button3.place(x = 120, y = 410)
    button4 = CTkButton(root, text = "Apply Default DNS", fg_color = "light blue", command = lambda:DefaultDNS(), text_color = "black", font = ('Arial', 14), corner_radius = 100, width = 150)
    button4.place(x = 120, y = 350)
    button5 = CTkButton(root, text = "About Me", fg_color = "light blue", command = lambda:AboutMe(), text_color = "black", font = ('Arial', 14), corner_radius = 100, width = 150)
    button5.place(x = 120, y = 380)
    loglabel = CTkLabel(root, text = 'Log:', width = 40, text_color = "orange", font = ('Arial', 14), corner_radius = 8)
    loglabel.place(x = 0, y = 440)
    templabel = CTkLabel(root, text = '-'*100, width = 40, text_color = "orange", font = ('Arial', 14), corner_radius = 0, height = 1)
    templabel.place(x = 0, y = 463)
    logtext.place(x = 0, y = 480)
    root.mainloop()
else:
    root = CTk()
    root.geometry('600x100')
    root.resizable(False, False)
    root.title("No ADS Spotify")
    if not ctypes.windll.shell32.IsUserAnAdmin() and not is_connected_to_network():
        Text = "PROGRAM IS NOT RUNNING AS ADMINISTRATOR!\nPLEASE MAKE SURE YOU RUN THE PROGRAM AS ADMINISTRATOR!\nYOU ARE NOT CONNECTED TO A NETWORK!\nPLEASE MAKE SURE YOU ARE CONNECTED TO A NETWORK!"
    elif not ctypes.windll.shell32.IsUserAnAdmin():
        Text = "PROGRAM IS NOT RUNNING AS ADMINISTRATOR!\nPLEASE MAKE SURE YOU RUN THE PROGRAM AS ADMINISTRATOR!"
    elif not is_connected_to_network():
        Text = "YOU ARE NOT CONNECTED TO A NETWORK!\nPLEASE MAKE SURE YOU ARE CONNECTED TO A NETWORK!"
    labeltemp = CTkLabel(root, text = Text, fg_color = 'orange', width = 40, text_color = "black", font = ('Arial', 14), corner_radius = 8)
    labeltemp.pack()
    buttemp = CTkButton(root, text = "CLOSE", fg_color = "light blue", command = root.destroy, text_color = "black", font = ('Arial', 14), corner_radius = 100)
    buttemp.pack()
    root.mainloop()
