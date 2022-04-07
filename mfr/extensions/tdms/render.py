import os
import base64
from io import BytesIO

import nptdms
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.core import utils

class TdmsRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('nptdms_version', nptdms.version.__version__)

    def render(self):
        """Render a tdms file to html."""
        maxTableLength = 100  # maximum rows to include in data table
        minDigitLength = 4  # minumum digits before scientific notation is used
        formatString = "{:." + str(minDigitLength) + "g}"

        fig, ax = plt.subplots()  # create matplotlib figure object
        ax.grid(True, alpha=0.1)  # specify matplotlib grid properties

        # empty data structures to be filled with file data in loops
        channelNames = []
        lineCollections = []
        properties = ""
        data = pd.DataFrame()

        tdms_file = nptdms.TdmsFile.open(self.file_path, raw_timestamps=True)
        fileMetadata = TdmsRenderer.formatMetadata(tdms_file.properties.items())

        # Parse group data and metadata and generate html
        for group in tdms_file.groups():
            groupClass = group.name.replace(" ", "")
            buttonId = groupClass + "Button"
            showHide = "showHide(\'" + groupClass + "\', \'" + buttonId + "\')"
            rowTag = "<tr class=\'group\' onclick=\"" + showHide + "\">"
            buttonTag = "<td class=\'button\' id=\'" + buttonId + "\'>+</td>"
            properties += rowTag + "<td>Group " + group.name + "</td>"
            properties += buttonTag + "</tr>"

            # Parse channel data and metadata and generate html
            for channel in group.channels():
                channelClass = channel.name.replace(" ", "")
                buttonId = channel.name.replace(" ", "") + "Button"
                showHide = "showHide(\'" + channelClass + "\', \'" + buttonId + "\')"
                rowTag = "<tr class=\'channel " + groupClass + "\' onclick=\"" + showHide + "\">"
                buttonTag = "<td class=\'button\' id=\'" + buttonId + "\'>+</td>"
                properties += rowTag + "<td>Channel " + channel.name + "</td>" + buttonTag + "</tr>"
                channelLength = len(channel)

                # Parse dictionary of properties:
                for property, value in channel.properties.items():
                    rowTag = "<tr class=\'property " + channelClass + " " + groupClass + "Child\'>"
                    leftCol = rowTag + "<td>" + property + "</td>"
                    if utils.isfloat(value):  # reformat float values
                        value = formatString.format(float(value))
                    rightCol = "<td>" + str(value) + "</td></tr>"
                    properties += leftCol + rightCol

                # Access numpy array of data for channel:
                if (channelLength > 1):  # Only access channels with datasets > 1
                    # Plotting on a time axis
                    if (channel.properties['wf_start_time'] and channel.properties['wf_increment']):
                        start = channel.properties['wf_start_time'].as_datetime()
                        start = (start - datetime.datetime(1904, 1, 1)).total_seconds()
                        increment = channel.properties['wf_increment']
                        stop = start + increment * channelLength
                        timeAxis = np.linspace(start, stop, channelLength)
                        line = ax.plot(timeAxis, channel, linewidth=2, label=channel.name)
                        plt.xticks(rotation=45)
                        plt.xlabel("Time (s)")
                    else:
                        line = ax.plot(channel, linewidth=2, label=channel.name)

                    lineCollections.append(line)
                    channelNames.append(channel.name)
                    data[channel.name] = channel[:maxTableLength]

        ax.legend(channelNames, bbox_to_anchor=(1, 1))
        plotFile = BytesIO()  # create byte sream object
        fig.savefig(plotFile, format='png', bbox_inches='tight')  # export plot to png in byte stream
        encoded = base64.b64encode(plotFile.getvalue()).decode('utf-8')  # encode base 64 byte stream data
        plot = '\'data:image/png;base64,{}\''.format(encoded)  # format encoded data as string
        table = data.to_html()  # export pandas DataFrame to HTML

        return self.TEMPLATE.render(base=self.assets_url, fileMetadata=fileMetadata, properties=properties, plot=plot, table=table)

    def formatMetadata(items):
        # Parse property value pairs in file level metadata and generate html

        minDigitLength = 4  # minumum digits before scientific notation is used
        formatString = "{:." + str(minDigitLength) + "G}"
        fileMetadata = ""

        for property, value in items:
            value = str(value)
            if value.find("\n") > 1:
                value = value.split("\n")
                fileMetadata += "<li>" + value[0] + "</li>"
                fileMetadata += "<ul>"
                for v in value[1:]:
                    v = v.replace("\\n", " ").replace("\"", "").split("=")
                    v[0] = "".join(v[0].split(".")[1:])
                    v[1] = v[1].strip()
                    if utils.isfloat(v[1]):  # reformat float values
                        v[1] = formatString.format(float(v[1]))
                    fileMetadata += "<li>" + "= ".join(v) + "</li>"
                fileMetadata += "</ul>"
            else:
                fileMetadata += "<li>" + str(property) + ": " + value + "</li>"
        fileMetadata += "</ul>"

        return fileMetadata

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
