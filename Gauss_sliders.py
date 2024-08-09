from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

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

X=plt.axes([0.1,0.90,0.3,0.05])
sliderX=Slider(X,label="X",valinit=0.5,valmin=-1,valmax=2)
sliderX.on_changed(lambda new_x: sliderX_update(new_x,circles[circle_index],gausses[circle_index],scatters,circle_index))

