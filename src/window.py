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

@GtkTemplate(ui='/org/gnome/Ff/window.ui')
class FfWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'FfWindow'

    scaledown, scaleup, paste, copy, image = GtkTemplate.Child.widgets(5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.image_pixbuf = None
        self.scale = 1

    @GtkTemplate.Callback
    def paste_clicked_cb(self, widget):
        print("button paste clicked")
        self.image_pixbuf = self.clipboard.wait_for_image()
        if self.image_pixbuf != None:
            self.image.set_from_pixbuf(self.image_pixbuf)

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
        self.scale += 0.1
        new_pixbuf = self.image_pixbuf.scale_simple(self.image_pixbuf.get_width() * self.scale,
                                               self.image_pixbuf.get_height() * self.scale,
                                               InterpType.BILINEAR)
        self.image.set_from_pixbuf(new_pixbuf)

    @GtkTemplate.Callback
    def scaledown_clicked_cb(self, widget):
        print("button scaledown clicked")
        print("width %d", self.image.get_pixbuf().get_width())
        self.scale -= 0.1
        new_pixbuf = self.image_pixbuf.scale_simple(self.image_pixbuf.get_width() * self.scale,
                                               self.image_pixbuf.get_height() * self.scale,
                                               InterpType.BILINEAR)
        self.image.set_from_pixbuf(new_pixbuf)
