import pygame
import socket

#Address of the Rpi server that we're connecting to
HOST = '192.168.137.2'
PORT = 21000

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
direction1 = 'N'
direction2 = 'N'
direction3 = 'N'
PWMVAL1 = 0
PWMVAL2 = 0
PWMVAL3 = 0
pwmr = 0
pwml = 0

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 50)

    def Print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 45
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
        
#Function to map joystick values to PWM values    
def valmap(value, istart=0, istop=1, ostart=0, ostop=250):
	return ostart + (ostop-ostart) * ((value - istart) / (istop - istart))

#Function to arrange data to be sent to Pi in the proper format.
def datasend(direction,PWM,PWM2,direction2,PWM3):
    try:
        msg = '<'+direction+','+str(PWM)+','+str(PWM2)+','+direction2+','+str(PWM3)+'>' #concatenation of strings and integers in proper order
        s.sendall(msg) #sends message to Pi server
        amnt_recvd = 0
        amnt_expct = len(msg)

        while amnt_recvd < amnt_expct:
            data = s.recv(1024) #Read data that has just been sent. If no. of characters is the same then assume data
            amnt_recvd += len(data) #was not corrupted during transmission and communication was successful
            print('Received ', data) 
    finally:
        print 'Communication complete'
##        print 'Closing socket'
##        s.close()

pygame.init()
 
# Set the width and height of the screen [width,height]
size = [1000, 900]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    #Socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print  "Joystick button pressed."
        if event.type == pygame.JOYBUTTONUP:
            print "Joystick button released."
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.Print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.Print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.Print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.Print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()

        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.Print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.Print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.Print(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.Print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.Print(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()
        
        textPrint.unindent()

        x = joystick.get_axis(3)
        if x < -0.1:
            direction1 = 'F'
        if x > 0.1:
            direction1 = 'B'
        if x > -0.1 and x < 0.1:
            direction1 = 'N'
        PWMVAL1 = valmap(abs(x))
        print 'direction1: %c, PWM value1: %3.4f' %(direction1,PWMVAL1)

        y = joystick.get_axis(2)
        if y < -0.1:
            direction2 = 'L'
        if y > 0.1:
            direction2 = 'R'
        if y > -0.1 and y < 0.1:
            direction2 = 'N'
        PWMVAL2 = valmap(abs(y)) #determines by how much to curve to the left or right
        print 'direction2: %c, PWM value2: %3.4f' %(direction2,PWMVAL2)

        z = joystick.get_axis(0)
        if z < -0.1:
            direction3 = 'U'
        if z > 0.1:
            direction3 = 'D'
        if z > -0.1 and z < 0.1:
            direction3 = 'N'
        PWMVAL3 = valmap(abs(z))
        print 'direction3: %c, PWM value3: %3.4f' %(direction3,PWMVAL3)

        if direction2 == 'R':
            if direction1 == 'N':
                direction1 = 'F'
            pwmr = PWMVAL1 - PWMVAL2  #Reduce speed of right motor
            pwml = PWMVAL1 + PWMVAL2  #Increase speed of left motor so as to turn right.
        if direction2 == 'L':
            if direction1 == 'N':
                direction1 = 'F'
            pwmr = PWMVAL1 + PWMVAL2 #Increase speed of right motor
            pwml = PWMVAL1 - PWMVAL2 #Reduce speed of left motor so as to turn left.
        if direction2 == 'N':
            pwmr = PWMVAL1  #Set speed of left motor equal to that of right motor so
            pwml = PWMVAL1  #as to move forward
        if pwmr < 20:
            pwmr = 0 #to avoid speed region where motor doesn't have enough power to rotate
        if pwmr > 150:
            pwmr = 150 #to limit the maximum speed to PWM value 250
        if pwml < 20:
            pwml = 0  #to avoid speed region where motor doesn't have enough power to rotate
        if pwml > 150:
            pwml = 150  #to limit the maximum speed to PWM value 250
        if PWMVAL3 < 20:
            PWMVAL3 = 0 #to avoid speed region where motor doesn't have enough power to rotate
        if PWMVAL3 > 200:
            PWMVAL3 = 200 #to limit the maximum speed to PWM value 250
        print str(pwmr) + "  " + str(pwml) #print values of pwmr and pwml on the screen
        datasend(direction1,pwmr,pwml,direction3,PWMVAL3)  #send data to raspberry pi
        


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    s.close()
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
