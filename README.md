Hi! this is a DNS Changer written in Python and the GUI is written with CustomTkinter library; made to help iranians to get through some of the prohibitions!
you can use the source code on both Linux and Windows!
i Tested the program on Linux Mint and windows 11 and it worked just fine.
the program works by using shell commands in subprocess module of python!
for using this DNS Changer on Windows you need to run it as administrator. also dont forget to have internet connection.
on Linux, just run the program as sudo and be connected to an internet.

Linux users should note that:

    everytime the DNS changes, the program restarts your network to apply the changes. so after every change in your DNS, just wait for your internet to get connected again which takes about 1 or 2 seconds depending on your network.
    if you get any error after changing the DNS, it might be due to not having internet connection as i mentioned above! just wait for the connection.
  
on Linux run the program by using the following command in terminal:

in release builds:

    sudo ./Auspicious_DNS_Changer 

while running the source code:

    sudo python3 Auspicious_DNS_Changer.py

dependencies:

  python3
  
  Linux:
  
  debain based distros:
  
    sudo pip install customtkinter
  
    sudo pip install pywin32-ctypes
  
    sudo pip install dnspython
  
    sudo apt-get install python3-tk
    
  arch based distros:
  
    clone the repository of customtkinter and build it
    for other packages just simply use: sudo pip install + <package name>

  Windows:

    pip install customtkinter
  
    pip install pywin32-ctypes
  
    pip install dnspython
  
    pip install tk
