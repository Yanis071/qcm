#-*-coding:utf8;-*-
#qpy:console

import sqlite3
from tkinter import *
import scroll_list as Slist

conn=sqlite3.connect("data.sq3")
cur=conn.cursor()

class Adtool(object):
    def __init__(self):
        self.root= Tk()
        self.root.title('Adtool')
        cur.execute("select question from question")
        self.listbox = Slist.ListBox(self.root, cur)            #Slist.ListBox = module pour fabriquer une liste avec scroll
        self.listbox.grid(row = 1, column = 1, rowspan=5)
        
        #liste des id de chaque question :
        cur.execute("select id from question")
        self.list = []    
        for it in cur:
            self.list.append(it[0])
            
        Button(self.root, text='Modify', command=self.modify).grid(row = 1, column = 2)
        Button(self.root, text='Delete', command=self.delete).grid(row=2, column=2)
        Button(self.root, text='Add', command=self.add).grid(row=3, column=2)
        Button(self.root, text='Quit', command=self.root.destroy).grid(row=4, column=2)

    def update(self):
        self.root.destroy()
        self.__init__()
        self.root.mainloop()
        
    def modify(self):        
        self.Wmodify = Toplevel(self.root)                  #nouvelle fenetre
        self.select = self.listbox.bListe.curselection()    #sortir choix liste 
        self.select = self.select[0]                        #prendre juste le chiffre car tupple
        self.id = self.list[self.select]
        for it in cur.execute("select question,answer,good_answer,difficulty,subject from question where id=?",(self.id,)):
            self.quest = it
        self.entry = []             #liste contenant les entrée
        for it in self.quest:
            self.entry.append(Entry(self.Wmodify, width=30))
            self.entry[-1].insert(0,it)
            self.entry[-1].pack()
        
        Button(self.Wmodify, text='Save', command=self.modify_save).pack()
        Button(self.Wmodify, text='Cancel', command=self.Wmodify.destroy).pack(side=RIGHT)

    def modify_save(self):          #save for modify settings
        cur.execute("update question set difficulty=? where id=?",(self.entry[3].get(),self.id))
        cur.execute("update question set subject=? where id=?",(self.entry[4].get(),self.id))
        cur.execute("update question set answer=? where id=?",(self.entry[1].get(),self.id))
        cur.execute("update question set question=? where id=?",(self.entry[0].get(),self.id))
        cur.execute("update question set good_answer=? where id=?",(self.entry[2].get(),self.id))
        conn.commit()
        self.update()


    def delete(self):
        self.Wdelete = Toplevel(self.root)
        self.select = self.listbox.bListe.curselection()        #current selection
        self.select = self.select[0]                            #prendre chiffre car tuple
        self.select = self.list[self.select]                    #prendre reel id et non index
        for it in cur.execute("select question from question where id=?",(self.select,)):
            Label(self.Wdelete, text='Do you really want to delete :').pack()
            Label(self.Wdelete, text=it).pack()
        Button(self.Wdelete, text='Cancel', command=self.Wdelete.destroy).pack(side=RIGHT)
        Button(self.Wdelete, text='Delete', command=self.delete_delete).pack(side=LEFT)

    def delete_delete(self):
        cur.execute("delete from question where id=?",(self.select,))
        conn.commit()
        self.update()

    def add(self):
        self.Wadd = Toplevel(self.root)
        self.label = ('Question :', 'Answer :(...@...@...)', 'Dificulty :', 'Subject :', 'Good answer :')
        self.entry = []
        for it in self.label:
            self.entry.append(Entry(self.Wadd, width=30))
            self.entry[-1].insert(0, it)
            self.entry[-1].pack()
        Button(self.Wadd, text='Cancel', command=self.Wadd.destroy).pack(side=RIGHT)
        Button(self.Wadd, text='Save', command=self.add_save).pack(side=LEFT)

    def add_save(self):
        cur.execute("insert into question(question,answer,difficulty,subject,good_answer) values(?,?,?,?,?)",(self.entry[0].get(),
                                                                                                              self.entry[1].get(),
                                                                                                              self.entry[2].get(),
                                                                                                              self.entry[3].get(),
                                                                                                              self.entry[4].get()))
        conn.commit()
        self.update()


class Login(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Qcm login')
        self.label = Label(self.root, text='Username :')
        self.label.pack()
        self.entry = Entry(self.root)
        self.entry.bind("<Return>",self.login)
        self.entry.pack()
        self.root.mainloop()

    def login(self,event):
        if self.entry.get() == 'admin':
            self.label.configure(text='Password :')
            self.entry.delete(0,END)
            self.entry.configure(show="*")
            self.entry.bind("<Return>",self.passw)
        else:
            Luser = []
            for it in cur.execute("select username from user"):
                Luser.append(it[0])
            if self.entry.get() in Luser:
                Choice(self.entry.get())
                self.root.destroy()
            else:
                cur.execute("insert into user(username) values(?)",(self.entry.get(),))
                Choice(self.entry.get())
                self.root.destroy()

    def passw(self,event):
        if self.entry.get() == 'admin':
            Adtool()


class Choice(object):
    def __init__(self, username):
        self.root = Tk()
        self.root.title('Qcm')
        self.username = username    
        self.Bdifficulty = Button(self.root, text='Difficulty', command=self.difficulty_choice)
        self.Bdifficulty.grid(row=1, column=1, pady=5, padx=5)
        self.Bsubject = Button(self.root, text='Subject', command=self.subject_choice)
        self.Bsubject.grid(row=2, column=1, pady=5, padx=5)
        Button(self.root, text='All', command=self.all).grid(row=3, column=1, pady=5, padx=5)
        Button(self.root, text='Quit', command=self.root.destroy).grid(row=4, column=4)
        Label(self.root, text=self.username).grid(row=2, column=2, columnspan=2)
        #take best score of username :
        cur.execute("select bestscore from user where username=?",(self.username,))
        for it in cur:
            if it:
                Label(self.root, text='Best score : '+str(it[0])).grid(row=3, column=2, columnspan=2)

    def difficulty_choice(self):
        self.Bdifficulty.destroy()
        Label(self.root, text='Difficulty :').grid(row=1, column=1)
        Button(self.root, text=1, command=lambda: self.difficulty(1)).grid(row=1, column=2)
        Button(self.root, text=2, command=lambda: self.difficulty(2)).grid(row=1, column=3)
        Button(self.root, text=3, command=lambda: self.difficulty(3)).grid(row=1, column=4)

    def difficulty(self, diff):
        cur.execute("select question,answer,good_answer from question where difficulty=?",(diff,))
        self.game()

    def subject_choice(self):
        self.Bsubject.destroy()
        cur.execute("select subject from question")       
        self.list = []          #liste des sujets pour eviter les doublons :
        for it in cur:
            if it not in self.list:
                self.list.append(it[0])
        self.listbox = Slist.ListBox(self.root, self.list)
        self.listbox.grid(row=2, column=1)
        Button(self.root, text='Play', command=self.subject).grid(row=4, column=1)

    def subject(self):
        select = self.listbox.bListe.curselection()
        select = select[0]
        select = self.list[select]
        cur.execute("select question,answer,good_answer from question where subject=?",(select,))
        self.game()
    
    def all(self):
        cur.execute("select question,answer,good_answer from question")
        self.game()

    def game(self):
        self.score = 0
        self.questions = []
        self.answers = []
        self.good_answers = []
        for it in cur:
            self.questions.append(it[0])
            self.answers.append(it[1])
            self.good_answers.append(it[2])

        self.count_question = len(self.questions)
        self.play()

    def play(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title('Game')
        self.question = Label(self.root, text=self.questions[0])
        self.question.grid(row=1, column=1)
        self.answer = self.answers[0].split('@')
        self.var = StringVar()
        for it in self.answer:
            index = self.answer.index(it)
            Radiobutton(self.root, text=it, variable=self.var, value=it).grid(row=index+2, column=1)
        Button(self.root, text='Submit', command=self.submit).grid(row=index+3,column=1)

    def submit(self):
        if self.var.get() == self.good_answers[0]:
            self.score += 1
        self.questions, self.answers, self.good_answers = self.questions[1:], self.answers[1:], self.good_answers[1:]
        if not self.questions:
            self.end()
        else:
            self.play()

    def end(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title('END')
        Label(self.root, text=self.username).pack()
        Label(self.root, text=str(self.score)+" bonnes reponses sur "+str(self.count_question)).pack()
        Button(self.root, text='Try again', command=lambda: (self.root.destroy() , Choice(self.username))).pack(side=LEFT)
        Button(self.root, text='Quit', command=self.root.destroy).pack(side=RIGHT)
        for it in cur.execute("select bestscore from user where username=?",(self.username,)):
            if it[0]:
                if self.score > it[0]:
                    cur.execute("update user set bestscore=? where username=?",(self.score, self.username))
            else:
                cur.execute("update user set bestscore=? where username=?",(self.score, self.username))
            conn.commit()

Login()
#bonjour
