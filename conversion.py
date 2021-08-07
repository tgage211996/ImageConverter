# from collections import Counter
# from functools import partial
from threading import currentThread
import time
from functools import partial
import multiprocessing as mp
import tkinter.messagebox
import PIL.Image
import PIL.ImageEnhance
from alive_progress import alive_bar
import win32console
import win32gui
import win32con
import random

class Functions():
    
    def convert_files(files):  
        """
            This function is the beginning phase image coversion. The function starts by assigning a new win32consol to the
            thread that this function was called within; this thread is not the same thread that main proccess was called on.
            Due to the nature of pythons
        
        """
        win32console.FreeConsole()
        win32console.AllocConsole()
        console = win32console.GetConsoleWindow()
        win32gui.ShowWindow(console,1)
        win32gui.SetWindowPos(console, win32con.HWND_TOP,0,0, 25, 25, win32con.SW_SHOW)
       
        limit = 0
        num_of_files = len(files)
        start = time.time()
       
        a = str(files[0]) + '/' + str(files[1])
    
        date = time.ctime().replace(" ","_").replace(":","~")
        cpuCount = mp.cpu_count()/2 
        finalCpu = 0

        if cpuCount >= 1:
            finalCpu = 6
        else:
            finalCpu = 1

        print(num_of_files-3)
        print(finalCpu)
        for i in enumerate(files[3:num_of_files]):
            print(i)
       
        pool = mp.Pool(processes=finalCpu)

        while limit != (num_of_files-3):
            with alive_bar(num_of_files-3) as percentage:
                func = partial(Functions.convert, a, files[2], date, (num_of_files-3))
                for x in pool.imap(func, files[3:num_of_files]):
                    limit += 1
                    percentage()
        executionTime = str((time.time() - start))
        Functions.popup_showinfo("done and process time took " + executionTime + " seconds")

        #function that creates a pop-up window that shows a message that is provided when called
    def popup_showinfo(text):
        tkinter.messagebox.showinfo("Window", text)

        # function that takees a file path, count, the new file name, and the directory where the file will be located
        # uses this information to convert the original file into the desired format. Note: right now the only format 
        # to convert to is ".png" but there will be a format selection added
    def convert(final, im_type, date, num_of_files, filePath):
        
        final_path = final + '_' + date + '_' + str(random.SystemRandom()).replace("<random.SystemRandom object at ", "").replace(">","")+ im_type 
        if im_type == '.jpg':
            try:
                with PIL.Image.open(filePath) as im:
                    print("jpg : " + final_path)
                    # if(im.width > 2000):
                    #     final_image = im.resize([im.width // 3, im.height // 3],PIL.Image.NEAREST) #create a uniform size plus stay within 1000 x 1000 - 2000 x 2000
                    #     final_image.save(final_path, compress_level=3, dpi=(300,300), quality=95) #compression level can be changed according to how we want it
                    # else:
                    im.save(final_path, compress_level=3, dpi=(300,300), quality=95)
            except OSError:
                print(OSError)
        elif im_type == '.png':
            try:
                with PIL.Image.open(filePath) as im:
                    # if(im.width > 2000):
                    #     image = im.resize([im.width // 3, im.height // 3],PIL.Image.NEAREST) #create a uniform size plus stay within 1000 x 1000 - 2000 x 2000
                    #     final_image = PIL.ImageEnhance.Sharpness(image).enhance(2.5)
                    #     final_image.save(final_path, compress_level=3, dpi=(300,300), quality=95) #compression level can be changed according to how we want it
                    # else:
                    print("PNG : " + final_path)
                    im.save(final_path, compress_level=3, dpi=(300,300), quality=95)
            except OSError:
                print(OSError)