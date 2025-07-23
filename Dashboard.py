from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
import pymysql
import matplotlib.pyplot as plt
import time
from tkVideoPlayer import TkinterVideo
import datetime
import winsound
import cv2
from LogIn import LogIN
import threading

class Dashboard():
    def __init__(self, window): 
        #self.username = LoginForm.
        self.window = window
        self.window.title('System Management Dashboard')
        self.window.geometry('1366x768')
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.config(background='#eff5f6')
        self.people_count_list = []
        self.pred = []
        self.conf = [] 
        self.detected_frames = []
        self.available_spots =[]
        self.bg_frame = Image.open('FYP\\pic21.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image = photo )
        self.bg_panel.image = photo 
        self.bg_panel.pack(fill='both', expand= 'No')
    
        # window Icon
        icon = PhotoImage(file='FYP\images\pic-icon.png')
        self.window.iconphoto(True, icon)

        # =====================================================================================
        # ============================ HEADER =================================================
        # =====================================================================================
        #self.logout_text = Button(text='Logout', bg='white', font=("", 13, "bold"), bd=0, fg='black',
        #                          cursor='hand2', activebackground='#32cf8e', command= self.destroy)
        #self.logout_text.place(x=1200, y=15)

        # =====================================================================================
        # ============================ SIDEBAR =================================================
        # =====================================================================================
        back = '#030E18'

        self.sidebar = Frame(self.window, bg=back)
        self.sidebar.place(x=0, y=0, width=300, height=850)


        # =============================================================================
        # ============= BODY ==========================================================
        # =============================================================================

        # ==============================================================================
        # ================== SIDEBAR ===================================================
        # ==============================================================================

        # logo
        self.logoImage = Image.open('FYP\\images\\hyy.png')
        photo = ImageTk.PhotoImage(self.logoImage)
        self.logo = Label(self.sidebar, image=photo, bg=back )
        self.logo.image = photo
        self.logo.place(x=70, y=80)
        
        # Name of brand/person
        
        self.brandName = Label(self.sidebar, text='James Bond', bg=back,fg='white', font=("", 15, "bold"))
        self.brandName.place(x=80, y=200)

        # Settings
        self.settingsImage = Image.open('FYP\\images\\settings-icon.png')
        photo = ImageTk.PhotoImage(self.settingsImage)
        self.settings = Label(self.sidebar, image=photo, bg=back)
        self.settings.image = photo
        self.settings.place(x=35, y=300)

        self.settings_text = Button(self.sidebar, text='Settings',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command = self.setting)
        self.settings_text.place(x=80, y=300)
        

        self.Monior_Activities = Button(self.sidebar, text='Crowd Analytics',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff', command=self.Moniter)
        self.Monior_Activities.place(x=85, y=360)
        
        self.Queue = Button(self.sidebar, text='Queue Management',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.Queue_Management)
        self.Queue.place(x=85, y=420)           
        
        self.parking = Button(self.sidebar, text='Parking Analysis',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.Parking_Windows)
        self.parking.place(x=85, y=480)
        
        self.Heat = Button(self.sidebar, text='Heat Maps',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.HeatMaps)
        self.Heat.place(x=85, y=540) 

        self.Fireandsmoke = Button(self.sidebar, text='Fire&Smoke Detections',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.FireAndSmoke)
        self.Fireandsmoke.place(x=85, y=600)                

        self.Robbery_detections = Button(self.sidebar, text='Robbery_detections',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.Robbery_detections)
        self.Robbery_detections.place(x=85, y=660)                

        self.reports = Button(self.sidebar, text='Report Analytics',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.reports_analysis)
        self.reports.place(x=85, y=720)     

        self.MoniterAll = Button(self.sidebar, text='MoniterAll',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=self.MonitorAll)
        self.MoniterAll.place(x=85, y=765)                         


        root = self.window
        self.intro = Label(root, text="Ace Surveillance",  fg="white",bg="#030625",font=("yu gothic ui", 22, "bold"))
        self.intro.place(x=730, y=100) 
        self.introp = Label(root,text ='''Welcome to ACE Surveillance, the game-changer for the retail industry! Our cutting-edge system brings 
        together the power of crowd analysis,heat mapping, anomaly detection, and parking analysis to revolutionize 
        your retail space. Gain valuable insights into customer behavior, optimize store layouts, enhance security, 
        and simplify parking management—all with ACE Surveillance.Unlock the potential of data-driven decision-making
        and create exceptional experiences for your customers.Join us on this journey of innovation and take your retail
        business to new heights with ACE Surveillance!            
        ''', fg="white",bg="#030625",font=("yu gothic ui", 16, "bold"))
        self.introp.place(x=340, y=150) 
        
        # Exit
        self.exitImage = Image.open('FYP\\images\\exit-icon.png')
        photo = ImageTk.PhotoImage(self.exitImage)
        self.exit = Label(self.sidebar, image=photo, bg=back)
        self.exit.image = photo
        self.exit.place(x=25, y=800)

        self.exit_text = Button(self.sidebar, text='Exit',bg=back,fg='white', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command= self.destroy)
        self.exit_text.place(x=85, y=810)  
        self.stop_threads = False

    def get_text(self):
        self.th_crowd = self.entry.get()
        # print(self.th_crowd)

        self.th_Parking = self.entry_Parking.get()
        # print(self.th_Parking) 

        self.th_queue = self.entry_queue.get()
        # print(self.th_queue) 

        self.th_PNO = self.entry_pNo.get()
        # print(self.th_PNO)
        from crowdAnalytics import display
        display(self.th_crowd, self.th_Parking, self.th_queue, self.th_PNO)
        return self.th_crowd, self.th_Parking, self.th_queue, self.th_PNO
    
      
        
    def setting(self):
        root = self.window
        self.intro.destroy()
        self.introp.destroy()
        self.th = Label(root, text="Enter the maximum capacity of your shop/mall",  fg="white",bg="#030625",font=("yu gothic ui", 22, "bold"))
        self.th.place(x=400, y=150)         
        # Create an Entry widget for the user to type into
        self.entry = Entry(root)
        self.entry.place(x=400,y=200)    
        
        self.th_Parking = Label(root, text="Enter the maximum parking capacity of your shop/mall",  fg="white",bg="#030625",font=("yu gothic ui", 22, "bold"))
        self.th_Parking.place(x=400, y=250)         
        # Create an Entry widget for the user to type into
        self.entry_Parking = Entry(root)
        self.entry_Parking.place(x=400,y=300)

        self.th = Label(root, text="Enter the maximum queue capacity of your shop/mall",  fg="white",bg="#030625",font=("yu gothic ui", 22, "bold"))
        self.th.place(x=400, y=350)         
        # Create an Entry widget for the user to type into
        self.entry_queue = Entry(root)
        self.entry_queue.place(x=400,y=400)           

        self.th_pNo = Label(root, text="Enter your Phone Number for Alerts",  fg="white",bg="#030625",font=("yu gothic ui", 22, "bold"))
        self.th_pNo.place(x=400, y=450)         
        # Create an Entry widget for the user to type into
        self.entry_pNo = Entry(root)
        self.entry_pNo.place(x=400,y=500)
        # Define a function to retrieve the text entered by the user
        # Create a button to submit the text
        self.submit = Button(root, text='Submit',bg="black",fg='white', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff', command = self.get_text) 
        self.submit.place(x=400, y=550)    

        return 
    
    def Moniter(self):
        self.introp.destroy()
        self.introp.destroy()
        root = self.window
        self.mframe = Frame(root, bg='navy')
        self.mframe.place(x=400, y=90, width=1000, height=700)
        # videoplayer = TkinterVideo(master=self.mframe, scaled=True)
        # videoplayer.load(r"FYP/v.mp4")
        # videoplayer.pack(expand=True, fill="both")
        # videoplayer.play() # play the video
        self.th_crowd, self.th_Parking, self.th_queue, self.th_PNO = self.get_text()
        from crowdAnalytics import crowd
        self.people_count_list = crowd(self.mframe,self.th_crowd)
        self.mframe.destroy()

    def MonitorAll(self):
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        self.MAframe = Frame(root, bg='yellow')
        self.MAframe.place(x=400, y=90, width=1000, height=700) 
        from MonitorAll import mainFunc
        self.All = mainFunc(self.MAframe)
        self.All.destroy()  

    def Queue_Management(self):
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        if self.mframe:
            self.mframe.destroy()
        self.qframe = Frame(root)  
        self.qframe.place(x=400, y=90, width=1000, height=700)
        from QueueManag import queue
        self.people_count_list = queue(self.qframe)
        self.qframe.destroy()

    def Parking_Windows(self):
        self.qframe.destroy()
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        self.pframe = Frame(root, bg='green')
        self.pframe.place(x=400, y=90, width=1000, height=700)   
        from ParkingAnalysis import Parking
        self.available_spots  = Parking(self.pframe) 
        root.mainloop()  
        self.pframe.destroy()

    def HeatMaps(self):
        self.pframe.destroy()
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        self.hframe = Frame(root, bg='yellow')
        self.hframe.place(x=400, y=90, width=1000, height=700) 
        from newheatmap import Heatmap
        self.heatmap = Heatmap(self.hframe)
        self.hframe.destroy()

    def FireAndSmoke(self):
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        self.Bframe = Frame(root,bg='black')
        self.Bframe.place(x=400, y=90, width=1000, height=700) 
        from fs import mainFunc
        self.pred, self.conf = mainFunc(self.Bframe)
        self.Bframe.destroy()

    def Robbery_detections(self):
        self.Bframe.destroy()
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        self.Aframe = Frame(root, bg='black')
        self.Aframe.place(x=400, y=90, width=1000, height=700) 
        from Robbery_detection import Robbery
        self.detected_frames = Robbery(self.Aframe) 
        self.Aframe.destroy()

        #self.stop_threads = True
    def reports_analysis(self):
        self.Aframe.destroy()
        self.introp.destroy()
        self.introp.destroy()        
        root = self.window
        self.rframe = Frame(root, bg='black')
        self.rframe.place(x=300, y=80, width=600, height=400)
        from QueueManag import display_previous_plots    
        display_previous_plots(self.people_count_list,self.rframe) 

        from ParkingAnalysis import plot_data
        self.Pkframe = Frame(root, bg='black')
        self.Pkframe.place(x=300, y=480, width=600, height=400)
        plot_data(self.available_spots,self.Pkframe )

        from Robbery_detection import plot_robbery_graph
        self. RBframe = Frame(root, bg='black')
        self.RBframe.place(x=900, y=475, width=600, height=400)
        #plot_robbery_graph(self.detected_frames,self.RBframe )

        from fs import plot_fire
        self.Fsframe = Frame(root,bg='black')
        self.Fsframe.place(x=900, y=80, width=600, height=400)

    def destroy(self):
        self.window.destroy()
        LogIN()


def dashboard():
    window = Tk()
    Dashboard(window)
    window.mainloop()


if __name__ =='__main__':
    plt.show()
    dashboard()