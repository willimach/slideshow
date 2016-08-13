import os, glob,time,random
import tkinter as tk
from PIL import ImageTk
from PIL import Image,ExifTags

from slideshow_lib import *


#Ordner rawbilder
str_raw='/home/pi/sharepi3/slideshow/pics/'
#Ordner Resized Bilder
str_resize='/home/pi/sharepi3/slideshow/resized/'

delay = 2.5
x=480
y=320

os.chdir(str_raw)
#set hat keine Ordnung, lässt sich dadurch einfacher vergleichen
files = set(glob.glob('*.*'))
os.chdir(str_resize)
files_resized = set(glob.glob('*.*'))
os.chdir(str_raw)


resizeflag=False
print(str(len(files_resized))+'/'+str(len(files)))

#Filenamen ohne .ext zum Vergleich
filenames_raw     = set([os.path.splitext(file)[0] for file in files])
filenames_resized = set([os.path.splitext(file)[0] for file in files_resized])
filenames_missing=filenames_raw-filenames_resized


#scale pictures and DELETE original from folder
if len(filenames_raw)!=0:
        print(filenames_raw)
        print('Loading images...',end='\r')
        i=0
        for image in files:
                img = Image.open(image)	
                #print('load '+image + '\t' + str(img.size))
                print('Loading images...'+str(i)+'/'+str(len(files)),end='\r')
                ratio=img.size[0]/img.size[1]
                if ratio < 4/3: #hochformatiger
			#print('HHH')
			#img = img.rotate(90)
                        scale=(y/img.size[1])
                        img = img.resize((int(img.size[0]*scale),y))
                if ratio >= 4/3: #querformatiger
                        scale=(x/img.size[0])
                        img = img.resize((x,int(img.size[1]*scale)))
                img.save(str_resize+str(image)[:-3]+'png','png')	
                os.remove(image)
                i=i+1
        print('Loading complete!')



os.chdir(str_resize)
files_resized = glob.glob('*.*')      
files = glob.glob(str_resize+'*.png')

# create the root window
root = tk.Tk()
root.config(cursor="none")
#Fullsrceen
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# use a button to display the slides
button = tk.Button(root, command=root.destroy)
button.config(width=x,height=y)
button.pack(padx=0, pady=0)

#for image in files:
while 1:
        image=random.choice(files)
        photo = ImageTk.PhotoImage(file=image) 
        root.title(image)
        button["image"] = photo
        root.update()
        time.sleep(delay)
        
# execute the event loop
root.mainloop()
