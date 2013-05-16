import xbmc
import xbmcgui
import xbmcaddon
import time
import os
import random

#root = os.getcwd()
settings = xbmcaddon.Addon(id='script.usb.autoplay')
df = settings.getSetting("defaultfolder")
af = settings.getSetting("advertfolder")
adlimit = float(settings.getSetting("limit"))
retry = True

xbmc.executebuiltin("Notification('Default Folder', '%s')" % df)
time.sleep(3)

while retry:
	try: 
		xbmc.executebuiltin("Notification('%s','blah')" % len(os.listdir(df)))
		time.sleep(3)
		retry = False
	except:
		xbmc.executebuiltin("Notification('Error', 'Default directory not found.')")
		time.sleep(3) 
	
defaultfiles = []
for file in os.listdir(df):
	defaultfiles.append(file)
	
advertfiles = []
for file in os.listdir(af):
	advertfiles.append(file)
	
xbmc.executebuiltin("Notification('%s files found in Default', '%s files found in Adverts')" % (len(defaultfiles),len(advertfiles)))
time.sleep(3)
totalplaytime = 0.0
adplaytime = 0.0
lasttime = time.time()

justdonead = False

def isvideo(fn):
        if fn.endswith("avi"):
                return True
        if fn.endswith("mp4"):
                return True
        if fn.endswith("3gp"):
                return True
        if fn.endswith("flv"):
                return True
        if fn.endswith("mpg"):
                return True
        if fn.endswith("mpeg"):
                return True
        return False

while 1:
	if not xbmc.Player().isPlaying():
		totalplaytime += (time.time() - lasttime)
		#xbmc.executebuiltin("Notification('Total running time','%s')" % totalplaytime)
		xbmc.executebuiltin("Notification('adlimit','%s')" % (adlimit/100.0))
		time.sleep(3)
		if justdonead:
			adplaytime += (time.time() - lasttime)
		lasttime = time.time()
		if adplaytime < (totalplaytime * (adlimit / 100)):
			#xbmc.executebuiltin("Notification('attempting Playing advert','%s')" % adplaytime)
			#time.sleep(5)
			filen = af + advertfiles[random.randint(0,(len(advertfiles)-1))]
			if isvideo(filen):
                                xbmc.executebuiltin("Notification('Playing advert','%s')" % filen)
                                xbmc.executebuiltin("PlayMedia(%s)" % filen)
			justdonead = True
			
		else:
			#xbmc.executebuiltin("Notification('attempting Playing video','%s')" % totalplaytime)
			#time.sleep(5)
			filen = df + defaultfiles[random.randint(0,(len(defaultfiles)-1))]
			if isvideo(filen):
                                xbmc.executebuiltin("Notification('Playing video','%s')" % filen)
                                xbmc.executebuiltin("PlayMedia(%s)" % filen)
			justdonead = False
		time.sleep(5)

	time.sleep(1)
