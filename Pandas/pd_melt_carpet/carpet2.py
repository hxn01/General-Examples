# RESOURCES:
# carpet plots: https://en.wikipedia.org/wiki/Carpet_plot
# good plotly offline examples: https://github.com/SayaliSonawane/Plotly_Offline_Python/blob/master/Line%20Chart/line_chart.py
# other python for carpet plots: https://github.com/steve855/pyCarpetPlot/blob/master/pyCarpetPlot.py

#!/usr/local/bin/python
"""

    pyCarpetPlot.py 

Library of functions to generate carpet plots 

Copyright (c) 2004-2013 by pyACDT Developers
All rights reserved.
Revision: Stephen Andrews - $Date: 02/04/2014$


Developers:
-----------
- Stephen Andrews (SA) 

History
-------
    v. Stephen Andrews  - 
"""

__version__ = '$Revision: $'

"""
To Do:
    - 
"""

# =============================================================================
# Standard Python modules
# =============================================================================
import os, sys
import pdb
from math import radians, sin, cos, ceil

# =============================================================================
# External Python modules
# =============================================================================
import numpy
import matplotlib.pyplot as plt

# =============================================================================
# Extension modules
# =============================================================================
sys.path.append(os.path.abspath('../'))

# =============================================================================
# 
# =============================================================================

def carpet_plot(x1, x2, y, ofst = 1.0, ofst2 = 0.0, axis = None, x1_skip = 1, x2_skip = 1, idep2_style = None,
        label1 = '', label2 = '',  label1_loc = 'end', label2_loc = 'end', label1_ofst = (15, 0), label2_ofst = (15, 0), 
        title = '', title_loc = (1.0, 0.9), dep_title = '', contour_data = None, contour_format = [{}], clabel_format = {}, x_cheat_out = None):
    '''

    Generates a carpet plot of the data 

    Plots the data in :math:`y` against the 'cheater axis' 

    _math::

        x_{cheat} = x_1 + \mathrm{ofst} \cdot x_2

    This shows the relationship between x1 and x2 with y but destroys information about how y varries with
    x1 and x2 

    **Inputs** 

    - x1 -> (n x 1) numpy array: Vector of first independent values.
    - x2 -> (m x 1) numpy array: Vector of second independent values.
    - y -> (n x m) numpy.array: Matrix of dependant values.
    - ofst -> FLOAT: Offset factor, can be used to change the shape of the plot, *Default 1.0*
                        - ofst = 1 : trend of y with x1 and x2 of similar magnitude
                        - ofst > 1 : trend of y with x2 more pronounced 
                        - ofst < 1 : trend of y with x1 more pronounced
    - ofst2 -> FLOAT: Offset for plotting multiple carpet plots on one axis
    - idep2_style -> STR: Format string for second independent variable lines. None is same as x1 *Default: None*
    - axis -> matplotlib.pyplot.axis: An axis object to plot on
    - x1_skip -> INT: Value n to read every n values. 
    - x2_skip -> INT: Value n to read every n values.
    - label1 -> STR: Labels to append to the curves of x1. *Default: ''* 
    - label2 -> STR: Labels to append to the curves of x2. *Default: ''* 
    - label1_loc -> STR: Location of x1 labels. *Default: 'end'* 
                    - 'end': at the end of the data 
                    - 'start': at the start of the data 
                    - None: do not show labels
    - label2_loc -> STR: Location of x2 labels. *Default: 'end'* 
                    - 'end': at the end of the data 
                    - 'start': at the start of the data 
                    - None: do not show labels
    - label1_ofst -> 2-TUPPLE: X and Y offset, in pixels, from the selected vertex 
    - label2_ofst -> 2-TUPPLE: X and Y offset, in pixels, from the selected vertex
    - title -> STR: String to place above the carpet plot
    - title_loc -> 2-TUPPLE: X and Y modifiers for the title location 
            - [0] modifier to the midpoint of the x range 
            - [1] modifier to the max y point
    - dep_title -> STR: Title to append to the dependent axis
    - contour_data - > LIST of (n x m) numpy.array: List of  matrices of dependent values to plot as a contour. *Default: None*
    - contour_format -> LIST of DICT: List of Dictionaries of contour formating inputs 
    - cabel_format -> LIST DICT: List of Dictionaries of contour label formating inputs 
    - x_cheat_out -> LIST: IO variable for cheater axis values

    '''

    # Input checks and conditioning
    y = numpy.array(y)
    # contour_data = numpy.array(contour_data)

    # for var in [y, contour_data]: 
    #     if var.shape == (): 
    #         pass
    #     elif not (len(x2), len(x1)) == var.shape:
    #         raise Exception('Shape of input does not agree %s != (%d x %d)'%(var.shape, len(x2), len(x1)))
    #     #end
    # #end

    def label_map(label_loc):     
        if label_loc == None : return None
        elif label_loc.lower()[0] == 's': return 0
        elif label_loc.lower()[0] == 'e': return -1
        else: raise Exception('Invalid data label location')
    #end
    
    label1_loc, label2_loc = map(label_map, [label1_loc, label2_loc])

    xx1, xx2 = numpy.meshgrid(x1, x2)

    # pdb.set_trace()
    x_cheat = ofst2 + (xx1 + ofst * xx2)
    x_cheat_out = x_cheat
    # x_cheat = ofst2 + (xx1 + 10.0 * xx2)
    
    if axis == None:
        ax1 = plt.subplot(111)
    else:
        ax1 = axis
    #end

    if idep2_style == None:
        idep2_style = '-k'
    #end

    for i in range(0,len(x1),x1_skip):
        ax1.plot(x_cheat[:,i], y[:,i], idep2_style)
        if not label1_loc == None:
            ax1.annotate(r'%s%3.2f'%(label1, x1[i]), xy = (x_cheat[label1_loc,i], y[label1_loc,i]), xytext = label1_ofst, textcoords = 'offset points')
        #end
    #end
    for i in range(0,len(x2),x2_skip):
        ax1.plot(x_cheat[i,:], y[i,:], '-k')
        if not label2_loc == None:
            ax1.annotate(r'%s%3.2f'%(label2, x2[i]), xy = (x_cheat[i,label2_loc], y[i,label2_loc]), xytext = label2_ofst, textcoords = 'offset points')
        #end
    #end

    if title == '':
        pass
    else:
        ax1.annotate('%s'%(title), xy = (title_loc[0] * 0.5 * (numpy.max(x_cheat) + numpy.min(x_cheat)), title_loc[1] * numpy.max(y)), xytext = (0,0), textcoords = 'offset points', bbox = {'facecolor':'white', 'alpha':0.5})
    #end

    if not contour_data == None:
        try:
            for i in range(len(contour_data)):
                if 'filled' in contour_format[i]:
                    filled = contour_format[i].pop('filled')
                    format_dict = {}
                else:
                    filled = False
                    format_dict = {'colors': 'b'}
                #end
                format_dict.update(contour_format[i])
                if filled:
                    CS = ax1.contourf(x_cheat, y, contour_data[i], **format_dict)
                else:
                    CS = ax1.contour(x_cheat, y, contour_data[i], **format_dict)
                format_dict = {'fontsize': 9, 'inline':1}
                format_dict.update(clabel_format)
                ax1.clabel(CS, **format_dict)
            #end
        except Exception as inst:
            pdb.post_mortem()
            raise Exception("pyCarpetPlot: Could not plot contours of independent data due to %s"%(inst))
            pass
        #end
    #end

    ax1.set_ylabel(dep_title)
    ax1.axes.get_xaxis().set_visible(False)

    return ax1
#end

def hatched_line(x, y, axis, spc = 0.03, theta = 45, len_tick = 0.015, flip = False, linestyle = None):
    try:
        from scipy.interpolate import interp1d 
    except:
        raise Exception('scipy required to plot hatched lines')
    #end

    x = numpy.array(x)
    y = numpy.array(y)
    
    # Calculate the aspect ratio of the plot
    aspect_ratio = axis.axis()
    aspect_ratio = (aspect_ratio[1] - aspect_ratio[0]) / (aspect_ratio[3] - aspect_ratio[2])

    if flip:
        flip = -1
    else:
        flip = 1
    #end

    # Calcualte the distance along the curve
    ds = numpy.sqrt((x[1:] - x[:-1])**2 + ((y[1:] - y[:-1])*aspect_ratio)**2)
    s_tot = sum(ds)
    ds = numpy.concatenate(([0.0], numpy.cumsum(ds)))

    # Determine the x and y corrdinates of the tick root
    s_tick = numpy.linspace(0, s_tot, ceil(1 / spc))
    x_tick = interp1d(ds, x, bounds_error = False)(s_tick)
    y_tick = interp1d(ds, y, bounds_error = False)(s_tick)

    # Calcualte the normal to the curve at the tick root
    delta_s = spc * s_tot
    v_tick = (x_tick - interp1d(ds, x, bounds_error = False)(s_tick + delta_s)) / delta_s
    u_tick = (y_tick - interp1d(ds, y, bounds_error = False)(s_tick + delta_s)) / (delta_s * aspect_ratio)
    n = numpy.sqrt(u_tick **2 + v_tick **2)
    
    # Calcualte the offset in x and y for the tick
    theta = radians(theta)
    trans_matrix = numpy.array([[cos(theta), -sin(theta)],[sin(theta), cos(theta)]])
    dxy = numpy.dot(numpy.array([u_tick / n , v_tick / n]).T, trans_matrix) * len_tick * s_tot 

    # Draw the base line
    base_line = plt.Line2D(x_tick, y_tick)
    axis.add_line(base_line)

    # Draw each tick
    for i in range(len(x_tick)):
        axis.add_line(plt.Line2D([x_tick[i], x_tick[i] - flip * dxy[i,0]], [y_tick[i], (y_tick[i] - flip * dxy[i,1] / aspect_ratio)]))
    #end

    return axis
#end




f = lambda x1 ,x2: x1**2+x2**1-2*x1-2*x2+2

x1 = numpy.linspace(2,5,4)
x2 = numpy.linspace(1,3,3)

fobj = []
for i in range(len(x1)):
	tmp = []
	for j in range(len(x2)):
		tmp.append(f(x1[i], x2[j]))
	#end
	fobj.append(tmp)
#end

fobj = numpy.array(fobj)

print(x1)
print(x2)
print(fobj)

# pdb.set_trace()
ax1 = carpet_plot(x1,x2,fobj.T, ofst = 1, label1 = r'$x_{1}=$', label2 = r'$x_{2}=$', 
	label1_loc = 'end', dep_title = 'Dependant Variable', title = 'Graph Title')
plt.show()




