import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from ipywidgets import interactive, widgets
import matplotlib.animation as animation

def plot_manipulator(angle1,angle2):
    
    link1_length = 0.3
    link2_length = 0.2
    # Convert joint angles to radians
    theta1 = np.radians(angle1)
    theta2 = np.radians(angle2)

    # Calculate end effector position
    x_end = link1_length * np.cos(theta1) + link2_length * np.cos(theta1 + theta2)
    y_end = link1_length * np.sin(theta1) + link2_length * np.sin(theta1 + theta2)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot links using patches
    link1 = patches.Rectangle((0, 0), link1_length, 0.05, angle=np.degrees(theta1), ec='black', fc='C0',alpha=0.5)
    link2 = patches.Rectangle((link1_length * np.cos(theta1), link1_length * np.sin(theta1)), link2_length, 0.05,
                              angle=np.degrees(theta1 + theta2), ec='black', fc='C1',alpha=0.5)
    
    ground = patches.Rectangle((-1, -1), 2, 0.5, angle=0, fc='C2',alpha=0.7)

    # Add patches to the axis
    ax.add_patch(link1)
    ax.add_patch(link2)
    ax.add_patch(ground)
    
    # Set plot limits and aspect ratio
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    ax.set_aspect('equal', 'box')

    # Set labels and title
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Simple Leg')

    # Show the plot
    plt.grid(True)
    
def f(**kwargs):
    plot_manipulator(**kwargs)
    # plt.show()
    

sldr = lambda v, mi, ma: widgets.FloatSlider(
    value=v,
    min=mi,
    max=ma,
    step=.01,
)

names = [
    ['angle1', [-45, -180, 180]],
    ['angle2', [30, -180, 180]],
]

i_sldr = lambda v, mi, ma: widgets.IntSlider(
    value=v,
    min=mi,
    max=ma,
    step=1,
)

interactive_leg = interactive(f, **{s[0] : sldr(*s[1]) for s in names})

def f_gait(**kwargs):
    
    plot_manipulator(**kwargs)


class GaitTrajectory:
    
    def __init__(self,theta_1,theta_2):
         
        assert len(theta_1)==len(theta_2),"The number of hip angles (%d) must equal the number of knee angles (%d)."%(len(theta_1),len(theta_2))
         
        self.theta_1 = theta_1+theta_1
        self.theta_2 = theta_2+theta_2
        
        self.rn = [0,0,min(len(self.theta_1),len(self.theta_2))-1]
        
        
    def plot_m(self,timestep):
        
        plot_manipulator(self.theta_1[timestep],self.theta_2[timestep])
        self.plot_foot_trajectory()
        # plt.show()
        
    def get_plot(self):
        
        return interactive(self.plot_m, **{'timestep':i_sldr(*self.rn)})
    
    
    def plot_foot_trajectory(self):
        
        
        link1_length = 0.3
        link2_length = 0.2
        # Convert joint angles to radians
        theta1 = np.radians(self.theta_1)
        theta2 = np.radians(self.theta_2)

        # Calculate end effector position
        x_end = link1_length * np.cos(theta1) + link2_length * np.cos(theta1 + theta2)
        y_end = link1_length * np.sin(theta1) + link2_length * np.sin(theta1 + theta2)
        
        
        plt.plot(x_end,y_end,label='foot position')
        plt.grid(True)
    
def plot_foot_trajectory(theta_1,theta_2):
    
        assert len(theta_1)==len(theta_2),"The number of hip angles (%d) must equal the number of knee angles (%d)."%(len(theta_1),len(theta_2)) 
        
        link1_length = 0.3
        link2_length = 0.2
        # Convert joint angles to radians
        theta1 = np.radians(theta_1)
        theta2 = np.radians(theta_2)

        # Calculate end effector position
        x_end = link1_length * np.cos(theta1) + link2_length * np.cos(theta1 + theta2)
        y_end = link1_length * np.sin(theta1) + link2_length * np.sin(theta1 + theta2)
        
        plt.plot(x_end,'-o',label='foot x position')
        plt.plot(y_end,'-o',label='foot y position')

        plt.grid(True)
        plt.legend()
        
        plt.show()
