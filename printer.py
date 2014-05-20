# -*- coding: utf-8 -*-
import base64
from helpers.zebra import zebra

class PrinterController(object):
    def output(self, format="epl2", **kwargs):
        '''Print the passed-in data. Corresponds to "printer_proxy.print"'''

        if format.lower() == "epl2":
            return self.output_epl2(**kwargs)
        return {'success': False, 'error': "Format '%s' not recognized" % format}


    def output_epl2(self, printer_name='zebra_python_unittest', data=[], raw=False, test=False):
        '''Print the passed-in EPL2 data.'''

        printer = zebra(printer_name)

        if isinstance(data, basestring):
            data = [data]

        for datum in data:
            if not raw:
                datum = base64.b64decode(datum)
            printer.output(datum)

        return {'success': True}
