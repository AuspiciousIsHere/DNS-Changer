Hi! this is a DNS Changer written in Python and the GUI is written with CustomTkinter library; made to help iranians to get through some of the prohibitions!
you can use the source code on both Linux and Windows!
i Tested the program on Linux Mint and it worked just fine.
the program works by using shell commands in subprocess module of python!
for using this DNS Changer on Windows you need to run it as administrator. also dont forget to have internet connection.
on Linux just run the program as sudo and be connected to an internet.

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
