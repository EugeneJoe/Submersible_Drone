import pygame
import socket

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

##port = "/dev/ttyACM0"
##rate = 9600
##
##s1 = serial.Serial(port,rate)
##s1.flushInput()
##
##comp_list = ["Flash complete\r\n","Hello Pi,This is Arduino UNO...\r\n"]

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
def valmap(value, istart=0, istop=1, ostart=0, ostop=100):
	return ostart + (ostop-ostart) * ((value - istart) / (istop - istart))

def datasend(direction,PWM,PWM2):
##    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    s.connect((HOST, PORT))
    try:
        msg = '<'+direction+','+str(PWM)+','+str(PWM2)+'>' 
        s.sendall(msg)
        amnt_recvd = 0
        amnt_expct = len(msg)

        while amnt_recvd < amnt_expct:
            data = s.recv(1024)
            amnt_recvd += len(data)
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
        if x < 0:
            direction1 = 'F'
        if x > 0:
            direction1 = 'B'
        if x == 0:
            direction1 = 'N'
        PWMVAL1 = valmap(abs(x))
        print 'direction1: %c, PWM value1: %3.4f' %(direction1,PWMVAL1)
        datasend(direction1,PWMVAL1,"0")

        y = joystick.get_axis(2)
        if y < 0:
            direction2 = 'L'
        if y > 0:
            direction2 = 'R'
        if y == 0:
            direction2 = 'N'
        PWMVAL2 = valmap(abs(y))
        print 'direction2: %c, PWM value2: %3.4f' %(direction2,PWMVAL2)
##        datasend(direction2,PWMVAL2,"0")

        z = joystick.get_axis(1)
        if z < 0:
            direction3 = 'U'
        if z > 0:
            direction3 = 'D'
        if z == 0:
            direction3 = 'N'
        PWMVAL3 = valmap(abs(z))
        print 'direction3: %c, PWM value3: %3.4f' %(direction3,PWMVAL3)
        #datasend(direction3,PWMVAL3,'0')

        ##Put code for secondary movements
##        if direction1 != 'N' and direction2 != 'N':
##            if PWMVAL1 > 1 and PWMVAL2 > 1:
##                if x < 0 and y < 0:                    
##                    datasend('H',PWMVAL1,PWMVAL2);
##                if x > 0 and y < 0:
##                    datasend('D',PWMVAL1,PWMVAL2);
##                if x > 0 and y > 0:
##                    datasend('C',PWMVAL1,PWMVAL2);
##                if x < 0 and y > 0:
##                    datasend('G',PWMVAL1,PWMVAL2);


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
