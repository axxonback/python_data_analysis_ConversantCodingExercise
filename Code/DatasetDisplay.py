"""
Program file: DatasetDisplay.py.

This program plots and displays a given dataset
"""

import matplotlib.dates as dt
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter


class DatasetDisplay:
    """
    Summary: plots and displays given dataset.

    Instances:
    1. dataset
    2. dcs_to_graph

    Methods:
    1. format_axes
    2. plot_dataset
    3. show_plot
    """

    def __init__(self, dataset, dcs_names):
        """DatasetDisplay constructor."""
        self.dataset = dataset
        self.dcs_to_graph = dcs_names

    def format_axes(self, ax=None):
        """
        Summary: helper function for customizing graph display.

        Decription:
        * Create and set major/minor locators for graph's major/minor ticks.
        * Format dates/times of x axis.
        * Autoscale graph view.
        * Show grid on graph.
        """
        # HourLocator creates major ticks every 2 hours in a 24 hour period
        hours = HourLocator(byhour=range(24), interval=2)
        ax.xaxis.set_major_locator(hours)

        # MinuteLocator creates minor ticks every 30 minutes in a 1 hour period
        minutes = MinuteLocator(byminute=range(60), interval=30)
        ax.xaxis.set_minor_locator(minutes)

        # Creates format 'Hour:MinutePeriod Month/Day/Year' x-axis ticks
        # Example: '5:30PM 9/23/15'
        time_fmt = DateFormatter('%H:%M%p %x')
        ax.xaxis.set_major_formatter(time_fmt)

        # Formats x-axis information 'Weekday Month Day Hour:MinutePeriod'
        # Example: 'Tuesday Sep 23 12:15PM'
        ax.fmt_xdata = DateFormatter('%A %b %d %H:%M%p')

        ax.autoscale_view()

        ax.grid(True)

    def plot_dataset(self, name=None, ax=None):
        """Function to plot data for a specified Data Center."""
        values = []
        times = []
        max_value = 0
        max_value_time = 0
        for record in self.dataset[:]:
            if record[0] == name:
                times.append(dt.epoch2num(record[1]))
                values.append(record[2])

                if record[2] > max_value:
                    max_value = record[2]
                    max_value_time = dt.epoch2num(record[1])
                self.dataset.remove(record)
            else:
                pass

        value_mean = sum(values) / float(len(values))
        print(
            "Data Center:{}\nMax Value:{}, {}\nAverage Value:{}\n".format(
                name, max_value, dt.num2date(max_value_time), value_mean
            )
        )

        ax.plot_date(times, values, xdate=True)

    def show_plot(self):
        """
        Summary: function that graphs data center dataset.

        Description:
        * Formats plot axes for proper display
        * Plots specified data centers on display
        * Labels display title, x-axis, y-axis
        * Creates a legend according to specified data centers
        """
        # List of plotted data centers for dynamic legend creation
        plotted_dc = []

        # Creating figure and axes objects for display
        fig, ax = plt.subplots()

        # Formatting y and x axis for effective plotting
        self.format_axes(ax)

        # Iterating through list of data centers to be plotted together.
        for dc in self.dcs_to_graph:
            # For each data center, 'dc', plot it's data from dataset.
            self.plot_dataset(dc, ax)

            # Add data center to list of plotted dcs for dynamic legend
            plotted_dc.append(dc)

        fig.autofmt_xdate()

        # Giving scatterplot a title
        plt.title("Data Centers(Value vs. Time)")
        # Making axis labels
        plt.xlabel('Time')
        plt.ylabel('Value')

        # Making a legend for the graph
        plt.legend(['Data Center: ' + dc for dc in plotted_dc])

        plt.show()
