#!/usr/bin/env python

# Copyright (c) 2011-2013 Ben Croston
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os.path
import sys

if sys.platform.lower().startswith('win'):
    IS_WINDOWS = True
    import win32print
else:
    IS_WINDOWS = False
    import subprocess

class zebra(object):
    """A class to communicate with (Zebra) label printers using EPL2"""

    def __init__(self, queue=None):
        """queue - name of the printer queue (optional)"""
        self.queue = queue

    def _output_unix(self, commands):
        if self.queue == 'zebra_python_unittest':
            p = subprocess.Popen(['cat','-'], stdin=subprocess.PIPE)
        else:
            p = subprocess.Popen(['lpr','-P%s'%self.queue], stdin=subprocess.PIPE)
        p.communicate(commands)
        p.stdin.close()

    def _output_win(self, commands):
        if self.queue == 'zebra_python_unittest':
            print commands
            return
        hPrinter = win32print.OpenPrinter(self.queue)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ('Label',None,'RAW'))
            try:
                win32print.StartPagePrinter(hPrinter)
                win32print.WritePrinter(hPrinter, commands)
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

    def output(self, commands):
        """Output EPL2 commands to the label printer

        commands - EPL2 commands to send to the printer
        """
        assert self.queue is not None
        if sys.version_info[0] == 3:
            if type(commands) != bytes:
                commands = str(commands)#.encode()
        else:
            commands = str(commands)#.encode()
        if IS_WINDOWS:
            self._output_win(commands)
        else:
            self._output_unix(commands)

    def _getqueues_unix(self):
        queues = []
        try:
            output = subprocess.check_output(['lpstat','-p'], universal_newlines=True)
        except subprocess.CalledProcessError:
            return []
        for line in output.split('\n'):
            if line.startswith('printer'):
                queues.append(line.split(' ')[1])
        return queues

    def _getqueues_win(self):
        printers = []
        for (a,b,name,d) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            printers.append(name)
        return printers

    def getqueues(self):
        """Returns a list of printer queues on local machine"""
        if IS_WINDOWS:
            return self._getqueues_win()
        else:
            return self._getqueues_unix()

    def setqueue(self, queue):
        """Set the printer queue"""
        self.queue = queue

    def setup(self, direct_thermal=None, label_height=None, label_width=None):
        """Set up the label printer. Parameters are not set if they are None.

        direct_thermal - True if using direct thermal labels
        label_height   - tuple (label height, label gap) in dots
        label_width    - in dots
        """
        commands = '\n'
        if direct_thermal:
            commands += ('OD\n')
        if label_height:
           commands += ('Q%s,%s\n'%(label_height[0],label_height[1]))
        if label_width:
            commands += ('q%s\n'%label_width)
        self.output(commands)

    def store_graphic(self, name, filename):
        """Store a .PCX file on the label printer

        name     - name to be used on printer
        filename - local filename
        """
        assert filename.lower().endswith('.pcx')
        commands = '\nGK"%s"\n'%name
        commands += 'GK"%s"\n'%name
        size = os.path.getsize(filename)
        commands += 'GM"%s"%s\n'%(name,size)
        self.output(commands)
        self.output(open(filename,'rb').read())

if __name__ == '__main__':
    z = zebra()
    print 'Printer queues found:',z.getqueues()
    z.setqueue('zebra_python_unittest')
    z.setup(direct_thermal=True, label_height=(406,32), label_width=609)    # 3" x 2" direct thermal label
    z.store_graphic('logo','logo.pcx')
    label = """
N
GG419,40,"logo"
A40,80,0,4,1,1,N,"Tangerine Duck 4.4%"
A40,198,0,3,1,1,N,"Duty paid on 39.9l"
A40,240,0,3,1,1,N,"Gyle: 127     Best Before: 16/09/2011"
A40,320,0,4,1,1,N,"Pump & Truncheon"
P1
"""
    z.output(label)

