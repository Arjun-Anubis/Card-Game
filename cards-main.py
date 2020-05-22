from random import randint
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from time import *
from pygame import mixer
import threading
import socket
global sel,keep
sel = []
keep = True
global sel2,keep2
sel2 = []
keep2 = True
mixer.init()
mixer.music.load("click.mp3")
global root
root = Tk()
root.title("Player 1")

#root.iconbitmap("./cardy.ico")
root.configure(background = "green")
global bottom_frame
bottom_frame = Frame(root)
bottom_frame.pack(side = BOTTOM)
global top_frame
top_frame = Frame(root)
top_frame.pack(side = TOP)
global mid_frame
mid_frame = Frame(root)
mid_frame.pack(side = BOTTOM)
global right_frame
right_frame = Frame(root)
right_frame.pack(side = LEFT)


image = Image.open("PNG/green_back.png")
image = image.resize((100, 153), Image.ANTIALIAS) ## The (250, 250) is (height, width)
back = ImageTk.PhotoImage(image)


global to_drop
to_drop = False
global pile_save
pile_save = []


global to_send
to_send = False

global win
win = False
class card:
    def __init__(self,suit,value,id):
            self.suit = suit
            self.value = value
            self.id = id


            image = Image.open("PNG/" +str(value) + self.suit[0] + ".png")
            image = image.resize((100, 153), Image.ANTIALIAS)


            self.photo = ImageTk.PhotoImage(image)


deck = []


for i in range(13):
    k = card(suit='Spade',value = i+1,id = i+1001)
    deck.append(k)


for i in range(13):
    k = card(suit='Heart',value = i+1,id = i+2001)
    deck.append(k)


for i in range(13):
    k = card(suit='Diamond',value = i+1,id = i+3001)
    deck.append(k)


for i in range(13):
    k = card(suit='Club',value = i+1,id = i+4001)
    deck.append(k)


def shuffle(deck,length):
    r_list = []
    s_d = []
    while len(s_d) < length:
        a = randint(0,length-1)
        if deck[a] not in s_d:
            s_d.append(deck[a])
            r_list.append(a)
    return s_d,r_list

def pick_d_pile():
    global to_drop
    if not to_drop:
        global user_deck
        user_deck.append(d_pile)

        mixer.music.play()

        global move
        to_drop = True

        mixer.music.play()
        move = "d_pile"

def pick_pile():
    global to_drop,move
    if not to_drop:
        global user_deck,pile,pile_save
        user_deck.append(pile[0])
        mixer.music.play()
        if len(pile) >1:
            pile = pile[1:]
            to_drop= True
            refresh_pile()
            mixer.music.play()
            move = "pile"
            #print(pile_save)
        else:
            pile,_ = shuffle(pile_save[:-1],len(pile_save)-1)
            pile_save = []
            pile = pile[1:]
            to_drop= True
            refresh_pile()
            mixer.music.play()
def drop(item):
    global to_drop
    if to_drop:
        to_drop = False
        global d_pile,pile_save
        d_pile = item
        pile_save.append(item)
        global user_deck,drop_index
        drop_index = user_deck.index(item)
        user_deck.remove(item)
        user_deck = sorted(user_deck,key = get_index)
        refresh()
        mixer.music.play()
        disable()
        global to_send
        to_send = True
def disp(item):
    btn = Button(mid_frame,image = item.photo,bg = "green",command = lambda :drop(item),borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_d(item):
    btn = Button(mid_frame,image = item.photo,bg = "green",command = lambda :select(item),borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_inbframe(item):
    btn = Button(bottom_frame,image = item.photo,bg = "green",command = lambda :drop(item),borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_inbframe_d(item):
    btn = Button(bottom_frame,image = item.photo,bg = "green",command = lambda :select(item),borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_intframe(item):
    btn = Button(top_frame,image = item.photo,bg = "green",command = pick_d_pile,borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_intframe_pile(item):
    btn = Button(top_frame,image = item.photo,bg = "green",borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_back(item):
    btn = Button(top_frame,image = back,bg = "green",command = pick_pile,borderwidth = 0)
    btn.pack(side = LEFT)
    
def disp_inrframe(item):
     btn = Button(bottom_frame,image = item.photo,bg = "red",command = lambda: drop(item),borderwidth = 0)
     btn.pack(side = LEFT)
     
def undisp(item,frame_name):
    lbl = Label(frame_name,image = item.photo,bg = "green",borderwidth = 0)
    lbl.pack(side = LEFT)
    
def undisp_intframe_pile(item):
    lbl = Label(top_frame,image = item.photo,bg = "green",borderwidth = 0)
    lbl.pack(side = LEFT)
   
def undisp_back(item):
    lbl = Label(top_frame,image = back,bg = "green",borderwidth = 0)
    lbl.pack(side = LEFT)
     
def printd(list):
    for item in list:
        if item.value == 1:
            print("A of " + item.suit)
        if 11 > item.value > 1:
            print( str(item.value) + " of " + item.suit)
        if item.value == 11:
            print("J of " + item.suit)
        if item.value == 12:
            print("Q of " + item.suit)
        if item.value == 13:
            print("K of " + item.suit)
def get_index(item):

    return item.id
def refresh():
    global bottom_frame
    global top_frame
    global mid_frame
    global user_deck
    top_frame.destroy()
    mid_frame.destroy()
    bottom_frame.destroy()
    bottom_frame = Frame(root)
    bottom_frame.pack(side = BOTTOM)
    top_frame = Frame(root)
    top_frame.pack(side = TOP)
    mid_frame = Frame(root)
    mid_frame.pack(side = BOTTOM)
    for i in range(7):
        disp(user_deck[i])
    for i in range(6):
        disp_inbframe(user_deck[i+7])
    disp_back(pile[0])
    disp_intframe(d_pile)
def disable():
    global bottom_frame
    global top_frame
    global mid_frame
    global user_deck
    top_frame.destroy()
    mid_frame.destroy()
    bottom_frame.destroy()
    root.configure(background = "green")
    bottom_frame = Frame(root)
    bottom_frame.pack(side = BOTTOM)
    top_frame = Frame(root)
    top_frame.pack(side = TOP)
    mid_frame = Frame(root)
    mid_frame.pack(side = BOTTOM)
    for i in range(7):
        undisp(user_deck[i],mid_frame)
    for i in range(6):
        undisp(user_deck[i+7],bottom_frame)
    undisp_back(pile[0])
    undisp(d_pile,top_frame)
    global to_send
    to_send = True
def refresh_pile():
    global bottom_frame
    global top_frame
    global mid_frame
    top_frame.destroy()
    mid_frame.destroy()
    bottom_frame.destroy()
    root.configure(background = "green")
    bottom_frame = Frame(root)
    bottom_frame.pack(side = BOTTOM)
    top_frame = Frame(root)
    top_frame.pack(side = TOP)
    mid_frame = Frame(root)
    mid_frame.pack(side = BOTTOM)
    right_frame = Frame(root)
    right_frame.pack(side = LEFT)
    for i in range(7):
        disp(user_deck[i])
    for i in range(6):
        disp_inbframe(user_deck[i+7])
    disp_back(pile[0])
    disp_intframe(d_pile)
    disp_inrframe(user_deck[-1])
def set_cards():
    global bottom_frame
    global top_frame
    global mid_frame
    global user_deck
    top_frame.destroy()
    mid_frame.destroy()
    bottom_frame.destroy()
    root.configure(background = "green")
    bottom_frame = Frame(root)
    bottom_frame.pack(side = BOTTOM)
    top_frame = Frame(root)
    top_frame.pack(side = TOP)
    mid_frame = Frame(root)
    mid_frame.pack(side = BOTTOM)
    for i in range(7):
        try:
            disp_d(user_deck[i])
        except:
            pass
    for i in range(6):
        try:
            disp_inbframe_d(user_deck[i+7])
        except:
            pass
def select(item):
    global sel
    sel.append(item)
    set_cards()
def submit(event):
    global sel,keep
    k = 1
    if len(sel) < 2:
        ans = messagebox.showerror("Error","That is incorrect")
        if ans == "ok":
            sel = []
            keep = True
            finish()
    else:
        for item in sel[:-1]:
            a = (item.suit == sel[k].suit)
            b = (sel[k].id == item.id +1 or sel[k].id == item.id - 12)
            c = (item.value == sel[k].value)
            d = (len(sel) >= 3)
            if (a and b and d) or (c and d):
                k += 1 
            else: 
                keep = False
        if keep:
            for item in sel:
                user_deck.remove(item)
            sel = []
            finish()
        else:
            ans = messagebox.showerror("Error","That is incorrect")
            if ans == "ok":
                sel = []
                keep = True
                finish()
def declare_start(event):
    global old_user_deck
    old_user_deck = []
    for item in user_deck:
        old_user_deck.append(item)
    set_cards()
def finish():
    if user_deck == []:
        print("You Win!!")
        global win
        win = True
        root.destroy()
    else:
        set_cards()
def cancel(event):
    global user_deck,btn,btns,top_frame
    user_deck = old_user_deck
    refresh()
    #refresh2()
    disable()
def recv_loop():
    s = socket.socket()
    s.bind(("",8007))
    s.listen(5)
    clientsocket,addr = s.accept()
    while True:
        msg = clientsocket.recv(1024)
        print(msg.decode("utf-8"))
        global d_pile,pile,comp_deck
        temp  = msg.decode("utf-8").split(" ")
        try:
            the_card = card(temp[1],int(temp[2]),int(temp[3]))
        except:
            pass
        if temp[0] == "pile":
            comp_deck.append(the_card)
            pile = pile[1:]
            comp_deck = sorted(comp_deck,key = get_index)
            d_pile = the_card
        elif temp[0] == "d_pile":
            comp_deck.append(d_pile)
            comp_deck.pop(int(temp[4]))
            comp_deck = sorted(comp_deck,key = get_index)
            d_pile = the_card
        elif temp[0] == "won":
            print("sorry you lost,better luck next time")
            root.destroy()
            s.close()
            exit()
        elif temp[0] == 'quit':
            quit()
        refresh()
def send_loop():
    global to_send
    s2 = socket.socket()
    host = socket.gethostname() 
    port = 9519
    s2.bind(("", port))
    s2.listen(5)
    clientsocket, addr = s2.accept()
    print(f'Got connection from{addr}')
    while True:
        if to_send:
            clientsocket.send(bytes(move + " " + d_pile.suit + " " + str(d_pile.value) + " " + str(d_pile.id) + " " + str(drop_index) + " " + str(drop_index),"utf-8"))
            to_send = False
        elif win:
            clientsocket.send(bytes("won","utf-8"))
def listen_for_quit():
    s = socket.socket()
    s.bind(('',3201))
    s.listen(1)
    c,a  =s.accept()
    if c.recv(1024).decode('utf-8') == 'quit':
        os._exit(0)

t1 = threading.Thread(target=recv_loop ,daemon = True)
t2 = threading.Thread(target = send_loop ,daemon = True)
t3 = threading.Thread(target = listen_for_quit ,daemon = True)
t1.start()
t2.start()
t3.start()
root.bind("<Return>",declare_start)
root.bind("<Key-c>",cancel)
root.bind("<Key-s>",submit)


#deck,r_list = shuffle(deck,52)
r_list = range(52)
summ = ''
for item in r_list:
    summ += (str(item) + " ")
m_s = socket.socket()
m_s.bind(("",3580))
m_s.listen(1)
c,a = m_s.accept()
   
c.send(bytes(summ,"utf-8"))
global comp_deck
comp_deck = deck[13:26]
comp_deck = sorted(comp_deck, key = get_index)
global user_deck
user_deck = deck[:13]
user_deck = sorted(user_deck, key = get_index)
global d_pile
d_pile = deck[26]
pile_save.append(d_pile)
global pile
pile = deck[27:]
for i in range(7):
    disp(user_deck[i])
for i in range(6):
    disp_inbframe(user_deck[i+7])
disp_back(pile[0])
disp_intframe(d_pile)   
root.mainloop()
m_s = socket.socket()
m_s.connect(('',3200))
m_s.send(bytes('quit',"utf-8")) 
quit()
quit()