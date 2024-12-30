import cx_Oracle
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


#functionality

def clear():
    emailEntry.delete(0,END)
    UsernameEntry.delete(0,END)
    PasswordEntry.delete(0,END)
    confirmpasswordEntry.delete(0,END)
    check.set(0)

def login_page():
    Signup.destroy()
    import signin

def connect_database():
    global swap_count
    swap_count += 1
    if swap_count > 5:
        Signup.destroy()
        return
    if emailEntry.get()=='' or UsernameEntry.get()=='' or PasswordEntry.get()=='' or  confirmpasswordEntry.get()=='':
        messagebox.showerror('Error','All Fields are Required')
    elif PasswordEntry.get() != confirmpasswordEntry.get():
        messagebox.showerror('Error','Password mismatch')
    elif '@' and '.com' not in emailEntry.get():
        messagebox.showinfo('Error','Enter valid email\n For example-abc@gmail.com,abc@yahoo.com')
    elif check.get()==0:
        messagebox.showerror('Error', 'Please accept our terms and services')
    else:
        conn = cx_Oracle.connect(user='airline', password='mmmk')
        cur=conn.cursor()
        #if user already exists
        query=f"select * from data where username=:1"
        cur.execute(query,(UsernameEntry.get(),))
        row=cur.fetchone()
        if row!=None:
            messagebox.showerror('Error', 'User already exists,Please change your username')
        else:
        # to insert new user
            a=f"insert into data(email,username,password) values('{emailEntry.get()}','{UsernameEntry.get()}','{PasswordEntry.get()}')"
            cur.execute(a)
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo('Success','You have successfully registered')
            clear()
            Signup.destroy()
            import signin

#GUI part
Signup=Tk()
Signup.geometry("1279x600+50+100")
Signup.resizable(False,False)
Signup.title("Signup Page")

#Adding Image
bgimg=ImageTk.PhotoImage(file='login1.jpg')
bgLabel=Label(Signup,image=bgimg)
bgLabel.place(x=0,y=0)

#adding frame
Frame_login=Frame(Signup,bg="white",highlightbackground='dodger blue',highlightthickness=2,)
Frame_login.place(x=490,y=70,height=500,width=350)
#Adding labels and Entry fields for email
#heading=Label(Signup,text='CREATE AN ACCOUNT',font=("Impact",28,"bold"),bg='deeppink',fg='grey1')
heading=Label(Signup,text='CREATE AN ACCOUNT',font=("Open Sans",20,"bold"),bg='dodger blue',fg='yellow')
heading.place(x=500,y=100)

#adding label and entry fiel for email
emailEntry=StringVar()
email=Label(Signup,text="Email",font=("RBNO2 Light Light",12,'bold'),fg="dodger blue",bg="white")
email.place(x=500,y=170)
emailEntry=Entry(Signup,width=27,font=('Monotype',11),bd=2,fg='black',bg="white",)
emailEntry.place(x=520,y=200)


#adding label and entry fiel for username
UsernameEntry=StringVar()
Username=Label(Signup,text="Username",font=("Open sans",12,'bold'),fg="dodger blue",bg="white")
Username.place(x=500,y=235)
UsernameEntry=Entry(Signup,width=27,font=('Monotype',11),bd=2,fg='black',bg="white")
UsernameEntry.place(x=520,y=260)

#aading label and entry fiel for Password
PasswordEntry=StringVar()
Password=Label(Signup,text="Password",font=("Open sans",12,'bold'),fg="dodger blue",bg="white")
Password.place(x=500,y=300)
PasswordEntry=Entry(Signup,width=27,font=('Monotype',11),bd=2,fg='black',bg="white",show='*')
PasswordEntry.place(x=520,y=325)

#aading label and entry fiel for confirmPassword
confirmpassword=Label(Signup,text="ConfirmPassword",font=("Open sans",12,'bold'),fg="dodger blue",bg="white")
confirmpassword.place(x=500,y=360)
confirmpasswordEntry=Entry(Signup,width=27,font=('Monotype',11),bd=2,fg='black',bg="white",show='*')
confirmpasswordEntry.place(x=520,y=390)

#check Button
check=IntVar()
terms=Checkbutton(Signup,text='I agree to the Terms and Conditions',font=('Microsoft Yahei UI Light',11,'bold'),fg='red',
                  bg='white',activebackground="white",activeforeground="red",cursor='hand2',variable=check)
terms.place(x=500,y=420)


#SignUp Button
signupbutton=Button(Signup,text="Sign Up",font=('Microsoft Yahei UI Light',12,'bold'),bd=0,width=25,fg="white",bg="dodger blue",
                    activebackground="dodger blue",activeforeground="white",cursor='hand2',command=connect_database)
signupbutton.place(x=520,y=470)

#label and login button
alreadyaccount=Label(Signup,text="Already Have an account?",font=("Open Sans",11,"bold"),bg='white',fg='red')
alreadyaccount.place(x=520,y=530)
Loginbutton=Button(Signup,text='Login',font=('Open Sans',9,'bold underline'),bd=0,fg='blue',bg='white',activeforeground='blue',
                   activebackground='white',cursor='hand2',width=10,command=login_page)
Loginbutton.place(x=720,y=530)








Signup.mainloop()
