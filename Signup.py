from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
import pymysql
import matplotlib.pyplot as plt
import time
from tkVideoPlayer import TkinterVideo
import datetime
import winsound
from LogIn import LogIN
from Splash import splash
class SignupForm:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1366x768')
        self.window.state('zoomed')
        self.window.resizable(0,0)
        
        # ==================background image=============== 
        self.bg_frame = Image.open('FYP\\17.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image = photo )
        self.bg_panel.image = photo 
        self.bg_panel.pack(fill='both', expand= 'yes')
        
        
        #===================Login Form======================
        self.lgn_frame = Frame(self.window, bg='#040405', width='950', height=600)
        self.lgn_frame.place(x=200, y= 70)
        
        self.txt = 'WELCOME'
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui',25,'bold'), bg='#040405', fg='white')
        self.heading.place(x=80, y=40, width=300, height=40)
        
        #=================== left side image ===================
        self.side_image = Image.open('FYP\\3.jpg')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)
        
        #=======================Sign In Image=======================
        self.sign_in_image = Image.open('FYP\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=50)
    
    
        #=============== Label=======================================
        self.sign_in_label = Label(self.lgn_frame, text="Create An Account", bg="#040405", fg="white",font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=610, y=150)    
        
        #=======================Email==============================
        self.Email_label = Label(self.lgn_frame, text="Email", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.Email_label.place(x=550, y=200)

        self.Email_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"))
        self.Email_entry.place(x=580, y=235, width=270)

        self.Email_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.Email_line.place(x=550, y=259)

        #=======================username==============================
        self.username_label = Label(self.lgn_frame, text="username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=270)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=305, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=325)
        
        # ============================password====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=330)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=580, y=370, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=390)

        # ============================confirm password====================================
        self.conf_password_label = Label(self.lgn_frame, text="Confirm Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.conf_password_label.place(x=550, y=400)

        self.conf_password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*")
        self.conf_password_entry.place(x=580, y=430, width=244)

        self.conf_password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.conf_password_line.place(x=550, y=460)        
        
        # ============================SignIn button================================
        self.signup = Button(self.lgn_frame, text='SIGNUP', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command = self.connect_database)
        self.signup.place(x=560, y=500) 
        # =============================Account label ===============================
        self.Loglabel = Label(self.lgn_frame, text='Already have an account ?', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.Loglabel.place(x=560, y=550)  
        
        #====================Login LInk ================================================
        self.button = Button(self.lgn_frame, text='Log In',font=("yu gothic ui", 9, "bold underline"),
                    relief=FLAT, bg = 'white', cursor='hand2',bd =0, activebackground = 'white', fg='blue', activeforeground='blue', command= self.destroy )
        
        self.button.place(x=750, y=550)
        
    def connect_database(self):
        
        if self.Email_entry.get() =='' or self.username_entry.get() =='' or self.password_entry.get() =='' or self.conf_password_entry.get() =='' :
            messagebox.showerror('Error','All Fields Are Required')
        elif self.password_entry.get() != self.conf_password_entry.get():
            messagebox.showerror('Error', 'Password Mismatch')
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='1234')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
                return
        try:    
            query = 'create database userdata'
            mycursor.execute(query)
            query = 'use userdata'
            mycursor.execute(query)
            query= 'create table data(id int auto_increment primary key not null, email varchar(50), username varchar(100), password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')
        
        query ='select * from data where username=%s'
        mycursor.execute(query,(self.username_entry.get()))
        
        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error','Username Already exists')
        else:
            query = 'insert into data(email, username, password) values(%s, %s, %s)'
            mycursor.execute(query,(self.Email_entry.get(),self.username_entry.get(),self.conf_password_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration is successful')
            self.clear()
            self.destroy()
        
    def clear(self):
        self.Email_entry.delete(0,END)
        self.username_entry.delete(0,END)
        self.password_entry.delete(0,END)
        self.conf_password_entry.delete(0,END)

    def destroy(self):
        self.window.destroy() 
        LogIN()          

def SignUp():
    signup_window = Tk()
    SignupForm(signup_window)
    signup_window.mainloop()            

if __name__ == '__main__':
    splash()
    SignUp() 