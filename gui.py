from tkinter import *
import subprocess

METHODS = ["naive-hashing", "pk-based", "server-aided", "ot-based"]

class GUI(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.title("PSI Demonstation")
        
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('%dx%d+0+0' % (width,height))

        self.expected_displayed = False
        self.results_displayed = False
        self.hashing_displayed = False

        self.display_method_options()
        self.display_initial_lists()
        self.display_submit_button()

    def display_method_options(self):
        frame = Frame(self)
        frame.pack()

        method_label = Label(frame, text="Please select the PSI method: ")
        method_label.pack(side=LEFT, padx=10, pady=10)
        
        self.method = StringVar(self)
        self.method.set(METHODS[3]) # default value

        method_options = OptionMenu(frame, self.method, METHODS[0], METHODS[1], METHODS[2], METHODS[3])
        method_options.pack(padx=10, pady=10)

    def display_initial_lists(self):
        
        def get_lines(filepath):
            initial_list = ""
            with open(filepath, "r") as f:
                for line in f:
                    initial_list = initial_list + line
            return initial_list

        self.listA = get_lines("sample_sets/emails_alice.txt")
        self.listB = get_lines("sample_sets/emails_bob.txt")

        frame = Frame(self)
        frame.pack()

        labelA = Label(frame, text="Alice's dataset")
        self.textboxA = Text(frame)
        labelA.pack(side=LEFT, padx=10, pady=10)
        self.textboxA.pack(side=LEFT)

        labelB = Label(frame, text="Bob's dataset")
        self.textboxB = Text(frame)
        labelB.pack(side=RIGHT, padx=10, pady=10)
        self.textboxB.pack(side=RIGHT)

        self.textboxA.insert(END, self.listA)
        self.textboxB.insert(END, self.listB)


    def display_submit_button(self):
        submit_method = Button(self, text="Submit", command=self.on_submit)
        submit_method.pack(padx=10, pady=10)


    def find_intersection(self, listA, listB):
        intersection_list = {}
        
        A_array = self.listA.split("\n")
        B_array = self.listB.split("\n")

        for line in A_array:
            if line == "":
                continue
            else:
                intersection_list[line] = 1
            
        for line in B_array:
            if line == "":
                continue
            else:
                if intersection_list.get(line) is None:
                    intersection_list[line] = 1
                else:
                    intersection_list[line] = intersection_list[line] + 1

        intersections = []
        for key, value in intersection_list.items():
            if value > 1:
                intersections.append(key)
        return intersections


    def display_expected_intersections(self):
        intersections = self.find_intersection(self.listA, self.listB)

        num_intersections = len(intersections)
        calculated_intersection = StringVar()
        calculated_intersection.set("Expected Intersections: " + str(num_intersections))

        if self.expected_displayed:
            self.listBoxI.delete(0, END)
            self.calculated_intersection.configure(textvariable=calculated_intersection)

        else :
            frame = Frame(self)
            frame.pack(side=LEFT)

            num_intersections = len(intersections)
            self.calculated_intersection = Label(frame, textvariable=calculated_intersection)
            self.calculated_intersection.pack()

            self.listBoxI = Listbox(frame)
            self.listBoxI.config(width=0)
            self.listBoxI.pack(expand=True)
        
        for item in intersections:
            self.listBoxI.insert(END, item)

        self.expected_displayed = True


    def get_actual_intersection(self):
        lines = ""
        with open("output/result.out") as f:
            lines = f.read().split("\n")
            non_empty_lines = [line for line in lines if line.strip() != ""]
        return non_empty_lines
      

    def display_actual_intersection(self):
        intersections = self.get_actual_intersection()

        num_intersections = len(intersections)
        actual_intersection = StringVar()
        actual_intersection.set("Actual Intersections: " + str(num_intersections))

        if self.results_displayed:
            self.listBoxA.delete(0, END)
            self.actual_intersection.configure(textvariable=actual_intersection)
    
        else :
            frame = Frame(self)
            frame.pack(side=LEFT)

            num_intersections = len(intersections)
            self.actual_intersection = Label(frame, textvariable=actual_intersection)
            self.actual_intersection.pack()

            self.listBoxA = Listbox(frame)
            self.listBoxA.config(width=0)
            self.listBoxA.pack(expand=True)
        
        for item in intersections:
            self.listBoxA.insert(END, item)

        self.results_displayed = True

    
    def get_hashes(self):
        ABlines = []
        with open("output/naive-psi.out") as f:
            all_lines = f.read().split("SEPARATION")
            print(len(all_lines))
            for sep_lines in all_lines:
                lines = sep_lines.split("\n")
                non_empty_lines = [line for line in lines if line.strip() != ""]
                ABlines.append(non_empty_lines)
        return ABlines

    def display_naive_psi(self):
        ABlines = self.get_hashes()
        hashesA = ABlines[0]
        hashesB = ABlines[1]

        if self.hashing_displayed:
            self.listBoxAH.delete(0, END)
            self.listBoxBH.delete(0, END)
        
        else :
            frameA = Frame(self)
            frameA.pack(side=LEFT)

            frameB = Frame(self)
            frameB.pack(side=LEFT)

            self.hashesA = Label(frameA, text="Alice's hashes")
            self.hashesA.pack()

            self.listBoxAH = Listbox(frameA)
            self.listBoxAH.config(width=0)
            self.listBoxAH.pack(expand=True)

            self.hashesB = Label(frameB, text="Bob's hashes")
            self.hashesB.pack()

            self.listBoxBH = Listbox(frameB)
            self.listBoxBH.config(width=0)
            self.listBoxBH.pack(expand=True)
        
        for item in hashesA:
            self.listBoxAH.insert(END, item)

        for item in hashesB:
            self.listBoxBH.insert(END, item)

        self.hashing_displayed = True

    def display_process(self):
        if self.method_index == 0:
            self.display_naive_psi()

    def on_submit(self):
        method = self.method.get()
        self.method_index = METHODS.index(method)

        self.listA = self.textboxA.get("1.0", "end-1c")
        self.listB = self.textboxB.get("1.0", "end-1c")
        listA_path = "sample_sets/input_A.txt"
        listB_path = "sample_sets/input_B.txt"

        with open(listA_path, "w") as f:
            f.write(self.listA)
        with open(listB_path, "w") as f:
            f.write(self.listB)

        processes = []
        for i in range(0, 2):
            if i == 0:
                args = ("./demo.exe -r " + str(i) + " -p " + str(self.method_index) + " -f " + listA_path).split()
            else:
                args = ("./demo.exe -r " + str(i) + " -p " + str(self.method_index) + " -f " + listB_path).split()
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            processes.append(popen)

            # seems like there's a bug in dh-based, need to call again
            if self.method_index == 1:
                args = ("./demo.exe -r 1 -p 1 -f sample_sets/input_A.txt").split()
                popen = subprocess.Popen(args, stdout=subprocess.PIPE)
                processes.append(popen)
        
        lists = []
        for process in processes:
            process.wait()
            output = process.stdout.read()
            lists.append(output)
        
        self.display_process()
        self.display_expected_intersections()
        self.display_actual_intersection()


    def display_results(self):
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self)
        self.listbox.pack()

        for initial_list in lists:
            lines = initial_list.split(b'\n')
            for line in lines:
                self.listbox.insert(END, line)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

app = GUI()
app.mainloop()
