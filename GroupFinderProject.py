#!/usr/bin/env python
# coding: utf-8

# In[40]:


import tkinter as tk
from tkinter import *
from tkinter import ttk #Just like CSS is used to style an HTML element, we use tkinter. ttk to style tkinter widgets.
from tkinter import messagebox
import tkinter.font as font #used to change the font of components


# In[41]:


class MainApp(tk.Tk):
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
        
        self.userid=tk.StringVar()
        #self.userid.set("-")
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LoginPage,RegisterPage,MainPage,ProfilePage,ActiveGroupsPage):
            #**sent container as the first parameter of other classes(to __init_(constructor)) will be Frame,
            #the self will be sent as 'App';
            frame = F(parent=container,controller=self)
            #initializing frame of that object from LoginPage,RegisterPage,MainPage respectively with for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew") #nsew=north-south-east-west,
            #own-'grid' yerine pack kullanilirsa yalnizca kullanilan component'in alani kadar yer kaplanir.
            #'pack()'' is limited in precision compared to place() and grid() which feature absolute positioning.
            
        self.show_frame(LoginPage) #ActiveGroupsPage
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.title("Group Finder")


# In[42]:


##??????????????????????????????
#To get the current logined user's id via inheriting this super class by sub classes,identify all required datas which will be used
#by subclasses(pages) here;
class ParentPage:
    loginedUserId='' #logined user's id which will be used on ProfilePage
    loginedUserFullname=''#fullname of logined user,will be used on ProfilePage
    loginedUserSN=''#school number  of logined user,will be used on ProfilePage


# In[43]:


#LoginPage which is the first window frame;
class LoginPage(tk.Frame,ParentPage): #???class LoginPage(tk.Frame,ParentPage):==>parentpage is given for test purpose
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        border=tk.LabelFrame(self,text="Login",bg='ivory',bd=10,font=("Arial",20))
        border.pack(fill="both",expand="yes",padx=100,pady=100)
        
        #Controlling the sent types to LoginPage from App class;
        #print(type(self))
        #print(type(parent))
        #print(type(controller))
        
        #self.controller=controller
        #self.userid=controller.userid
        
        def login():
            flag=False
            if ((E1.get() == "") or (E2.get() == "")):
                messagebox.showerror("Empty Field", "Please fill both username and password fields")   
            else:
                try:
                    userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r")
                    for userinfo in userInfos:
                        userdatas=userinfo.rstrip('\n').split("-")
                        if(E1.get() == str(userdatas[4])) and (E2.get() == str(userdatas[5])):
                            messagebox.showinfo("Successful Login...", "Welcome to Group Finder")
                            print("Welcome to Group Finder...")
                            flag=True
                            #Logined user's informations are assigned to common properties from inherited super class;
                            ParentPage.loginedUserId=str(userdatas[0]) #logined user's id is taken from file to use it for 
                            #ActiveGroups and UserProfile pages later by passing it(e.g. on MainPage-self.userid);
                            ParentPage.loginedUserFullname=str(userdatas[1])+" "+str(userdatas[2])
                            ParentPage.loginedUserSN=str(userdatas[3])
                            #to control logined user;
                            print("Logined user on Login Page: ",end='')
                            print(ParentPage.loginedUserId,ParentPage.loginedUserFullname,ParentPage.loginedUserSN,sep="-")
                            
                            controller.show_frame(MainPage)
                            clearLoginFields()
                            break
                    userInfos.close()
                except:
                    messagebox.showerror("An error has been occured!", "File error!") 
            if(flag==False):   
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

        btnRegister = ttk.Button(border, text ="Register/Signup", command = lambda : controller.show_frame(RegisterPage))
        # putting the button in its place by using grid
        #btnRegister.grid(row = 1, column = 1, padx = 10, pady = 10)
        btnRegister.place(x=150,y=100)
        entryText = tk.StringVar()

        def clearLoginFields():
            entry_text1.set("")
            entry_text2.set("")


# In[44]:


#RegisterPage which is the second window frame;
class RegisterPage(tk.Frame,ParentPage):
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        
        border=tk.LabelFrame(self,text="Sign Up",bg='ivory',bd=10,font=("Arial",20))
        border.pack(fill="both",expand="yes",padx=100,pady=100)
        
        def register():
            flag=False
            if ((E1.get() == "") or (E2.get() == "") or (E3.get() == "") or (E4.get() == "") or (E5.get() == "")):
                messagebox.showerror("Empty Field", "All fields are required to be filled to register!")   
            else:
                try:
                    if((isUsernameExists()==False) and (isSNExists()==False)):
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
                        flag=True #if there is no duplication,then the flag can be assigned as True and user can register.
                    else:
                        messagebox.showerror("Exist user info!", "The username or/and school number exists...")   
                        #flag will be False
                except:
                    messagebox.showerror("An error has been occured!", "File error!") 
            if(flag==True):
                messagebox.showinfo("Successful Registration...", "You succesfully signed up to Group Finder...")
                clearSignupFields()
                
        
        def isUsernameExists():
            try:
                userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r")
                if(E4.get() in userInfos.read()): #if the file contains the username(duplicate situation)
                    return True #entered username exists,user cannot register
                else:
                    return False #entered username does not exist,user can register
            except:
                messagebox.showerror("An error has been occured!", "File error!") 
                
        
        def isSNExists(): #control school number duplication
            flag=False
            try:
                userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r") 
                for userinfo in userInfos:
                    userdatas=userinfo.rstrip('\n').split("-")
                    if(E3.get() == str(userdatas[3])):
                        flag=True
                        break #if the entered school number already exist, then break the loop to return True
                    else:
                        continue
                userInfos.close()
                return flag
            except:
                messagebox.showerror("An error has been occured!", "File error!") 
            
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


# In[45]:


#MainPage which includes the buttons to redirect the user to the related pages with respect to user choice;
class MainPage(tk.Frame,ParentPage): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller=controller
                        
        self.border=tk.LabelFrame(self,text="Main Page",bg='#1577E8',fg='#FFFFFF',bd=20,font=("Arial",20))
        #bd used for width of frame
        self.border.pack(fill="both",expand="yes",padx=100,pady=100)
        
        ##**For test purpose;
        #This label is used for test purpose to check whether logined user id is fetched or not-will be deleted later;
        #self.userid=tk.StringVar() #it will be assigned when the 
        #lblUserId = tk.Label(self.border,width=15,textvariable=self.userid) #to test whether logined user id is fetched or not
        #lblUserId.place(x=20, y=5)
        
        button_font = font.Font(family='Helvetica') #to change the font of Buttons
        
        btnCheckGroups = tk.Button(self.border,text="Check Active Groups",bg='#FFFFFF',
                                   command = lambda:controller.show_frame(ActiveGroupsPage))
        btnCheckGroups.place(x=120,y=20)
        btnCheckGroups.config(height=2,width=35)
        btnCheckGroups['font'] = button_font #to change the font of Buttons
  
        btnSetGroup = tk.Button(self.border, text ="Set Up A Group",bg='#FFFFFF',command ="")
        btnSetGroup.place(x=120,y=90)
        btnSetGroup.config(height=2,width=35)
        btnSetGroup['font'] = button_font
        
        btnShowProfile = tk.Button(self.border, text ="Show My Profile",bg='#FFFFFF',
                                   command = lambda:controller.show_frame(ProfilePage))
        btnShowProfile.place(x=120,y=160)
        btnShowProfile.config(height=2,width=35)
        btnShowProfile['font'] = button_font
        
        ##**For Test Purpose;
        #This button will be used for a test purpose which will show whether logined user id is fetched or not;
        #btnTestLoginedUserId=tk.Button(self.border, text ="Fetch The Id",bg='#FFFFFF',command=self.fetchLoginedUserId)
        #btnTestLoginedUserId.place(x=80,y=210)
        #btnTestLoginedUserId.config(height=1,width=15)
        #btnTestLoginedUserId['font'] = button_font
        #btnTestLoginedUserId.bind("<Button-1>",self.fetchLoginedUserId) #=>this works too with fetchLoginedUserId(self,var) method
        
        #This button will be used for a test purpose which will show whether logined user id is fetched or not;
        #btnBack=tk.Button(self.border, text ="Back",bg='#FFFFFF',command = lambda:controller.show_frame(LoginPage))
        #btnBack.place(x=10,y=5)
        #btnBack.config(height=1,width=8)
        #btnBack['font'] = button_font
        

        
    ##For Test Purpose;  
    #def fetchLoginedUserId(self,var): ==>this will be used if the bind() is used;
        #self.userid.set(ParentPage.loginedUserId)
        
    ##**For Test Purpose;
    #def fetchLoginedUserId(self):
        #self.userid.set(ParentPage.loginedUserId)
        #Asagidaki mantikla bir butona tiklandiginda ilgili componentleri getirecek sekilde ornegin Profil sayfasina 
        #Profilim diye bir buton daha koyarak buna tiklaninca hem logineduserid alinacak hem de o kullaniciya ozgu componentler
        #getirilecek
        #lbla = tk.Label(self.border,width=15,text="Deneme") #to test whether logined user id is fetched or not
        #lbla.place(x=30, y=200)
       
    #**For test purpose too;
    #def clearMainPageFields(self):
            #self.userid.set("")
            #self.controller.show_frame(LoginPage)


# In[46]:


#????ActiveGroupsPage sonrasinda buraya frame4 eklenerek listbox icerisinde sag tarafta eger ki profili acilan kisi grubu 
#kuran kisi ise o gruba katilmak icin atilan davetlere onay veya red verebilecek ve bununla birlikte her kullanici icin
#katilmak istedigi gruplardan onay veya red almasi durumunda bu bilgilendirme bu kisimda gosterilecek;

class ProfilePage(tk.Frame,ParentPage): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller=controller #to reach the controller for redirecting to another page in another method.
        self.userid="" #it will be assigned when the btnMyProfile is clicked
        self.fullname=""
        self.sn="" #to assign the school number of logined user
                 
        self.border=tk.LabelFrame(self,text="Profile Page",bg='#1577E8',fg='#FFFFFF',bd=10,font=("Arial",18))
        #bd used for width of frame
        self.border.pack(fill="both",expand="yes",padx=50,pady=50)
        
        button_font = font.Font(family='Helvetica') #to change the font of Buttons
        
        self.btnBack = tk.Button(self.border, text ="Back",bg='#FFFFFF',command= lambda:controller.show_frame(MainPage))
        self.btnBack.place(x=10,y=5)
        self.btnBack.config(height=1,width=8)
        self.btnBack['font'] = button_font
              
        self.btnMyProfile = tk.Button(self.border,text="Check Profile",bg='#FFFFFF',command = self.redirectToSpecificProfile)
        self.btnMyProfile.place(x=100,y=110)
        self.btnMyProfile.config(height=3,width=50)
        self.btnMyProfile['font'] = button_font #to change the font of Buttons
  
    def redirectToSpecificProfile(self):
        self.userid=ParentPage.loginedUserId
        self.fullname=ParentPage.loginedUserFullname
        self.sn=ParentPage.loginedUserSN
        
        #new components will be shown and the previous ones will be deleted;
        self.btnBack.destroy()
        self.btnMyProfile.destroy()
        self.createNewComponents(self.userid,self.fullname,self.sn)#new components will be created with the usage of this method
        
    def createNewComponents(self,uid,fname,snumber):
        #print(uid,fname,snumber)
        frame1 = Frame(self.border)
        #frame1.pack(pady=10)
        frame1.place(x=0,y=8)
        #*Logined user's listbox;
        lb1 = Listbox(frame1,width=25,height=1,font=('Times',14),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none") 
        #activestyle="none" removes the underline when an item is selected on listbox and 'selectbackground' for 
        #selected item's colour
        lb1.pack(side=LEFT,fill=BOTH)
        lb1.insert(END,fname+'-'+snumber)
        
        #*Lectures listbox;
        #lblLectures=tk.Label(self.border,font="Times 12",width=25,text="Click to below lectures to see whether\nyou have a group for them or not",justify=LEFT)
        lblLectures=tk.Label(self.border,font="Times 12",width=25,text="Select a lecture",bd=4)
        lblLectures.place(x=0,y=50)
        #text'in sonuna secilen grup icin sag tarafta gostereceksen 'on the right side' ekleyebilirsin.
        
        frame2=Frame(self.border)
        frame2.place(x=0,y=75)
        self.lb2 = Listbox(frame2,width=25,height=3,font=('Times',14),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
        self.lb2.pack(side=LEFT,fill=BOTH)
        lectures = ["SEN4015","SEN3304","SEN3006"]
        for item in lectures:
            self.lb2.insert(END,item) #END is used to add the new item to the end of the list.
            
        btnShowRelatedGroup=tk.Button(self.border,text="Show Current Related Group",bg='#FFFFFF',
                                      command=self.getRelatedGroup)
        btnShowRelatedGroup.place(x=20,y=155)
        btnShowRelatedGroup.config(height=1,width=25)
        
        
        #?????????????????????????????????
        #**The field which shows the requests of users and responses of group admins;
        #Request notifications;
        lblRequests=tk.Label(self.border,font="Times 12",width=30,text="Request Notifications",bd=4)
        lblRequests.place(x=0,y=200)
        
        frame4=Frame(self.border)
        frame4.place(x=0,y=230)
        self.lb4 = Listbox(frame4,width=30,height=4,font=('Times',14),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
        self.lb4.pack(side=LEFT,fill=BOTH)
        
        sb1 = Scrollbar(frame4)
        sb1.pack(side=RIGHT,fill=BOTH)
        self.lb4.config(yscrollcommand=sb1.set) #listbox is bind with the scrollbar
        sb1.config(command=self.lb4.yview) #yview provides to move the scrollbar vertically
        
        #Accept And Deny buttons will be shown below request notifications for the messages which logined user is a
        #group admin for them;
        btnAccept=tk.Button(self.border,text="Accept",bg='#FFFFFF',command="")
        btnAccept.place(x=50,y=330)
        btnAccept.config(height=1,width=8)
        
        btnDeny=tk.Button(self.border,text="Deny",bg='#FFFFFF',command="")
        btnDeny.place(x=130,y=330)
        btnDeny.config(height=1,width=8)
        
        #Response notifications;
        lblResponses=tk.Label(self.border,font="Times 12",width=36,text="Response Notifications",bd=4)
        lblResponses.place(x=320,y=200)
        frame5=Frame(self.border)
        frame5.place(x=320,y=230)
        self.lb5 = Listbox(frame5,width=36,height=4,font=('Times',14),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
        self.lb5.pack(side=LEFT,fill=BOTH)
        
        sb2 = Scrollbar(frame5)
        sb2.pack(side=RIGHT,fill=BOTH)
        self.lb5.config(yscrollcommand=sb2.set) #listbox is bind with the scrollbar
        sb2.config(command=self.lb5.yview) #yview provides to move the scrollbar vertically
        
        #This button will redirect the user to Main Page
        btnBack=tk.Button(self.border, text ="Back",bg='#FFFFFF',command = lambda:self.controller.show_frame(MainPage))
        btnBack.place(x=320,y=330)
        btnBack.config(height=1,width=10)
        
    #**It brings the related group of specific user for the selected lecture via using logined user's id and selected lecture;    
    def getRelatedGroup(self):      
        fnOfParticipants=[] #fullNames of participants
        idOfGroup="Group id: "
        maxPcOfGroup="Max Participant Count: " #max participant count of group
        currentPcOfGroup="Current Participant Count: " #current participant count of group
        statusOfGroup="Status of group: "
        participants="Participants of group: " #last version list for fullnames of participants of a group
        
        try:
            selectedListItem=self.lb2.get(self.lb2.curselection()) #it will be taken after the user clicks to See Current 
            #Related Group button,it can be taken like that since the selection is assigned just for single item, if it was
            #assigned for multiple selection, then a for loop would be required to get the selected list items.
            
            #Both files will be opened before the loop to not open it many times in the loop;
            usersGroups=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r") #this file is taken as an example,not original one
            participantsInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r")
            
            for usergroup in usersGroups:
                groupInfo=usergroup.rstrip('\n').split("-") #a list
                groupParticipants=groupInfo[6].split(",") #a list,more than one user can be in the group
                if(str(groupInfo[4])==selectedListItem) and (self.userid in groupParticipants):
                    #Details(id,status etc.) of related group of user will be assigned before finding the relevant participant 
                    #infos;
                    idOfGroup+=str(groupInfo[0])
                    statusOfGroup+=str(groupInfo[1])
                    maxPcOfGroup+=str(groupInfo[2])
                    currentPcOfGroup+=str(groupInfo[3])
                    for participantinfo in participantsInfos:
                        userInfo=participantinfo.rstrip('\n').split("-")
                        for participant in groupParticipants:
                            if(str(userInfo[0])==participant):#if the userids match to get participant's informations from user file
                                fnOfParticipants.append(str(userInfo[1])+" "+str(userInfo[2]))
            
            usersGroups.close()
            participantsInfos.close()
            #print(fnOfParticipants) #For test purpose...  
            
            lblDetails=tk.Label(self.border,font="Times 12",width=36,text="Details Of Your Related Group For Selected Lecture",
                                  bd=4)
            lblDetails.place(x=260,y=8)
            frame3=Frame(self.border)
            frame3.place(x=260,y=35)
            self.lb3 = Listbox(frame3,width=45,height=5,font=('Times',12),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
            self.lb3.pack(side=LEFT,fill=BOTH)
            
            for item in fnOfParticipants:
                if item==fnOfParticipants[-1]: #to prevent adding ',' after last item.
                     participants+=item
                else:
                     participants+=item+","   
                        
            self.lb3.insert(END,idOfGroup)
            self.lb3.insert(END,maxPcOfGroup)
            self.lb3.insert(END,currentPcOfGroup)
            self.lb3.insert(END,statusOfGroup)
            self.lb3.insert(END,participants)
            
            sb3 = Scrollbar(frame3,orient='horizontal')
            sb3.pack(side=BOTTOM,fill='x')
            self.lb3.config(xscrollcommand=sb3.set) #listbox is bind with the scrollbar
            sb3.config(command=self.lb3.xview) #yview provides to move the scrollbar vertically
            
        except:
            messagebox.showerror("An error has been occured!", "File error or you did not select a lecture!")


# In[47]:


#Active Groups Page
class ActiveGroupsPage(tk.Frame,ParentPage): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller=controller
                        
        self.border=tk.LabelFrame(self,text="Active Group Check",bg='#1577E8',fg='#FFFFFF',bd=20,font=("Arial",18))
        #bd used for width of frame
        self.border.pack(fill="both",expand="yes",padx=40,pady=40)
        
        ##**For test purpose;
        #This label is used for test purpose to check whether logined user id is fetched or not-will be deleted later;
        #self.userid=tk.StringVar() #it will be assigned when the 
        #lblUserId = tk.Label(self.border,width=15,textvariable=self.userid) #to test whether logined user id is fetched or not
        #lblUserId.place(x=20, y=5)
        
        button_font = font.Font(family='Helvetica') #to change the font of Buttons
        
        btnCheckGroups = tk.Button(self.border,text="Check Active Groups",bg='#FFFFFF',command = "")
        btnCheckGroups.place(x=120,y=20)
        btnCheckGroups.config(height=2,width=35)
        btnCheckGroups['font'] = button_font #to change the font of Buttons
  
        btnSetGroup = tk.Button(self.border, text ="Set Up A Group",bg='#FFFFFF',command ="")
        btnSetGroup.place(x=120,y=90)
        btnSetGroup.config(height=2,width=35)
        btnSetGroup['font'] = button_font
        
        btnShowProfile = tk.Button(self.border, text ="Show My Profile",bg='#FFFFFF',
                                   command = lambda:controller.show_frame(ProfilePage))
        btnShowProfile.place(x=120,y=160)
        btnShowProfile.config(height=2,width=35)
        btnShowProfile['font'] = button_font
        
        ##**For Test Purpose;
        #This button will be used for a test purpose which will show whether logined user id is fetched or not;
        #btnTestLoginedUserId=tk.Button(self.border, text ="Fetch The Id",bg='#FFFFFF',command=self.fetchLoginedUserId)
        #btnTestLoginedUserId.place(x=80,y=210)
        #btnTestLoginedUserId.config(height=1,width=15)
        #btnTestLoginedUserId['font'] = button_font
        #btnTestLoginedUserId.bind("<Button-1>",self.fetchLoginedUserId) #=>this works too with fetchLoginedUserId(self,var) method
        
        #This button will be used for a test purpose which will show whether logined user id is fetched or not;
        btnBack=tk.Button(self.border, text ="Back",bg='#FFFFFF',command = lambda:controller.show_frame(MainPage))
        btnBack.place(x=10,y=5)
        btnBack.config(height=1,width=8)
        btnBack['font'] = button_font
        
        
    ##For Test Purpose;  
    #def fetchLoginedUserId(self,var): ==>this will be used if the bind() is used;
        #self.userid.set(ParentPage.loginedUserId)
        
    ##**For Test Purpose;
    #def fetchLoginedUserId(self):
        #self.userid.set(ParentPage.loginedUserId)
        #Asagidaki mantikla bir butona tiklandiginda ilgili componentleri getirecek sekilde ornegin Profil sayfasina 
        #Profilim diye bir buton daha koyarak buna tiklaninca hem logineduserid alinacak hem de o kullaniciya ozgu componentler
        #getirilecek
        #lbla = tk.Label(self.border,width=15,text="Deneme") #to test whether logined user id is fetched or not
        #lbla.place(x=30, y=200)
       
    #**For test purpose too;
    #def clearMainPageFields(self):
            #self.userid.set("")
            #self.controller.show_frame(LoginPage)


# In[53]:


#if __name__ == '__main__':
app=MainApp()
app.maxsize(800,500)
app.mainloop() #The method mainloop plays a vital role in Tkinter as it is a core application that waits for events and helps in updating 
#the GUI or in simple terms, we can say it is event-driven programming. If no mainloop() is used then nothing will 
#appear on the window Screen.

