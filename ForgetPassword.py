# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 21:13:44 2023

@author: Bazla Rashid
"""
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

class ForgetPasswordForm():
    
    def __init__(self, window):
        self.window = window
        self.window.geometry('600x600')
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
        
        #=============== Label=======================================
        self.sign_in_label = Label(self.lgn_frame, text="Reset Password", bg="#040405", fg="white",font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=610, y=100)   

        #=======================username==============================
        self.username_label = Label(self.lgn_frame, text="username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=160)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=205, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=225)

        # ============================password====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=245)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=580, y=290, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=310)

        # ============================confirm password====================================
        self.conf_password_label = Label(self.lgn_frame, text="Confirm Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.conf_password_label.place(x=550, y=325)

        self.conf_password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*")
        self.conf_password_entry.place(x=580, y=360, width=244)

        self.conf_password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.conf_password_line.place(x=550, y=390)    
        
        # ============================Submit button================================
        self.signup = Button(self.lgn_frame, text='Reset', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.change_pass)
        self.signup.place(x=560, y=450) 
        
        self.backtolgn = Button(self.lgn_frame, text='Back', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.destroy)
        self.backtolgn.place(x=560, y=490) 
        
    def destroy(self):
        self.window.destroy() 
        LogIN()
        
    def change_pass(self):
        
        if self.username_entry.get()=='' or self.password_entry.get()=='' or self.conf_password_entry.get()=='':
            messagebox.showerror('Error', 'All Fields Are Required')
        elif self.password_entry.get() != self.conf_password_entry.get():
            messagebox.showerror('Error', 'Password Mismatch')            
        else:
            try:
                con= pymysql.connect(host='localhost',user='root',password='1234')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Connection is not established :( try again)')
                return
            
        query = 'use userdata'
        mycursor.execute(query)            
        query = 'select * from data where username=%s'
        mycursor.execute(query,(self.username_entry.get()))
        row = mycursor.fetchone()
        
        if row == None:
            messagebox.showerror('Error','Incorrect username',parent=self.window)
        else:
            query='update data set password=%s where username=%s'
            mycursor.execute(query,(self.password_entry.get(),self.username_entry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Password is reset, please login with new password', parent=self.window)
            LogIN()   
            
def ForgetPassword():
    ForgetPass_window = Tk()
    ForgetPasswordForm(ForgetPass_window)
    ForgetPass_window.mainloop()

if __name__ == '__main__':
    ForgetPassword()            