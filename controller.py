import tkinter as tk
import random
from view import View
from model import Model

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.view = View(self.root, self)
        self.score = 0
        self.time = 100 #need to fix
        self.values = []
        self.val=0
        self.level = 0
        self.levels = []
        self.question_num = 0
        self.ranking = []
        self.mode = None
        self.model = Model()
        self.root.mainloop()

    def normal_mode_menu(self):
        self.view.normal_mode_menu()

    #function to work the normal mode 
    def normal_mode(self, level, question_num):
        self.mode=0
        self.question_num= question_num
        if self.question_num == 0:
            self.level = level
        else :
            self.question_num += 1
            #question is appended and so is value (see lines below) in order to display the review later on 
            # with the correct questions (and values) in the correct order 
            self.levels.append(self.level)
        ##3 questions are displayed per training exercise 
        if self.question_num==4:
            # after final question is answered summary is displayed
            self.show_summary()
            return
        self.val = self.get_values(level)
        #values for the question are passed from get_value function
        self.values.append(self.val)
        #list appends the values for the review 
      
        #display correct question with the correct values
        self.view.display_questions(self.level,self.val,0,0)
        
        return self.val 
    
    #function to work the random question generator mode
    def random_question_generator(self):
        self.mode=1
        self.question_num += 1
        if self.question_num == 1:
            self.mode = 1
        #The limit is set to 10 questions over all exercises
        if self.question_num == 11:
            #if last question is accomplished, show summery with score
            self.show_summary()
            return
        #chooses a random level to display a question from
        self.level = random.randint(1, 7)
        #appends question for the review (same way as for normal mode)
        self.levels.append(self.level)
        #value for the question is passed
        values_for_question=self.get_values(self.level)
        #append value for the review
        self.values.append(values_for_question)
        #display question with paramters
        self.view.display_questions(self.level, values_for_question,0,1)
       

    #function that gets the a tuple of values for each question from the model
    def get_values(self,level):
        
        if level==1:
            self.val = self.model.retrieve_values_ex1()
            return self.val
        
        elif level ==2: 
            self.val = self.model.retrieve_values_ex2()
            return self.val
        
        elif level == 3:
            self.val = self.model.retrieve_values_ex3()
            return self.val 
        
        elif level == 4:
            self.val = self.model.retrieve_values_ex4()
            return self.val
        
        elif level == 5 :
            self.val = self.model.retrieve_values_ex5()
            return self.val 
        
        elif level == 6 :
            self.val = self.model.retrieve_values_ex6()
            return self.val 
       
        elif level ==7 :
            self.val = self.model.retrieve_values_ex7()
            return self.val 

    #checks the user input and depending on mode updates the score 
    def check_answer(self, input):
        val = self.val
        if input != None: 
            result=self.model.check_answer(input,self.level,val)
            # for random generator mode, the score is obtained
            if result[0]:
                self.score = self.model.calculate_score(result[0])
            else:
                self.score = self.model.calculate_score(result[0])
        #user skipped the question so the result is shown
        elif input == None:
            answer = self.model.check_answer(1, self.level, val)
            result = [3, answer[1]]
        
        #if user answered correctly, the score is updated
        self.view.update_score(self.score)
        if self.mode==1:
            self.view.show_score()
        #show result message depeending on the answer given (correct/wrong or skip)
        self.view.show_result(result)
       

    #if in random question generator mode, the final score is sent to the database through the model
    def send_score(self,score):
        self.model.sendtodbrandom(score)


    # At the end of a set of questions, a summary is displayed based on the mode and values are initilised
    def show_summary(self):
        self.question_num = 0
        self.score = 0
        # Random question generator
        if self.mode == 1:
            self.view.show_summary(1)
            #self.view.show_summary(self.ranking, 1)
        # Normal Mode
        elif self.mode == 0:
            self.view.show_summary(0)
            #self.view.show_summary(self.ranking, 0)
    
    # function that works the review
    def review(self):
        self.question_num += 1
        #if the review has reached the last question, end of review message is shown
        if (self.question_num-1)==len(self.levels):
            self.view.end_of_review()
        else:
            #the next quesion in review is diplayed with the associated answer
            self.view.display_questions(self.levels[self.question_num-1], self.values[self.question_num-1],1,self.mode)

    #calculates the answer for question in review (called by view)
    def get_answer_for_review(self):
        print("self.question nm:",self.question_num)
        answer = self.model.calculate_answer(self.levels[self.question_num-1], self.values[self.question_num-1])
        return answer

    #displays ranking in new window
    def show_rankingrqg(self):
        self.view.show_rankingrqg()
    

    #display the UI to allow teachers to add new values for the exercises
    def show_create_questions(self):
        self.view.show_create_questions()
    

    #display the UI to allow teachers to add new values for the exercises 
    def show_create_form(self,level):
        self.level = 0
        self.view.show_create_form(level)
    

    #function that controlls the next button in the create section mode, if the last exercise is reached, 
    # pressing next will go to the create question main page, where useer can choose another question.
    #otherwise it moves to the next exercise 
    def show_create_form_next(self,level):
        if level == 7 :
            self.view.show_create_questions()
        else :
            self.view.show_create_form(level+1)
    
 ### functions that retrieve the useer input from the create question forms and passes them to the model
    # so they can be sent to the database     
    def values_for_exercise1(self,input):
        #checks that the input is valid otherwise throws error and asks for user to type in again
        try:
            print("in try")
            val=int(input)

        except ValueError:
            self.view.show_error_1()
            return

        self.model.values_for_exercise1(val)
    
    def values_for_exercise2(self,input,input2,input3):
        try:
                val=int(input)
                val2=int(input2)
                val3=int(input3)
        except ValueError:
                self.view.show_error_2
        self.model.values_for_exercise2(val,val2,val3)
    
    def values_for_exercise3(self,input,input2,input3):
        val=int(input)
        val2=int(input2)
        val3=int(input3)
        self.model.values_for_exercise3(val,val2,val3)
    
    def values_for_exercise4(self,input,input2,input3):
        val=int(input)
        val2=int(input2)
        val3=int(input3)
        self.model.values_for_exercise4(val,val2,val3)
    
    def values_for_exercise5(self,input,input2,input3):
        val=int(input)
        val2=int(input2)
        val3=int(input3)
        self.model.values_for_exercise5(val,val2,val3)
        
    
    def values_for_exercise6(self,input,input2,input3,input4):
        val=int(input)
        val2=int(input2)
        val3=int(input3)
        val4=int(input4)
        self.model.values_for_exercise6(val,val2,val3,val4)
    
    def values_for_exercise7(self,input,input2,input3):
        #makes string eentered in upercase
        val= input.upper()
        val2=int(input2)
        val3=int(input3)
        self.model.values_for_exercise7(val,val2,val3)
    
    # redirects the user back to the main page 
    def back_to_main(self):
        self.question_num = 0
        self.score = 0
        self.values = []
        self.view.back_to_main()
        self.model.back_to_main()
        
    
   
if __name__ == '__main__':
    app = Controller()
