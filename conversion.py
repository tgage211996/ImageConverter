# from collections import Counter
# from functools import partial
from os import system
import sys
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
import cv2 as cv

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
        cpuCount = mp.cpu_count()
        finalCpu = 0

        if cpuCount >= 10:
            finalCpu = 6
        elif 9 == cpuCount: 
            finalCpu = 5

        elif 8 == cpuCount:
            finalCpu = 4
        elif 7 == cpuCount:
            finalCpu = 3
        elif 6 == cpuCount:
            finalCpu = 2
        elif 5 == cpuCount:
            finalCpu = 1
        else:
            Functions.popup_showinfo("You are not able to use this program. Please consult Ben or Justin on why this application is not able to run")
            sys.exit(1)

        print(num_of_files-3)
        print(finalCpu)
        for i in enumerate(files[3:num_of_files]):
            print(i)
       
        pool = mp.Pool(processes=finalCpu)
        while limit != (num_of_files-3):
            with alive_bar(num_of_files-3) as percentage:
                func = partial(Functions.convert, a, files[2], date)
                for x in pool.imap(func, files[3:num_of_files]):
                    limit += 1
                    percentage()
                pool.close()


        
        executionTime = str((time.time() - start))
        Functions.popup_showinfo("done and process time took " + executionTime + " seconds")

        #function that creates a pop-up window that shows a message that is provided when called
    def popup_showinfo(text):
        tkinter.messagebox.showinfo("Window", text)

        # function that takees a file path, count, the new file name, and the directory where the file will be located
        # uses this information to convert the original file into the desired format. Note: right now the only format 
        # to convert to is ".png" but there will be a format selection added
    def convert(final, im_type, date, filePath):
        
        final_path = final + '_' + date + '_' + str(random.SystemRandom().normalvariate(50.00, 100.00)).replace("<random.SystemRandom object at ", "").replace(">","")+ im_type 
        if im_type == '.jpg':
            
            im = cv.imread(filePath,cv.IMREAD_COLOR)
            cv.imwrite(final_path,im, [int(cv.IMWRITE_JPEG_QUALITY), 100 , cv.IMWRITE_JPEG_OPTIMIZE, 36])
          
        elif im_type == '.png':
            width=None
            height=None
            im = cv.imread(filePath,cv.IMREAD_COLOR)
            if ( im.shape[0] > 2000 or im.shape[1] > 2000):
                width = int(im.shape[1] * 60 / 100)
                height = int(im.shape[0] * 60 / 100)
            res = cv.resize(im, (width,height),interpolation=cv.INTER_AREA)
            cv.imwrite(final_path,res, [cv.IMWRITE_PNG_COMPRESSION,2] )
            