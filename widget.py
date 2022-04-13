import datetime
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import matplotlib.widgets as widgets

# Usage:
#
# 1) Import this module.
# >> import widget
#
# 2) Prepare the data to be displayed.
# >> data = np.random.normal(0, 2, (262, 1639))
#
# 3) Initialize the widget as follows.
# >> widget.PrizmScope(data)

class PrizmScope:
    """ . """

    # PRIZM data.
    data = None

    # Matplotlib objects.
    figure = None
    axes = dict()
    plots = dict()
    buttons = dict()
    sliders = dict()
    controls = dict()
    selectors = dict()
    colormaps = {'red': pyplot.cm.Reds, 'blue': pyplot.cm.Blues, 'black': pyplot.cm.Greys}

    # Boolean status indicators.
    active_selector = None
    active_button = None
    active_control = None


    def __init__(self, data):
        """ . """

        # Initializes the figure.
        self.figure = pyplot.figure(figsize=(6,6))

        # Plots
        self.data = data
        self.plot()


    def plot(self):
        """ Plots the input data as an interactive spectrogram. """

        # Initializes all plot and widget axes.
        self.add_axes()

        # Populates the spectrogram and colorscale axes with their respective plots.
        self.plots['spectrogram'] = self.axes['spectrogram'].imshow(self.data, interpolation='none', cmap=pyplot.cm.RdBu, aspect='auto')
        self.plots['colorscale'] = self.figure.colorbar(self.plots['spectrogram'], cax=self.axes['colorscale'], orientation='horizontal')

        # Initializes all interactive widgets.
        self.add_buttons()
        self.add_sliders()
        self.add_controls()
        self.add_selectors()

        # Displays everything.
        pyplot.show()

        return


    def add_axes(self):
        """ Initializes all axes. """

        axes_parameters = [
            ('colorscale',    [.10,.91,.80,.02],    'top', 'none',      None, None,                    None,                               None, None, None, 'black', 0),
            ('colortuner',    [.10,.91,.80,.01],   'none', 'none',      None, None,                    None,                               None,   [],   [], 'black', 1),
            ('spectrogram',   [.10,.52,.80,.30],   'none', 'none',      None, None,                    None,                               None,   [],   [], 'black', 1),
            ('spectragraph',  [.10,.22,.80,.30], 'bottom', 'left', 'ν (MHz)', None, [0, self.data.shape[1]], [self.data.min(), self.data.max()], None, None, 'black', 1),
            ('scaletuner',    [.90,.22,.01,.30],   'none', 'none',      None, None,                    None,                               None,   [],   [], 'black', 0),
            ('blackbutton',   [.88,.82,.02,.02],   'none', 'none',      None, None,                    None,                               None,   [],   [], 'white', 0),
            ('bluebutton',    [.86,.82,.02,.02],   'none', 'none',      None, None,                    None,                               None,   [],   [], 'white', 0),
            ('redbutton',     [.84,.82,.02,.02],   'none', 'none',      None, None,                    None,                               None,   [],   [], 'white', 0),
            ]

        for (name, box, xtickposition, ytickposition, xlabel, ylabel, xlimits, ylimits, xticklabels, yticklabels, framecolor, level) in axes_parameters:
            # Initializes the axes.
            self.axes[name] = self.figure.add_axes(box)

            # Sets the tick positions for both the 'x' and 'y' axes.
            self.axes[name].xaxis.set_ticks_position(xtickposition)
            self.axes[name].yaxis.set_ticks_position(ytickposition)

            # Sets the labels for both the 'x' and 'y' axes.
            self.axes[name].xaxis.set_label_text(xlabel)
            self.axes[name].yaxis.set_label_text(ylabel)

            # Sets the limits for both the 'x' and 'y' axes.
            if xlimits is not None: self.axes[name].set_xlim(xlimits)
            if ylimits is not None: self.axes[name].set_ylim(ylimits)

            # Sets the tick labels for both the 'x' and 'y' axes.
            if xticklabels is not None: self.axes[name].set_xticklabels(xticklabels)
            if yticklabels is not None: self.axes[name].set_yticklabels(yticklabels)

            # Sets the color for the axes frame.
            self.axes[name].spines['bottom'].set_color(framecolor)
            self.axes[name].spines['top'].set_color(framecolor)
            self.axes[name].spines['right'].set_color(framecolor)
            self.axes[name].spines['left'].set_color(framecolor)

            # Sets the axes layer level.
            self.axes[name].set_zorder(level)

        return


    def add_buttons(self):
        """ Initializes all button widgets. """

        buttons_parameters = [
            ('black', self.axes['blackbutton'], None, self.set_selector, self.colormaps['black'](0.8), self.colormaps['black'](0.8)),
            ('blue',   self.axes['bluebutton'], None, self.set_selector,  self.colormaps['blue'](0.2),  self.colormaps['blue'](0.8)),
            ('red',     self.axes['redbutton'], None, self.set_selector,   self.colormaps['red'](0.2),   self.colormaps['red'](0.8)),
            ]

        for (name, axes, label, function, color, hovercolor) in buttons_parameters:
            # Initializes a button.
            self.buttons[name] = widgets.Button(axes, label, color=color, hovercolor=hovercolor)

            # Sets the button function.
            self.buttons[name].on_clicked(function)

        return


    def add_sliders(self):
        """ Initializes all slider widgets. """

        sliders_parameters = [
            ('scaletuner', self.axes['scaletuner'], None,  self.set_scale, (self.data.min(), self.data.max()),   'vertical', 'black', False),
            ('colortuner', self.axes['colortuner'], None, self.set_colors, (self.data.min(), self.data.max()), 'horizontal', 'black', False),
            ]

        for (name, axes, label, function, limits, orientation, color, visible) in sliders_parameters:
            # Initializes a slider.
            self.sliders[name] = widgets.RangeSlider(axes, label, min(limits), max(limits), valinit=limits, orientation=orientation, color=color)

            # Sets the slider function and visibility.
            self.sliders[name].on_changed(function)
            self.sliders[name].valtext.set_visible(visible)

        return


    def add_controls(self):
        """ Initializes all control widgets. """

        controls_parameters = [
            ]

        for (name, axes, label, function, color, hovercolor, labelcolor) in controls_parameters:
            # Initializes a control button.
            self.controls[name] = widgets.Button(axes, label, color=color, hovercolor=hovercolor)

            # Sets the button function and label color.
            self.controls[name].label.set_color(labelcolor)
            self.controls[name].on_clicked(function)

        return


    def add_selectors(self):
        """ Initializes all span selector widgets. """

        selectors_parameters = [
            ('black', self.axes['spectrogram'], self.set_span, 'vertical', dict(alpha=0.5, edgecolor='black', facecolor='black', linewidth=1.0), True,  True),
            ('red',   self.axes['spectrogram'], self.set_span, 'vertical', dict(alpha=0.5,   edgecolor='red',   facecolor='red', linewidth=1.0), True, False),
            ('blue',  self.axes['spectrogram'], self.set_span, 'vertical', dict(alpha=0.5,  edgecolor='blue',  facecolor='blue', linewidth=1.0), True, False),
            ]

        for (name, axes, function, orientation, rectprops, span_stays, active) in selectors_parameters:
            # Initializes a span selector.
            self.selectors[name] = widgets.SpanSelector(axes, function, orientation, rectprops=rectprops, span_stays=span_stays)#, useblit=True)

            # Sets the selector initial state.
            self.selectors[name].set_active(active)

        return


    def set_selector(self, event):
        """ Sets the span selector. """

        # Activates span selector whose color matches the clicked button.
        for name, selector in self.selectors.items(): selector.set_active(event.inaxes == self.buttons[name].ax)

        # Sets the color of each button.
        for name, button in self.buttons.items():
            if event.inaxes == button.ax: button.color = self.colormaps[name](0.8)
            if event.inaxes != button.ax: button.color = self.colormaps[name](0.2)
            event.inaxes.figure.canvas.draw_idle()

        # Draws all updates.
        self.figure.canvas.draw_idle()

        return


    def set_colors(self, values):
        """ Sets the spectrogram's color scale. """

        # Re-defines the color scale limits in the spectrogram plot.
        self.plots['spectrogram'].set_clim([min(values), max(values)])

        # Draws all updates.
        self.figure.canvas.draw_idle()

        return


    def set_scale(self, values):
        """ Sets the vertical scale of the spectra graph. """

        # Re-defines the 'y' scale limits in the spectra graph.
        self.axes['spectragraph'].set_ylim([min(values), max(values)])

        # Draws all updates.
        self.figure.canvas.draw_idle()

        return


    def set_span(self, start, end):
        """ Sets the spectra span to be graphed. """

        # Gets the color of the span selector which is currently active.
        for _, selector in self.selectors.items():
            if selector.active: color = selector.rectprops['facecolor']

        # Removes the previously drawn spectra.
        for spectra in self.axes['spectragraph'].get_lines():
            if color == spectra.get_color(): spectra.remove()

        # Updates the row indices spanned by the currently active span selector.
        indices = np.ceil(np.arange(start - 0.5, end)).astype(int)

        # Plots the spectra associated with the selected indices.
        self.axes['spectragraph'].plot(self.data[indices,:].T, color=color, linewidth=1.0, alpha=0.5)

        # Draws all updates.
        self.figure.canvas.draw_idle()

        return


    def save(self, event):
        """ Saves the figure. """

        # Retrieves the current date and time.
        now = datetime.datetime.now()

        # Saves the figure.
        pyplot.savefig(now.strftime("%Y-%m-%d_%H%M%S") + '.png')

        return
