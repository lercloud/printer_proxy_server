# -*- coding: utf-8 -*-
import base64
from helpers.zebra import zebra

PIL_SUPPORTED_FORMATS = [
        'bmp', 'cur', 'dcx', 'eps', 'flc', 'fli',
        'fpx', 'gbr', 'gd', 'gif', 'icns', 'ico',
        'im', 'imt', 'iptc-naa', 'jpeg', 'jpeg2000',
        'jpg', 'mcidas', 'msp', 'pcd', 'pcx', 'png',
        'ppm', 'psd', 'sgi', 'spider', 'tga', 'tiff',
        'wal', 'webp', 'xbm', 'xpm'
] 

class PrinterController(object):
    def output(self, format="epl2", **kwargs):
        '''Print the passed-in data. Corresponds to "printer_proxy.print"'''

        if format.lower() == "epl2":
            return self.output_epl2(**kwargs)
        if format.lower() in PIL_SUPPORED_FORMATS:
            return self.output_img(**kwargs)

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

    def output_img(self, printer_name='zebra_python_unittest', data=[], raw=False, test=False):
        '''Print the passed-in image data.'''

        printer = zebra(printer_name)

        if isinstance(data, basestring):
            data = [data]

        for datum in data:
            if not raw:
                datum = base64.b64decode(datum)
            printer.print_graphic(datum, 0, 0)

        return {'success': True}
