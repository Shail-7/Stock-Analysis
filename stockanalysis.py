# print("hello world")
from tkinter import *
from tkinter import font
from typing import Collection
import tkinter.messagebox

import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf

from matplotlib.figure import Figure 

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

from datetime import date
import pandas as pd
from pandas import Series, DataFrame


root=Tk()
root.title("Stock Analysis")
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (width, height))
# root.geometry("700x500")
root.resizable(False, False)


#function to get the stock name
def getVals():
    print(f"Entered stock name is {stockName.get()}")
    if stockName.get(): #if some val is entered into the input box
        stock=(stockName.get()+".NS").upper()
        print(stock)
        start = "2015-01-01"
        end = '2021-11-01'
        stockData = yf.download(stock,start,end)
        print("stockData :",stockData)

        if stockData.empty:
            tkinter.messagebox.showerror("Invalid Stock Name.","Stock name is invalid or it is not traded at NSE.")
        else:
            print("valid stock")
        # stockData['Open'].plot(label = 'stockData', figsize = (15,7))
        # plt.title(f'Stock Price of{stock}')
        # plt.legend()
        # plt.show()

            print(stockData)
            fig = Figure(figsize = (15, 4), 

                    dpi = 100) 
            y=stockData['Open']
            
            plot1 = fig.add_subplot(111) 
            plot1.plot(y)
        

            # tcs['Open'].plot(label = 'TCS', figsize = (15,7))

            global f1
            f1=Frame(root,bg="white",borderwidth=8,relief=SUNKEN)
            f1.pack()

            canvas = FigureCanvasTkAgg(fig, 

                                master = f1)   

            canvas.draw() 

    

            # placing the canvas on the Tkinter window 

            
            lbl3=Label(f1,text=f"{(stockName.get()).upper()}",bg="white",fg="black",font="comicsansms 16 bold")
            lbl3.pack()
        
            canvas.get_tk_widget().pack()


    

            # creating the Matplotlib toolbar 

            toolbar = NavigationToolbar2Tk(canvas, 

                                    f1) 

            toolbar.update() 

    

            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack() 

            
            stockInfoLbl1=Label(f1,text=f"ALL TIME HIGH: {stockData['High'].max()} ",bg="white",fg="green",font="comicsansms 13 bold").pack(side=LEFT,padx=8)
            stockInfoLbl2=Label(f1,text=f"ALL TIME LOW: {stockData['Low'].min()} ",bg="white",fg="red",font="comicsansms 13 bold").pack(side=LEFT,padx=8)

            print(stockData['High'])

            # enabling the clear btn
            clrBtn["state"] = "normal"
            volBtn["state"] = "disabled"
            probabilityBtn["state"] = "disabled"
            submitBtn["state"] = "disabled"
        
    else:    #if no val is entered into the input box
        print("Please enter the name of the stock")

        #Showing pop-up of no val found
        tkinter.messagebox.showerror("No value Found.","Please enter the stock name")

        # lbl2=Label(text="please enter the stock name",bg="red",fg="white",font="comicsansms 17 bold")
        # lbl2.grid(row=3,column=1)

def findProbability():
    # print("prob fn here")
    print(f"Entered stock name is {stockName.get()}")
    if stockName.get(): #if some val is entered into the input box
        stock=(stockName.get()+".NS").upper()
        print(stock)
        start = "2015-01-01"
        end = '2021-11-01'
        stockData = yf.download(stock,start,end)

        if stockData.empty:
            tkinter.messagebox.showerror("Invalid Stock Name.","Stock name is invalid or it is not traded at NSE.")
        else:
            print("valid stock")
            datList=[]
            highList=[]


            datList=list(stockData['High'].index)
            highList=list(stockData['Close'].values)

            highTree={          #Dictionary
                'root':['High'],
                # 'Date':datList,
                'High':highList
                # 'D1':[],
                # 'D2':[],
                # 'H1':[],
                # 'H2':[]
            }
            visited=[]
            queue=[]
            percentPriceChange=[]


            def bfs(visited,ht,node):
                visited.append(node)
                queue.append(node)

                while queue:
                    s = queue.pop(0) 
                    # print (s, end = " ") 

                    tmp=0.0
                    if s in ht:
                        for neighbour in ht[s]:
                            if neighbour not in visited:
                                visited.append(neighbour)
                                # print("visited len ",len(visited),end=" ")
                                if isinstance(visited[len(visited)-1],float):
                                    if tmp!=0.0:     #finding the %change in the stock according to high price
                                        percentPriceChange.append(((tmp-visited[len(visited)-1])*100)/(visited[len(visited)-1]))
                                        # print(((tmp-visited[len(visited)-1])*100)/(visited[len(visited)-1]),end=" ")

                                        # print(f"-1 {visited[len(visited)-1]} ",end=" ")
                                    tmp=visited[len(visited)-1]
                                queue.append(neighbour)
                    else:
                        # print("Not a key in dict")
                        pass


            bfs(visited, highTree, 'root')

            # print("\n\n\n visited queue ",visited)

            percentPriceChange.sort()  #now the percent in the list will get sorted in the ascending order
            print("Price change of stock ",percentPriceChange)   # len of list 1489

            probabilityOfChange=[]

            for i in range(1,(len(percentPriceChange)+1)):
                probabilityOfChange.append((i/(len(percentPriceChange)+1)))

            npPercentPriceChange=np.array(percentPriceChange)

            print((len(npPercentPriceChange[npPercentPriceChange>3.0])/len(percentPriceChange))*100) #prob in percentage that the return you get will be more than 3%
            print((len(npPercentPriceChange[npPercentPriceChange<3.0])/len(percentPriceChange))*100) #prob in percentage that the return you get will be less than 3%



            print("\n\n\n\nchances that there wil be a loss ",(len(npPercentPriceChange[npPercentPriceChange<0.0])/len(percentPriceChange))*100) #chances in percentage that there will be a loss
            print("\nchances that there wil be a gain ",(len(npPercentPriceChange[npPercentPriceChange>0.0])/len(percentPriceChange))*100) #chances in percentage that there will be a gain 

            print(len(npPercentPriceChange[npPercentPriceChange>=7.0]))

            cnt1=0
            cnt2=0
            cnt3=0
            cnt4=0


            for i in npPercentPriceChange:
                if i>0.0 and i<=5.99:
                    cnt1=cnt1+1

            for i in npPercentPriceChange:
                if i>=6.0 and i<=10.99:
                    cnt2=cnt2+1

            for i in npPercentPriceChange:
                if i>=11.0 :
                    cnt3=cnt3+1

            for i in npPercentPriceChange:
                if i<=0.0:
                    cnt4=cnt4+1

            cnt4No="{:.2f}".format((cnt4/len(npPercentPriceChange))*100)
            cnt1No="{:.2f}".format((cnt1/len(npPercentPriceChange))*100)
            cnt2No="{:.2f}".format((cnt2/len(npPercentPriceChange))*100)
            cnt3No="{:.2f}".format((cnt3/len(npPercentPriceChange))*100)

            print(f"Chances that this stock will provide less than 0% (loss)  returns {cnt4No}%")
            print(f"Chances that this stock will provide 0-5 %  returns {cnt1No}%")
            print(f"Chances that this stock will provide 6-10 %  returns {cnt2No}%")
            print(f"Chances that this stock will provide more 10%  returns {cnt3No}%")


            # bar diagram
            data = [(cnt4/len(npPercentPriceChange))*100, (cnt1/len(npPercentPriceChange))*100, (cnt2/len(npPercentPriceChange))*100, (cnt3/len(npPercentPriceChange))*100]
            fig=plt.figure(figsize=(15,4),
            dpi=100)

            plt.bar([f'<0 ({cnt4No}%)',f'0-5% ({cnt1No}%)',f'6-10% ({cnt2No}%)',f'>10% ({cnt3No}%)'], data, color='royalblue', alpha=0.7, width = 0.2)
            plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
            plt.xlabel('Returns in %')
            plt.ylabel('Chances to get mentioned returns in %')
            plt.title('Probability of getting returns divided in different classes')
            # data = [23, 45, 56, 78, 213]
            # plt.bar([1,2,3,4,5], data)

            plt.subplot(111)
            # plt.show()




            # fig = Figure(figsize = (15, 4), 

            #          dpi = 100) 
            y=plt
            
            # plot1 = fig.add_subplot(111) 
            # plot1.plot(y)
        

            # tcs['Open'].plot(label = 'TCS', figsize = (15,7))

            global f1
            f1=Frame(root,bg="white",borderwidth=8,relief=SUNKEN)
            f1.pack()

            canvas = FigureCanvasTkAgg(fig, 

                                master = f1)   

            canvas.draw() 

    

            # placing the canvas on the Tkinter window 

            
            lbl3=Label(f1,text=f"{(stockName.get()).upper()}",bg="white",fg="black",font="comicsansms 16 bold")
            lbl3.pack()
        
            canvas.get_tk_widget().pack()


    

            # creating the Matplotlib toolbar 

            toolbar = NavigationToolbar2Tk(canvas, 

                                    f1) 

            toolbar.update() 

    

            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack() 

            tmp1="{:.2f}".format(percentPriceChange[len(percentPriceChange)-1])
            tmp2="{:.2f}".format(percentPriceChange[0])
            Label(f1,text=f"Greatest Gain in 1 Day : {tmp1}%",bg="white",fg="green",font="comicsansms 13 bold").pack(pady=5,side=TOP,anchor="w")
            Label(f1,text=f"Greatest Loss in 1 Day : {tmp2}%\n",bg="white",fg="red",font="comicsansms 13 bold").pack(pady=5,side=TOP,anchor="w")
            
            tmp1="{:.2f}".format((len(npPercentPriceChange[npPercentPriceChange>0.0])/len(percentPriceChange))*100)
            tmp2="{:.2f}".format((len(npPercentPriceChange[npPercentPriceChange<0.0])/len(percentPriceChange))*100)
            Label(f1,text=f"Possibility of Gain : {tmp1}%",bg="white",fg="green",font="comicsansms 13 bold").pack(side=TOP,anchor="w")
            Label(f1,text=f"Possibility of Loss : {tmp2}%",bg="white",fg="red",font="comicsansms 13 bold").pack(pady=5,side=TOP,anchor="w")
            

            stockInfoLbl4=Label(f1,text=f"<0 (Loss) : {cnt4No}% ",bg="white",fg="red",font="comicsansms 13 bold").pack(side=LEFT,padx=8)
            stockInfoLbl1=Label(f1,text=f"0-5% : {cnt1No}% ",bg="white",fg="green",font="comicsansms 13 bold").pack(side=LEFT,padx=8)
            stockInfoLbl2=Label(f1,text=f"6-10%  : {cnt2No}% ",bg="white",fg="green",font="comicsansms 13 bold").pack(side=LEFT,padx=8)
            stockInfoLbl3=Label(f1,text=f">10% : {cnt3No}% ",bg="white",fg="green",font="comicsansms 13 bold").pack(side=LEFT,padx=8)

            recommend=" "
            if tmp1>tmp2:
                recommend="Yes"
            elif tmp1<tmp2:
                recommend="No"
            else:
                recommend="No"
            
            Label(f1,text=f"Recommended to Buy : {recommend}",bg="white",fg="blue",font="comicsansms 13 bold").pack(side=TOP,anchor="e",pady=5)

            
        

            clrBtn["state"] = "normal"
            volBtn["state"] = "disabled"
            probabilityBtn["state"] = "disabled"
            submitBtn["state"] = "disabled"


    else:  #if no val is entered into the input box
        print("Please enter the name of the stock")

        #Showing pop-up of no val found
        tkinter.messagebox.showerror("No value Found.","Please enter the stock name")

def findVol():
    # print(f"Entered stock name is {stockName.get()}")
    if stockName.get(): #if some val is entered into the input box
        stock=(stockName.get()+".NS").upper()
        print(stock)
        start = "2015-01-01"
        end = '2021-11-01'
        stockData = yf.download(stock,start,end)
        # stockData['Open'].plot(label = 'stockData', figsize = (15,7))
        # plt.title(f'Stock Price of{stock}')
        # plt.legend()
        # plt.show()

        if stockData.empty:
            tkinter.messagebox.showerror("Invalid Stock Name.","Stock name is invalid or it is not traded at NSE.")
        else:
            print("valid stock")

            print(stockData)
            fig = Figure(figsize = (15, 4), 

                    dpi = 100) 
            y=stockData['Volume']
            
            plot1 = fig.add_subplot(111) 
            plot1.plot(y)
        

            # tcs['Open'].plot(label = 'TCS', figsize = (15,7))

            global f1
            f1=Frame(root,bg="white",borderwidth=8,relief=SUNKEN)
            f1.pack()

            canvas = FigureCanvasTkAgg(fig, 

                                master = f1)   

            canvas.draw() 

    

            # placing the canvas on the Tkinter window 

            
            lbl3=Label(f1,text=f"{(stockName.get()).upper()}",bg="white",fg="black",font="comicsansms 16 bold")
            lbl3.pack()
        
            canvas.get_tk_widget().pack()


    

            # creating the Matplotlib toolbar 

            toolbar = NavigationToolbar2Tk(canvas, 

                                    f1) 

            toolbar.update() 

    

            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack() 

            
            stockInfoLbl1=Label(f1,text=f"HIGHEST VOL TRADED: {stockData['Volume'].max()} ",bg="white",fg="green",font="comicsansms 13 bold").pack(side=LEFT,padx=8)
            stockInfoLbl2=Label(f1,text=f"LOWEST VOL TRADED: {stockData['Volume'].min()} ",bg="white",fg="red",font="comicsansms 13 bold").pack(side=LEFT,padx=8)

            print(stockData['Volume'])

            # enabling the clear btn
            clrBtn["state"] = "normal"
            volBtn["state"] = "disabled"
            probabilityBtn["state"] = "disabled"
            submitBtn["state"] = "disabled"


        
    else:    #if no val is entered into the input box
        print("Please enter the name of the stock")

        #Showing pop-up of no val found
        tkinter.messagebox.showerror("No value Found.","Please enter the stock name")

        
# clearing the graph btn 
def clearGraph():
    for widgets in f1.winfo_children():
        widgets.destroy()
    f1.destroy()
    stockEntry.delete(0, 'end')
    stockEntry.focus()
    clrBtn["state"] = "disabled"
    volBtn["state"] = "normal"
    probabilityBtn["state"] = "normal"
    submitBtn["state"] = "normal"


#heading of the app
headLabel=Label(text="Stock Analysis",font="comicsansms 19 bold")
headLabel.pack(pady=5)

#entering val lbl text
lbl1=Label(text="Enter the stock name according to NSE:",font="comicsansms 16 bold")
lbl1.pack(pady=5)

#getting input 
stockName=StringVar()

stockEntry=Entry(root,textvariable=stockName)

stockEntry.pack(pady=5)
stockEntry.focus()

btnFrame=Frame(root)
btnFrame.pack()

# submit button for getting the name of the stock
submitBtn=Button(btnFrame,text="PRICE",command=getVals,height=2,width=12,bg="blue",fg="white",font="comicsansms 10 bold")
submitBtn.pack(side=LEFT,padx=20,pady=10)

#clear btn
clrBtn=Button(btnFrame,text="CLEAR",command=clearGraph,height=2,width=12,fg="white",bg="red",font="comicsansms 10 bold")
clrBtn.pack(side=LEFT,padx=20,pady=10)
clrBtn["state"] = "disabled"

# volume btn
volBtn=Button(btnFrame,text="VOLUME",command=findVol,height=2,width=12,fg="white",bg="green",font="comicsansms 10 bold")
volBtn.pack(side=LEFT,padx=20,pady=10)

#probability btn
probabilityBtn=Button(btnFrame,text="PROBABILITY",command=findProbability,height=2,width=12,fg="white",bg="orange",font="comicsansms 10 bold")
probabilityBtn.pack(side=LEFT,padx=20,pady=10)

# root.attributes('-fullscreen', True)
root.mainloop()