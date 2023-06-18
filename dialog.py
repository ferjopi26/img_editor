#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, Gio
import os
from PIL import Image, ImageFilter, ImageOps, ImageChops, ExifTags, ImageEnhance
from ctypes import *

class Dialog(Gtk.Window):
    def __init__(self, parent, efect, im):
        super(Dialog, self).__init__()

        self.so_file = "./effects.so"
        self.effects = CDLL(self.so_file)

        self.effects.adjust_brightness.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_double]
        self.effects.adjust_contrast.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_double]
        self.effects.adjust_saturation.argtypes = [c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_double]
        
        self.path = os.getcwd()
        self.parent = parent
        self.efect = efect
        self.im = im.copy()
        self.temp_im = im.copy()
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("dialog.glade")

        self.windialog = self.builder.get_object("windialog")
        self.adjustment = self.builder.get_object("adjustment")
        self.scale = self.builder.get_object("scale")
        self.btnApply = self.builder.get_object("btnApply")
        self.btnCancel = self.builder.get_object("btnCancel")

        self.value = self.scale.get_value()

        self.btnApply.connect("clicked", self.apply)
        self.btnCancel.connect("clicked", self.cancel)
        self.scale.connect("value-changed", self.value_changed)

        self.configure(efect)

        self.windialog.show()

    def configure(self, efect):
        if efect == "blend":
            self.open_image()

            self.adjustment.set_value(0.50)
            self.adjustment.set_lower(0.00)
            self.adjustment.set_upper(1.00)
            self.adjustment.set_step_increment(0.10)

            self.blend()
        
        if efect == "brightness":
            self.adjustment.set_value(1.00)
            self.adjustment.set_upper(2.00)
            self.adjustment.set_lower(0.00)
            self.adjustment.set_step_increment(0.10)

        if efect == "contrast" or efect == "saturation":
            self.adjustment.set_upper(1.00)
            self.adjustment.set_lower(-1.00)
            self.adjustment.set_step_increment(0.10)
            self.adjustment.set_value(0.00)

        if efect == "sharpness":
            self.adjustment.set_value(1.00)
            self.adjustment.set_lower(1.00)

        if efect == "gaussian_blur":
            self.adjustment.set_value(0.00)
            self.adjustment.set_lower(0.00)
            self.adjustment.set_upper(20.00)

        if efect == "autocontrast":
            self.adjustment.set_upper(49.00)

        if efect == "posterize":
            self.adjustment.set_lower(1)
            self.adjustment.set_upper(8)
            self.adjustment.set_step_increment(1)
            self.adjustment.set_value(8)

        if efect == "solarize":
            self.adjustment.set_lower(0)
            self.adjustment.set_upper(256)
            self.adjustment.set_value(256)

        if efect == "rotate":
            self.adjustment.set_lower(0)
            self.adjustment.set_upper(360)
            self.adjustment.set_value(0)
            self.adjustment.set_step_increment(1)

    def close(self, widget):
        self.windialog.destroy()

    def cancel(self, widget):
        self.parent.im_temp = self.temp_im.copy()
        self.parent.show_image(self.parent.im_temp)
        self.windialog.destroy()
        
    def value_changed(self, widget):
        self.value = self.adjustment.get_value()

        if self.efect == "blur":self.blur()
        if self.efect == "brightness":self.brightness()
        if self.efect == "contrast":self.contrast()
        if self.efect == "saturation":self.saturation()
        if self.efect == "sharpness":self.sharpness()
        if self.efect == "gaussian_blur":self.gaussian_blur()
        if self.efect == "autocontrast":self.autocontrast()
        if self.efect == "posterize":self.posterize()
        if self.efect == "solarize":self.solarize()
        if self.efect == "rotate":self.rotate()
        if self.efect == "blend":self.blend()

    def blur(self):
        box_blur = ImageFilter.BoxBlur(self.scale.get_value())
        self.im = self.parent.im_temp.copy()
        self.im = self.im.filter(filter=box_blur)
        self.parent.show_image(self.im.convert("RGB"))
        #self.parent.im_temp = im_blurred.copy()
        
    def brightness(self):
        pixels = self.parent.im_temp.tobytes()
        new_pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()
        
        self.effects.adjust_brightness(pixels, new_pixels, n_channels, width, height, rowstride, self.value)
        self.im = Image.frombytes("RGB", (width, height), new_pixels)
        self.parent.show_image(self.im)
        
    def contrast(self):
        pixels = self.parent.im_temp.tobytes()
        new_pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()
        
        self.effects.adjust_contrast(pixels, new_pixels, n_channels, width, height, rowstride, self.value)
        self.im = Image.frombytes("RGB", (width, height), new_pixels)
        self.parent.show_image(self.im)
        
    def saturation(self):
        pixels = self.parent.im_temp.tobytes()
        new_pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.adjust_saturation(pixels, new_pixels, n_channels, width, height, rowstride, self.value)
        self.im = Image.frombytes("RGB", (width, height), new_pixels)
        self.parent.show_image(self.im)

    def sharpness(self):
        self.im = self.parent.im_temp.copy()
        enhancer = ImageEnhance.Sharpness(self.im)
        self.im = enhancer.enhance(self.value)
        self.parent.show_image(self.im.convert(mode="RGB"))
        
    def gaussian_blur(self):
        self.im = self.parent.im_temp.copy()
        self.im = self.im.filter(ImageFilter.GaussianBlur(radius = self.value))
        self.parent.show_image(self.im.convert("RGB"))
        
    def autocontrast(self):
        self.im = self.parent.im_temp.copy()
        self.im = ImageOps.autocontrast(self.im, self.value)
        self.parent.show_image(self.im.convert("RGB"))
        
    def posterize(self):
        self.im = self.parent.im_temp.copy()
        self.im = ImageOps.posterize(self.im, int(self.value))
        self.parent.show_image(self.im)
        #self.parent.show_image(self.im_.convert("RGB"))
        
    def solarize(self):
        self.im = self.parent.im_temp.copy()
        self.im = ImageOps.solarize(self.im, threshold=self.value)
        self.parent.show_image(self.im)
        #self.parent.im_temp = self.im
        
    def blend(self):
        (width, height) = self.temp_im.size
        im1 = self.im.copy().resize((width, height)).convert(mode="RGB")
        self.im = Image.blend(im1, self.temp_im.convert(mode="RGB"), self.value)
        self.parent.show_image(self.im)
        self.im.show()
        
    def open_image(self):
        dialog = Gtk.FileChooserDialog(title="Abrir Arquivo", parent=self.windialog, action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        self.add_filters(dialog)

        dialog.set_local_only(False)
        dialog.set_current_folder(self.path)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            self.path = dialog.get_current_folder()

            self.im = Image.open(self.filename)
            self.im_converted = self.im.convert(mode="RGB")
            
            dialog.destroy()
            
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def add_filters(self, dialog:Gtk.FileChooserDialog):
        filter_image = Gtk.FileFilter()
        
        filter_image.set_name("Todos Arquivos de Imagem")
        filter_image.add_pattern("*.jpg")
        filter_image.add_pattern("*.jpeg")
        filter_image.add_pattern("*.JPG")
        filter_image.add_pattern("*.JPEG")
        filter_image.add_pattern("*.png")
        filter_image.add_pattern("*.PNG")
        filter_image.add_pattern("*.tiff")
        filter_image.add_pattern("*.bmp")
        dialog.add_filter(filter_image)
        
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos jpg")
        filter_image.add_pattern("*.jpg")
        dialog.add_filter(filter_image)

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos jpeg")
        filter_image.add_pattern("*.jpeg")
        dialog.add_filter(filter_image)
        
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos JPG")
        filter_image.add_pattern("*.JPG")
        dialog.add_filter(filter_image)

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos JPEG")
        filter_image.add_pattern("*.JPEG")
        dialog.add_filter(filter_image)      

        filter_image = Gtk.FileFilter()
        filter_image.set_name("Arquivos PNG")
        filter_image.add_pattern("*.png")
        dialog.add_filter(filter_image)

    def apply(self, widget):
        try:
            self.parent.im_temp = self.im.copy()
            self.windialog.destroy()
        except:
            pass
        self.windialog.destroy()
