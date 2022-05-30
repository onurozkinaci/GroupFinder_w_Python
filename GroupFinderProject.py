#!/usr/bin/env python
# coding: utf-8

# In[94]:


import tkinter as tk
from tkinter import *
from tkinter import ttk #Just like CSS is used to style an HTML element, we use tkinter. ttk to style tkinter widgets.
from tkinter import messagebox
import tkinter.font as font #used to change the font of components

import re #To use regex for RegisterPage fields' controls


# In[95]:


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
            
        self.show_frame(LoginPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.title("Group Finder")


# In[96]:


##??????????????????????????????
#To get the current logined user's id via inheriting this super class by sub classes,identify all required datas which will be used
#by subclasses(pages) here;
class ParentPage:
    loginedUserId='' #logined user's id which will be used on ProfilePage
    loginedUserFullname=''#fullname of logined user,will be used on ProfilePage
    loginedUserSN=''#school number  of logined user,will be used on ProfilePage


# In[97]:


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


# In[98]:


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
                
            elif isSNFormatApplicable()==False:
                messagebox.showerror("Empty Field", "The school number must be a number!")   
                
            elif isFullnameApplicable()==False:
                messagebox.showerror("Empty Field", "Check name and surname, correct format example: 'Mark' !")   
                
            elif isUnameAndPasswordApplicable()==False:
                messagebox.showerror("Empty Field", "Check username and password, correct format example: 'mrogers123_' !") 
                              
            else:
                try:
                    if((isUsernameExists()==False) and (isSNExists()==False)):
                        userInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                                   "r")
                        users = userInfos.readlines() #returns a list containing each line in the file as a list item.
                        userInfos.close()
                        
                        #if there is no registered user in the file yet,then give first user's id as 1;
                        if len(users)==0:
                            id=0
                        else:
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
                
                
        #*To check whether entered school number matches with the regex pattern or not(must be a number(only contains digits));
        def isSNFormatApplicable():
            path = re.compile(r"[0-9]+[\S]")#school number must be digit and it cannot be passed as empty or with space.
            if re.fullmatch(path,E3.get()): #"fullmatch" checks whether whole entered String matches with regex or not,re is
                #imported at the beginning.
                return True
            else:
                return False
            
        #*To check whether entered name and surname matches with the regex pattern or not(must be a letter);
        def isFullnameApplicable():
            path = re.compile(r"[A-z]+[\S]") #must be a letter and cannot be passed with space or empty
            if (re.fullmatch(path,E1.get())) and (re.fullmatch(path,E2.get())):
                return True
            else:
                return False
            
         #*To check whether entered username and password matches with the regex pattern or not;
        def isUnameAndPasswordApplicable():
            path = re.compile(r"[\w]+[\S]") #can be letter,number,_ and .(some characters) and cannot be passed with space or empty,
            #same with [a-zA-Z0-9_]+ format.
            if (re.fullmatch(path,E4.get())) and (re.fullmatch(path,E5.get())) :
                return True
            else:
                return False

                                
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


# In[99]:


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
        
        #The user can signout and will be redirected to Login Page;
        btnSignout=tk.Button(self.border, text ="Sign Out",bg='#FFFFFF',command = lambda:controller.show_frame(LoginPage))
        btnSignout.place(x=10,y=5)
        btnSignout.config(height=1,width=8)
        btnSignout['font'] = button_font
        
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


# In[100]:


#Active Groups Page
class ActiveGroupsPage(tk.Frame,ParentPage): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller=controller
        #self.clearFields()
        
        self.border=tk.LabelFrame(self,text="Active Group Check",bg='#1577E8',fg='#FFFFFF',bd=20,font=("Arial",18))
        #bd used for width of frame
        self.border.pack(fill="both",expand="yes",padx=40,pady=40)
        
        #**Lecture Selection;
        lblLecture=tk.Label(self.border,font="Times 12",width=30,text="Please select a lecture to see it's active groups",bd=4)
        lblLecture.place(x=200,y=10)
    
        self.currentLecture = tk.StringVar()
        cmbLectures = ttk.Combobox(self.border,width=30,textvariable=self.currentLecture) #combobox to provide lectures that the user wants
        
        # set a default lecture to prevent the situation which the user does not select a lecture;
        #currentLecture = "SEN4015"
        #cmbLectures.set(currentLecture)
        
        cmbLectures['values'] = ('SEN4015', 'SEN3304', 'SEN4018')
        cmbLectures['state'] = 'readonly' #value typing by user is prevented on combobox
        cmbLectures.place(x=230,y=40)
        cmbLectures.bind('<<ComboboxSelected>>',self.lectureSelection) #binding the lecture selection from combobox.'<<ComboboxSelected>>' 
        #virtual event is created when selected value of combobox changes.We can bind this event to handle with it;
        
        button_font = font.Font(family='Helvetica') #to change the font of Buttons
        
        #This button will be used for a test purpose which will show whether logined user id is fetched or not;
        self.btnBack=tk.Button(self.border, text ="Back",bg='#FFFFFF',command = self.clearFields)
        self.btnBack.place(x=10,y=5)
        self.btnBack.config(height=1,width=8)
        self.btnBack['font'] = button_font
        
    #after lecture selection from combobox,active groups related with this lecture will be shown on listbox in order;
    def lectureSelection(self,event):
        #print(self.currentLecture.get())    
        #fnOfParticipants=[] #fullNames of participants
        #idOfGroup="Group id:"
        #currentPcOfGroup="Current Participant Count:" #current participant count of group
        #participants="Participants:" #last version list for fullnames of participants of a group
        activeGroups=[] #a list which will store the all active groups of the related lecture
        
        self.userid=ParentPage.loginedUserId #it will be assigned when the btnMyProfile is clicked
        self.fullname=ParentPage.loginedUserFullname
        
        try:
            self.selectedLecture=self.currentLecture.get() #the selected lecture from combobox
            
            #Both files will be opened before the loop to not open them many times in the loop;
            currentGroups=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r") #this file is taken as an example,not original one
            #participantsInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               #"r")
            #participantsInfos=""
            
            for currentgroup in currentGroups:
                groupInfo=currentgroup.rstrip('\n').split("-") #a list
                groupParticipants=groupInfo[6].split(",") #a list,more than one user can be in the group
                if(str(groupInfo[4])==self.selectedLecture) and (str(groupInfo[1])=="OPENED"): #related groups with selection which does not 
                    #filled completely yet and open to requests.
                    #Details(id,current participant count etc.) of related group will be assigned;
                    idOfGroup=str(groupInfo[0])
                    #currentPcOfGroup=str(groupInfo[3])
                    fnOfParticipants=[] #to check the different group's participants by initializing it for each line if the lecture 
                    participantsInfos=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt",
                               "r")
                    for participantinfo in participantsInfos:
                        userInfo=participantinfo.rstrip('\n').split("-")
                        for participant in groupParticipants:
                            if(str(userInfo[0])==participant):#if the userids match to get participant's informations 
                                #from user file;
                                fnOfParticipants.append(str(userInfo[1])+" "+str(userInfo[2]))
                    activeGroups.append([idOfGroup,fnOfParticipants])
                    participantsInfos.close()

            currentGroups.close()
            #participantsInfos.close()
            #print(activeGroups) #For test purpose...
                        
            self.lblDetails=tk.Label(self.border,font="Times 12",width=36,text="Active Groups For "+self.selectedLecture,
                                  bd=4)
            self.lblDetails.place(x=0,y=80)
            
            self.frameLectures=Frame(self.border)
            self.frameLectures.place(x=0,y=110)
            
            self.lbLectureInfos = Listbox(self.frameLectures,width=75,height=8,font=('Times',12),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
            self.lbLectureInfos.pack(side=LEFT,fill=BOTH)
            
            i=0
            while i < len(activeGroups):
                participants=""
                for fullname in activeGroups[i][1]:
                    if fullname==activeGroups[i][1][-1]: #to prevent adding ',' after last item.
                         participants+=fullname 
                    else:
                         participants+=fullname+","       
                #print("Group id:"+activeGroups[i][0]+",Lecture:"+selectedLecture+",Current Participants:"+participants)
                self.lbLectureInfos.insert(END,"Group id:"+activeGroups[i][0]+",Lecture:"+self.selectedLecture
                                           +",Current Participants:"+participants)
                i +=1
                
            #Adding both vertical and horizontal scrollbars;              
            self.sbvertical = Scrollbar(self.frameLectures,orient='vertical')
            self.sbvertical.pack(side= RIGHT,fill="y")
            self.sbhorizontal = Scrollbar(self.frameLectures, orient='horizontal')
            self.sbhorizontal.pack(side= BOTTOM, fill= "x")
            
            self.lbLectureInfos.config(yscrollcommand=self.sbvertical.set) #listbox is bind with the scrollbar vertically
            self.lbLectureInfos.config(xscrollcommand=self.sbhorizontal.set) #listbox is bind with the scrollbar horizontally
            self.sbvertical.config(command=self.lbLectureInfos.yview) #yview provides to move the scrollbar vertically
            self.sbhorizontal.config(command=self.lbLectureInfos.xview) #xview provides to move the scrollbar horizontally
            
            self.btnRequest=tk.Button(self.border, text ="Send Request To Participate",bg='#FFFFFF',command = self.sendRequest)
            self.btnRequest.place(x=220,y=290)
            self.btnRequest.config(height=2,width=30)
            
        except:
            messagebox.showerror("An error has been occured!", "File error!")  
            
    def sendRequest(self):
        
        try:
            selectedListItem=self.lbLectureInfos.get(self.lbLectureInfos.curselection()) #selected group from listbox
            selectedgroup=selectedListItem.split(":") #a list of selected group from listbox
            selectedgroup_id=selectedgroup[1].split(",")[0]
             #print(selectedListItem,selectedgroup,selectedgroup_id,self.selectedLecture,self.userid,self.fullname)

            groupRequests=open(r"C:\Users\Umur\Desktop\GroupRequests1.txt","a")
            if self.isUserParticipatedBefore(self.userid)==True :
                messagebox.showerror("You already have a group for this lecture!",
                                     "You cannot send a request for this lecture again!")                
            elif self.isRequestSentBefore(self.userid,selectedgroup_id):
                messagebox.showerror("You have already sent a request for this group!",
                                     "You cannot send a request for this group again,you can send to another one...")                                                
            else:
                requestinfo = selectedgroup_id+ "-" + self.selectedLecture+"-"+self.fullname+"-"+self.userid
                #fullname and user id of logined user are taken at the beginning of lectureSelection() method
                groupRequests.write(requestinfo + '\n')
                messagebox.showinfo("Successful Request...", "Your request have been sent successfully")
            groupRequests.close()
        except:
            messagebox.showerror("An error has been occured!", "File error or you did not select a group or lecture") 
    
    def isUserParticipatedBefore(self,uid): #if the logined user have already a group for selected lecture, he/she will be 
        #warned and cannot send a request for this lecture again(to any group unlike isRequestSentBefore()'s' work logic);
        flag=False
        try:
            groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r") 
            for groupinfo in groupInfos:
                groupdatas=groupinfo.rstrip('\n').split("-")
                if(groupdatas[4]==self.selectedLecture) and (uid in groupdatas[6]):
                    flag=True
                    break
                else:
                    continue
            groupInfos.close()
            return flag
        except:
            messagebox.showerror("An error has been occured!", "File error2!")
            
           
    def isRequestSentBefore(self,uid,gid): #if the logined user have already sent a request for the selected group,
        #he/she will be warned and cannot send a request for this group again. However,they can send a request to another
        #group for the same lecture(selected lecture);
        flag=False
        try:
            groupRequests=open(r"C:\Users\Umur\Desktop\GroupRequests1.txt","r") 
            for grouprequest in groupRequests:
                groupdatas=grouprequest.rstrip('\n').split("-")
                if(groupdatas[0]==gid) and (groupdatas[3]==uid):
                    flag=True
                    break
                else:
                    continue
            groupRequests.close()
            return flag
        except:
            messagebox.showerror("An error has been occured!", "File error3!")
            
    def clearFields(self):
        self.lblDetails.destroy()
        self.frameLectures.destroy()
        self.lbLectureInfos.destroy()
        self.sbvertical.destroy()
        self.sbhorizontal.destroy()
        self.btnRequest.destroy()
        self.currentLecture.set("") #to set the combobox value to unselected when the user clicks to 'Back' button.
        #Also all the listbox elements and frame will be deleted to not leave the same listbox when new user login after signout
        #after user clicks to 'Back' button on this page and these listbox elements will be created again when the user selects
        #a lecture from combobox;
        self.controller.show_frame(MainPage) #redirect the user to MainPage when he/she clicks to 'Back' button


# In[101]:


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
        
        self.btnBack1 = tk.Button(self.border, text ="Back",bg='#FFFFFF',command=self.getDestroyedComponents)
        self.btnBack1.place(x=10,y=5)
        self.btnBack1.config(height=1,width=8)
        self.btnBack1['font'] = button_font
              
        self.btnMyProfile = tk.Button(self.border,text="Check Profile",bg='#FFFFFF',command = self.redirectToSpecificProfile)
        self.btnMyProfile.place(x=110,y=110)
        self.btnMyProfile.config(height=3,width=50)
        self.btnMyProfile['font'] = button_font #to change the font of Buttons
  
    def redirectToSpecificProfile(self):
        self.userid=ParentPage.loginedUserId #it will be assigned when the btnMyProfile is clicked
        self.fullname=ParentPage.loginedUserFullname
        self.sn=ParentPage.loginedUserSN #to assign the school number of logined user
        
        #new components will be shown and the previous ones will be deleted;
        self.btnBack1.destroy()
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
        lectures = ["SEN4015","SEN3304","SEN4018"]
        for item in lectures:
            self.lb2.insert(END,item) #END is used to add the new item to the end of the list.
            
        btnShowRelatedGroup=tk.Button(self.border,text="Show Current Related Group",bg='#FFFFFF',
                                      command=self.getRelatedGroup)
        btnShowRelatedGroup.place(x=20,y=155)
        btnShowRelatedGroup.config(height=1,width=25)
        
        
        #--------- ---------------------REQUESTS---------------------------------------------------
        #**The field which shows the requests of users and responses of group admins;
        #Request notifications;
        #lb4=Requests' listbox;
        lblRequests=tk.Label(self.border,font="Times 12",width=30,text="Request Notifications",bd=4)
        lblRequests.place(x=0,y=200)
        
        frame4=Frame(self.border)
        frame4.place(x=0,y=230)
        self.lb4 = Listbox(frame4,width=30,height=4,font=('Times',12),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
        self.lb4.pack(side=LEFT,fill=BOTH)
        self.fillRequestNotifications(uid)#to get the current requests for the groups which logined user is responsible for accept
        #or reject since he/she is a group leader!
        
        #Adding both vertical and horizontal scrollbars;              
        self.sbvertical = Scrollbar(frame4,orient='vertical')
        self.sbvertical.pack(side= RIGHT,fill="y")
        self.sbhorizontal = Scrollbar(frame4, orient='horizontal')
        self.sbhorizontal.pack(side= BOTTOM, fill= "x")

        self.lb4.config(yscrollcommand=self.sbvertical.set) #listbox is bind with the scrollbar vertically
        self.lb4.config(xscrollcommand=self.sbhorizontal.set) #listbox is bind with the scrollbar horizontally
        self.sbvertical.config(command=self.lb4.yview) #yview provides to move the scrollbar vertically
        self.sbhorizontal.config(command=self.lb4.xview) #xview provides to move the scrollbar horizontally
        #----------------------------------------------------------------------------------------------
        
        #Accept And Deny buttons will be shown below request notifications for the messages which logined user is a
        #group admin for them;
        btnAccept=tk.Button(self.border,text="Accept",bg='#FFFFFF',command=self.sendAcceptResponse)
        btnAccept.place(x=50,y=330)
        btnAccept.config(height=1,width=8)
        
        btnDeny=tk.Button(self.border,text="Deny",bg='#FFFFFF',command=self.sendRejectResponse)
        btnDeny.place(x=130,y=330)
        btnDeny.config(height=1,width=8)
        
        #----------------------------------RESPONSES---------------------------------------------------------
        #Response notifications;
        lblResponses=tk.Label(self.border,font="Times 12",width=32,text="Response Notifications",bd=4)
        lblResponses.place(x=350,y=200)
        frame5=Frame(self.border)
        frame5.place(x=350,y=230)
        self.lb5 = Listbox(frame5,width=32,height=4,font=('Times',12),bd=5,fg='#464646',highlightthickness=0,
                     selectbackground='#0000ff',activestyle="none",selectmode="single") #items also can be selected in 'multiple' mode
        self.lb5.pack(side=LEFT,fill=BOTH)
        self.fillResponseNotifications(uid)
        
        #Adding both vertical and horizontal scrollbars;              
        self.sbvertical = Scrollbar(frame5,orient='vertical')
        self.sbvertical.pack(side= RIGHT,fill="y")
        self.sbhorizontal = Scrollbar(frame5, orient='horizontal')
        self.sbhorizontal.pack(side= BOTTOM, fill= "x")

        self.lb5.config(yscrollcommand=self.sbvertical.set) #listbox is bind with the scrollbar vertically
        self.lb5.config(xscrollcommand=self.sbhorizontal.set) #listbox is bind with the scrollbar horizontally
        self.sbvertical.config(command=self.lb5.yview) #yview provides to move the scrollbar vertically
        self.sbhorizontal.config(command=self.lb5.xview) #xview provides to move the scrollbar horizontally
        #---------------------------------------------------------------------------------------------------------
        
        #This button will redirect the user to Main Page
        btnBack=tk.Button(self.border, text ="Back",bg='#FFFFFF',command = self.getDestroyedComponents)
        btnBack.place(x=350,y=330)
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
            
            
    def fillRequestNotifications(self,uid):
        try:
                #oncelikle request dosyasi acilacak ve buradaki requestlerin group id'si alinip group dosyasina gidilecek.
                #Son kolondan bir onceki kolon olan grubu olsuturan kisinin id'si ile login olan kisinin id'si ayni ise ona 
                #requestler gosterilecek,diger grup uyelerine degil,onayi verecek olan onlar degil cunku;
            currentRequests=[] #a list which will store the all active groups of the related lecture    

            #Both files will be opened before the loop to not open it many times in the loop;
            usersRequests=open(r"C:\Users\Umur\Desktop\GroupRequests1.txt","r")
            #groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r")
            #groupInfos="" #it will be assigned as a file in the loop
            
            for userrequest in usersRequests:
                requestInfo=userrequest.rstrip('\n').split("-") #a list 
                groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r")
                for groupinfo in groupInfos:
                    groupdata=groupinfo.rstrip('\n').split("-") #a list
                    if(str(requestInfo[0])==str(groupdata[0])) and (str(groupdata[5])==uid): 
                        #if the groupid of request and logined user info is equal to the group leader info;
                        currentRequests.append([requestInfo[0],requestInfo[1],requestInfo[2],requestInfo[3]])
                        #request infos will be taken
                groupInfos.close()
                        
            #print(currentRequests) 
            usersRequests.close()
            #groupInfos.close()
            
            i=0
            while i < len(currentRequests):
                #self.lb4=Requests' listbox;
                self.lb4.insert(END,"Group id:"+currentRequests[i][0]+",Lecture:"+currentRequests[i][1]
                             +",Request owner:"+currentRequests[i][2]+",Request owner id:"+currentRequests[i][3])
                i +=1
        except:
            messagebox.showerror("An error has been occured!", "File or System error!")
            
    
    def sendAcceptResponse(self):
        try:
            selectedListItem=self.lb4.get(self.lb4.curselection()) #selected group from lb4(requests listbox)
            selectedgroup=selectedListItem.split(":") #a list of selected group from listbox
            selectedgroup_id=selectedgroup[1].split(",")[0]
            selectedlecture=selectedgroup[2].split(",")[0]
            selectedrequestowner=selectedgroup[3].split(",")[0]
            selectedrequestowner_id=selectedgroup[4]
            #print(selectedgroup,selectedgroup_id,selectedlecture,selectedrequestowner,selectedrequestowner_id)
            
            groupResponses=open(r"C:\Users\Umur\Desktop\GroupResponses1.txt","a")
            groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","a")
            
            if self.isResponseSentBefore(selectedrequestowner_id,selectedgroup_id)==True :
                messagebox.showerror("You have already sent a response for this group!",
                              "You cannot send a response for this group again!")    
                
            elif self.isGroupFull(selectedgroup_id,self.userid)==True:
                messagebox.showerror("Max limit have reached!", 
                                     "You cannot accept this request since the related group is closed(full)!")
                
            elif self.isUserParticipatedBefore(selectedlecture,selectedrequestowner_id)==True:
                messagebox.showerror("Request owner already have a group!", 
                                     "You cannot accept this request since request owner added for another group!")
                
                
            else: #There is no problem, user can be added to response file and related group info can be updated on group file;
                #------------------------------Adding response to a file---------------------------------------------
                responseinfo = selectedgroup_id+ "-" +selectedlecture+"-"+selectedrequestowner+"-"+selectedrequestowner_id+"-"+"ACCEPTED"
                #fullname and user id of logined user are taken at the beginning of lectureSelection() method
                groupResponses.write(responseinfo + '\n')
                #----------------------------------------------------------------------------------------------------
                
                #-------------------------------Updating Related Group File-----------------------------------------------------
                #**Updating related group infos on groups' file if it is accepted by group leader.Whole file(write again) 
                #need to be updated even if one line of it need to be changed as below;
                groupInfos = open(r"C:\Users\Umur\Desktop\GroupInfos.txt", "r")
                loflines = groupInfos.readlines() #a list which holds the lines of opened text
                flag=False #to check whether the file is updated or not 
                    
                i=0
                while i<len(loflines):
                    relatedgroup=loflines[i].rstrip('\n').split("-")
                    if(relatedgroup[0]==selectedgroup_id) and (relatedgroup[5]==self.userid): #self.userid=logined user(group leader control)
                        changedgroup_size= int(relatedgroup[3])+1
                        if relatedgroup[2]==str(changedgroup_size):
                            relatedgroup[1]="CLOSED" #if the max and current participant count becomes equal when new participant is added,
                            #then the status of group will be updated as "CLOSED"!
                        addeduserid=relatedgroup[6]+","+selectedrequestowner_id #request owner will be added to group file's last column
                        loflines[i]=relatedgroup[0]+"-"+relatedgroup[1]+"-"+relatedgroup[2]+"-"+str(changedgroup_size)+"-"+relatedgroup[4]+"-"+relatedgroup[5]+"-"+addeduserid+'\n'
                        groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","w")
                        groupInfos.writelines(loflines)
                        groupInfos.close()
                        flag=True
                        break
                    i+=1

                if flag==True:
                    groupResponses.close()
                    groupInfos.close()
                    messagebox.showinfo("Successful Transaction...", "Your response have been sent successfully...")

                else:
                    messagebox.showerror("An error occured!", "Update Error!")
                   
        except:
            messagebox.showerror("An error has been occured!", "File or System error(or you did not select a request!)")
           #---------------------------------------------------------------------------------------------------------------- 
            
    def sendRejectResponse(self):
        try:
            selectedListItem=self.lb4.get(self.lb4.curselection()) #selected group from lb4(requests listbox)
            selectedgroup=selectedListItem.split(":") #a list of selected group from listbox
            selectedgroup_id=selectedgroup[1].split(",")[0]
            selectedlecture=selectedgroup[2].split(",")[0]
            selectedrequestowner=selectedgroup[3].split(",")[0]
            selectedrequestowner_id=selectedgroup[4]
            #print(selectedgroup,selectedgroup_id,selectedlecture,selectedrequestowner,selectedrequestowner_id)
            
            groupResponses=open(r"C:\Users\Umur\Desktop\GroupResponses1.txt","a")
            if self.isResponseSentBefore(selectedrequestowner_id,selectedgroup_id)==True :
                messagebox.showerror("You have already sent a response for this group!",
                              "You cannot send a response for this group again!")                                                           
            else:
                responseinfo = selectedgroup_id+ "-" +selectedlecture+"-"+selectedrequestowner+"-"+selectedrequestowner_id+"-"+"REJECTED"
                #fullname and user id of logined user are taken at the beginning of lectureSelection() method
                groupResponses.write(responseinfo + '\n')
                messagebox.showinfo("Successful Transaction...", "Your response have been sent successfully")
            groupResponses.close()
            
        except:
            messagebox.showerror("An error has been occured!", "File error or you did not select a request") 
            
            
    def isResponseSentBefore(self,uid,gid): #if the logined user have already sent a request for the selected group,
        #he/she will be warned and cannot send a request for this group again. However,they can send a request to another
        #group for the same lecture(selected lecture);
        flag=False
        try:
            groupResponses=open(r"C:\Users\Umur\Desktop\GroupResponses1.txt","r") 
            for groupresponse in groupResponses:
                groupdatas=groupresponse.rstrip('\n').split("-")
                if(groupdatas[0]==gid) and (groupdatas[3]==uid):
                    flag=True
                    break
                else:
                    continue
            groupResponses.close()
            return flag
        except:
            messagebox.showerror("An error has been occured!", "File error3!")
            
    def fillResponseNotifications(self,uid):
        try:
            currentResponses=[] #a list which will store the all active groups of the related lecture    

            #Both files will be opened before the loop to not open it many times in the loop;
            responseInfos=open(r"C:\Users\Umur\Desktop\GroupResponses1.txt","r")
            
            for responseinfo in responseInfos:
                response=responseinfo.rstrip('\n').split("-") #a list 
                if str(response[3])==uid: 
                    #The response infos will be shown to logined user if they belong to him/her;
                    currentResponses.append([response[0],response[1],response[4]])#response's group id,lecture and result infos 
                    #will be taken.               
            #print(currentRequests) 
            responseInfos.close()
            
            i=0
            while i < len(currentResponses):
                #self.lb5=Responses' listbox;
                self.lb5.insert(END,"Your request to participate group id "+currentResponses[i][0]+" for "+
                                currentResponses[i][1]+" is "+currentResponses[i][2].lower()+".")
                i +=1
                
        except:
            messagebox.showerror("An error has been occured!", "File or System error!")
            
            
    #*If the current and max participant count of a related group is equal, then an error will be given to group leader which
    #warns him/her about that he/she cannot Accept this request since the max count has been reached;
    def isGroupFull(self,gid,uid):
        flag=False
        try:
            groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r")
            for groupinfo in groupInfos:
                relatedgroup=groupinfo.rstrip('\n').split("-")
                if(relatedgroup[0]==gid) and (relatedgroup[5]==uid):
                    if (relatedgroup[2]==relatedgroup[3]) or (relatedgroup[1]=="CLOSED"):
                        #*Both conditions have the same meaning,'or' operator can be used to be sured.
                        flag=True
                        break
                else:
                     continue
                        
            groupInfos.close()
            return flag
        
        except:
            messagebox.showerror("An error has been occured!", "File error4!")
        
        
    #*if the request owner is added for another group already,then the group leaders cannot accept this request owner and
    #they will be warned by error message above;
    def isUserParticipatedBefore(self,slecture,uid):
        flag=False
        try:
            groupInfos=open(r"C:\Users\Umur\Desktop\GroupInfos.txt","r") 
            for groupinfo in groupInfos:
                groupdatas=groupinfo.rstrip('\n').split("-")
                if(groupdatas[4]==slecture) and (uid in groupdatas[6]):
                    flag=True
                    break
                else:
                    continue
            groupInfos.close()
            return flag
        except:
            messagebox.showerror("An error has been occured!", "File error5!")
            
                    
    def getDestroyedComponents(self):
        #Recreate the required components to get logined user info without closing the frame since it causes a problem and
        #does not get the logined user id etc. when they Sign Out and login again.It is happened since the 'Check Profile'
        #button is destroyed when new components are created on it.Also you need to delete the components which are already
        #created.
        
        for widgets in self.border.winfo_children():#To destroy the all current components in order to get back below buttons
        #instead of them;
                      widgets.destroy()
        
        button_font = font.Font(family='Helvetica') #to change the font of Buttons
        self.btnBack1 = tk.Button(self.border, text ="Back",bg='#FFFFFF',command= lambda:controller.show_frame(MainPage))
        self.btnBack1.place(x=10,y=5)
        self.btnBack1.config(height=1,width=8)
        self.btnBack1['font'] = button_font
        
        self.btnMyProfile = tk.Button(self.border,text="Check Profile",bg='#FFFFFF',command = self.redirectToSpecificProfile)
        self.btnMyProfile.place(x=100,y=110)
        self.btnMyProfile.config(height=3,width=50)
        self.btnMyProfile['font'] = button_font
        self.controller.show_frame(MainPage) #redirect the user to MainPage when he/she clicks to 'Back' button


# In[ ]:


#if __name__ == '__main__':
app=MainApp()
app.maxsize(800,500)
app.mainloop() #The method mainloop plays a vital role in Tkinter as it is a core application that waits for events and helps in updating 
#the GUI or in simple terms, we can say it is event-driven programming. If no mainloop() is used then nothing will 
#appear on the window Screen.


# In[ ]:


r1=open(r"C:\Users\Umur\Documents\GitHub\GroupFinderwPython\GroupFinder_w_Python\Users_SEN4015Project.txt","r")
print(r1.readlines())


# In[ ]:




