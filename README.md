# SiraTool v0.1 MRSmokki

Description

A tool has been created, which automates a set of tools that are used to carry out pentesting exercises.
The functions it performs are:

- IPS scanning in the network with the Arp-Scan tool, with subsequent IP selection in a simple way.
- Port scan with Nmap tool on selected IP
- Scanning web vulnerabilities with the Nikto tool
- Scanning of web directories with the Dirsearch tool.
- Generation of a file with a .txt extension with all the information obtained and a mini-analysis of the information with ChatGPT.
- (You can modify the parameters of the tools for each of the needs, modifying the python script)

-----------------------------------------------------------------------------------------------------------------------------------

Steps

Create a folder in which to add the tool and the logs will also be recorded.

Replace line 81 with your api-key where it says <YOUR API KEY>
  
Run the tool with SUDO ex: sudo python3 SiraTool.py
  
-----------------------------------------------------------------------------------------------------------------------------------
