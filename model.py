import random
import mysql.connector 
from datetime import date
from sympy.ntheory.factor_ import totient
import random


class Model:
    def __init__(self):
        self.answer = 0
        self.score = 0
        self.ranking = []
        
    
    def back_to_main(self):
        self.score = 0

    #calculates answer for given question in order to compare it with user input
    def calculate_answer(self, level, val):
    
        if level == 1:
            answer = self.exercise1(val)
        elif level == 2 or level == 4 or level == 6:
            answer = self.exercise2_4_6(val)
        elif level == 3:
            answer = self.exercise3(val)
        elif level == 5:
            answer = self.exercise5(val)
        elif level == 7:
            answer = self.exercise7(val)
        return answer

    #checks the answer given by the user with the one calculated
    def check_answer(self, user_answer, level, question_num):
        self.answer = self.calculate_answer(level, question_num)
        #checks whether user answer is valid, if not in correct format throws error and asks user to retype the answer
        if level != 7:
            try: 
                user_answer = int(user_answer)
            except ValueError:
                return [2, self.answer]
        if level == 7:
            if not str(user_answer).isalpha():
                return [2, self.answer]
            else : 
                #for question 7, trnasforms user input into correct format for comparing
                temp= user_answer.upper()
                user_answer=[]
                for i in range(len(temp)):
                    char = temp[i]
                    user_answer.append(char)
        #comparison 
        if user_answer == self.answer:
            return [1, self.answer]
        else:
            return [0, self.answer]
          

    def calculate_score(self, bool):
        if bool:
            self.score += 100
        return self.score
    
    # query to SQL database with to insert in the ranking table the score and time of the attempt  
    def sendtodbrandom(self,score):
        date_ = date.today()
        points=score
    
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Athelstan2006&",
            database = "ranking"
        )
        mycursor= db.cursor()
        mycursor.execute("INSERT INTO testscores (`date`,`score`) VALUES (%s,%s)",(date_,points))
        db.commit()
        db.close()
        print("Inserted",mycursor.rowcount,"row(s) of data.")
   
###exercises to calculate answer at each question
    def exercise1(self, n):
        int_n= int(n[0])
        answer=totient(int_n)
        return answer

    def exercise2_4_6(self,tuple):
        base=int(tuple[0])
        exponent=int(tuple[1])
        modulo=int(tuple[2])
        answer = pow(base,exponent,modulo)
        return answer
    
    def exercise3(self,tuple):
        div=int(tuple[0])
        r=int(tuple[1])
        modulo=tuple[2]
        for x in range(0,modulo):
            if ((div*x - r)%modulo)== 0:
                return x

    def exercise5(self, tuple):
        p=int(tuple[0])
        q=int(tuple[1])
        e=int(tuple[2])
        pq=p*q
        phi_pq=totient(pq)
        answer=(phi_pq+1)/e
        return answer

    def exercise7(self, tuple):
        a=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','al','be','ga','de','ep','et']
        encoded_word=tuple[0]
        print(encoded_word)
        key=int(tuple[1])
        modulo=int(tuple[2])
        answer=[]
        for letter in encoded_word:
                val= a.index(letter)
                newval = (val**key)%modulo
                newletter = a[newval]
                answer.append(newletter)
        return answer
    

### Send SQL query to insert the user input for the parameters of each question in their respective tables of the database
    def values_for_exercise1(self,val):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor= db.cursor()
        sql = "INSERT INTO exercise1 (number) VALUES (%s)"
        mycursor.execute(sql, (val,))
        print("Inserted",mycursor.rowcount,"row(s) of data.")
        db.commit()
        db.close()


    def values_for_exercise2(self,base,exp,mod):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO exercise2 (`base`,`exponent`,`mod`) VALUES (%s,%s,%s)", (base,exp,mod))
        db.commit()
        db.close()
        
    def values_for_exercise3(self,div,rest,mod):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO exercise3 (`divisor`,`rest`,`modulo`) VALUES (%s,%s,%s)", (div,rest,mod))
        db.commit()
        db.close()
        

    def values_for_exercise4(self,div,rest,mod):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO exercise4 (`divisor`,`rest`,`modulo`) VALUES (%s,%s,%s)", (div,rest,mod))
        db.commit()
        db.close()


    def values_for_exercise5(self,p,q,e):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO exercise5 (`p`,`q`,`e`) VALUES (%s,%s,%s)", (p,q,e))
        db.commit()
        db.close()


    def values_for_exercise6(self,p,q,e,m):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO exercise6 (`p`,`q`,`e`,`m`) VALUES (%s,%s,%s,%s)", (p,q,e,m))
        db.commit()
        db.close()
    

    def values_for_exercise7(self,mess,key,mod):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO exercise7 (`encrypted_message`,`key`,`mod`) VALUES (%s,%s,%s)", (mess,key,mod))
        db.commit()
        db.close()

#### SQL query to get values from the database and use for exercise questions.
    ## In order to avoid displaying the question with the same parameters in the same order everytime, all the values for an exercise are collected 
    ## from respective table and stored in a list which is then shuffled and the first element of the list is passed to the controller.
    ##here the parameters are sent from the database in tuples, so the selected tuple is sent to the controller.

    def retrieve_values_ex1(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT number FROM exercise1 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple
                

    def retrieve_values_ex2(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT `base`,`exponent`,`mod` FROM exercise2 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple


    def retrieve_values_ex3(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT `divisor`,`rest`,`modulo` FROM exercise3 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple
    
    def retrieve_values_ex4(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT `divisor`,`rest`,`modulo` FROM exercise4 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple
    
    def retrieve_values_ex5(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT `p`,`q`,`e` FROM exercise5 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple

    
    def retrieve_values_ex6(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT `p`,`q`,`e`,`m` FROM exercise6 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple
            
    
    def retrieve_values_ex7(self):
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Athelstan2006&",
                database = "questions"
            )
        mycursor = db.cursor()
        mycursor.execute("SELECT `encrypted_message`,`key`,`mod` FROM exercise7 ")
        integers=[]
        for x in mycursor:
                integers.append(x)
        random.shuffle(integers)
        tuple=integers[0]
        return tuple
