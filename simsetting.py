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
        self.theortest = None
        self.grid_test = None
        self.osctest = None
        self.osctick = None
        self.branchtest = None
        self.branchset = None
        self.boundstest = None
        self.boundsset = None
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
            self.theortest = Seventh(root)
            root.mainloop()
            if self.theortest.test_values[0]:
                root = Tk()
                root.geometry("500x500")
                self.theorsweep = TheorSweepSelect(root)
                root.mainloop()
            elif self.theortest.test_values[1]:
                root = Tk()
                root.geometry("500x500")
                self.osctest = Osctest(root)
                root.mainloop()
                root = Tk()
                root.geometry("500x500")
                self.osctick = Osctick(root)
                root.mainloop()
            elif self.theortest.test_values[2]:
                root = Tk()
                root.geometry("500x500")
                self.branchtest = BranchProbtest(root)
                root.mainloop()
                root = Tk()
                root.geometry("500x500")
                self.branchset = BranchProbset(root)
                root.mainloop()
            elif self.theortest.test_values[3]:
                root = Tk()
                root.geometry("500x500")
                self.boundstest = BoundsTest(root)
                root.mainloop()
                root = Tk()
                root.geometry("500x500")
                self.boundsset = BoundsSet(root)
                root.mainloop()
        elif self.secondwindow.test_values[7]:
            root = Tk()
            root.geometry("500x500")
            self.grid_test = Eighth(root)
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
                           "Make Different Theoretical Plots",
                           "Run the experimental Code Test",
                           "Static Gridsweep scross K and N"]
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
        self.checkbutton[1].select()
        # creating a button instance
        quitButton = Button(self, text="Next", command=lambda: [self.first_box(), self.master.destroy()])
        quitButton.place(x=0, y=450)

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
        self.users = 100
        self.runs = 1000
        self.init_window()

    def init_window(self):
        self.master.title("Static Tree")
        self.pack(fill=BOTH, expand=1)

        l1 = Label(self.master, text="No of users collided in the first Slot")
        l1.place(x=0, y=0)
        l2 = Label(self.master, text="No of Runs to take the mean throughput")
        l2.place(x=0, y=100)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '500')
        self.e1.place(x=250, y=0)
        self.e2 = Entry(self.master)
        self.e2.insert(0, '1000')
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
        self.master.title("Sweep Through No if Users")
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
        self.simtime = 1000
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

        self.master.title("Sweep Through No if Users")
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
        self.test_names = ["Compare Different Theoretical Formulas",
                           "Length/ThrouhgputVsN",
                           "Optimal Branch Probabilty",
                           "Bounds on Traffic Analysis"]
        self.checkbutton = self.checkbutton * len(self.test_names)
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("Select Theoretical Test")

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
        quitButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.test_names)):
            self.test_values.append(self.var_array[i].get())


class Eighth(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.n1 = 10
        self.n2 = 50
        self.n3 = 100
        self.k_start = 1
        self.k_stop = 10
        self.k_step = 1
        self.runs = 10
        self.param = [self.n1, self.n2, self.n3, self.k_start, self.k_stop, self.k_step, self.runs]
        self.labels = ["First N", "Second N", "Third N",
                       "Start of K sweep", "End of K sweep", "Step of K sweep", "No of runs to average from"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("Grid Sweep Across K and N")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = int(self.e[i].get())
        self.update_param()

    def update_param(self):
        self.n1 = self.param[0]
        self.n2 = self.param[1]
        self.n3 = self.param[2]
        self.k_start = self.param[3]
        self.k_stop = self.param[4]
        self.k_step = self.param[5]
        self.runs = self.param[6]


class TheorSweepSelect(Frame):

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
        l1.place(x=0, y=350)
        l2 = Label(self.master, text="Note - Cannot be higher than 15 if using any Recursive Equation")
        l2.place(x=0, y=400)

        self.e1 = Entry(self.master)
        self.e1.insert(0, '15')
        self.e1.place(x=250, y=350)
        # creating a button instance
        quitButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        quitButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.test_names)):
            self.test_values.append(self.var_array[i].get())
        self.n_stop = int(self.e1.get())


class Osctest(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.k1 = 1
        self.k2 = 2
        self.k3 = 4
        self.k4 = 8
        self.k5 = 16
        self.n_stop = 100
        self.param = [self.k1, self.k2, self.k3, self.k4, self.k5, self.n_stop]
        self.labels = ["First K", "Second K", "Third K", "Fourth K", "Fifth K", "Stop of N sweep"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("Select Test Parameters")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = int(self.e[i].get())
        self.update_param()

    def update_param(self):
        self.k1 = self.param[0]
        self.k2 = self.param[1]
        self.k3 = self.param[2]
        self.k4 = self.param[3]
        self.k5 = self.param[4]
        self.n_stop = self.param[5]

class Osctick(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.test_values = []
        self.var_array = []
        self.checkbutton = [None]
        self.test_names = ["Throughput?", "X scale Log?", "Y scale Log?", "Start N at 1?",
                           "Plot the Max?", "Normalize Length with K"]
        self.checkbutton = self.checkbutton * len(self.test_names)
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("Check Documentation for Settings")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.test_names)):
            self.var_array.append(BooleanVar())
            self.checkbutton[i] = Checkbutton(self.master, text=self.test_names[i], variable=self.var_array[i],
                                              onvalue=True,
                                              offvalue=False)
            self.checkbutton[i].place(x=0, y=50 * i)
        self.checkbutton[0].select()
        self.checkbutton[1].select()
        self.checkbutton[3].select()
        # creating a button instance
        quitButton = Button(self, text="Next", command=lambda: [self.first_box(), self.master.destroy()])
        quitButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.test_names)):
            self.test_values.append(self.var_array[i].get())


class BranchProbtest(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.k1 = 1
        self.k2 = 2
        self.k3 = 4
        self.k4 = 8
        self.k5 = 16
        self.param = [self.k1, self.k2, self.k3, self.k4, self.k5]
        self.labels = ["First K", "Second K", "Third K", "Fourth K", "Fifth K"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("Select K sweep")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = int(self.e[i].get())
        self.update_param()

    def update_param(self):
        self.k1 = self.param[0]
        self.k2 = self.param[1]
        self.k3 = self.param[2]
        self.k4 = self.param[3]
        self.k5 = self.param[4]


class BranchProbset(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.users = 100
        self.p_start = 0.1
        self.p_stop = 0.9
        self.p_step = 0.1
        self.param = [self.users, self.p_start, self.p_stop, self.p_step]
        self.labels = ["Fixed Users", "Start of P Sweep", "Stop of P Sweep", "Step of P Sweep"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("Select P sweep")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = float(self.e[i].get())
        self.update_param()

    def update_param(self):
        self.users = self.param[0]
        self.p_start = self.param[1]
        self.p_stop = self.param[2]
        self.p_step = self.param[3]


class BoundsTest(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.k1 = 1
        self.k2 = 2
        self.k3 = 4
        self.k4 = 8
        self.k5 = 16
        self.param = [self.k1, self.k2, self.k3, self.k4, self.k5]
        self.labels = ["First K", "Second K", "Third K", "Fourth K", "Fifth K"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("Select K sweep")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = int(self.e[i].get())
        self.update_param()

    def update_param(self):
        self.k1 = self.param[0]
        self.k2 = self.param[1]
        self.k3 = self.param[2]
        self.k4 = self.param[3]
        self.k5 = self.param[4]


class BoundsSet(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.m = 50
        self.start = 0.1
        self.stop = 25
        self.no_of_readings = 2500
        self.param = [self.m, self.start, self.stop, self.no_of_readings]
        self.labels = ["M", "Start of LambdaDelta", "Stop of LambdaDelta", "Readings in Between"]
        self.e = [None]
        self.e = self.e * len(self.labels)
        self.init_window()

    def init_window(self):

        self.master.title("M and Lambda_Delta Linspace Settings")
        self.pack(fill=BOTH, expand=1)

        for i in range(len(self.labels)):
            l = Label(self.master, text=self.labels[i])
            l.place(x=0, y=i * 50)
            self.e[i] = (Entry(self.master))
            self.e[i].insert(0, str(self.param[i]))
            self.e[i].place(x=250, y=i * 50)

        NextButton = Button(self, text="Done", command=lambda: [self.first_box(), self.master.destroy()])
        NextButton.place(x=0, y=450)

    def first_box(self):
        for i in range(len(self.labels)):
            self.param[i] = float(self.e[i].get())
        self.update_param()

    def update_param(self):
        self.m = self.param[0]
        self.start = self.param[1]
        self.stop = self.param[2]
        self.no_of_readings = self.param[3]
