import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import json
import requests
import subprocess
import os
import time
import pyperclip as pyp

bwd = os.getcwd()
        
def newbot(name):
    os.makedirs(name)
    wd = os.getcwd() + f"/{name}"
    os.chdir(wd)
    variables_file = open("variables.json", "w")
    variables_file.write("{}")
    variables_file.close()
    config_file = open("config.json", "w")
    config_file.write('{"token":"", "prefix":"!", "ownerid":"0"}')
    config_file.close()
    with open("config.json", "r") as config_file:
        global config
        config = json.loads(config_file.read())
    cmdsinfo_file = open("cmdsinfo.json", "w")
    cmdsinfo_file.write('{}')
    cmdsinfo_file.close()
    with open("cmdsinfo.json", "r+") as cmdsinfo_file:
        global cmdsinfo
        cmdsinfo = json.loads(cmdsinfo_file.read())

def editbot(name):
    os.chdir(os.getcwd() + f"/{name}")
    with open("config.json", "r") as config_file:
        global config
        config = json.loads(config_file.read())
    with open("cmdsinfo.json", "r+") as cmdsinfo_file:
        global cmdsinfo
        cmdsinfo = json.loads(cmdsinfo_file.read())
    
LARGE_FONT= ("Verdana", 12)

global iscmdedit
iscmdedit = False

def editjson(file, key, value):
    with open(file + ".json", "r+") as openedfile:
        data = json.loads(openedfile.read())
        data[key] = value
        openedfile.seek(0)
        json.dump(data, openedfile)
        openedfile.close()


                                                                    ############
                                                                    ### MAIN ###
                                                                    ############

         
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, BotEditor, OptionsPage, CommandEditor):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        menubar = frame.menubar()
        self.configure(menu=menubar)

        if str(frame).endswith('startpage'):
            os.chdir(bwd)


                                                                    #################
                                                                    ### HOME PAGE ###
                                                                    #################

def copy(data):
    pyp.copy(data)
    pyp.paste()
def popup(text,typ):
    pop = tk.Tk()
    pop.title("Popup")
    pop.resizable(width=False, height=False)
    pop.geometry("200x100")
    if typ == "text":
        lbl = tk.Label(pop, text=text)
        lbl.pack()
        btn = tk.Button(pop, text="Ok",command= lambda: pop.destroy())
        btn.pack()
    if typ == "link":
        lbl = tk.Label(pop, text=text)
        lbl.pack()
        btn = tk.Button(pop, text="Ok",command= lambda: pop.destroy())
        btn.pack()
        btn = tk.Button(pop, text="Copy",command= lambda: copy(text))
        btn.pack()
    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        controller.title("Python Discord Bot Creator")
        controller.geometry("700x500")
        
        tk.Label(self, text="Strona główna", font=LARGE_FONT).grid(row=0, column=0)

        tk.Label(self, text="Nazwa: ").grid(row=1, column=0, pady=30)
        self.ent_botname = tk.Entry(self)
        self.ent_botname.grid(row=1, column=1)
        btn_editbot = tk.Button(self, text="Edytuj Bota", command=lambda: clseditbot(self, controller))
        btn_editbot.grid(row=1, column=2, padx=20)
        btn_newbot = tk.Button(self, text="Nowy bot", command=lambda: clsnewbot(self, controller))
        btn_newbot.grid(row=1, column=3, padx=20)

        btn_options = tk.Button(self, text="Ustawienia", command=lambda: controller.show_frame(OptionsPage))
        btn_options.grid(row=2, column=0, pady=30)

        tk.Label(self, text="0.0.2").grid(row=5, pady=50)
        
        def clsnewbot(self, controller):
            StartPage.name = self.ent_botname.get()
            if StartPage.name != "":
                bots = os.listdir(os.getcwd())
                if StartPage.name not in bots:
                    newbot(StartPage.name)
                    controller.show_frame(BotEditor)
                else:
                    messagebox.showerror("Błąd", "Taki bot już istnieje")
            else:
                messagebox.showerror("Błąd", "Nazwa bota nie może być pusta")

        def clseditbot(self, controller):
            StartPage.name = self.ent_botname.get()
            if StartPage.name != "":
                bots = os.listdir(os.getcwd())
                if StartPage.name in bots:
                    editbot(StartPage.name)
                    controller.show_frame(BotEditor)
                else:
                    messagebox.showerror("Błąd", "Taki bot nie istnieje")
            else:
                messagebox.showerror("Błąd", "Nazwa bota nie może być pusta")

    def menubar(self):
        self.menu = tk.Menu(self) 
        cascade = tk.Menu(self.menu)
        self.menu.add_cascade(label="Program", menu = cascade)        
        cascade.add_command(label = "Developer", command=lambda: popup("Montarex23#6909 + Nimplex#6232", "text"))
        cascade.add_command(label = "Discord server", command=lambda: popup("https://discord.gg/NKumSM4", "link"))
        return self.menu


                                                                    ##################
                                                                    ### BOT EDITOR ###
                                                                    ##################


class BotEditor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Bot", font=LARGE_FONT).grid(row=0, column=1)

        try:
            i = 0
            for file in os.listdir(os.getcwd()):
                if str(file).endswith('.py'):
                    i = i + 1
        except:
            nothing = 1

        BotEditor.edit = False
        BotEditor.cmdname = "none"

        self.lb_icmd = tk.Label(self)
        self.lb_icmd.grid(row=1)
        self.lb_icmd.configure(text="Ładowanie...")

        tk.Label(self, text="-" * 120).grid(row=2, column=0, columnspan=4)

        label2 = tk.Label(self, text="Token: ").grid(row=3, column=0)
        self.ent_token = tk.Entry(self, show="*", width=50)
        self.ent_token.grid(row=3, column=1)
        #btn_tokenhelp = tk.Button(self, text="?", command=lambda: messagebox.showinfo("a", "b"), width=3).grid(row=3, column=2)
        label3 = tk.Label(self, text="Prefix: ").grid(row=4, column=0)
        self.ent_prefix = tk.Entry(self, width=15)
        self.ent_prefix.grid(row=4, column=1)
        self.ent_prefix.delete(0,"end")

        try:
            self.ent_prefix.insert(0,config["prefix"])
        except:
            self.ent_prefix.insert(0,"Ładowanie...")
        lb_ownerid = tk.Label(self, text="ID Właściciela: ").grid(row=5, column=0)
        self.ent_ownerid = tk.Entry(self, width=30)
        self.ent_ownerid.grid(row=5, column=1)
        self.ent_ownerid.delete(0,"end")
        try:
            self.ent_ownerid.insert(0,config["ownerid"])
        except:
            self.ent_prefix.insert(0,"Ładowanie...")
        btn_save = tk.Button(self, text="Zapisz", command=lambda: self.save_config(), width=10).grid(row=6)

        tk.Label(self, text="-" * 120).grid(row=7, column=0, columnspan=4)

        tk.Label(self, text="Nazwa komendy do edytowania: ").grid(row=8, column=0)
        self.ent_cmdtoedit = tk.Entry(self, width=40)
        self.ent_cmdtoedit.grid(row=8, column=1)
        tk.Button(self, text="Edytuj komende", command=lambda: editcmd(self, controller, self.ent_cmdtoedit.get())).grid(row=8,column=2)

        btn_newcmd = tk.Button(self, text="Nowa komenda", command=lambda: controller.show_frame(CommandEditor)).grid(row=9,pady=10)

        tk.Label(self, text="-" * 120).grid(row=10, column=0, columnspan=4)
        
        btn_runbot = tk.Button(self, text="Uruchom bota", command=lambda: runbot(self, StartPage.name)).grid(row=11)

        btn_backtohome = tk.Button(self, text="Wróć do głównej", command=lambda: controller.show_frame(StartPage))
        btn_backtohome.grid(row=12, pady=100)

        self.update_frame()

        def editcmd(self, controller, cmdtoedit):
            global iscmdedit
            iscmdedit = True
            global cmdnameedit
            cmdnameedit = cmdtoedit
            controller.show_frame(CommandEditor)

        def runbot(self, name):
            os.chdir('..')
            open("runbot.txt", "w").write(name)
            subprocess.Popen(["runbot.exe"])
            os.chdir(os.getcwd() + f"/{StartPage.name}")

    def update_frame(self):
        try:
            i = len(cmdsinfo.keys())
        except:
            i = "Ładowanie..."
        self.lb_icmd.configure(text=f"Komendy: {i}")
        self.lb_icmd.after(1000, self.update_frame)
        global repeat
        try:
            if repeat == True:
                nothing = 2
        except:
            repeat = True
        if repeat == True:
            self.ent_prefix.delete(0,"end")
            try:
                self.ent_prefix.insert(0,config["prefix"])
                repeat = False
            except Exception as e:
                self.ent_prefix.insert(0,"Ładowanie...")

            self.ent_ownerid.delete(0,"end")
            try:
                self.ent_ownerid.insert(0,config["ownerid"])
                repeat = False
            except Exception as e:
                self.ent_ownerid.insert(0,"Ładowanie...")

    def save_config(self):
        if self.ent_token.get() != "":
            editjson("config", "token", self.ent_token.get())
        if self.ent_prefix.get() != "":
            editjson("config", "prefix", self.ent_prefix.get())
        if self.ent_ownerid.get() != "":
            editjson("config", "ownerid", self.ent_ownerid.get())

    def menubar(self):
        self.menu = tk.Menu(self) 
        cmdsmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Komendy", menu = cmdsmenu)
        for key in cmdsinfo.keys():
            cmdsmenu.add_command(label = str(key).split('.')[0], command=lambda: print("xD"))
        return self.menu


                                                                    ####################
                                                                    ### OPTIONS PAGE ###
                                                                    ####################

class OptionsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Ustawienia", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Wróć do głównej", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        rb_var = tk.StringVar()
        rb_male = tk.Radiobutton(self, variable = rb_var, value = "pl", text = "Polski", command=lambda: popup("haha", "text"))

        rb_male.pack()

    def menubar(self):
        self.menu = tk.Menu(self) 
        cascade = tk.Menu(self.menu)
        self.menu.add_cascade(label="Program", menu = cascade)        
        cascade.add_command(label = "Developer", command=lambda: popup("Montarex23#3653", "text"))
        cascade.add_command(label = "Discord server", command=lambda: popup("https://discord.gg/NKumSM4", "link"))  
        return self.menu


                                                                    ######################
                                                                    ### COMMAND EDITOR ###
                                                                    ######################


class CommandEditor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Label(self, text="Edytor komend", font=LARGE_FONT).grid(row=0, column=1)
        tk.Label(self, text="Nazwa komendy").grid(row=1, column=0)
        self.ent_cmdname = tk.Entry(self, width=40)
        self.ent_cmdname.grid(row=3, column=0)

        tk.Label(self, text="Output komendy").grid(row=4, column=0)
        self.tb_output = tk.Text(self, width = 80, height = 30)
        self.tb_output.grid(row=5, column=0)
        
        tk.Label(self, text="* - Opcjonalne Akcje:").grid(row=2, column=2)
        self.treeview = ttk.Treeview(self)
        send = ["Wysyła wiadomośc", "tekst - Tekst wiadomości"]
        createChannel = ["Tworzy kanał", "typ - voice/text", "nazwa - nazwa kanału"]
        script = ["DLA ZAAWANSOWANYCH", "Evaluje linijke","linijka - linijka pythona"]
        deleteMessage = ["Usuwa wiadomość", "msg - usermsg/botmsg/id", "  usermsg - komenda", "  botmsg - ostatnia wiad. bota", "  id - id wiadomości"]
        log = ["Zapisuje dany tekst", "tekst - Tekst"]
        args = ["Argumenty z wiadomości", "arg - numer argumentu", "var - Nazwa zmiennej"] #todo
        status = ["Ustawia status bota", "nazwa - text wyświetlany w statusie bota", "typ - Typ statusu", "watching","playing","listening"]

        
        self.add_values(send, ".send:tekst")
        self.add_values(deleteMessage, ".deleteMessage:msg")
        self.add_values(log, ".log:tekst")
        self.add_values(createChannel, ".createChannel:typ, nazwa")
        #self.add_values(args, ".args:arg = var")
        self.add_values(script, ".script:linijka")
        self.add_values(status, ".status:nazwa, typ")

        self.sb_treeview = tk.Scrollbar(self)
        self.treeview.config(yscrollcommand = self.sb_treeview.set)
        self.sb_treeview.config(command = self.treeview.yview)
        self.sb_treeview.place(in_ = self.treeview, relx = 1., y = 0, relheight = 1.)
        self.treeview.grid(row=3, column=2, rowspan=3)

        btn_create = tk.Button(self, text="Stwórz/edytuj", width=20, command=lambda:createbutton())
        btn_create.grid(row=6, column=1, pady=20)

        btn_back = tk.Button(self, text="Wróć", width=20, command=lambda:controller.show_frame(BotEditor))
        btn_back.grid(row=7, column=1, pady=30)

        def createbutton():
            CommandEditor.create(self, self.ent_cmdname.get(), self.tb_output.get("1.0","end"))
            controller.show_frame(BotEditor)

        self.update_frame()

    def update_frame(self):
        global iscmdedit
        global cmdnameedit
        if iscmdedit == True:
            iscmdedit = False
            self.ent_cmdname.delete(0,"end")
            self.ent_cmdname.insert(0,cmdnameedit)
            self.tb_output.delete(0.1,"end")
            self.tb_output.insert(0.1,cmdsinfo[cmdnameedit])
        self.ent_cmdname.after(1000, self.update_frame)
            

    def add_values(self, values, name):
        value = self.treeview.insert("", 'end', name, text = name)
        for i in values:
            self.treeview.insert(value, 'end', i, text = i)
    def add_items(self, iid, values):
        for i in values:
            self.treeview.insert(iid, 'end', i, text = i, anchor = Tkinter.W)

    def create(self, cmdname, output):
            
        output = output.split('''
''')
        cmdscript = "\n".join(output)
        
        cmdsinfo[cmdname] = cmdscript
        with open("cmdsinfo.json", "w") as cmdsinfo_file:
            json.dump(cmdsinfo, cmdsinfo_file)
            cmdsinfo_file.close()
        
        
    def menubar(self):
        self.menu = tk.Menu(self) 
        cascade = tk.Menu(self.menu)
        self.menu.add_cascade(label="Program", menu = cascade)        
        cascade.add_command(label = "Developer", command=lambda: popup("Montarex23#3653", "text"))
        cascade.add_command(label = "Discord server", command=lambda: popup("https://discord.gg/NKumSM4", "link"))  
        return self.menu


app = Main()
app.mainloop()
