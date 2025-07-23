# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 21:07:15 2023

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

class LoginForm():
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
        
        #=======================Sign In Image=======================
        self.sign_in_image = Image.open('FYP\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)
    
    
        #=============== Label=======================================
        self.sign_in_label = Label(self.lgn_frame, text="LOGIN", bg="#040405", fg="white",font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)        
        
        #=======================username==============================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"))
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        
        # ===== Username icon =========
        self.username_icon = Image.open('FYP\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)  
        
        # ============================login button================================
        self.lgn_button = Image.open('FYP\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.Logged_user_database)
        self.login.place(x=20, y=10)  
        
        #=============================Forgot Password===============================
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT,
                                    activebackground="#040405"
                                    , borderwidth=0, background="#040405", cursor="hand2", command= self.destroy2)
        self.forgot_button.place(x=630, y=510)
        
        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)

        self.signup_img = ImageTk.PhotoImage(file='FYP\\register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#040405", activebackground="#040405" , command= self.destroy)
        self.signup_button_label.place(x=670, y=555, width=111, height=35)        
        
        # ============================password====================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*")
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        
        # ======== Password icon ================
        self.password_icon = Image.open('FYP\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='FYP\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='FYP\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*') 
    def destroy(self):
        self.window.destroy() 
        from Signup import SignUp 
        SignUp()   
    def destroy2(self):
        self.window.destroy() 
        from ForgetPassword import ForgetPassword
        ForgetPassword() 
        
    def Logged_user_database(self):
        if self.username_entry.get()=='' or self.password_entry.get()=='':
            messagebox.showerror('Error', 'All Fields Are Required')
        else:
            try:
                con= pymysql.connect(host='localhost',user='root',password='1234')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Connection is not established :( try again)')
                return
            
        query = 'use userdata'
        mycursor.execute(query)
        query = 'select * from data where username=%s and password=%s'
        mycursor.execute(query,(self.username_entry.get(),self.password_entry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error','Invalid username or password')
        else:
            messagebox.showinfo('Welcome', 'Login is successful')
            self.window.destroy()
            from Dashboard import dashboard
            dashboard()       

def LogIN():
    Login_window = Tk()
    LoginForm(Login_window)
    Login_window.mainloop()
        
if __name__ == '__main__':
    from Splash import splash
    splash()
    LogIN()