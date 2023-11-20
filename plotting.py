import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, show
from bokeh.models.glyphs import Quad


def interactive_leg():
  # Initialize the angles (in radians)
  theta1 = np.radians(-90)
  theta2 = np.radians(0)

  l1, l2 = 0.3, 0.2

  x0, y0 = 0, 0
  x1 = l1 * np.cos(theta1)
  y1 = l1 * np.sin(theta1)
  x2 = x1 + l2 * np.cos(theta1 + theta2)
  y2 = y1 + l2 * np.sin(theta1 + theta2)

  source1 = ColumnDataSource(data=dict(x=[x0, x1], y=[y0, y1]))
  source2 = ColumnDataSource(data=dict(x=[x1, x2], y=[y1, y2]))

  plot = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1))
  plot.line('x', 'y', source=source1, line_width=3, line_alpha=0.6, color="blue")
  plot.line('x', 'y', source=source2, line_width=3, line_alpha=0.6, color="orange")

  ground = Quad(left=-1, right=1, top=-0.5, bottom=-1, fill_color="green", line_color="green", fill_alpha = 0.5)
  plot.add_glyph(ground)

  theta1_slider = Slider(start=-180, end=180, value=-90, step=1, title="angle1")
  theta2_slider = Slider(start=-180, end=180, value=0, step=1, title="angle2")

  callback = CustomJS(args=dict(source1=source1, source2=source2, theta1=theta1_slider, theta2=theta2_slider, l1=l1, l2=l2),
                      code="""
      const theta1_rad = (theta1.value * Math.PI) / 180;
      const theta2_rad = (theta2.value * Math.PI) / 180;

      const x1 = l1 * Math.cos(theta1_rad);
      const y1 = l1 * Math.sin(theta1_rad);
      const x2 = x1 + l2 * Math.cos(theta1_rad + theta2_rad);
      const y2 = y1 + l2 * Math.sin(theta1_rad + theta2_rad);

      source1.data = { x: [0, x1], y: [0, y1] };
      source2.data = { x: [x1, x2], y: [y1, y2] };
  """)

  theta1_slider.js_on_change('value', callback)
  theta2_slider.js_on_change('value', callback)

  show(column(theta1_slider, theta2_slider, plot))


def GaitTrajectory(theta1_list, theta2_list):

  l1, l2 = 0.3, 0.2

  def calculate_end_effector(theta1, theta2):
      theta1_rad = np.radians(theta1)
      theta2_rad = np.radians(theta2)
      x1 = l1 * np.cos(theta1_rad)
      y1 = l1 * np.sin(theta1_rad)
      x2 = x1 + l2 * np.cos(theta1_rad + theta2_rad)
      y2 = y1 + l2 * np.sin(theta1_rad + theta2_rad)
      return x2, y2

  trajectory_x, trajectory_y = zip(*[calculate_end_effector(theta1, theta2) for theta1, theta2 in zip(theta1_list, theta2_list)])

  initial_angles = (theta1_list[0], theta2_list[0])
  x0, y0 = 0, 0
  x1 = l1 * np.cos(np.radians(theta1_list[0]))
  y1 = l1 * np.sin(np.radians(theta1_list[0]))
  x2 = x1 + l2 * np.cos(np.radians(theta1_list[0] + theta2_list[0]))
  y2 = y1 + l2 * np.sin(np.radians(theta1_list[0] + theta2_list[0]))

  source_manipulator = ColumnDataSource(data=dict(x=[x0, x1, x2], y=[y0, y1, y2]))
  source_trajectory = ColumnDataSource(data=dict(x=trajectory_x, y=trajectory_y))

  plot = figure(width=400, height=400, x_range=(-1, 1), y_range=(-1, 1))

  plot.line('x', 'y', source=source_trajectory, line_width=1, color="gray", alpha=0.6)
  plot.circle('x', 'y', source=source_trajectory, size=5, color="gray", alpha=0.6)

  plot.line('x', 'y', source=source_manipulator, line_width=3, line_alpha=0.6, color="blue")

  ground = Quad(left=-1, right=1, top=-0.5, bottom=-1, fill_color="green", line_color="green", fill_alpha=0.5)
  plot.add_glyph(ground)

  time_step_slider = Slider(start=0, end=len(theta1_list)-1, value=0, step=1, title="Time Step")

  callback = CustomJS(args=dict(source_manipulator=source_manipulator, time_step_slider=time_step_slider, theta1_list=theta1_list, theta2_list=theta2_list, l1=l1, l2=l2),
                      code="""
      const time_step = time_step_slider.value;
      const theta1_deg = theta1_list[time_step];
      const theta2_deg = theta2_list[time_step];
      const theta1_rad = theta1_deg * Math.PI / 180;
      const theta2_rad = theta2_deg * Math.PI / 180;

      const x1 = l1 * Math.cos(theta1_rad);
      const y1 = l1 * Math.sin(theta1_rad);
      const x2 = x1 + l2 * Math.cos(theta1_rad + theta2_rad);
      const y2 = y1 + l2 * Math.sin(theta1_rad + theta2_rad);

      source_manipulator.data = { x: [0, x1, x2], y: [0, y1, y2] };
  """)

  time_step_slider.js_on_change('value', callback)

  show(column(plot, time_step_slider))
