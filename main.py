"""System module."""
import os
import threading
import tkinter
import tkinter.filedialog
import multiprocessing
import sys
import win32console
import win32gui
import conversion as Functions

class GUI(tkinter.Tk):
    """A dummy docstring."""
    def __init__(self):
        super().__init__()
        self.title("Image File Converter")
        self.geometry("550x200")

        self.console = win32console.GetConsoleWindow()
        win32gui.ShowWindow(self.console,0)

        
        self.file_types= [" ",".png", ".jpg"]
        self.var = tkinter.StringVar(self)
        self.var.set("Select an option")
        self.submit_thread = object

        
        self.label_project=tkinter.Label(self,text="Enter project's name", width=16, fg="blue")
        self.label_project.place(x=1, y=5)
        self.project_name = tkinter.Entry(self, bd=3, width=16)
        self.project_name.place(x=135, y=5)
        self.label_directory_dest=tkinter.Label(self, text="Being saved to location", width=18, fg="blue")
        self.label_directory_dest.place(x=1, y=35)
        self.select_directory_name = tkinter.Entry(self, bd=3)
        self.select_directory_name.place(x=135, y=35)
        self.select_directory_button=tkinter.Button(self, text="Choose Location", command=self.select_directory)
        self.select_directory_button.place(x=270, y=35)
        self.file_type_label=tkinter.Label(self, text="Convert to what file type", width=19,fg="blue")
        self.file_type_label.place(x=1,  y=70)
        self.file_type_options=tkinter.OptionMenu(self, self.var, *self.file_types)
        self.file_type_options.place(x=145, y=70)    
        self.label_directory=tkinter.Label(self,text = "Select file(s) to convert",width = 18,fg = "blue")
        self.label_directory.place(x=1, y=105)
        self.button_conversion = tkinter.Button(self,text = "Convert Files",command=self.start_process)
        self.button_conversion.place(x=145, y=105)
        self.button_exit = tkinter.Button(self, text="Exit", command=self.exit)
        self.button_exit.place(x=500, y=139)  

    def select_directory(self):
        """A dummy docstring."""
        self.select_directory_name.insert(1, tkinter.filedialog.askdirectory())

    def process(self):
        """A dummy docstring."""
        files = []

        directory = self.select_directory_name.get().__str__()
        files.append(directory)

        new_name = self.project_name.get()
        files.append(new_name)

        file_type = self.var.get()
        files.append(file_type)

        for i in self.browse_files():
            files.append(i)

        Functions.Functions.convert_files(files)

    def browse_files(self):
        """A dummy docstring."""
        files = []
        for file in tkinter.filedialog.askopenfilenames():
            files.append(file)

        return files
    def exit(self):
        """A dummy docstring."""
        self.destroy()

    
    def start_process(self):
        """A dummy docstring."""
        self.submit_thread = threading.Thread(target=self.process())
        self.submit_thread.daemon = True
        self.submit_thread.start()
        self.check_thread()  

    def check_thread(self):
        """A dummy docstring."""
        if self.submit_thread.is_alive():
            self.after(50,self.check_thread)
        else:
            self.destroy()
            os.system("ImageConverterApplication.exe")

def main():
    """A dummy docstring"""
    app = GUI()
    app.mainloop()

if __name__ == '__main__':
    #important for adding multiprocessing due to the program being "frozen" to produce a windows executable: so do not delete
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    main()
