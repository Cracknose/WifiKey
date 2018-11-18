from tkinter import *
import subprocess

# "NISSE"

ssids = []
keys = []
tab = "    "


def get_ssid(cmd):
	results = []
	process = subprocess.Popen(cmd,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE)

	for line in process.stdout:
		string = str(line)
		if 'All User Profile' in string:
			edit = string[29:]	# Returns the 30th Char and forward
			edit1 = edit[:-5]  # remove the last 4 chars

			results.append(edit1)
			#results.sort()		# Same thing but maybe dosent sort Caps and Lower alike
			results = sorted(results, key=str.lower)
	
	errcode = process.returncode
	
	if errcode is not None:
		raise Exception('cmd %s failed, see above for details', cmd)

	return results

def get_pass(ssid):		# DENNA FUNKTION ÄR EJ KLAR, check auth open, else clean and set pass,   använd även ssid inputen + pass för RETURN
	cmd = 'netsh wlan show profile name="' + ssid + '" key=clear'
	process = subprocess.Popen(cmd,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE)

	for line in process.stdout:
		string = str(line)
		if "Authentication" and "Open" in string:
			#if "Open" in string:
			keys.append(ssid + " : <OPEN>")

		if "Key Content" in string:
			string = string.replace("b'    Key Content            : ", "")
			string = string[:-5] # GÖR SÅHÄR IST I FUNC ge_ssid
			#print(ssid + " : " + string)
			ssidandkey = ssid + " : " + string
			keys.append(ssidandkey)


def printList(e):
	lst = ['a', 'b', 'c', 'd']  
	for x in lst:
		t.insert(END, x + '\n')
	t.pack()
	
def stopProg(e):
    root.destroy()
    
def transfertext(e):
    #label1.configure(text="Hello World")
    pass
 
def getKeys(e):
	t.delete(1.0,END)
	ssids = get_ssid("netsh wlan show profile")

	for ssid in ssids:
		get_pass(ssid)

	for result in keys:
		t.insert(END,tab+result+'\n')

	t.config(state=DISABLED)
 
### GUI ###
root=Tk()
root.title("  WifiKey")
labelBanner = Label(root, text="\nCrackNose's WifiKey 1.1\n")
labelBanner.pack()
t = Text(root)
t.config(width=60)
t.pack()
button1 = Button(root, text="Run")
button1.pack()
button1.bind('<Button-1>', getKeys)
button2 = Button(root, text="Exit")
button2.pack()
button2.bind('<Button-1>', stopProg)


root.mainloop()