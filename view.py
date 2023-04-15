from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter.font import Font
from settings import CANVAS_WIDTH, CANVAS_HEIGHT, GRID_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, LABLE_WIDTH, LABLE_HEIGHT, BLANK
from PIL import ImageTk, Image
import mysql.connector 
import urllib.request
from io import BytesIO

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        root.wm_title("Modular Arithmetic Exercises")
        self.windowsystem = root.call('tk', 'windowingsystem')
        self.frame = root
        root.tk.call('tk', 'scaling', 2.0)
        self.canvas = Canvas(self.frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="LightSkyblue1")
        self.canvas.pack(fill=BOTH, expand=FALSE)
        self.score = 0
        self.skip_button = Button(self.root, text="SKIP", command=lambda: self.skip(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
        self.question_num = 0
        self.level=0
        self.mode= None
        self.init_fonts()
        self.show_main_menu()

    def init_fonts(self):
        self.bigfont = font.Font(family="Arial", size=24, weight="bold")
        self.scorefont = font.Font(family="Arial", size=16, weight="bold")

    def init_score(self):
        self.score_text = self.canvas.create_text(5, 5, anchor="nw")
        self.canvas.itemconfig(self.score_text, text="Score:", font=self.scorefont, fill="white")
        self.time_text = self.canvas.create_text(CANVAS_WIDTH, GRID_SIZE*16, anchor="ne")
        self.canvas.itemconfig(self.time_text, text="TIME", font=self.scorefont, fill="yellow")

    def show_main_menu(self):
        # Load the cloud.gif image from file
        self.cloud_gif = Image.open("cloud.gif")
        # Resize the image to fit the canvas size
        self.cloud_gif = self.cloud_gif.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.ANTIALIAS)
        # Convert the image to a PhotoImage object
        self.cloud_gif = ImageTk.PhotoImage(self.cloud_gif)
        # Create a canvas background with the cloud.gif image
        self.canvas.create_image(0, 0, anchor=NW, image=self.cloud_gif)

        self.img = (Image.open("My project.png"))
        self.imgrsz = self.img.resize((300,300), Image.ANTIALIAS)
        self.newimg = ImageTk.PhotoImage (self.imgrsz)
        self.canvas.create_image(CANVAS_WIDTH / 8, 5*CANVAS_HEIGHT/6, image=self.newimg)


        self.score = 0
        
        message1 = " Modular Arithmetics Quiz "
        self.canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, text=message1,font=("Arial", 80, "bold"), fill="black")
        
        level_button = Button(self.root, text="Normal Mode", font=("Arial", 30), command=self.controller.normal_mode_menu, relief="raised", borderwidth=3, bg="#F7D9C4", fg="#4B4E6D", width=12, height=2, activebackground="#ECCFCB", activeforeground="#FFF")
        self.canvas.create_window(CANVAS_WIDTH / 2, 2 * CANVAS_HEIGHT / 6, window=level_button, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        random_button = Button(self.root, text="Random Question Generator", font=("Arial",25), command=self.controller.random_question_generator, relief="raised", borderwidth=3, bg="#BFE1D4", fg="#4B4E6D", width=20, height=2, activebackground="#9DC3C0", activeforeground="#FFF")
        self.canvas.create_window(CANVAS_WIDTH / 2, 3 * CANVAS_HEIGHT / 6, window=random_button, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        ###self.controller.choose_ranking
        ranking_button = Button(self.root, text="Ranking", font=("Arial", 30), command=self.controller.show_rankingrqg, relief="raised", borderwidth=3, bg="#F4F4F4", fg="#4B4E6D", width=12, height=2, activebackground="#D5D5D5", activeforeground="#FFF")
        self.canvas.create_window(CANVAS_WIDTH / 2, 4 * CANVAS_HEIGHT / 6, window=ranking_button, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        
        ##create questions
        create_button = Button(self.root, text="Create Questions", font=("Arial", 30), command=self.controller.show_create_questions, relief="raised", borderwidth=3, bg="#F4F4F4", fg="#4B4E6D", width=12, height=2, activebackground="#D5D5D5", activeforeground="#FFF")
        self.canvas.create_window(CANVAS_WIDTH / 2, 5 * CANVAS_HEIGHT / 6, window=create_button, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)



    def show_home_button(self):
        home_button = Button(self.root, text="HOME",font=("Arial", 20, "bold"), command=self.controller.back_to_main,relief="raised", borderwidth=3, bg="#F4F4F4", fg="#4B4E6D", width=12, height=2, activebackground="#D5D5D5", activeforeground="#FFF")
        self.canvas.create_window((CANVAS_WIDTH / 10, CANVAS_HEIGHT / 10), window=home_button, width=100, height=50)
    
    
    def back_to_main(self):
        self.canvas.delete("all")
        self.question_num = 0
        self.show_main_menu()

    def normal_mode_menu(self):
        self.canvas.delete("all")
        self.show_home_button()

        message = Label(self.root, text="   Select Exercise  ", foreground="pink", background="white", font=("Arial", 60, "bold"))
        x0, y0, x1, y1 = self.canvas.bbox(self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=message))
        self.canvas.create_oval(x0, y0, x1, y1, fill="white", outline="pink", width=4)


        for i in range (4):
            message = Label(self.root, text=("Level " + str(i + 1)), foreground="black",bg="LightSkyblue1",font=("Arial", 40,"bold"))
            self.canvas.create_window((i + 1) * BLANK + (i + 0.5) * LABLE_WIDTH, LABLE_HEIGHT * 0.5 + CANVAS_HEIGHT / 3, window=message)

        button_style = {
            'font': ('Arial', 30),
            'bg': '#2196f3',
            'fg': 'black',
            'activebackground': '#0d47a1',
            'activeforeground': 'white',
            'bd': 0,
            'highlightthickness': 0
        }

        button_1 = Button(self.root, text="Exercise 1", command=lambda: self.controller.normal_mode(1,0), **button_style)
        self.canvas.create_window(BLANK + 0.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_1, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_2 = Button(self.root, text="Exercise 2", command=lambda: self.controller.normal_mode(2,0), **button_style)
        self.canvas.create_window(BLANK + 0.5 * LABLE_WIDTH, 2.5 * LABLE_HEIGHT + 2 * BLANK + CANVAS_HEIGHT / 3, window=button_2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_3 = Button(self.root, text="Exercise 3", command=lambda: self.controller.normal_mode(3,0), **button_style)
        self.canvas.create_window(2 * BLANK + 1.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_4 = Button(self.root, text="Exercise 4", command=lambda: self.controller.normal_mode(4,0), **button_style)
        self.canvas.create_window(2 * BLANK + 1.5 * LABLE_WIDTH, 2.5 * LABLE_HEIGHT + 2 * BLANK + CANVAS_HEIGHT / 3, window=button_4, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_5 = Button(self.root, text="Exercise 5", command=lambda: self.controller.normal_mode(5,0), **button_style)
        self.canvas.create_window(3 * BLANK + 2.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_5, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_6 = Button(self.root, text="Exercise 6", command=lambda: self.controller.normal_mode(6,0), **button_style)
        self.canvas.create_window(3 * BLANK + 2.5 * LABLE_WIDTH, 2.5 * LABLE_HEIGHT + 2 * BLANK + CANVAS_HEIGHT / 3, window=button_6, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_7 = Button(self.root, text="Exercise 7", command=lambda: self.controller.normal_mode(7,0), **button_style)
        self.canvas.create_window(4 * BLANK + 3.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_7, width=LABLE_WIDTH, height=LABLE_HEIGHT)

    #displaying the questions
    def display_questions(self, level, value, review, mode):
        
        self.mode = mode 
        self.question_num += 1
        # reset question num for the review mode
        if self.question_num == 11:
            self.question_num = 0
        # Clear the canvas and display the home button and score
        self.canvas.delete("all")
        self.show_home_button()
        if self.mode==1:
            self.show_score()
        self.canvas.create_window(9 * CANVAS_WIDTH / 10, 9 * CANVAS_HEIGHT / 10, window=self.skip_button, width=100, height=50, tags="skip_button")
        
        #label for the review in normal mode
        if self.mode==1 and review==1:
            label_message = f"Exercise {level}\n {self.question_num+1} / 10"
            exercise_label = Label(self.root, text=label_message, foreground="pink", background="white", font=("Arial", 40, "bold"))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 8, window=exercise_label)
        
        elif self.mode==1:
            label_message = f"Exercise {level}\n {self.question_num} / 10"
            exercise_label = Label(self.root, text=label_message, foreground="pink", background="white", font=("Arial", 40, "bold"))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 8, window=exercise_label)

        #label for the review in the quiz mode
        elif self.mode ==0  and review==1:
            label_message = f"Exercise {level}\n Question {self.question_num-3}/3"
            exercise_label = Label(self.root, text=label_message, foreground="pink", background="white", font=("Arial", 40, "bold"))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 8, window=exercise_label)
        
        else :
            label_message = f"Exercise {level}\n Question {self.question_num}/3"
            exercise_label = Label(self.root, text=label_message, foreground="pink", background="white", font=("Arial", 40, "bold"))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 8, window=exercise_label)


        # Set the message based on the level
        message = None
        #as the values are in tuples, each valuee within the tuple has to be extracted
        if level == 1:
            n=value[0]
            message = f"For the given integer n = {n}, compute its totient using Euler's method."
        elif level == 2:

            
            print("view ex 2",value)
            base=value[0]
            exp=value[1]
            mod=value[2]
            superscript_char = str(exp).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
            message = f"Compute the following expression: {base}{superscript_char}(mod {mod})."
        elif level == 3:

            print("view ex 3",value)
            divisor=value[0]
            rest=value[1]
            mod=value[2]
            message = f"Solve for x: {divisor} × x = {rest} (mod {mod})."
        elif level == 4:

            print("view ex 4",value)
            divisor=value[0]
            rest=value[1]
            mod=value[2]
            superscript_char = str(divisor).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
            message = f"Solve for x: x{superscript_char} = {rest} (mod {mod})."
        elif level == 5:
            print("view ex 5",value)
            p=value[0]
            q=value[1]
            e=value[2]
            message = f"Two secret primes are distributed : {p} and  {q}, the public key is a tuple (g, e) where, \n g is the totient of the secret primes and e is {e}.\n Using your knowledge on RSA algorithm find d of the private key (d,g). "
        elif level == 6:
            print("view ex 6",value)
            p=value[0]
            q=value[1]
            e=value[2]
            m=value[3]
            message = f"Two secret primes are distributed : {p} and  {q}, the public key is a tuple (g, e) where, \n g is the totient of the secret primes and e is {e}.Knowing that the encrypted message m is {m}, \n Using your knowledge on RSA algorithm find d of the private key (d,g) to decrypt the message m."
        elif level == 7:
            print("view ex 7",value)
            mess=value[0]
            key=value[1]
            mod=value[2]
            message = f" Any given integer between 0 and 30 is associated to a letter or a symbol in the following way : \n A->0, B->1, C->2 ... Z->25 and α->26, β->27, γ->28, δ ->29, ε->30 \n Every integer x undergoes an encryption transformation such that x becomes y, \n where y is the remainder of the divison of {mod} by x. \n Knowing that the decryption key is {key}, \n Decrypt the following message {mess}." 

        # Create label for the question
        if level ==7 or level ==6 or level ==5:
            question_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 20))
            self.canvas.create_window(CANVAS_WIDTH / 2, 1.50* CANVAS_HEIGHT / 4, window=question_label)
        
        else:
            question_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 4, window=question_label)

        if review == 0:
                self.canvas.create_window(9 * CANVAS_WIDTH / 10, 9 * CANVAS_HEIGHT / 10, window=self.skip_button, width=100, height=50, tags="skip_button")
                # Create label for the instruction
                label_message = "Please key in your answer:"
                instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
                self.canvas.create_window(CANVAS_WIDTH / 2, 2 * CANVAS_HEIGHT / 3, window=instruction_label)

                # Create text entry box
                self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
                self.entry.bind("<Return>", self.on_return_pressed)
                self.canvas.create_window(CANVAS_WIDTH / 2, 3 * CANVAS_HEIGHT / 4, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        #display of the review for questions   
        if review == 1:
             # Create button to go to next question
            next_button = Button(self.root, text="NEXT", command=lambda: self.controller.review(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 9 * CANVAS_HEIGHT / 10, window=next_button, width=100, height=50)

            # show answer
            answer = self.controller.get_answer_for_review()
            #answer = self.controller.get_answer_for_review(self.question_num)
            label_message = f"The answer is {answer}"
            label = Label(self.root, text=label_message, foreground="green", background="palegreen", font=font.Font(family="Arial", size=28, weight="bold"))
            self.canvas.create_window(CANVAS_WIDTH / 2, 6 * CANVAS_HEIGHT / 8, window=label)

    
        self.level=level
        return self. level
    
    def end_of_review(self):
        self.canvas.delete("all")
        self.show_home_button()
        label_message = " This is the end of review, please return back to the main menu"
        label = Label(self.root, text=label_message, font= ("Arial", 20))
        self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, window=label)

    #show result based on user input
    def show_result(self, result):
        self.canvas.delete("skip_button")
        fg_color = "red"
        if result[0] == 0:
            message = f"You answer was wrong :( \n The correct answer is: {result[1]}"
            fg_color = "red"
        elif result[0] == 1:
            message = "Your answer is correct! Well done!"
            fg_color = "green"
        elif result[0] == 2:
            message = "You answer was not valid :("
            label = Label(self.root, text=message, foreground=fg_color, background="#F6D55C", font=font.Font(family="Arial", size=28, weight="bold"))
            self.canvas.create_window(CANVAS_WIDTH / 2, 7 * CANVAS_HEIGHT / 8, window=label, tags="error")
            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.entry.bind("<Return>", self.on_return_pressed)
            self.canvas.create_window(CANVAS_WIDTH / 2, 3 * CANVAS_HEIGHT / 4, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)
            return
        
        elif result[0] == 3:
            message = f"You skipped the question :( \n The correct answer is: {result[1]}"
        
        label = Label(self.root, text=message, foreground=fg_color, background="#F6D55C", font=font.Font(family="Arial", size=28, weight="bold"))
        self.canvas.create_window(CANVAS_WIDTH / 2, 7 * CANVAS_HEIGHT / 8, window=label)

        if self.mode == 0:

        # Create button to go to next question
            next_button = Button(self.root, text="NEXT", command=lambda: self.controller.normal_mode(self.level,self.question_num), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 9 * CANVAS_HEIGHT / 10, window=next_button, width=100, height=50)
        
        else :
            next_button = Button(self.root, text="NEXT", command=lambda: self.controller.random_question_generator(), font=font.Font(family="Arial", size=16, weight="bold"),foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 9 * CANVAS_HEIGHT / 10, window=next_button, width=100, height=50)
        
    #when return key  is pressed answer is sumbitted
    def on_return_pressed(self, bool):
        input = self.entry.get()
        self.entry.config(state='disabled')
        self.entry.unbind("<Return>")
        self.controller.check_answer(input)
    
    #skip button 
    def skip(self):
        self.entry.config(state='disabled')
        self.entry.unbind("<Return>")
        self.controller.check_answer(None)
    

    def update_score(self, score):
        self.score = score
    
    def show_score(self):
        score_label = Label(self.root, text=f'Score: {self.score}')
        self.canvas.create_window((9 * CANVAS_WIDTH / 10, CANVAS_HEIGHT / 10), window=score_label, width=100, height=50)

    
    #meassage that appears at the end of set of exercises or random question generator and gives the option to review questions
    def show_summary(self,mode):

        if mode == 1:
            self.canvas.delete("all")
            self.show_home_button()
            self.show_review_button()
            score_label = Label(self.root, text=("Congratulations ! You have reached the end of the quiz. \n You got: \n" + str(self.score)+ "\n Would you like to review each answer? , click review \n Find your rankings in the ranking page!"), font= ("Arial", 20))
            self.controller.send_score(self.score)
            self.canvas.create_window((CANVAS_WIDTH / 2, 2*CANVAS_HEIGHT /5), window=score_label)


        if mode == 0:
            self.canvas.delete("all")
            self.show_home_button()
            self.show_review_button()
            message = "Congratulations ! You have reached the end of the training exercise.\n Would you like to review each answer ?, click review"
            label = Label(self.root, text=message, font=("Arial", 20))
            self.canvas.create_window(CANVAS_WIDTH / 2, 2 * CANVAS_HEIGHT / 5, window=label)


    def show_review_button(self):

        review_button = Button(self.root, text="REVIEW", command=self.controller.review, foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF", font=("Arial", 40))
        self.canvas.create_window(CANVAS_WIDTH / 2, 3 * CANVAS_HEIGHT / 5, window=review_button, width=200, height=100)



    #creates a pop up window with scores from all the attempts and the date, retriveves the datafrom the databas e
    
    def show_rankingrqg(self):
        
        #query to the database 
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Athelstan2006&",
            database = "ranking"
        )

        mycursor= db.cursor()
        mycursor.execute("SELECT * FROM testscores")

        #creating new window
        my_w = tk.Tk()
        my_w.geometry("300x700") 
        
        #displays table 
        e=Label(my_w,width=10,text='Attempt n°',borderwidth=2,anchor='c',bg='LightSkyBlue1')
        e.grid(row=0,column=0)
        e=Label(my_w,width=10,text='Date',borderwidth=2,anchor='c',bg='LightSkyBlue1')
        e.grid(row=0,column=1)
        e=Label(my_w,width=10,text='Score',borderwidth=2,anchor='c',bg='LightSkyBlue1')
        e.grid(row=0,column=2)
        
        i=1
        for x in mycursor: 
            for j in range(len(x)):
                e = Entry(my_w, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, x[j])
            i=i+1
        for x in mycursor: 
            for j in range(len(x)):
                e = Entry(my_w, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, x[j])
            i=i+1

   
   
    # main menu to give new valuees for the exercises      
   
    def show_create_questions(self):
        self.canvas.delete("all")

        self.show_home_button()

        message = Label(self.root, text="   Select Exercise Type  ", foreground="pale green", background="white", font=("Arial", 60, "bold"))
        x0, y0, x1, y1 = self.canvas.bbox(self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=message))
        self.canvas.create_oval(x0, y0, x1, y1, fill="white", outline="pink", width=4)


        for i in range (4):
            message = Label(self.root, text=("Level " + str(i + 1)), foreground="black",bg="LightSkyblue1",font=("Arial", 40,"bold"))
            self.canvas.create_window((i + 1) * BLANK + (i + 0.5) * LABLE_WIDTH, LABLE_HEIGHT * 0.5 + CANVAS_HEIGHT / 3, window=message)

        button_style = {
            'font': ('Arial', 25),
            'bg': '#2196f3',
            'fg': 'black',
            'activebackground': '#0d47a1',
            'activeforeground': 'white',
            'bd': 0,
            'highlightthickness': 0
        }

        button_1 = Button(self.root, text="Exercise Type 1", command=lambda: self.controller.show_create_form(1), **button_style)
        self.canvas.create_window(BLANK + 0.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_1, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_2 = Button(self.root, text="Exercise Type 2", command=lambda: self.controller.show_create_form(2), **button_style)
        self.canvas.create_window(BLANK + 0.5 * LABLE_WIDTH, 2.5 * LABLE_HEIGHT + 2 * BLANK + CANVAS_HEIGHT / 3, window=button_2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_3 = Button(self.root, text="Exercise Type 3", command=lambda: self.controller.show_create_form(3), **button_style)
        self.canvas.create_window(2 * BLANK + 1.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_4 = Button(self.root, text="Exercise Type 4", command=lambda: self.controller.show_create_form(4), **button_style)
        self.canvas.create_window(2 * BLANK + 1.5 * LABLE_WIDTH, 2.5 * LABLE_HEIGHT + 2 * BLANK + CANVAS_HEIGHT / 3, window=button_4, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_5 = Button(self.root, text="Exercise Type 5", command=lambda: self.controller.show_create_form(5), **button_style)
        self.canvas.create_window(3 * BLANK + 2.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_5, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_6 = Button(self.root, text="Exercise Type 6", command=lambda: self.controller.show_create_form(6), **button_style)
        self.canvas.create_window(3 * BLANK + 2.5 * LABLE_WIDTH, 2.5 * LABLE_HEIGHT + 2 * BLANK + CANVAS_HEIGHT / 3, window=button_6, width=LABLE_WIDTH, height=LABLE_HEIGHT)

        button_7 = Button(self.root, text="Exercise Type 7", command=lambda: self.controller.show_create_form(7), **button_style)
        self.canvas.create_window(4 * BLANK + 3.5 * LABLE_WIDTH, 1.5 * LABLE_HEIGHT + BLANK + CANVAS_HEIGHT / 3, window=button_7, width=LABLE_WIDTH, height=LABLE_HEIGHT)
    

    #show error if invalid imput is given
    def show_error_1(self):
        
        message = "You answer was not valid :("
        label = Label(self.root, text=message, foreground="red", background="#F6D55C", font=font.Font(family="Arial", size=28, weight="bold"))
        self.canvas.create_window(CANVAS_WIDTH / 2, 7 * CANVAS_HEIGHT / 8, window=label, tags="error")
        self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
        self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 3, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)
            
        submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex1(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
        self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)
        #self.canvas.delete(label)
    
    
    #sends user input to the controller, value is then passed to model to be sent to the database
    def send_input_ex1(self):
        input = self.entry.get()
        self.entry.config(state='disabled')
        print(input)
        self.controller.values_for_exercise1(input)
    
    def send_input_ex2(self):
        input = self.entry.get()
        input2 = self.entry2.get()
        input3 = self.entry3.get()
        self.entry.config(state='disabled')
        self.entry2.config(state='disabled')
        self.entry3.config(state='disabled')
        print(input,input2,input3)
        self.controller.values_for_exercise2(input,input2,input3)
    
    def send_input_ex3(self):
        input = self.entry.get()
        input2 = self.entry2.get()
        input3 = self.entry3.get()
        self.entry.config(state='disabled')
        self.entry2.config(state='disabled')
        self.entry3.config(state='disabled')
        print(input,input2,input3)
        self.controller.values_for_exercise3(input,input2,input3)

    def send_input_ex4(self):
        input = self.entry.get()
        input2 = self.entry2.get()
        input3 = self.entry3.get()
        self.entry.config(state='disabled')
        self.entry2.config(state='disabled')
        self.entry3.config(state='disabled')
        print(input,input2,input3)
        self.controller.values_for_exercise4(input,input2,input3)
    
    def send_input_ex5(self):
        input = self.entry.get()
        input2 = self.entry2.get()
        input3 = self.entry3.get()
        self.entry.config(state='disabled')
        self.entry2.config(state='disabled')
        self.entry3.config(state='disabled')
        print(input,input2,input3)
        self.controller.values_for_exercise5(input,input2,input3)
    
    def send_input_ex6(self):
        input = self.entry.get()
        input2 = self.entry2.get()
        input3 = self.entry3.get()
        input4 = self.entry4.get()
        self.entry.config(state='disabled')
        self.entry2.config(state='disabled')
        self.entry3.config(state='disabled')
        self.entry4.config(state='disabled')
        print(input,input2,input3,input4)
        self.controller.values_for_exercise6(input,input2,input3,input4)
    
    def send_input_ex7(self):
        input = self.entry.get()
        input2 = self.entry2.get()
        input3 = self.entry3.get()
        self.entry.config(state='disabled')
        self.entry2.config(state='disabled')
        self.entry3.config(state='disabled')
        print(input,input2,input3)
        self.controller.values_for_exercise7(input,input2,input3)
    

    # creates a form for each question, where the parameters need to be entered 
    
    def show_create_form(self,level):

    
        self.canvas.delete("all")
        self.show_home_button()

        #instructions for adding the values
        message = None
        
        if level == 1:
            message = f" New set of questions for Exercise 1"

            new_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=new_label)
            
            label_message = "Please enter an integer:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 3, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)
            
            submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex1(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)



        elif level == 2:

            message = f" New set of questions for Exercise 2"

            new_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=new_label)
            
            label_message = "Please enter an integer for the base:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 3, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the exponent:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2 * CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry2 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  1.75* CANVAS_HEIGHT / 3, window=self.entry2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the modulo:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  3* CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry3 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2.50* CANVAS_HEIGHT / 3, window=self.entry3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex2(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)

        
        elif level == 3 or level == 4 :

            if level == 3:

                message = f" New set of questions for Exercise 3"
            else :
                message = f" New set of questions for Exercise 4"

            new_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=new_label)

            label_message = "Please enter an integer for the divisor:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 3, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the rest:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2 * CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry2 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  1.75* CANVAS_HEIGHT / 3, window=self.entry2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the modulo:"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  3* CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry3 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2.50* CANVAS_HEIGHT / 3, window=self.entry3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex3(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)

        
        elif level == 5:

            message = f" New set of questions for Exercise 5"

            new_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=new_label)

            label_message = "Please enter an integer for the secret prime 'p':"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 3, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the secret prime 'q':"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2 * CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry2 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  1.75* CANVAS_HEIGHT / 3, window=self.entry2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for 'e':"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  3* CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry3 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2.50* CANVAS_HEIGHT / 3, window=self.entry3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex5(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)


        elif level == 6:
            
            message = f" New set of questions for Exercise 6"

            new_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 7, window=new_label)

            label_message = "Please enter an integer for the secret prime 'p':"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 5, window=instruction_label)

            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2, 1.15 * CANVAS_HEIGHT / 4, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the secret prime 'q':"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2 * CANVAS_HEIGHT / 5, window=instruction_label)

            self.entry2 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  1.95 * CANVAS_HEIGHT / 4, window=self.entry2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for 'e':"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  3* CANVAS_HEIGHT / 5, window=instruction_label)

            self.entry3 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2.75 * CANVAS_HEIGHT / 4, window=self.entry3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter a secret message 'm' (integer) :"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  4 * CANVAS_HEIGHT / 5, window=instruction_label)

            self.entry4 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  3.55* CANVAS_HEIGHT / 4, window=self.entry4, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex6(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)


            
        elif level == 7:

            message = f" New set of questions for Exercise 7"

            new_label = Label(self.root, text=message, foreground="black", background="white", font=("Arial", 30))
            self.canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 6, window=new_label)

            label_message = "Please enter an encrypted message (string) :"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  CANVAS_HEIGHT / 3, window=self.entry, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for the secret key :"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2 * CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry2 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  1.75* CANVAS_HEIGHT / 3, window=self.entry2, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            label_message = "Please enter an integer for modulo :"
            instruction_label = Label(self.root, text=label_message, foreground="black", background="white", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  3* CANVAS_HEIGHT / 4, window=instruction_label)

            self.entry3 = Entry(self.canvas, width=40, bg="white", fg="black", font=("Arial", 18))
            self.canvas.create_window(CANVAS_WIDTH / 2,  2.50* CANVAS_HEIGHT / 3, window=self.entry3, width=LABLE_WIDTH, height=LABLE_HEIGHT)

            submit_button = Button(self.root, text="SUBMIT", command=lambda: self.send_input_ex7(), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
            self.canvas.create_window(9 * CANVAS_WIDTH / 10, 6 * CANVAS_HEIGHT / 10, window=submit_button, width=100, height=50)


        
        next_button = Button(self.root, text="NEXT", command=lambda: self.controller.show_create_form_next(level), font=font.Font(family="Arial", size=16, weight="bold"), foreground="#4B4E6D", background="#3CAEA3", activebackground="#2C7B8E", activeforeground="#FFF")
        self.canvas.create_window(9 * CANVAS_WIDTH / 10, 9 * CANVAS_HEIGHT / 10, window=next_button, width=100, height=50)
    

