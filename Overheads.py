#Everything should be turned on at once in here, it's too subdued.
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
import numpy as np
from Gauss_sliders import *

fig, ax = plt.subplots()
#make spatially relevent
ax.set_aspect("equal")

#create slider functions before creating sliders
def sliderX_update(new_x,circle,gauss,scatters,index):
    scatter=scatters[index]
    if scatter is not None:
        scatter.remove()
        pass
    try:
        circle.x=new_x
        new_scatter=dot.update_graph(circle,gauss,LEDs)
        scatters[index]=new_scatter
    except Exception as e:
        print(e) 

def sliderY_update(new_y):
    global light
    if light is not None:
        light.remove()
    try:
        circle.y=new_y
        light=dot.update_graph(circle,gauss,LEDs)
        plt.show() 
    except Exception as e:
        print(e) 

def sliderR_update(new_r):
    global light
    if light is not None:
        light.remove()
    try:
        circle.r=new_r
        light=dot.update_graph(circle,gauss,LEDs)
        plt.show() 
    except Exception as e:
        print(e) 

def sliderH_update(new_h):
    global light
    if light is not None:
        light.remove()
    try:
        gauss.height=new_h
        light=dot.update_graph(circle,gauss,LEDs)
        plt.show()
    except Exception as e:
        print(e)

def sliderM_update(new_m):
    global light
    if light is not None:
        light.remove()
    try:
        gauss.mean=new_m
        light=dot.update_graph(circle,gauss,LEDs)
        plt.show() 
    except Exception as e:
        print(e)
        
def sliderD_update(new_d):
    global light
    if light is not None:
        light.remove()
    try:
        gauss.deviation=new_d
        light=dot.update_graph(circle,gauss,LEDs)
        plt.show() 
    except Exception as e:
        print(e)

#create point source
class Circle():
    def __init__(self,x,y,init_vx,init_vy,colour):
        self.x=x
        self.y=y
        self.vx=init_vx
        self.vy=init_vy
        self.colour=colour
              
#define gauassian
class Gaussian():
    def __init__(self,height,mean,deviation):
        self.height=height
        self.mean=mean
        self.deviation=deviation
    def calc(self,xr,yr,xp,yp):
        radius=np.sqrt(np.power(xp-xr,2)+np.power(yp-yr,2))
        output=self.height*np.exp(-0.5*np.power(((radius-self.mean)/self.deviation),2))
        return output
        

class LED_Array():
    def __init__(self):
        #store starting positions
        self.xs=np.tile((np.array([0,12.5,30.0,60.0,77.5,90])/100),160)
        self.xs=self.xs.reshape(160,6)
        self.start_y_locations=np.array([0,20,15,30,20,10])/1000
        self.LED_spacings=0.030

        #set up 'stage'
        self.ys=np.zeros((160,6))
        self.size=np.ones((160,6))
        #calulate all other positions and store/plot
        rows=np.arange(160).reshape(-1,1)
        self.ys=self.start_y_locations+rows*self.LED_spacings

#create movement of object
        
class Graph_Updater():
    #Process the LEDs aginst the location of the circle   
    def update_graph(self,circle,gauss,LEDs):
        mask=(((circle.y-gauss.mean-gauss.deviation*4)<=LEDs.ys) & (LEDs.ys<=(circle.y+gauss.mean+gauss.deviation*4)))
        rad_field=np.where(
            mask,
            np.vectorize(lambda x,y: gauss.calc(circle.x,circle.y,x,y))(LEDs.xs,LEDs.ys),
            LEDs.size*0
            )
        scatter=ax.scatter(LEDs.ys,LEDs.xs,rad_field**2,circle.colour)
        return scatter

LEDs=LED_Array()
backdrop=ax.scatter(LEDs.ys,LEDs.xs,LEDs.size,'black')

circles=[Circle(x=0.5,y=2.0,init_vx=0.5,init_vy=0.6,colour="red"),Circle(x=0.5,y=2.0,init_vx=0.5,init_vy=0.6,colour="blue")]
circle_index=0 #define which index in circles is to be operated on by the sliders
gausses=[Gaussian(10,0.5,0.05),Gaussian(10,0.25,0.05)]
scatters=[ax.scatter(LEDs.ys,LEDs.xs,LEDs.size,'black'),ax.scatter(LEDs.ys,LEDs.xs,LEDs.size,'black')]
dot=Graph_Updater()

#create sliders
X=plt.axes([0.1,0.90,0.3,0.05])
sliderX=Slider(X,label="X",valinit=0.5,valmin=-1,valmax=2)
sliderX.on_changed(lambda new_x: sliderX_update(new_x,circles[circle_index],gausses[circle_index],scatters,circle_index))

Y=plt.axes([0.1,0.85,0.3,0.05])
sliderY=Slider(Y,label="Y",valinit=0,valmin=0.5,valmax=4)
sliderY.on_changed(sliderY_update)

R=plt.axes([0.1,0.80,0.3,0.05])
sliderR=Slider(R,label="R",valinit=0,valmin=0,valmax=1)
sliderR.on_changed(sliderR_update)

H=plt.axes([0.5,0.90,0.3,0.05])
sliderH=Slider(H,label="H",valinit=0,valmin=0,valmax=12)
sliderH.on_changed(sliderH_update)

M=plt.axes([0.5,0.85,0.3,0.05])
sliderM=Slider(M,label="M",valinit=0.5,valmin=0.0,valmax=1)
sliderM.on_changed(sliderM_update)

D=plt.axes([0.5,0.80,0.3,0.05])
sliderD=Slider(D,label="D",valinit=0.1,valmin=0.0,valmax=1)
sliderD.on_changed(sliderD_update)

for i,circle in enumerate(circles):
    scatters[i]=dot.update_graph(circle,gausses[i],LEDs)

# def animate(frame):
#     for circle in circles:
#         sliderX.set_val(sliderX.val+0.1*circle.vx)
#         sliderY.set_val(sliderY.val+0.1*circle.vy)
#         if (circle.x<sliderX.valmin) or (circle.x>sliderX.valmax):
#             circle.vx*=-1
#         if (circle.y<sliderY.valmin) or (circle.y>sliderY.valmax):  
#             circle.vy*=-1
#         return sliderX.ax,sliderY.ax

#ani=FuncAnimation(fig,animate,frames=100,interval=1,blit=True)
#ani.save('animation.gif', writer='ffmpeg')  # Export as MP4
plt.show()