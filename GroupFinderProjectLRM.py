#!/usr/bin/env python
# coding: utf-8

# In[15]:


import tkinter as tk
from tkinter import ttk #Just like CSS is used to style an HTML element, we use tkinter. ttk to style tkinter widgets.
from tkinter import messagebox
import tkinter.font as font #used to change the font of components


# In[16]:


class App(tk.Tk):
    # __init__ function for class App
    def __init__(self, *args, **kwargs): 
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, minsize=500)
        container.grid_columnconfigure(0, minsize=800)
  
        # initializing frames to an empty dictionary;
        self.frames = {} #dictionary
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LoginPage,RegisterPage,MainPage):
            #**sent container as the first parameter of other classes(to __init_(constructor)) will be Frame,
            #the self will be sent as 'App';
            frame = F(container, self)
            #initializing frame of that object from LoginPage,RegisterPage,MainPage respectively with for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew") #nsew=north-south-east-west,
            #own-'grid' yerine pack kullanilirsa yalnizca kullanilan component'in alani kadar yer kaplanir.
            #'pack()'' is limited in precision compared to place() and grid() which feature absolute positioning.
        self.show_frame(LoginPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.title("Group Finder")


# In[17]:


#LoginPage which is the first window frame;
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        border=tk.LabelFrame(self,text="Login",bg='ivory',bd=10,font=("Arial",20))
        border.pack(fill="both",expand="yes",padx=100,pady=100)
        
        #Controlling the sent types to LoginPage from tkinterApp class;
        #print(type(self))
        #print(type(parent))
        #print(type(controller))
        
        def login():
            flag=False
            if ((E1.get() == "") or (E2.get() == "")):
                messagebox.showerror("Empty Field", "Please fill both username and password fields")   
            else:
                userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r")
                for userinfo in userInfos:
                    userdatas=userinfo.rstrip('\n').split("-")
                    if(E1.get() == str(userdatas[4])) and (E2.get() == str(userdatas[5])):
                        #L3['text'] = ("Giriş Başarılı...")
                        messagebox.showinfo("Successful Login...", "Welcome to Group Finder")
                        print("Welcome to Group Finder...")
                        flag=True
                        controller.show_frame(MainPage)
                        clearLoginFields()
                        break
            if(flag==False):   
                #L3['text'] = ("Please register at first if you do not have an account!")
                messagebox.showerror("Non Exist User Info", "Please register at first if you do not have an account") 
        
        ##To set the entry field items later(to clear them etc.) after successful operation(Login);
        entry_text1=tk.StringVar()
        entry_text2=tk.StringVar()
        
        L1 = ttk.Label(border, text ="Username")
        L1.place(x=50, y=20)
        
        E1 = ttk.Entry(border, width=25,textvariable=entry_text1)
        #The Entry widget is used to display a single-line text field for accepting values from a user.
        E1.place(x=120,y=20)

        L2 = ttk.Label(border, text ="Password")
        #The Label widget is used to provide a single-line caption for other widgets. It can also contain images.
        L2.place(x=50, y=50)

        E2 = ttk.Entry(border,show='*', width=25,textvariable=entry_text2)
        E2.place(x=120, y=50)

        btnLogin = ttk.Button(border, text="Login",command=login) #own=>padx ve pady ile butonun x ve y duzlemindeki boyutu veriliyor.
        #bt.grid(row = 0, column = 1, padx = 20, pady = 5)
        btnLogin.place(x=50,y=100)

        #window.mainloop() #The method mainloop plays a vital role in Tkinter as it is a core application that waits for events and helps in updating 
        #the GUI or in simple terms, we can say it is event-driven programming. If no mainloop() is used then nothing will 
        #appear on the window Screen.
  
        btnRegister = ttk.Button(border, text ="Register/Signup", command = lambda : controller.show_frame(RegisterPage))
        # putting the button in its place by using grid
        #btnRegister.grid(row = 1, column = 1, padx = 10, pady = 10)
        btnRegister.place(x=150,y=100)
        entryText = tk.StringVar()

        def clearLoginFields():
            entry_text1.set("")
            entry_text2.set("")
        
        #clearLoginFields() #clear the fields when Login Page is opened -> calismiyor su an!!!!!


# In[18]:


#RegisterPage which is the second window frame;
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        
        border=tk.LabelFrame(self,text="Sign Up",bg='ivory',bd=10,font=("Arial",20))
        border.pack(fill="both",expand="yes",padx=100,pady=100)
        
        def register():
            flag=False
            if ((E1.get() == "") or (E2.get() == "") or (E3.get() == "") or (E4.get() == "") or (E5.get() == "")):
                messagebox.showerror("Empty Field", "All fields are required to be filled to register!")   
            else:
                userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r")
                users = userInfos.readlines() #returns a list containing each line in the file as a list item.
                userInfos.close()
                id=int(users[-1].split("-")[0]) #last user's id in the file is be taken to be incremented by 1 for the next registered user to file and
                #it is converted to int to be used for calculation
                
                #Opening the file again for appending after registration;
                userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "a")
                registeredUserInfo = str(id+1) + "-" + E1.get() + "-" + E2.get() + "-" + E3.get() + "-" + E4.get() + "-" + E5.get()
                userInfos.write(registeredUserInfo + '\n')
                userInfos.close()
                flag=True
            if(flag==True):
                messagebox.showinfo("Successful Registration...", "You succesfully signed up to Group Finder...")
                clearSignupFields()
    
        #To set the entry field items later(to clear them etc.) after successful operation(Registration);
        entry_text1=tk.StringVar()
        entry_text2=tk.StringVar()
        entry_text3=tk.StringVar()
        entry_text4=tk.StringVar()
        entry_text5=tk.StringVar()
                
        L1 = ttk.Label(border,width=15,text ="Name")
        L1.place(x=50, y=20)
        
        E1 = ttk.Entry(border,width=25,textvariable=entry_text1)
        E1.place(x=150,y=20)
        
        L2 = ttk.Label(border,width=15,text ="Surname")
        L2.place(x=50, y=50)
        
        E2 = ttk.Entry(border, width=25,textvariable=entry_text2)
        E2.place(x=150,y=50)
        
        L3 = ttk.Label(border,width=15,text ="School Number")
        L3.place(x=50, y=80)

        E3 = ttk.Entry(border, width=25,textvariable=entry_text3)
        E3.place(x=150,y=80)
        
        L4 = ttk.Label(border,width=15,text ="Username")
        L4.place(x=50, y=110)

        E4 = ttk.Entry(border,width=25,textvariable=entry_text4)
        E4.place(x=150, y=110)

        L5 = ttk.Label(border,width=15,text ="Password")
        L5.place(x=50, y=140)

        E5 = ttk.Entry(border,show='*', width=25,textvariable=entry_text5)
        E5.place(x=150, y=140)

        btnLogin = ttk.Button(border, text="Login",command = lambda : controller.show_frame(LoginPage))
        btnLogin.place(x=50,y=170)

        btnSubmit = ttk.Button(border,text ="Submit",command = register)
        btnSubmit.place(x=150,y=170)

        def clearSignupFields():
            entry_text1.set("")
            entry_text2.set("")
            entry_text3.set("")
            entry_text4.set("")
            entry_text5.set("")


# In[19]:


#MainPage which includes the buttons to redirect the user to the related pages with respect to user choice;
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        border=tk.LabelFrame(self,text="Main Page",bg='#1577E8',fg='#FFFFFF',bd=20,font=("Arial",20)) #bd used for width of frame
        border.pack(fill="both",expand="yes",padx=100,pady=100)
        
        button_font = font.Font(family='Helvetica') #to change the font of Buttons
        
        btnCheckGroups = tk.Button(border,text="Check Active Groups",bg='#FFFFFF',command = "")
        btnCheckGroups.place(x=120,y=20)
        btnCheckGroups.config(height=2,width=35)
        btnCheckGroups['font'] = button_font #to change the font of Buttons
  
        btnSetGroup = tk.Button(border, text ="Set Up A Group",bg='#FFFFFF',command = "")
        btnSetGroup.place(x=120,y=90)
        btnSetGroup.config(height=2,width=35)
        btnSetGroup['font'] = button_font
        
        btnShowProfile = tk.Button(border, text ="Show My Profile",bg='#FFFFFF',command = "")
        btnShowProfile.place(x=120,y=160)
        btnShowProfile.config(height=2,width=35)
        btnShowProfile['font'] = button_font


# In[20]:


app = App()
app.maxsize(800,500)
app.mainloop()


# In[ ]:




