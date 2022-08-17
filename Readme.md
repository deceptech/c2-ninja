### About

This is a C2 agent that I found online when attempting to research creating a custom C2 server. Credits go to 0xRick for this, I will be attempting to continue adding new features to make this a more fleshed out tool.

Blog post with very detailed breakdown (does not include any changes I made/make): [https://0xrick.github.io/misc/c2/](https://0xrick.github.io/misc/c2/)

AMSI bypass utilized (Modified By: Shantanu Khandelwal (@shantanukhande), Original Author: Paul Laîné (@am0nsec)) - https://gist.githubusercontent.com/shantanu561993/6483e524dc225a188de04465c8512909/raw/db219421ea911b820e9a484754f03a26fbfb9c27/AMSI_bypass_Reflection.ps1

### How to use

Just clone the repository and install the requirements:

```
git clone https://github.com/deceptech/c2-ninja.git
cd c2-ninja
pip3 install -r requirements.txt
```

Then start the server:

```
./c2.py
```
### New Features

```
August 2022:
'upload' command: Upload file by passing along literal filepath e.g. "upload C:\system.ini" (currently only works when interacting with PowerShell agents). Stored in data/listeners/{listenername}/downloads

Implemented a different AMSI bypass for the PowerShell oneliner. The original one worked for a bit but Defender might have caught on to it by now. Replaced with what I believe is a more reliable bypass (tested against Defender August 17th, 2022) I found from this article - https://systemweakness.com/evade-windows-defender-mimikatz-detection-by-patching-the-amsi-dll-4bd9b3964c03
```
