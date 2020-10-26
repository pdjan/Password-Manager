'''
Password Generator application
version: 0.12
author: Predrag Nikolic
online help: github.com/pdjan
date: June 2020

'''

import string
import random
import csv
import shelve
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import Menu

class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent) 

        self.canvas = Canvas(self, borderwidth=0, background="#2E3D52", highlightthickness=0)
        self.viewPort = Frame(self.canvas, background="#2E3D52") 
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview) 
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0,0), window=self.viewPort, anchor="nw", tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)


class TableWidget(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)

        # define widget elements
        # Add two entry widgets
        self.entrypass = ttk.Entry(self, width=15)
        self.entrynote = ttk.Entry(self, width=40)
        

        # add two buttons, delete and copy to clipboard
        self.btndel = Button(self, text="Del", width=5, command=self.delClick)
        self.btndel.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 9))

        self.btncopy = Button(self, text="Copy", width=5, command=self.copyClick)
        self.btncopy.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 9))

        # pack widgets
        self.entrypass.pack(side="left", fill="both")
        self.entrynote.pack(side="left", fill="both")
        self.btndel.pack(side="left", fill="both")
        self.btncopy.pack(side="left", fill="both")

    # add command functions
    def delClick(self):
        # print("del btn clicked")
        self.entrypass.delete(0, END)
        self.entrynote.delete(0, END)
        #! widget is not deleted, only values
        self.destroy()
        # create new empty widget if number of widgets les than 13
        global application
        
        # check number of widgets present
        nowidgets = len(application.scrollFrame.viewPort.winfo_children())
        if nowidgets < 12:
            application.tablew = TableWidget(application.scrollFrame.viewPort)
            application.tablew.pack(side="top")

    def copyClick(self):
        # print("copy btn clicked")
        root.clipboard_clear()
        root.clipboard_append(self.entrypass.get())


class PassGen:
    def __init__(self, master):
       
        # app left frame
        lFrame = Frame(root, bg="#2E3D52")
        lFrame.place(x=0, y=0, width=400, height=400)

        # app name label
        self.lbl = Label(lFrame, text="Password Manager", width=30)
        self.lbl.config(fg="white", bg="#2E3D52", relief="flat", font=("Tahoma", 14))
        self.lbl.place(relx=0.5, rely=0, y=70, anchor=CENTER)
        
        # generate button
        self.gbtn = Button(lFrame, text="Generate", width=15, command = self.gen_pass)
        self.gbtn.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 10))
        self.gbtn.place(relx=0.5, rely=0.5, y=-40, anchor=CENTER)

        # pent - password entry widget in left frame
        self.pent = ttk.Entry(lFrame, justify='center')
        self.pent.place(relx=0.5, rely=0.5, anchor=CENTER)

        # save password button
        self.sbtn = Button(lFrame, text="Use", width=10, command = self.save_pass)
        self.sbtn.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 10))
        self.sbtn.place(relx=0.5, rely=0.5, y=40, anchor=CENTER)

        # save to shelve
        self.stsbtn = Button(lFrame, text="Save", width=10, command = self.save_to_shelve)
        self.stsbtn.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 10))
        self.stsbtn.place(relx=0.5, rely=0.5, x=-120, y=150, anchor=CENTER)

        # update table button
        self.upbtn = Button(lFrame, text="Refresh", width=10, command=self.update)
        self.upbtn.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 10))
        self.upbtn.place(relx=0.5, rely=0.5, y=150, anchor=CENTER)

        # export to csv button
        self.exbtn = Button(lFrame, text="Export", width=10, command=self.exportdata)
        self.exbtn.config(fg="white", bg="#3E8CD0", relief="raised", font=("Tahoma", 10))
        self.exbtn.place(relx=0.5, rely=0.5, x=120, y=150, anchor=CENTER)

        # app right frame for storing passwords
        self.rFrame = Frame(root, borderwidth=0, bg="#2E3D52")
        self.rFrame.place(x=400, y=0, width=600, height=400)
        
        # make scrollFrame
        self.scrollFrame = ScrollFrame(self.rFrame)

        # add 13 TableWidget instances to right Frame or all
        shelve_size = len(self.get_shelve())
        table_size = 12 if shelve_size <= 12 else shelve_size
        
        for j in range(table_size):
            self.tw = TableWidget(self.scrollFrame.viewPort)
            self.scrollFrame.pack(side="top", fill="both", expand=True)
            self.tw.pack(side="top") 

        # add menus
        self.menuBar = Menu(root)
        root.config(menu=self.menuBar)

        # File menu
        self.fileMenu = Menu(self.menuBar)
        self.fileMenu = Menu(self.menuBar, tearoff=0) # removes dashes
        self.menuBar.add_cascade(label="Command", menu=self.fileMenu)

        self.fileMenu.add_command(label="New password", command=self.gen_pass)
        self.fileMenu.add_command(label="Add to manager", command=self.save_pass)
        self.fileMenu.add_command(label="Save all", command=self.save_to_shelve)
        self.fileMenu.add_command(label="Refresh list", command=self.update)
        self.fileMenu.add_command(label="Export to csv", command=self.exportdata)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit program", command=self._quit)

        # Help menu
        self.helpMenu = Menu(self.menuBar, tearoff=0) # 6
        self.helpMenu.add_command(label="Online help", command=self.gohome)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)        
        

        # write data 
        self.update_table_from_shelve()

    def gohome(self):
        # open url when btn is clicked
        webbrowser.open_new(r"https://github.com/pdjan")
        
        
    def gen_pass(self):
        # generate new password
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '!#$%&+,-.=?@_'
        size = 8        
        newpass = ''.join(random.choice(chars) for x in range(size, 20))
        self.pent.delete(0, END)
        self.pent.insert(0, newpass)
      
    def save_pass(self):
        # USE button clicked
        # read entry value
        # if not empty
        pval = self.pent.get()
        done = False # not written in table
        # write to table
        for child in self.scrollFrame.viewPort.winfo_children():
            if child.entrypass.get() == '':
                child.entrypass.insert(0, pval)
                done = True
                break # leave for
        
        # self.update_shelve_from_table() > this saves values as SAVE btn is clicked
        if not done:
            # value not used, create new widget
            self.tw = TableWidget(self.scrollFrame.viewPort)
            self.tw.pack(side="top")
            # enter value to newly created widget
            self.tw.entrypass.insert(0, pval)
        # delete generated value from left frame 
        self.pent.delete(0, END)
        
    def del_all(self):
        # delete all widgets
        for child in self.scrollFrame.viewPort.winfo_children():
            child.entrypass.delete(0, END)
            child.entrynote.delete(0, END)

    def get_table(self):
        # save all non empty value and return list
        v = []
        for child in self.scrollFrame.viewPort.winfo_children():
            passfield = child.entrypass.get()
            notefield = child.entrynote.get()
            # append non empty elements
            if (passfield != '') or (notefield != ''):
                el = [passfield, notefield]
                v.append(el)
        return v

    def get_shelve(self):
        # return shelve values as list
        v = []
        d = shelve.open("datafile", writeback=True)
        for key in d:
            v.append([key,d[key]])
        d.close()
        return v

    def update(self):
        #! should also delete all empty widgets up until 12 of them 
        # save all non empty value
        v = self.get_table()
        # delete table and write v to it
        self.del_all()
        for child in self.scrollFrame.viewPort.winfo_children():
            if len(v)>0:
                el = v.pop(0)
                child.entrypass.insert(0, el[0])
                child.entrynote.insert(0, el[1])
            else:
                break

    def exportdata(self):
        # export table to csv file
        v = self.get_table()
        with open('data.csv', mode='w') as datafile:
            ewriter = csv.writer(datafile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for el in v:
                ewriter.writerow(el)

    def update_shelve_from_table(self):
        # update shelve file
        v = self.get_table()
        d = shelve.open("datafile", writeback=True)
        # first delete shelve
        for key in d:
            del d[key]
        # enter new elements
        for el in v:
            d[el[0]] = el[1]
        d.close()

    def update_table_from_shelve(self):
        v = self.get_shelve()
        if len(v) > 0:
            # datafile is not empty
            self.del_all()
            index = 0
            for child in self.scrollFrame.viewPort.winfo_children():
                child.entrypass.insert(0, v[index][0])
                child.entrynote.insert(0, v[index][1])
                if index < (len(v)-1):
                    index += 1
                else:
                    break

    def save_to_shelve(self):
        self.update()
        self.update_shelve_from_table()
        
    def _quit(self):
        root.quit()
        root.destroy()
        exit()
                        
root = Tk()
root.geometry("1000x400")
root.title("Password Manager")
root.resizable(False, False)
root.config(background="#2E3D52")
application = PassGen(root)
root.mainloop()
