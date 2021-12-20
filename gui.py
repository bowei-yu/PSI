from tkinter import *
import subprocess

METHODS = ["naive-hashing", "server-aided", "pk-based", "ot-based"]
pk_based_result_path = "output/pk-based/pk-based.out"

class GUI(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.title("PSI Demonstation")
        
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('%dx%d+0+0' % (width,height))

        self.expected_displayed = False
        self.results_displayed = False
        self.hashing_displayed = False
        self.keys_displayed = False
        self.matches_displayed = False

        self.display_method_options()
        self.display_initial_lists()
        self.display_submit_button()

        self.mainframe = Frame(self)
        self.mainframe.pack(anchor=CENTER)

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

        for line in B_array:
            if line == "":
                continue
            else:
                intersection_list[line] = 1
            
        for line in A_array:
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
            frame = Frame(self.mainframe)
            frame.pack(side=LEFT, fill="both")

            num_intersections = len(intersections)
            self.calculated_intersection = Label(frame, textvariable=calculated_intersection)
            self.calculated_intersection.pack()

            self.listBoxI = Listbox(frame)
            self.listBoxI.config(width=0)
            self.listBoxI.pack(expand=True, fill="both")
        
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
            frame = Frame(self.mainframe)
            frame.pack(side=LEFT, fill="both")

            num_intersections = len(intersections)
            self.actual_intersection = Label(frame, textvariable=actual_intersection)
            self.actual_intersection.pack()

            self.listBoxA = Listbox(frame)
            self.listBoxA.config(width=0)
            self.listBoxA.pack(expand=True, fill="both")
        
        for item in intersections:
            self.listBoxA.insert(END, item)

        self.results_displayed = True

    
    def get_hashes_or_encrypted_keys(self, path):
        ABlines = []
        with open(path) as f:
            all_lines = f.read().split("SEPARATION")
            for sep_lines in all_lines:
                lines = sep_lines.split("\n")
                non_empty_lines = [line for line in lines if line.strip() != ""]
                ABlines.append(non_empty_lines)

        keys = []
        if (path == pk_based_result_path):
            with open("output/pk-based/pk-based_keyA.out") as f:
                keyA = f.read()
                keys.append(keyA)
            with open("output/pk-based/pk-based_keyB.out") as f:
                keyB = f.read()
                keys.append(keyB)
        return ABlines, keys


    def get_matches_wrt_sender(self, path):
        A_lines = []
        B_lines = []
        with open(path + "/A.out") as f:
            lines = f.read().split("\n")
            A_lines = [line for line in lines if line.strip() != ""]
            A_lines.sort()
        with open(path + "/B.out") as f:
            lines = f.read().split("\n")
            B_lines = [line for line in lines if line.strip() != ""]
            B_lines.sort()
        return A_lines, B_lines

    def display_hashes_or_encrypted_keys(self, path, keyphrase):
        ABhashes, keys = self.get_hashes_or_encrypted_keys(path)
        hashesA = ABhashes[0]
        hashesB = ABhashes[1]

        # if (path == pk_based_result_path):
            
        if (self.keys_displayed):
            self.listBoxKA.delete(0, END)
            self.listBoxKB.delete(0, END)

        else:
            frameK = Frame(self.mainframe)
            frameK.pack(side=LEFT, fill="both")

            self.keyA = Label(frameK, text="Alice's Key")
            self.keyA.pack()

            self.listBoxKA = Listbox(frameK)
            self.listBoxKA.config(width=0)
            self.listBoxKA.pack(expand=True)

            self.keyB = Label(frameK, text="Bob's Key")
            self.keyB.pack()

            self.listBoxKB = Listbox(frameK)
            self.listBoxKB.config(width=0)
            self.listBoxKB.pack(expand=True)

            self.keys_displayed = True

        if (len(keys) > 0):
            self.listBoxKA.insert(END, keys[0])
            self.listBoxKB.insert(END, keys[1])

        if self.hashing_displayed:
            self.listBoxAH.delete(0, END)
            self.listBoxBH.delete(0, END)
        
        else:
            frameA = Frame(self.mainframe)
            frameA.pack(side=LEFT, fill="both")

            frameB = Frame(self.mainframe)
            frameB.pack(side=LEFT, fill="both")

            self.hashesA = Label(frameA, text="Alice's " + keyphrase)
            self.hashesA.pack()

            self.listBoxAH = Listbox(frameA)
            self.listBoxAH.config(width=0)
            self.listBoxAH.pack(expand=True, fill="both")

            self.hashesB = Label(frameB, text="Bob's " + keyphrase)
            self.hashesB.pack()

            self.listBoxBH = Listbox(frameB)
            self.listBoxBH.config(width=0)
            self.listBoxBH.pack(expand=True, fill="both")

        for item in hashesA:
            self.listBoxAH.insert(END, item)

        for item in hashesB:
            self.listBoxBH.insert(END, item)

        self.hashing_displayed = True

    # elif (path == "output/naive-psi/naive-psi.out"):
    #     if self.hashing_displayed:
    #         self.listBoxAH.delete(0, END)
    #         self.listBoxBH.delete(0, END)
        
    #     else:
    #         frameA = Frame(self.mainframe)
    #         frameA.pack(side=LEFT, fill="both")

    #         frameB = Frame(self.mainframe)
    #         frameB.pack(side=LEFT, fill="both")

    #         self.hashesA = Label(frameA, text="Alice's " + keyphrase)
    #         self.hashesA.pack()

    #         self.listBoxAH = Listbox(frameA)
    #         self.listBoxAH.config(width=0)
    #         self.listBoxAH.pack(expand=True, fill="both")

    #         self.hashesB = Label(frameB, text="Bob's " + keyphrase)
    #         self.hashesB.pack()

    #         self.listBoxBH = Listbox(frameB)
    #         self.listBoxBH.config(width=0)
    #         self.listBoxBH.pack(expand=True, fill="both")

    #     for item in hashesA:
    #         self.listBoxAH.insert(END, item)

    #     for item in hashesB:
    #         self.listBoxBH.insert(END, item)

    #     if (path == pk_based_result_path):
    #         self.listBoxKA.insert(END, keys[0])
    #         self.listBoxKB.insert(END, keys[1])
    #         self.keys_displayed = True

    #     self.hashing_displayed = True


    def display_matches(self, path):
        matchesA, matchesB = self.get_matches_wrt_sender(path)

        if self.matches_displayed:
            self.listBoxAM.delete(0, END)
            self.listBoxBM.delete(0, END)

        else:
            frameC = Frame(self.mainframe)
            frameC.pack(side=LEFT, fill="both")

            frameD = Frame(self.mainframe)
            frameD.pack(side=LEFT, fill="both")

            self.matchesA = Label(frameC, text="Alice's match indexes")
            self.matchesA.pack()

            self.listBoxAM = Listbox(frameC)
            self.listBoxAM.config(width=0)
            self.listBoxAM.pack(expand=True, fill="both")

            self.matchesB = Label(frameD, text="Bob's match indexes")
            self.matchesB.pack()

            self.listBoxBM = Listbox(frameD)
            self.listBoxBM.config(width=0)
            self.listBoxBM.pack(expand=True, fill="both")

        for item in matchesA:
            self.listBoxAM.insert(END, item)

        for item in matchesB:
            self.listBoxBM.insert(END, item)

        self.matches_displayed = True
        

    def display_naive_psi(self):
        self.display_hashes_or_encrypted_keys("output/naive-psi/naive-psi.out", "hashes")
        self.display_matches("output/naive-psi")

    
    def display_pk_based(self):
        self.display_hashes_or_encrypted_keys(pk_based_result_path, "ciphertexts")
        # self.display_matches("output/pk-based")


    def display_process(self):
        if self.method_index == 0:
            self.display_naive_psi()
        elif self.method_index == 2:
            self.display_pk_based()

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

            # for server-aided, need another server
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
