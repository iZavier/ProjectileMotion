"""
Aim:
To simulate (2D) the trajectories of an object projected at various angles,
varying speeds, with and without air resistance and calculate range and
        self.parent = parent
        self.master.title("Introduction")
        canvas = Canvas(self, background="lightblue")
        canvas.create_text(20, 300, anchor=W, font="Purisa",
                    text="The ball or body is in motion through the air, "
                          "the only forces acting on it being its weight\n"
                          "and the resistance to its motion due to the air. "
                          "\n\nJugglers know that if you throw a ball, a bean "
                          "bag, or a pin into the air, it will follow a curved "
                          "path. \nThis curve is what naturally happens when an"
                          " object can move in two dimensions—horizontal and"
                          " vertical— at the \nsame time. \n\nA motion like "
                          "this is called projectile motion and is very "
                          "common especially in sport, for example \nbasketball"
                          " and tennis. \n\nRoad accidents often involve "
                          "projectile motions, for example that of the "
                          "shattered glass of windscreen.  \nThe drop of "
                          "water that from the jet from a hosepipe behave  as "
                          "projectile. \n\nWhy is it useful to investigate "
                          "projectile?\nSport coaches want to know how to "
                          "improve performance. \nPolice accident investigators"
                          " want to determine car speeds \nfrom the position of"
                          " glass and other objects at the scene \nof an "
                          "accident \n \nIn these and other instances "
                          "mathematical modelling of \nprojectile motion proves"
                          " very useful \n\nThis application will shows:\n"
                          "How is the projectile motion change when initial"
                          " velocity is changed? \nAt which angle a projectile "
                          "should be launch, so that it travels the longer"
                          " distance?\nWhat happens to the projectile motion "
                          "when gravity/drag is changed?\n\nPlease press the "
                          "START button")
        canvas.pack(fill=BOTH, expand=1)
        """
        We create an instance of the Button widget.
        """
        startBtn = Button(self.parent, text="START", command=self.new_window)
        """
        We use the place geometry manager to position the button in absolute
        coordinates. (x,y) pixel from the top-left corner of the window.
        """
        startBtn.place(x=450, y=560)

    def new_window(self):
        """
        Close current frame and initiate new frame.
        """
        self.destroy()  # close this frame and it widgets
        self.newWindow = Projectile(self.parent)

class Projectile(Frame):
    """
    Our Projectile class inherits from the Frame container widget
    (in our case it is a window). In the __init__() constructor method
    we call the constructor of our inherited class. The background
    parameter specifies the background color of the Frame widget.
    """
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        """
        We save a reference to the parent widget. The parent widget is
        the Tk root window in our case
        """
        self.parent = parent
        print(self.parent)

        """
        We delegate the creation of the user interface to the initUI() method.
        """
        self.initUI()

    def InitSystemData(self):
        """
        Declare method to initialise system data, called by Erase Button
        and at startup by initUI
        """

        self.x1, self.x2, self.x3, self.y1, self.y2, self.y3 = [0], [0], \
                                                               [0], [0], [0],\
                                                               [0]
        self.p, self.p1, self.p2, self.p3 = [], [], [], []
        self.t = ["Angle (°)", "Speed (ms-1)", "Gravity (ms-2)", "Mass (kg)",
                  "Radius (m)", "Drag", "Air Density (kg m-3)",
                  "Launch Height (m)", "Max Height (m)", "Max Range (m)",
                  "Time (s)"]
        self.lower_bounds = [0.25, 0.5, 1.6, 0.0001, 0.0001, 0, 0.0001, 0]
        self.upper_bounds = [89.99, 500, 100, 0.25, 0.05, 0.9999, 8, 1000]
        self.values = []
        self.height = 0
        self.gravity = 0
        self.angle = 0
        self.speed = 0
        self.DeltaT = 0.01

    def initUI(self):
        """
        Declare method to initialise the system, using layout manger to
        put widgets in a frame.
        """
        print("InitUI")
        """
        We delegate the initialising of the system data to InitSystemData
        method
        """
        self.InitSystemData()
        print("User inputs: ",self.values)
        """
        We set the title of the window using the title() method.
        """
        self.parent.title("Projectile")

        """
        The pack() method is one of the three geometry managers in Tkinter.
        It organizes widgets into horizontal and vertical boxes. Here we
        put the Frame widget, accessed via the self attribute to the Tk
        root window. It is expanded in both directions. In other words,
        it takes the whole client space of the root window.
        """
        self.pack(fill=BOTH, expand=1)

        """
        We create an instance of the Button widget. The parent of this
        button is the Frame container. We provide a label for the button
        and a command. The command specifies a method that is called when
        we press the button. As an example the quit() method is called,
        which terminates the application.
        """
        quitBtn = Button(self.parent, text="Quit", command=self.quitp)
        plotBtn = Button(self.parent, text="Plot", command=self.validate)
        eraseBtn = Button(self.parent, text="Erase", command=self.erase)
        saveBtn = Button(self.parent, text="Save", command=self.save)
        """
        We use the place geometry manager to position the button in absolute
        coordinates. (x,y) pixel from the top-left corner of the window.
        """
        plotBtn.place(x=675, y=550)
        eraseBtn.place(x=725, y=550)
        saveBtn.place(x=775, y=550)
        quitBtn.place(x=825, y=550)

        """
        We create label and entry for the system data, The static text are
        held in self.t[] and entry data in self.p We use Tkinter lebal widget
        to display static text on the screen and Enter widget to get input
        text string.
        """
        for i in self.t:
          Label(self, text=i, background="white").grid(row=(self.t.index(i)),
                                           column=1, columnspan=2, rowspan=2)
          self.p.append(Entry(self)) # Entry to take inputs
          self.p[len(self.p)-1].grid(row=(self.t.index(i)), column=3, rowspan=2)
        """
        This allows us to lock text entry for the last 3 entry widgets.
        These are reserved to display maximum height, maximum range and flight time.
        """
        for x in range(8,11,1):
         (self.p[x]).configure(state='disabled')
        self.trajectoryPlot()

    def trajectoryPlot(self):
        """
        Function plots trajectory data using matplotlib
        """
        """
         We ensure that there are a minimum of at least 5 plot points along
         the x and y axis. This limit is because of inadequate number of data
         points or inadequate data range
        """
        if len(self.x1) < 5 and len(self.x1) > 1:
          self.x1 = [0]
          self.y1 = [0]
          easygui.msgbox(msg="The current plot is too small to display. ",
                         title="Error!", ok_button="OK")
        """
         This creates the plot window, with a fixed set size, [640x600].
        """
        self.f = Figure(figsize=(8.00, 7.5), dpi=80)
        """
         This sets the grid size for a plot frame.
        """
        self.a = self.f.add_subplot(111)
        """
         This sets each of the 3 graphs in the same figure, but in a
         different colour, (red,blue,green).
        """
        self.a.plot(self.x1, self.y1, 'r')
        self.a.plot(self.x2, self.y2, 'b')
        self.a.plot(self.x3, self.y3, 'g')
        """
         Create TK Figure Canvas to display on plotWin TopLevel window
        """
        self.dataPlot = FigureCanvasTkAgg(self.f, master=self)
        """
         Set axes, x label & ylabel, title, grid line style and colour.
        """
        self.a.set_xlabel('Range (m)')
        self.a.set_ylabel('Height (m)')
        self.a.set_title('Projectile Motion')
        self.a.grid(color='blue', linestyle='dotted')
        """
         This displays each of the 3 graphs in the same figure.
        """
        self.dataPlot.show()
        """
         Tkinter to fill screen with the plot, rows and columns start at zero
        """
        self.dataPlot.get_tk_widget().grid(row=0, column=0, columnspan=1, rowspan=14)
        """
         Update list by shifting displacement data list x2 & y2 to x3 & y3
         and current x1 & y1 to x2 & y2 the purpose is to ensure that x1,
         y1 is always the current list x2, y2 the previous list and x3, y3
         is the most earliest list, and similarly we also shift system data
         p3=p2 and p2=p1.
        """
        self.x3 = self.x2
        self.y3 = self.y2
        self.x2 = self.x1
        self.y2 = self.y1
        self.p3 = self.p2
        self.p2 = self.p1

    def validate(self):
        """
        Declare method called by start Button to validate system data
        This validates each value that is read from the entry box are in
        numeric form. It checks for invalid data, missing data and data
        limits and warns user for missing or invalid data. If user values
        are outside the limit, then upper or lower limits are used. The
        values read from the entry box are in string form these are converted
        into floating point
        """

        self.values = []

        print("Validating!")
        """
         This validates each value that is submitted by the form are
         in a numeric form.
        """
        error_flag = 0
        for i in self.p:
         #print(i.get())
         self.values.append(i.get())
         """
          Checks for data present
         """
         if len(i.get()) > 0:
          for x in self.p:
           try:
            """
            Read from entery box and convert to float value
            if not float than log error with the label
            """
            float(self.p[self.p.index(i)].get())
           except ValueError:
            error_flag += 1
            pos = self.t[self.p.index(i)]
        """
        If error than warn user.
        """
        if error_flag > 0:
         a=easygui.msgbox(msg="Invalid data! -> " + str(pos) + "",
                          title="Error!", ok_button="OK")
         print(easygui.msgbox)
         print("Errors -> User Inputs: ",self.values)
        else:
         """
          This checks that data are within the limit range.
         """
         error_flag = 0
         print("User inputs: ",self.values)
         for element in range(0,8,1):
          if len(self.values[element]) > 0:
           #print(self.values)
           if float(self.values[element]) <= self.lower_bounds[element]:
            self.values[element] = self.lower_bounds[element]
           if float(self.values[element]) >= self.upper_bounds[element]:
            self.values[element] = self.upper_bounds[element]
          (self.p[element]).delete(0, END)
          (self.p[element]).insert(0, self.values[element])
         """
         This checks that if drag coefficient is present than mass,
         radius and air density must be present, if not than warn user.
         """
         error_flag = 0
         if len(str((self.values[5]))) > 0 and float(self.values[5]) > 0:
          drag = float(self.values[5])
          """
           If mass is not present than log error with the label
          """
          if len(str((self.values[3]))) > 0:
           mass = float(self.values[3])
          else:
           error_flag = 1
           pos = self.t[3]

          if (error_flag == 0):
           """
            If radius is present than calculate area, else log error with
            the label
           """
           if len(str((self.values[4]))) > 0:
            radius = float (self.values[4])
            area = pi * (radius** 2)
           else:
            error_flag = 1
            pos = self.t[4]

          if (error_flag == 0):
           """
            If air density is present than calculate drag else log error with
            the label
           """
           if len(str((self.values[6]))) > 0:
            airdensity = float(self.values[6])
            self.dragd = (airdensity * area * drag) / (2* mass)
           else:
            error_flag = 1
            pos = self.t[6]
         else:
          self.dragd = 0

         """
          This checks that speed, gravity and angle are present if not than
          warn user.
         """
         if (error_flag == 0):
          for i in range(0,3):
           if len(str((self.values[i]))) <= 0:
            error_flag = 1
            pos = self.t[i]

         """
         If error than warn user.
         """
         if error_flag > 0:
          easygui.msgbox(msg="Data missing! -> " + str(pos) + "",
                         title="Error!", ok_button="OK")
         else:
          """
           set height value, if not present than set it to zero.
          """
          if len(str((self.values[7]))) > 0: self.height = \
           float(self.values[7])
          else: self.height = 0
          self.angle = float(self.values[0])
          self.speed = float(self.values[1])
          self.gravity = float(self.values[2])
          self.motion_algorithm()

    def motion_algorithm(self):
     """
     This is main computational (mathematical) algorithm that provide x and
     y displacement data for the trajectory plot and also provide projectile
     horizontal range, maximum height attain and the flight time. It models
     the motion trajectory as a discrete sequence of events in time.

     The acceleration, number of steps and time interval are set at the beginning of the program.
     The heart of the program is a while loop which executes repeatedly,
     updating velocity, acceleartion and position for each cycle.
     """

     """
      set status message on title bar
     """
     self.parent.title("Projectile - please wait for motion algorithm to "
                       "compile displacement data")
     print("Motion algorithm")
     """
      set displacement components at launch
     """
     self.x1 = [0]
     self.y1 = [self.height]
     velocityY = self.speed
     """
      We calculate the vertical component of velocity at launch
     """
     velocityY = velocityY * sin(radians(self.angle))
     yV = [velocityY]
     velocityX = self.speed
     """
      We calculate the horizontal component of velocity at launch
     """
     velocityX = velocityX * cos(radians(self.angle))
     xV = [velocityX]
     """
      We calculate the horizontal component and vertical component of
      acceleration at launch
     """
     sxA = (self.dragd * velocityX * sqrt(((velocityX ** 2) +
                                           (velocityY ** 2))) * -1)
     syA = (self.gravity * -1) + (self.dragd * velocityY *
                             sqrt(((velocityX ** 2) + (velocityY ** 2))) * -1)
     xA = [sxA]
     yA = [syA]

     print("VelocityX: " + str(velocityX) + " VelocityY: "+ str(velocityY)
           + "")
     """
      We loop until it hits the ground, i.e. when height value is slightly
      less than zero
     """
     while (self.y1[(len(self.y1) - 1)]) >= 0:
      """
       We calculate the new velocities in the x and y directions using finite time step Δt
      """
      yV.append(yV[len(yV) - 1] + yA[len(yA) - 1] * self.DeltaT)
      xV.append(xV[len(xV) - 1] + xA[len(xA) - 1] * self.DeltaT)
      """
       We calculate the new acceleartion components
      """
      yA.append(-self.gravity - self.dragd * float(yV[len(yV) - 1]) *
                sqrt((float(yV[len(yV) - 1]) ** 2) +
                     (float(xV[len(xV) - 1] ** 2))))
      xA.append(-self.dragd * xV[len(xV) - 1] * sqrt((xV[len(xV) - 1] ** 2)
                                                 + (yV[len(yV) - 1] ** 2)))
      """
       We calculate the new position of the projectile
      """
      self.x1.append(self.x1[(len(self.x1) - 1)] + (xV[(len(xV) - 1)] *
           self.DeltaT) + (0.5 * xA[len(xA) - 1] * (self.DeltaT ** 2)))
      self.y1.append(self.y1[(len(self.y1) - 1)] + (yV[(len(yV) - 1)] *
           self.DeltaT) + (0.5 * yA[len(yA) - 1] * (self.DeltaT ** 2)))
     """
      When object hit the ground, height value is slightly less than zero,
      for plotting purpose we set this value to zero
     """
     self.y1[len(self.y1) - 1] = 0
     print("Get size in bytes of the list.")
     print(getsizeof(self.x1))
     print(getsizeof(self.y1))
     print(getsizeof(xA))
     print(getsizeof(yA))
     print(getsizeof(yV))
     print(getsizeof(xV))
     """
      Horizontal range attain
     """
     x = sorted(self.x1)
     xa = len(x)-1
     maxrange = x[xa]
     print("Range: ",maxrange)
     """
      Maximum height attain
     """
     y = sorted(self.y1)
     ya = len(y)-1
     maxheight = y[ya]
     print("Height: ",maxheight)
     """
      Calcualte flight time
     """
     totaltime = len(self.x1) * self.DeltaT
     print("Time: ",totaltime)
     """
      we update the screen with height, range and time
     """
     (self.p[8]).configure(state='normal')
     (self.p[8]).delete(0, END)
     (self.p[8]).insert(0, round(maxheight, 2))
     (self.p[8]).configure(state='disabled')
     (self.p[9]).configure(state='normal')
     (self.p[9]).delete(0, END)
     (self.p[9]).insert(0, round(maxrange, 2))
     (self.p[9]).configure(state='disabled')
     (self.p[10]).configure(state='normal')
     (self.p[10]).delete(0, END)
     (self.p[10]).insert(0, round(totaltime, 2))
     (self.p[10]).configure(state='disabled')

     self.parent.title("Projectile")
     """
      We now plot the trajectory of the projectile
     """
     self.trajectoryPlot()
     """
      Update the system data list with height, range and time
     """
     self.values[8] = maxheight
     self.values[9] = maxrange
     self.values[10] = totaltime
     self.p1 = self.values;

     print(self.values)

    def erase(self):
        """
        Declare function called by Erase Button to initialise system data
        and redraw the form i.e. clears all entry data and the plots
        """
        print("Erasing!")
        self.initUI()

    def save(self):
        """
        Declare function called by Save Button to save current plot data
          A file to get the name of a file to save.
          Returns the name of a file, or None if user chose to cancel.
          If the "default" argument specifies a file name,
          than the dialog box will start with that file.
        """

        lx1 = len(self.x1) # get length of the list self.x1
        print(lx1)
        """
         check the length of list. The limit is set to prevent it taking a
         long time in file saving  process
        """
        if lx1 > 50000:
         easygui.msgbox(msg="File too large to be saved.", title="Error!",
                        ok_button="OK")
        else:
         total = 0
         """
          call filesavebox method to display the save file dialog box
          it returns a filename or empty if cancel button selected.
         """
         fileName = easygui.filesavebox(msg="Choose your file",
                         title="Projectile", default=None, filetypes=['*.csv'])
         textdata = ""
         """
          Test whether the user has provided the filename or empty if cancel
          button selected
         """
         if (fileName != None):
          """
           Returns a file object
          """
          f = open(fileName, "w+")
          print("File Name: ",fileName)
          """
           set status message on title bar
          """
          self.parent.title("Projectile - Writing to file: " + str(fileName) +
                            ", please wait! ")
          """
           compile system data into string
          """
          for i in self.p1:
           if len(str(i)) > 0:
            pos = self.p1.index(i)
            textdata += ("" + str(self.t[pos]) + "," + str(i) + "\r")
          textdata += ("Time(s), Range(m), Height(m) \r")
          t = 0
          total += sys.getsizeof(textdata)
          """
           compile displacement x and y data into string
          """
          for x in self.x1:
           ypos = self.x1.index(x)
           y = round(self.y1[ypos],4)
           textdata += ("" + str(t) + "," + str(round(x,4)) + "," + str(y) +
                        "\r")
           t += self.DeltaT
           """
            We check length so that we write a block of text data to a file.
            This is to prevent size of text data to grow enormously.
           """
           if (len(textdata)) > 30000:
            total += sys.getsizeof(textdata)
            f.write(textdata) # Write a sequence of byte strings to the file.
            textdata = ""
          total += sys.getsizeof(textdata)
          f.write(textdata) # Write a sequence of byte strings to the file.
          f.close()
          self.parent.title("Projectile")
          print(total)
         else:
          print("cancel file save")


    def quitp(self):
      """
      Declare function called by Quit Button, the application terminates when
      quit button is pressed
      """
      print("Quit!")
      self.parent.destroy()

def main():
    length, height = 900, 610
    CoordX, CoordY = 0,0
    """
    The root window is created. The root window is a main application window
    in our programs. It has a title bar and borders. These are provided by the
    window manager. It must be created before any other widgets.
    """
    root = Tk()
    """
    The geometry() method sets a size for the window and positions it on the
    screen. The first two parameters are width and height of the window. The
     last two parameters are x, y screen coordinates.
    """
    root.geometry(str(length) + "x" + str(height) + "+" + str(CoordX) + "+" +
                  str(CoordY))
    """
    Here we create the instance of the application class.
    """
    app = SplashScreen(root)

    """
    Finally, we enter the mainloop. The event handling starts from this point.
    The mainloop receives events from the window system and dispatches them to
    the application widgets. It is terminated when we click on the close button
    of the titlebar or call the quit() method.
    """
    #root.mainloop()
    root.mainloop()


if __name__ == '__main__':
    main()  
