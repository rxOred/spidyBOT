#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from urllib.request import Request, urlopen
import urllib.request, urllib.parse, urllib.error
import re
#from bs4 import BeautifulSoup
import sqlite3
import threading
import time
import sys

class Gui:
    def __init__(self, master, logo):
                
        self.hello = ttk.Label(master, text = "Hello, Im spidyBOT.")
        self.hello.grid(row = 0, column = 0, columnspan = 3)
        self.hello.config(font = ('Courier', 14, 'bold'))
        
        self.hello.config(image = logo)
        self.hello.config(compound = 'top')
#frame1       
        self.frame1 = Frame(master)
        self.frame1.grid(row = 1, column = 0)
        self.frame1.config(height = 70, width = 300)
        self.frame1.config(relief = FLAT)
        self.frame1.config(background = 'yellow')
        
        self.ask_url = ttk.Label(self.frame1, text = "Enter URL")
        self.ask_url.grid(row = 0, column = 0, padx =10, pady = 10)
        
        self.entry = ttk.Entry(self.frame1, width = 30)
        self.entry.grid(row = 0, column = 1)
        
        self.var = IntVar()
        self.checkbutton = ttk.Checkbutton(self.frame1, text = 'Crawl deep')
        self.checkbutton.config(variable = self.var)
        self.checkbutton.grid(row = 0, column = 2)
        
        self.no = IntVar()
        self.scrapbutton = ttk.Checkbutton(self.frame1, text= "Email scraper")
        self.scrapbutton.config(variable = self.no)
        self.scrapbutton.grid(row = 0, column = 3)
        
        self.okButton = ttk.Button(self.frame1, text = 'OK', command = self.okApp)
        self.okButton.grid(row = 0, column = 4) 
#frame2       
        self.frame2 = Frame(master)
        self.frame2.grid(row = 2, column  = 0, columnspan = 3)
        self.frame2.config(height = 70, width = 300, relief = FLAT)
        self.frame2.config(bg = 'yellow')
        
        self.progeressbar = ttk.Progressbar(self.frame2, orient = HORIZONTAL, length = 400)
        self.progeressbar.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.progeressbar.config(mode = 'indeterminate')
        #progress bar here
#frame3       
        self.frame3 = Frame(master)
        self.frame3.grid(row = 3, column  = 0, columnspan = 3, padx = 10, pady = 10)
        self.frame3.config(height = 100, width = 400, relief = FLAT)
    
        self.display_text = Text(self.frame3, width = 50, height= 5)
        self.display_text.grid(row=0, column = 0)
        self.display_text.config(relief = SOLID, wrap = 'word')
        #self.display_text.insert('1.0', 'SpidyBOT, go!')
        
        self.scroll_bar = Scrollbar(self.frame3, orient = VERTICAL, command = self.display_text.yview)
        self.scroll_bar.grid(row = 0, column = 1, sticky = 'ns')
        
        self.display_text.config(yscrollcommand = self.scroll_bar.set)
        
#buttons               
        self.startButton = ttk.Button(master, text = "Start", command = self.startApp)
        self.startButton.grid(row = 5, column = 0)
        self.startButton.config(state=DISABLED)
        
        self.backButton = ttk.Button(master, text = 'Back', command = self.backApp)
        self.backButton.grid(row = 5, column = 1)
        self.exitButton = ttk.Button(master, text = "Exit", command = self.exitApp).grid(row = 5, column = 2)

    def okApp(self):
        
        if len(self.entry.get()) == 0:
            #print("no input")
            self.message = messagebox.showerror(title='No input', message="Enter an url to crawl")
            self.startButton.config(state=DISABLED)
            #self.ErrorLabel = 
        else:
            self.entry.config(state=DISABLED)
            self.checkbutton.config(state=DISABLED)
            self.scrapbutton.config(state=DISABLED)
            self.startButton.config(state=NORMAL)
            self.backButton.config(state=NORMAL)
            self.okButton.config(state=DISABLED)
            
    def startApp(self):
        
        self.progeressbar.start()
        #print('clicked')
    
        self.startButton.config(state=DISABLED)
        self.backButton.config(state=DISABLED)
        self.entry.config(state=DISABLED)
        urllink = self.entry.get()
        
        if self.var.get() == 1 and self.no.get() == 0:
            #print("advance crawler")
            thread_1(urllink)
            #x.start()
        elif self.var.get() == 1 and self.no.get() == 1:
            scrap_Thread(urllink)
        
        elif self.var.get() == 0 and self.no.get() == 1:
            scrapthread(urllink)
        
        elif self.var.get() == 0 and self.no.get() == 0:
            #print('basic crawler')
            thread_2(urllink)
            
        
    def backApp(self):
        
        #print("back")
        self.okButton.config(state=NORMAL)
        self.checkbutton.config(state=NORMAL)
        self.scrapbutton.config(state=NORMAL)
        self.entry.config(state=NORMAL)
        self.startButton.config(state=DISABLED)
        self.backButton.config(state=DISABLED)
        #self.backButton.set
    
    def exitApp(self):
        sys.exit()
  
def email(url):
    try:
        outfile = open("emails.txt", 'a+', encoding='utf-8')
        
        req = Request(url, headers={'User-Agent': 'Mozilla/4.0'})  
        html = urllib.request.urlopen(req).read()
        e = re.findall("\S+@\S+", html.decode())
        
        print(e, file=outfile)
        
        mainapp.display_text.insert('1.0 + 6 lines', "\nFinished.")             
        mainapp.progeressbar.stop()
        mainapp.okButton.config(state=NORMAL)
        mainapp.entry.config(state=NORMAL)
        mainapp.backButton.config(state=NORMAL)
        
    except Exception as a:
        mainapp.display_text.insert('1.0 + 6 lines', "\nAn error occured.") 

def go(url, line, connection_to_datebase):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/4.0'})  
        html = urllib.request.urlopen(req)
        headers = html.info()
        html = html.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        jstags = soup('script')
        
        js = [x.get('src', None) for x in jstags]
        
        #print(type(headers.read()))
        #okkoma js walata mema krnn one
                    
        mainapp.display_text.insert('1.0 + 2 lines', '\ncrawling :' + url)
            
        connection_to_datebase.execute("INSERT INTO URL (Request, HTMLdoc, Headers, Javascript) VALUES (?, ?, ?, ?)", (url , html, str(headers), str(js)))
        connection_to_datebase.commit()
                    
        tags = soup('a')
        
        for eachtag in tags:
            url = eachtag.get('href', None)
            go(url, line+1, connection_to_datebase)
                                 
    except Exception as e:
        mainapp.display_text.insert('1.0 + 2 lines', '\nerror occured with your url.')
        return

def advance_crawler(url):
    
    mainapp.display_text.insert('1.0', 'SpidyBOT, go!')
    mainapp.display_text.insert('1.0 + 2 lines', '\ncreating database...')
    connection_to_datebase = sqlite3.connect('database.db')
    connection_to_datebase.execute('''CREATE TABLE IF NOT EXISTS URL(
        Request       TEXT     NOT NULL,
        HTMLdoc       TEXT     NOT NULL,
        Headers       TEXT     NOT NULL,
        Javascript    TEXT     NOT NULL) ;''')
    mainapp.display_text.insert('1.0 + 2 lines ', 'done.')
    
    go(url ,2, connection_to_datebase)

    #htmltags.close()
    mainapp.display_text.insert('1.0 + 6 lines', "\nFinished.")
    mainapp.display_text.insert('1.0 + 7 lines', '\nsee \'filepath/database.dp\'.')                  
    mainapp.progeressbar.stop()
    mainapp.okButton.config(state=NORMAL)
    mainapp.entry.config(state=NORMAL)
    mainapp.backButton.config(state=NORMAL)
    return

def basic_crawler(url):
    mainapp.display_text.insert('1.0', 'SpidyBOT, go!')
    mainapp.display_text.insert('1.0 + 2 lines', '\ncreating database...')
    connection_to_datebase = sqlite3.connect('database.db')
    connection_to_datebase.execute('''CREATE TABLE IF NOT EXISTS URL(
        Request       TEXT     NOT NULL,
        HTMLdoc       TEXT     NOT NULL) ;''')
    mainapp.display_text.insert('1.0 + 2 lines ', 'done.')
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/4.0'})  
        html = urllib.request.urlopen(req).read()
        
        mainapp.display_text.insert('1.0 + 2 lines', '\ncrawling :' + url)
            
        connection_to_datebase.execute("INSERT INTO URL (Request, HTMLdoc) VALUES (?, ?)", (url , html));
        connection_to_datebase.commit()
        
        htmltags = open("html_tags.txt", 'a+', encoding='utf-8')
            
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('a')
        
        #mainapp.display_text.insert('1.0 + 3 lines', '\ncrawling deep...')
        mainapp.display_text.insert('1.0 + 3 lines', '\nplease wait...')
        
        for eachtag in tags:
            links = eachtag.get('href', None)
            print(links, file=htmltags)
            
            try:
                #mainapp.display_text.insert('1.0 + 2 lines', '\ncrawling :' + links)
                
                reqs = Request(links, headers={'User-Agent': 'Mozilla/4.0'})
                htmls = urllib.request.urlopen(reqs).read()
                        
                connection_to_datebase.execute("INSERT INTO URL (Request, HTMLdoc) VALUES (?, ?)", (links, htmls));
                connection_to_datebase.commit()
                
            except (ValueError, urllib.error.URLError, urllib.error.HTTPError):
                pass
            
        htmltags.close()
        mainapp.display_text.insert('1.0 + 6 lines', "\nFinished.")
        mainapp.display_text.insert('1.0 + 7 lines', '\nsee \'filepath/database.dp\'.')                  
        mainapp.progeressbar.stop()
        mainapp.okButton.config(state=NORMAL)
        mainapp.entry.config(state=NORMAL)
        mainapp.backButton.config(state=NORMAL)
        
    except Exception as e:
        messagebox.errmsg = messagebox.showerror(title="Error", message= e)
        #mainapp.display_text.insert('1.0 + 2 lines', '\nerror occured with main url :' + url +'.')
        #valid url, internet connection 
        mainapp.progeressbar.stop()
        mainapp.okButton.config(state=NORMAL)
        mainapp.entry.config(state=NORMAL)
        mainapp.backButton.config(state=NORMAL)               

def thread_1(url):
    thread = threading.Thread(target=advance_crawler, args=(url,), daemon=True)
    thread.start()
    
def scrap_Thread(url):
    scraper = threading.Thread(target=email, args=(url,), daemon=True) 
    crawl = threading.Thread(target=advance_crawler, args=(url,), daemon=True)
    scraper.start()
    crawl.start()
    
def scrapthread(url):
    scraper = threading.Thread(target=email, args=(url,), daemon=True)
    scraper.start()
    
def thread_2(url):
    thread = threading.Thread(target=basic_crawler, args=(url,), daemon=True)
    thread.start()

#gui top window
root = Tk()
root.resizable(False, False)
root.config(bg = 'yellow')

hading = root.title('-SpidyBOT-')
image = PhotoImage(file = 'spid.png')
mainapp = Gui(root, image)

try:
    from bs4 import BeautifulSoup
except:
    mainapp.errormsg = messagebox.showerror(title = 'Import error', message = "couldnt find bs4. copy and paste bs4 on this directory ")
    exit() 

root.mainloop()
