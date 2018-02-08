# window.py
#
# Copyright (C) 2018 Honhe
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from gi.repository import Gtk, Gdk
from .gi_composites import GtkTemplate
from gi.repository.GdkPixbuf import Pixbuf, InterpType
import math

@GtkTemplate(ui='/org/gnome/Ff/window.ui')
class FfWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'FfWindow'

    scaledown, scaleup, paste, copy, image, scale1, adjustment1= GtkTemplate.Child.widgets(7)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.image_pixbuf = None
        self.scale = 1
        self.scale_delta = 0.1
        self.adjsutment_delta = 1
        self.scale_min = 0.1
        self.precision = 0.0001
        self.scale_max = 1.9

    def set_scale_and_adjustment(self, scale):
        self.scale = scale
        self.adjustment1.set_value(self.scale)

    @GtkTemplate.Callback
    def paste_clicked_cb(self, widget):
        print("button paste clicked")
        self.image_pixbuf = self.clipboard.wait_for_image()
        if self.image_pixbuf != None:
            self.image.set_from_pixbuf(self.image_pixbuf)
        # reset scale
        self.set_scale_and_adjustment(1)

    @GtkTemplate.Callback
    def copy_clicked_cb(self, widget):
        print("button copy clicked")
        if self.image.get_storage_type() == Gtk.ImageType.PIXBUF:
            self.clipboard.set_image(self.image.get_pixbuf())
        else:
            print("No image has been pasted yet.")

    @GtkTemplate.Callback
    def scaleup_clicked_cb(self, widget):
        print("button scaleup clicked")
        print("width %d", self.image.get_pixbuf().get_width())
        if math.fabs(self.scale - self.scale_max) < self.precision:
            return

        self.scale += self.scale_delta
        self.scale_image(self.scale)

    def scale_image(self, scale):
        new_pixbuf = self.image_pixbuf.scale_simple(self.image_pixbuf.get_width() * scale,
                                               self.image_pixbuf.get_height() * scale,
                                               InterpType.BILINEAR)
        self.image.set_from_pixbuf(new_pixbuf)
        self.adjustment1.set_value(scale)

    @GtkTemplate.Callback
    def scaledown_clicked_cb(self, widget):
        print("button scaledown clicked")
        print("width %d", self.image.get_pixbuf().get_width())
        if math.fabs(self.scale- self.scale_min) < self.precision:
            return

        self.scale -= self.scale_delta
        self.scale_image(self.scale)

    @GtkTemplate.Callback
    def scale1_value_changed_cb(self, widget):
         pass

    @GtkTemplate.Callback
    def adjustment1_value_changed_cb(self, widget):
         print(widget.get_value())
         self.scale = widget.get_value()
         self.scale_image(self.scale)
