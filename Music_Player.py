from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

root=tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

statusbar=ttk.Label(root,text="Welcome To Music Player",relief=SUNKEN,font="TImes 12 bold")
statusbar.pack(side=BOTTOM,fill=X)

# Create Menu
menubar=Menu(root)
root.config(menu=menubar)

# Create Submenu
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=submenu)

playlist=[]

def browes_file():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0
    playlist_box.insert(index,filename)
    playlist.insert(index,filename_path)
    index+=1
    

submenu.add_command(label="Open",command=browes_file)
submenu.add_command(label="Exit",command=root.destroy)

def about_app():
    tkinter.messagebox.showinfo("Play Music","This Is Music Player And You Can Play Anything You Want !!!")

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=submenu)
submenu.add_command(label="About App",command=about_app)

mixer.init()

root.title("Play Music")
root.iconbitmap(r"D:\PFP\SahilPatel\Python App And Program\Music Player\MUSIC1.ico")

leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=20)

playlist_box=Listbox(leftframe)
playlist_box.pack(pady=10)

addbtn=ttk.Button(leftframe,text="- ADD",command=browes_file)
addbtn.pack(side=LEFT,pady=10)

def del_song():
    try:
        selected_song=playlist_box.curselection()
        selected_song=int(selected_song[0])
        playlist_box.delete(selected_song)
        playlist.pop(selected_song)
    except:
        tkinter.messagebox.showerror("Select Error","Please Chhose The File You Want To Delete !")

delbtn=ttk.Button(leftframe,text="- DELETE",command=del_song)
delbtn.pack(pady=10)

rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()

lengthlabel=ttk.Label(topframe,text="Total Length : --:--",relief=GROOVE,font="Arial 10 bold")
lengthlabel.pack(pady=10)

crntimelabel=ttk.Label(topframe,text="Current Time : --:--",relief=GROOVE,font="Arial 10 bold")
crntimelabel.pack()

mdlframe=Frame(rightframe)
mdlframe.pack(padx=30,pady=20)

bttmframe=Frame(rightframe)
bttmframe.pack(padx=30,pady=10)

def show_details(play_song):
    file_data=os.path.splitext(play_song)
    if file_data[1] == ".mp3":
        audio=MP3(play_song)  
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length=a.get_length()
    
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    time_format="{:02d} : {:02d}".format(mins,secs)
    lengthlabel["text"]="Total Length"+"  :  "+time_format

    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.setDaemon(True)
    t1.start()

def start_count(t):
    global paused
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(current_time,60)
            mins=round(mins)
            secs=round(secs)
            time_format="{:02d} : {:02d}".format(mins,secs)
            crntimelabel["text"]="Current Time"+"  :  "+time_format
            time.sleep(1)
            current_time=current_time+1
    

def play_music():
    global paused
    global play_it
    if paused:
        mixer.music.unpause()
        statusbar["text"]="Music Resumed"+"  :  "+os.path.basename(play_it)
        paused=False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=playlist_box.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar["text"]="Playing Music"+"  :  "+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("File Not Found","Please Choose The Music File To Play !!")
    
play_photo=PhotoImage(file=r"D:\PFP\SahilPatel\Python App And Program\Music Player\play.png")
play_btn=ttk.Button(mdlframe,image=play_photo,command=play_music)
play_btn.grid(row=0,column=0,padx=5)

def stop_music():
    mixer.music.stop()
    

stop_photo=PhotoImage(file=r"D:\PFP\SahilPatel\Python App And Program\Music Player\stop.png")
stop_btn=ttk.Button(mdlframe,image=stop_photo,command=stop_music)
stop_btn.grid(row=0,column=1,padx=5)

paused=False
def pause_music():
    global paused
    paused=True
    mixer.music.pause()

pause_photo=PhotoImage(file=r"D:\PFP\SahilPatel\Python App And Program\Music Player\pause.png")
pause_btn=ttk.Button(mdlframe,image=pause_photo,command=pause_music)
pause_btn.grid(row=0,column=2,padx=5)

def rewind_music():
    play_music()
    statusbar["text"]="Music Restarted"

rewind_photo=PhotoImage(file=r"D:\PFP\SahilPatel\Python App And Program\Music Player\rewind.png")
rewind_btn=ttk.Button(bttmframe,image=rewind_photo,command=play_music)
rewind_btn.grid(row=0,column=0)

muted=False
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.4)
        sound_btn.config(image=sound_photo)
        scale.set(40)
        muted=False
    else:
        mixer.music.set_volume(0)
        sound_btn.config(image=mute_photo)
        scale.set(0.0)
        muted=True

sound_photo=PhotoImage(file=r"D:\PFP\SahilPatel\Python App And Program\Music Player\volume.png")
mute_photo=PhotoImage(file=r"D:\PFP\SahilPatel\Python App And Program\Music Player\mute.png")
sound_btn=ttk.Button(bttmframe,image=sound_photo,command=mute_music)
sound_btn.grid(row=0,column=1,padx=5)

def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)

scale=ttk.Scale(bttmframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(40)
mixer.music.set_volume(0.4)
scale.grid(row=0,column=2,padx=30)

root.mainloop()