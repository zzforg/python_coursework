



###################################################################
#
#   CSSE1001 - Assignment 2
#
#   Student Number:41870288
#
#   Student Name:Zhiguo ZENG
#
###################################################################


#
# Do not change the following import
#

from assign2_support import *

####################################################################
#
# Insert your code below
#
####################################################################

class PointFrame(Frame):
    """The bar shows the position of last clicked and current cursor positionof mouse both in real-world coordinates;
    left mouse click for display a position.
    """
    
    def __init__(self, master, parent):
        """create the PointFrame:
        master - toplevel window;
        parent - the app object.
        """

        Frame.__init__(self, master, bg='grey65')
        """inheriting the initialised information from the Frame class.
        """
        self.parent = parent
               
        Label(self, text='Last Point Clicked: ', bg='grey65').pack(side=LEFT)

        self.clickedPosition = StringVar() #set for display the mouse position
        Label(self, textvariable = self.clickedPosition, width = 15, bg='grey65').pack(side=LEFT)
        
        Label(self, text='Cursor Point: ', bg='grey65').pack(side=LEFT)

        self.cursorPosition = StringVar()        
        Label(self, textvariable = self.cursorPosition, width = 15, bg='grey65').pack(side=LEFT)


class FunctionFrame(Frame):
    """A bar for entering the functions and choose colour."""

    def __init__(self, master, parent):
        
        Frame.__init__(self, master, bd=2, relief=SUNKEN, bg='grey85')
        
        self.parent = parent
        Label(self, text='Function in x: ', bg='grey85').pack(side=LEFT)

        self.entryF = Entry(self, width=40)
        self.entryF.pack(side=LEFT)
        
        self.seletC = Button(self, text="Select", command = self.selectColor, bg='grey90')
        self.seletC.pack(side=RIGHT, padx=2)

        self.entryC = Entry(self, width=15)
        self.entryC.pack(side=RIGHT)
        self.entryC.insert(0, 'black') #default colour to be 'black'
        
        Label(self, text='Function Colour: ', bg='grey85').pack(side=RIGHT)

    def selectColor(self):
        """select the colour from using the askcolour function or entering a colour by user.
        """
        
        self.enterColor = self.entryC.get()
        _, color = askcolor(None)
        if color:
            self.entryC.delete(0,END)
            self.entryC.insert(0, color)
            
    def functionFrameErrors(self):
        """a method to returns the functions and colour for drawing;
        error message boxs are applied for report the invalid function of x and entered colour.
        """
        funcIn = self.entryF.get()
        
        try:
            funcCheck = make_function(funcIn) #make_function(string) -> (float -> float)
        except FunctionError:
            tkMessageBox.showerror("", " '%s' is not a valid function of x" % funcIn)
            return None
        
        inputColor = self.entryC.get()
        try:
            testline = self.parent.canvas.create_line(0,0,1,1, fill = inputColor) #exception raised by trying to draw a line
            self.parent.canvas.delete(testline)
        except TclError:
            tkMessageBox.showerror('', 'Invalid Colour')
            return None
        
        return (funcCheck, inputColor)

    
class PlotFrame(Frame):
    """A bar to ploting the star X, end X, satr Y, end Y and steps and return them as a tuple for drawing function.
    """
    def __init__(self, master, parent):
        
        Frame.__init__(self, master, bd=2, relief=SUNKEN, pady=5, bg='grey85')
        self.parent = parent

        Label(self, text='Plot Settings   ', bg='grey85').pack(side=LEFT)
        
        Label(self, text='Start X: ', bg='grey85').pack(side=LEFT)
        self.starX = Entry(self, width=10)
        self.starX.pack(side=LEFT)
        
        Label(self, text='End X: ', bg='grey85').pack(side=LEFT)
        self.endX = Entry(self, width=10)
        self.endX.pack(side=LEFT)
        
        Label(self, text='Start Y: ', bg='grey85').pack(side=LEFT)
        self.starY = Entry(self, width=10)
        self.starY.pack(side=LEFT)
        
        Label(self, text='End Y: ', bg='grey85').pack(side=LEFT)
        self.endY = Entry(self, width=10)
        self.endY.pack(side=LEFT)
        
        Label(self, text='Steps: ', bg='grey85').pack(side=LEFT)
        self.steps = Entry(self, width=10)
        self.steps.pack(side=LEFT)

    def NumCheck(self):
        """Error checking for user's input, error message box will report the invalid input;
        finally return the entered information --> tuple.
        """
        
        try:
            X1 = float(self.starX.get())
        except ValueError:
            tkMessageBox.showerror('', 'Start X must be a number')
            return None

        try:
            X2 = float(self.endX.get())
        except ValueError:
            tkMessageBox.showerror('', 'End X must be a number')
            return None

        try:
            Y1 = float(self.starY.get())
        except ValueError:
            tkMessageBox.showerror('', 'Start Y must be a number')
            return None

        try:
            Y2 = float(self.endY.get())
        except ValueError:
            tkMessageBox.showerror('', 'End Y must be a number')
            return None

        try:
            step = int(self.steps.get())
        except ValueError:
            tkMessageBox.showerror('', 'Number of steps must be an integer')
            return None

        if not X1  < X2:
            tkMessageBox.showerror('', 'End X must be greater than Star X')
            return None

        if not Y1 < Y2:
            tkMessageBox.showerror('', 'End Y must be greater than Star Y')
            return None

        if not step > 0:
            tkMessageBox.showerror('', 'Number of Steps must be positive')
            return None
        
        return (X1,X2,Y1,Y2,step)


class ButtonFrame(Frame):
    """A functional bar of buttons for user to interact to the application."""

    def __init__(self, master, parent):

        Frame.__init__(self, master)
        self.parent = parent
        
        self.add = Button(self, text="Add Function", command = self.parent.addFunc, bg='grey90')
        self.add.pack(side=LEFT)

        self.redraw = Button(self, text="Redraw All Functions", command = self.parent.redrawAll, bg='grey90')
        self.redraw.pack(side=LEFT)

        self.remove_Last = Button(self, text="Remove Last Function", command = self.parent.removeLast, bg='grey90')
        self.remove_Last.pack(side=LEFT)

        self.remove_All = Button(self, text="Remove All Functions", command = self.parent.removeAll, bg='grey90')
        self.remove_All.pack(side=LEFT)

        self.exit = Button(self, text="Exit", command = self.parent.exitApp, bg='grey90')
        self.exit.pack(side=LEFT)



class PlotApp(object):
    """The top-level plot appliaction class for interacting with user and plotting functions."""

    def __init__(self, master=None):
        """create the application:
        master - the toplevel window
        """
        
        self.master = master
        master.title('Function Plotter')
        master.minsize(700, 480)
        master.geometry("800x600")
        master.config(bg = 'grey65')
    
        #Add PointFrame
        self.pointFrame = PointFrame(master, self)
        self.pointFrame.pack(fill = BOTH)

        #Make Canvas
        self.canvas = Canvas(master, relief=SUNKEN, bd=2, bg='white', highlightbackground='gray80')
        self.canvas.pack(fill=BOTH, expand=1, padx=8)

        #Bind method for mouse position and application resize
        self.canvas.bind("<Motion>", self.mouseCursor)
        self.canvas.bind("<Button-1>", self.lastClicked)
        self.canvas.bind("<Configure>", self.resize)

        #Get the canvas width adn height
        self.canvasWidth = float(self.canvas.cget("width"))
        self.canvasHeight = float(self.canvas.cget("height"))
                 
        #Add FunctionFrame
        self.functionFrame = FunctionFrame(master, self)
        self.functionFrame.pack(fill =BOTH, pady=10)

        #Add PlotFrame
        self.plotFrame = PlotFrame(master, self)
        self.plotFrame.pack(fill = BOTH, pady=10)
        
        #Add ButtonFrame
        self.buttonFrame = ButtonFrame(master, self)
        self.buttonFrame.pack(pady=10)

        #Define variables: empty list for sotring functions and entered colours as pairs
        self.storeFuncColor = []
        self.getPoints = None
            
    def addFunc(self):
        """the 'Add Function' buttom to active the error checking of entered functions and colours;
        Every time add a function, the function and colour will be appended to the list as a tuple;
        then draw the funtioin by use the method 'drawlines'.
        """
        if self.functionFrame.functionFrameErrors():
            self.storeFuncColor.append(self.functionFrame.functionFrameErrors())
            self.drawlines()
         

    def drawlines(self):
        """method of drawing lines;
        clear the canvas first and active the error checking of plotframe;
        change the ploting information: startX, endX, startY, endY, steps stored as tuple;
        real world coordinate -> screen coordinate;
        world2screen(float, float) -> (float, float).
        """
        self.canvas.delete(ALL)
        self.getPoints = self.plotFrame.NumCheck()
        if self.getPoints is None: return None
          
        i = WorldScreen(self.getPoints[0], self.getPoints[2], self.getPoints[1], self.getPoints[3], self.canvasWidth, self.canvasHeight)
        for func in  self.storeFuncColor:
            
            x, y = 0,0 #draw functions by a set point to the first point
            for worldX, worldY in FunctionIterator(func[0], self.getPoints[0], self.getPoints[1], self.getPoints[4]):
                screenCoord = i.world2screen(worldX,worldY)
                self.canvas.create_line(x,y, screenCoord[0],screenCoord[1], fill = func[1])
                x,y = screenCoord[0],screenCoord[1] #to replace x, y by 1st point for keep on the loop
                           

    def mouseCursor(self, event):
        """a method to display the mouse current position, showing the real world coordinate;
        screen2world(float, float) -> (float, float).
        """
        if self.storeFuncColor == []: return
        i = WorldScreen(self.getPoints[0], self.getPoints[2], self.getPoints[1], self.getPoints[3], self.canvasWidth, self.canvasHeight)
        mouseCoord = i.screen2world(event.x, event.y)
        self.pointFrame.cursorPosition.set('( {0:.2f}, {1:.2f} )'.format(mouseCoord[0], mouseCoord[1]))

    def lastClicked(self, event):
        """a method to display the last mouse left click position, showing the real world coordinate;
        screen2world(float, float) -> (float, float).
        """
        if self.storeFuncColor == []: return
        i = WorldScreen(self.getPoints[0], self.getPoints[2], self.getPoints[1], self.getPoints[3], self.canvasWidth, self.canvasHeight)
        mouseCoord = i.screen2world(event.x, event.y)
        self.pointFrame.clickedPosition.set('( {0:.2f}, {1:.2f} )'.format(mouseCoord[0], mouseCoord[1]))

    def redrawAll(self):
        """redraw all the stored functions for new plotting  information;
        if function list is empty, do nothing.
        """
        if self.storeFuncColor == []: return
        self.drawlines()

    def removeLast(self):
        """remove the last add function;
        delete the last(-1) tuple from the list;
        redraw all the rest functions in the list.
        """
        if self.storeFuncColor == []: return
        self.storeFuncColor.pop(-1)
        if self.storeFuncColor == []:
            self.canvas.delete(ALL)
        self.redrawAll()

    def removeAll(self):
        """remove all drawings from canvas;
        empty the functions and colour list.
        """
        self.storeFuncColor = []
        self.canvas.delete(ALL)
        

    def exitApp(self):
        """exit the app."""
        self.master.destroy()

    
    def resize(self, event):
        """Callback for a resize event - reset the canvas size;
        redraw all the functions every time resize the window
        """
        
        self.canvasWidth = event.width
        self.canvasHeight = event.height-2
        self.redrawAll()

        
       
        


####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = PlotApp(root)
    root.mainloop()

if  __name__ == '__main__':
    main()
