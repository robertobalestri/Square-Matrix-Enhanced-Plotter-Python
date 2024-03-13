import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
print(matplotlib.get_backend())

matplotlib.use('Qt5Agg')

min_size_global = 5

class SquareMatrix:
    
    def __init__(self, matrix, title, ax=None):
        self.matrix = matrix
        self.title = title
        self.ratio = len(matrix[0]) / len(matrix)  # compute the aspect ratio

        
        if ax is None:
            self.fig, self.ax = plt.subplots(figsize=plt.figaspect(self.ratio) * 1.5)
        else:
            self.ax = ax
            self.fig = ax.get_figure()
            self.fig.set_size_inches(*plt.figaspect(self.ratio) * 1.5) # set the figure's size
        
        print(f"Matrix dtype before imshow: {matrix.dtype}")
        self.cax = self.ax.imshow(matrix, cmap='gray', interpolation='nearest', origin='lower',)
        
        # Set initial view to match the full extent of the matrix
        self.ax.set_xlim([0, self.matrix.shape[1] - 0.5])
        self.ax.set_ylim([0, self.matrix.shape[0]  - 0.5])
        
        #plt.colorbar(self.cax, ax=self.ax)
        self.ax.set_title(title)
        self.ax.set_aspect('equal', adjustable='box')
        
        
         # Store the initial size of the figure
        self.initial_figsize = self.fig.get_size_inches()
        
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()
        self.initial_xrange = self.initial_xlim[1] - self.initial_xlim[0]
        self.initial_yrange = self.initial_ylim[1] - self.initial_ylim[0]

        # Call to set the tick labels
        self.update_tick_labels()  # Set initial tick labels
        
        self.cursor = mplcursors.cursor(self.ax, hover=True)
    

        @self.cursor.connect("add")
        def on_add(sel):
            
            # Convert the floating point coordinates to integer matrix indices
            x, y = int(round(sel.target[0])), int(round(sel.target[1]))
            if 0 <= x < self.matrix.shape[1] and 0 <= y < self.matrix.shape[0]:
                sel.annotation.set_text(f'x={x}, y={y}')
            else:
                sel.annotation.set_text('Out of bounds')
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

            
        self.fig.canvas.mpl_connect('scroll_event', self.zoom_fun)
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_dragging)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        # Connect the resize event of the figure to the on_resize method
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)

        self.dragging = False
        self.press = None
        
        self.update_needed = False
        self.update_timer = None
        
    def update_tick_labels(self):
        # Get the current view range for both axes
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # Set the number of ticks
        num_ticks = 10

        # Generate evenly spaced ticks within the current view limits
        xticks = np.linspace(x_min + 0.5, x_max - 0.5, num_ticks)
        yticks = np.linspace(y_min + 0.5, y_max - 0.5, num_ticks)

        # Ensure that the ticks are within the valid range
        xticks = np.clip(xticks, 0.5, self.matrix.shape[1] - 0.5)
        yticks = np.clip(yticks, 0.5, self.matrix.shape[0] - 0.5)

        # Round ticks to nearest integer and ensure uniqueness
        xticks = np.unique(np.round(xticks).astype(int))
        yticks = np.unique(np.round(yticks).astype(int))

        # Set the tick positions and labels
        self.ax.set_xticks(xticks)
        self.ax.set_yticks(yticks)
        self.ax.set_xticklabels([str(tick) for tick in xticks])
        self.ax.set_yticklabels([str(tick) for tick in yticks])

         # Set minor ticks at positions shifted by 0.5 from the major ticks
        self.ax.set_xticks(xticks - 0.5, minor=True)
        self.ax.set_yticks(yticks - 0.5, minor=True)

        # Disable tick marks by setting their size to 0
        self.ax.tick_params(axis='both', which='major', length=0)
        
        # Disable tick marks by setting their size to 0
        self.ax.tick_params(axis='both', which='minor', length=5)

        # Enable grid only for minor ticks, offset by 0.5
        #self.ax.grid(True, which='minor', axis='both', linestyle='-', linewidth=0.2)

        # Optionally, turn off major grid lines
        #self.ax.grid(False, which='major')
    
    def request_update_tick_labels(self):
        self.update_needed = True
        if self.update_timer is None:
            self.update_timer = self.fig.canvas.new_timer(interval=100)  # 100ms delay
            self.update_timer.single_shot = True
            self.update_timer.add_callback(self.perform_update_tick_labels)
            self.update_timer.start()

    def perform_update_tick_labels(self):
        if self.update_needed:
            self.update_tick_labels()
            self.update_needed = False
        self.update_timer = None
        
    def zoom_fun(self, event):
        if event.inaxes != self.ax:
            return

        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        range = max(x_max - x_min, y_max - y_min)

        x_center = x_min + range / 2
        y_center = y_min + range / 2

        if event.button == 'up':
            # Check if the current range is already at the minimum size
            if range <= min_size_global:
                print('Blocked')
                return

            scale_factor = 1 / 2
            #self.on_release(event)
            self.request_update_tick_labels()
                
        elif event.button == 'down':
            scale_factor = 2
            #self.on_release(event)
            self.request_update_tick_labels()

        else:
            return

        new_range = range * scale_factor

        # Adjust the new limits considering the 0.5 bias
        new_xlim = np.clip([x_center - new_range / 2, x_center + new_range / 2], 0, self.matrix.shape[1] - 0.5)
        new_ylim = np.clip([y_center - new_range / 2, y_center + new_range / 2], 0, self.matrix.shape[0] - 0.5)

        # Update axes limits
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)

        #self.on_resize(None)  # Update the colorbar after zooming
        
        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        if event.button == 1:
            self.press = event.xdata, event.ydata
            self.dragging = True

        if self.ax.get_ylim() == self.initial_ylim or self.ax.get_xlim() == self.initial_xlim:
            self.dragging = False
            self.press = None
            

    def on_dragging(self, event):
        if self.press is None or not self.dragging:
            self.on_resize(None)  
            return

        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            self.dragging = False
            self.press = None
            self.on_release(event) 
            return

        x_press, y_press = self.press
        dx = event.xdata - x_press
        dy = event.ydata - y_press

        current_xlim = self.ax.get_xlim()
        current_ylim = self.ax.get_ylim()

        # Calculate potential new limits, without the 0.5 offset
        new_xlim = np.clip([current_xlim[0] - dx, current_xlim[1] - dx], 0, self.matrix.shape[1])
        new_ylim = np.clip([current_ylim[0] - dy, current_ylim[1] - dy], 0, self.matrix.shape[0])

        # Adjust new limits to maintain the view size
        new_xlim = np.clip(new_xlim, 0, self.matrix.shape[1] - 0.5)
        new_ylim = np.clip(new_ylim, 0, self.matrix.shape[0] - 0.5)
        
        # Calculate current range after setting new limits
        x_range = new_xlim[1] - new_xlim[0]
        y_range = abs(new_ylim[1] - new_ylim[0])  # Correct for the absolute value



        # Ensure the aspect ratio is maintained while dragging
        aspect_ratio = self.matrix.shape[1] / self.matrix.shape[0]
        if x_range > y_range * aspect_ratio:
            y_range = x_range / aspect_ratio
        elif y_range > x_range / aspect_ratio:
            x_range = y_range * aspect_ratio
            
        # Determine the smaller range but do not go below the global minimum size
        smaller_range = max(min(x_range, y_range), min_size_global)
            
        # If current range is smaller than minimum, adjust the limits
        if smaller_range > min(x_range, y_range):
            self.on_release(event)
        
        # Set the new limits
        self.ax.set_xlim(new_xlim[0], new_xlim[0] + x_range)
        self.ax.set_ylim(new_ylim[0], new_ylim[0] + y_range)
        
        self.fig.canvas.draw_idle()
        self.on_resize(None)

    def handle_minimum_range(self, ax, matrix, initial_xlim, initial_ylim, min_size):
        # Current axis limits and ranges
        current_xlim = ax.get_xlim()
        current_ylim = ax.get_ylim()
        x_range = current_xlim[1] - current_xlim[0]
        y_range = abs(current_ylim[1] - current_ylim[0])  # Correct for the absolute value

        # Determine the smaller range but do not go below the global minimum size
        smaller_range = max(min(x_range, y_range), min_size)

        # Calculate the center for both axes
        x_center = (current_xlim[0] + current_xlim[1]) / 2
        y_center = (current_ylim[0] + current_ylim[1]) / 2

        # Set new limits based on the smaller range
        new_xlim = [x_center - smaller_range / 2, x_center + smaller_range / 2]
        new_ylim = [y_center - smaller_range / 2, y_center + smaller_range / 2]

        # Apply the new limits, ensuring we stay within the matrix's boundaries
        new_xlim[0] = max(new_xlim[0], 0)
        new_xlim[1] = min(new_xlim[1], matrix.shape[1])
        new_ylim[0] = max(new_ylim[0], 0)
        new_ylim[1] = min(new_ylim[1], matrix.shape[0])

        # Check if y-axis is inverted and adjust accordingly
        if ax.get_ylim()[1] < ax.get_ylim()[0]:
            new_ylim = new_ylim[::-1]

        # Apply the new limits, ensuring we stay within the matrix's boundaries
        new_ylim = np.clip(new_ylim, 0, matrix.shape[0] - 0.5)
        new_xlim = np.clip(new_xlim, 0, matrix.shape[1] - 0.5)
        
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)


    def on_release(self, event):
        print('Released')
        self.dragging = False
        self.press = None
        self.handle_minimum_range(self.ax, self.matrix, self.initial_xlim, self.initial_ylim, min_size_global)
        self.on_resize(None)  

        self.fig.canvas.draw_idle()
        self.request_update_tick_labels()
        
        plt.gca().set_aspect('equal', adjustable='box')         

    def show(self):
        plt.show()
        
    def on_resize(self, event):
        pass
        """Recreates the colorbar to match the current plot."""
        #if hasattr(self, 'cbar')  and self.cbar:
            
            #try:
            #    self.cbar.remove()
            #except KeyError:
            #    pass

        #divider = make_axes_locatable(self.ax)
        #cax = divider.append_axes("right", size="5%", pad=0.05)
        #self.cbar = plt.colorbar(self.cax, cax=cax)

def plot_matrix(matrix, title):
    fig, ax = plt.subplots(figsize=(5, 5))
    zoomable_matrix = SquareMatrix(matrix, title, ax=ax)
    
    #divider = make_axes_locatable(ax)
    #cax = divider.append_axes("right", size="2%", pad=0.05)
    #zoomable_matrix.cbar = plt.colorbar(zoomable_matrix.cax, cax=cax)  # Store the colorbar

    plt.show()

def plot_matrices_side_by_side(*matrices, titles=None):
    n_matrices = len(matrices)
    fig, axes = plt.subplots(1, n_matrices, figsize=(5 * n_matrices, 5))

    if titles is None:
        titles = ['Matrix {}'.format(i+1) for i in range(n_matrices)]

    for ax, matrix, title in zip(axes, matrices, titles):
        zoomable_matrix = SquareMatrix(matrix, title, ax=ax)
        #divider = make_axes_locatable(ax)
        #cax = divider.append_axes("right", size="2%", pad=0.05)
        #zoomable_matrix.cbar = plt.colorbar(zoomable_matrix.cax, cax=cax)  # Store the colorbar



    plt.tight_layout()
    plt.show()
    
def plot_matrices_in_grid(matrices, titles=None, row_max=3, hspace=0.01):
    n_matrices = len(matrices)
    
    nrows = (n_matrices + row_max - 1) // row_max
    ncols = min(n_matrices, row_max)
    
    # Adjust figsize here, you might need to experiment with these values
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3 * nrows))
    
    if titles is None:
        titles = ['Matrix {}'.format(i + 1) for i in range(n_matrices)]

    if nrows > 1:
        axes = axes.flatten()

    for i, (matrix, title) in enumerate(zip(matrices, titles)):
        if nrows == 1:
            ax = axes[i]
        else:
            ax = axes[i] if i < len(axes) else fig.add_subplot(nrows, ncols, i + 1)
        
        SquareMatrix(matrix, title, ax=ax)

    for j in range(i + 1, nrows * ncols):
        fig.delaxes(axes[j])

    # Comment out tight_layout if it interferes with subplots_adjust
    # plt.tight_layout()

    # Adjust the height space between rows
    plt.subplots_adjust(hspace=hspace)
    
    plt.show()
