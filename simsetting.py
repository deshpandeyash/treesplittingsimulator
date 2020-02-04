from tkinter import *


class SimSetting(object):
    """
    Contains all important simulation setting
    """

    def __init__(self):
        self.firstwindow = None
        self.secondwindow = None
        self.vizwindow = None
        self.statictreewindow = None
        self.usersweep = None
        self.dynamictest = None
        self.theorsweep = None

        self.guiprocess()

    def guiprocess(self):
        root = Tk()
        root.geometry("300x500")
        self.firstwindow = First(root)
        root.mainloop()
        root = Tk()
        root.geometry("300x500")
        self.secondwindow = Second(root)
        root.mainloop()
        if sum(self.secondwindow.test_values) > 1:
            print("Please Select One Test only")
            return
        if self.secondwindow.test_values[0]:
            root = Tk()
            root.geometry("500x300")
            self.vizwindow = Third(root)
            root.mainloop()
        elif self.secondwindow.test_values[1]:
            root = Tk()
            root.geometry("500x300")
            self.statictreewindow = Fourth(root)
            root.mainloop()
        elif self.secondwindow.test_values[2]:
            root = Tk()
            root.geometry("500x300")
            self.usersweep = Fifth(root)
            root.mainloop()
        elif self.secondwindow.test_values[3] or self.secondwindow.test_values[4]:
            root = Tk()
            root.geometry("500x300")
            self.dynamictest = Sixth(root)
            root.mainloop()
        elif self.secondwindow.test_values[5]:
            root = Tk()
            root.geometry("500x500")
            self.theorsweep = Seventh(root)
            root.mainloop()


class First(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.test_values = []
        self.var_array = [IntVar(), IntVar(), BooleanVar(), DoubleVar()]
        self.test_names = ["Biased Split?", "Modified", "Unisplit", "SIC"]
        self.init_window()

    def init_window(self):

        self.master.title("Tree Algorithm Settings")
        self.pack(fill=BOTH, expand=1)

        l1 = Label(self.master, text="Q")
        l2 = Label(self.master, text="K")
        l3 = Checkbutton(self.master, text=self.test_names[0], variable=self.var_array[2], onvalue=True, offvalue=False)
        l4 = Label(self.master, text="Branch Probability if biased")

        l1.place(x=0, y=0)
        l2.place(x=0, y=50)
        l3.place(x=0, y=150)
        l4.place(x=0, y=200)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '2')
        self.e2 = Entry(self.master)
        self.e2.insert(0, '1')
        self.e3 = Entry(self.master)
        self.e3.insert(0, '0.5')

        self.e1.place(x=100, y=0)
        self.e2.place(x=100, y=50)
        self.e3.place(x=100, y=200)

        for i in range(1, len(self.test_names)):
            self.var_array.append(BooleanVar())
            c = Checkbutton(self.master, text=self.test_names[i], variable=self.var_array[i + 3], onvalue=True,
                            offvalue=False)
            c.place(x=0, y=50 * i + 200)

        NextButton = Button(self, text="Next", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=400)

    def first_box(self):
        self.test_values.append(self.e1.get())
        self.test_values.append(self.e2.get())
        self.test_values.append(self.var_array[2].get())
        self.test_values.append(self.e3.get())
        for i in range(len(self.test_names) - 1):
            self.test_values.append(self.var_array[i + 4].get())


class Second(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.test_values = []
        self.var_array = []
        self.checkbutton = [None]
        self.test_names = ["One Visualization of a tree", "Static Tree Simulated Multiple Times",
                           "Sweep Through different values of Users",
                           "Sweep Through different arrival rates in Free Access",
                           "Sweep Through different arrival rates in Gated Access",
                           "Sweep through users only of theoretical formulas"]
        self.checkbutton = self.checkbutton * len(self.test_names)
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("Select Test ( Only One)")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.test_names)):
            self.var_array.append(BooleanVar())
            self.checkbutton[i] = Checkbutton(self.master, text=self.test_names[i], variable=self.var_array[i],
                                              onvalue=True,
                                              offvalue=False)
            self.checkbutton[i].place(x=0, y=50 * i)
        self.checkbutton[0].select()
        # creating a button instance
        quitButton = Button(self, text="Next", command=lambda: [self.first_box(), self.master.destroy()])
        quitButton.place(x=0, y=400)

    def first_box(self):
        for i in range(len(self.test_names)):
            self.test_values.append(self.var_array[i].get())


class Third(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.users = 10
        self.init_window()

    def init_window(self):
        self.master.title("Tree Visualization")
        self.pack(fill=BOTH, expand=1)

        l1 = Label(self.master, text="Collided Users in the first slot")
        l1.place(x=0, y=0)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '10')
        self.e1.place(x=250, y=0)
        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=250)

    def first_box(self):
        self.users = int(self.e1.get())


class Fourth(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.users = 1000
        self.runs = 100
        self.init_window()

    def init_window(self):
        self.master.title("Static Tree")
        self.pack(fill=BOTH, expand=1)

        l1 = Label(self.master, text="No of users collided in the first Slot")
        l1.place(x=0, y=0)
        l2 = Label(self.master, text="No of Runs to take the mean throughput")
        l2.place(x=0, y=100)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '1000')
        self.e1.place(x=250, y=0)
        self.e2 = Entry(self.master)
        self.e2.insert(0, '100')
        self.e2.place(x=250, y=100)
        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=250)

    def first_box(self):
        self.users = int(self.e1.get())
        self.runs = int(self.e2.get())


class Fifth(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.n_stop = 30
        self.runs = 100
        self.init_window()

    def init_window(self):
        self.master.title("Sweep Through No if Users ( < 40")
        self.pack(fill=BOTH, expand=1)

        l1 = Label(self.master, text="Max No of Users")
        l1.place(x=0, y=0)
        l1 = Label(self.master, text="No of Runs to take the mean throughput")
        l1.place(x=0, y=100)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '30')
        self.e1.place(x=250, y=0)
        self.e2 = Entry(self.master)
        self.e2.insert(0, '100')
        self.e2.place(x=250, y=100)
        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=250)

    def first_box(self):
        self.n_stop = int(self.e1.get())
        self.runs = int(self.e2.get())


class Sixth(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.simtime = 10000
        self.runs = 5
        self.start = 0.20
        self.step = 0.05
        self.stop = 0.50
        self.param = [self.simtime, self.runs, self.start, self.step, self.stop]
        self.labels = ["No of slots for each run", "Runs to average for each arrival rate", "Arrival rate start",
                       "Arrival rate increment step", "Arrival rate stop"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("Sweep Through No if Users ( < 40")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=250)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = float(self.e[i].get())
            if i < 2:
                self.param[i] = int(self.param[i])
        self.update_param()

    def update_param(self):
        self.simtime = self.param[0]
        self.runs = self.param[1]
        self.start = self.param[2]
        self.step = self.param[3]
        self.stop = self.param[4]


class Seventh(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.test_values = []
        self.var_array = []
        self.checkbutton = [None]
        self.test_names = ["Quick Template - OWN PAPER", "SICTA",
                           "Captenakis Simple Tree",
                           "Recursive SICTA",
                           "Recursive Own Paper", "Giannakis QSICTA"]
        self.checkbutton = self.checkbutton * len(self.test_names)
        self.n_stop = 10
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("Theoretical N- sweep")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.test_names)):
            self.var_array.append(BooleanVar())
            self.checkbutton[i] = Checkbutton(self.master, text=self.test_names[i], variable=self.var_array[i],
                                              onvalue=True,
                                              offvalue=False)
            self.checkbutton[i].place(x=0, y=50 * i)
        self.checkbutton[0].select()

        l1 = Label(self.master, text="Max Numbers of users in the Sweep")
        l1.place(x=0, y=300)
        l2 = Label(self.master, text="Note - Cannot be higher than 15 if using any Recursive Equation")
        l2.place(x=0, y=350)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '15')
        self.e1.place(x=250, y=300)
        # creating a button instance
        quitButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        quitButton.place(x=0, y=400)

    def first_box(self):
        for i in range(len(self.test_names)):
            self.test_values.append(self.var_array[i].get())
        self.n_stop = int(self.e1.get())
