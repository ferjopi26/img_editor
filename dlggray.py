#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, Gio
from ctypes import *

class DialogGray:
    def __init__(self, im, parent) -> None:
        super(DialogGray, self).__init__()

        self.so_file = "./effects.so"
        self.effects = CDLL(self.so_file)

        self.effects.filter_red.argtypes = [c_char_p, c_int, c_int, c_int, c_int]
        self.effects.filter_green.argtypes = [c_char_p, c_int, c_int, c_int, c_int]
        self.effects.filter_blue.argtypes = [c_char_p, c_int, c_int, c_int, c_int]
        self.effects.filter_yellow.argtypes = [c_char_p, c_int, c_int, c_int, c_int]

        self.path = os.getcwd()
        self.im = im.copy()
        self.temp_im = im.copy()
        self.parent = parent
        
        builder = Gtk.Builder()
        builder.add_from_file("dlggray.glade")

        self.windlggray = builder.get_object("windlggray")
        btnRevert = builder.get_object("btnRevert")
        btnApply = builder.get_object("btnApply")

        btnNeutral = builder.get_object("btnNeutral")
        btnRed = builder.get_object("btnRed")
        btnGreen = builder.get_object("btnGreen")
        btnBlue = builder.get_object("btnBlue")
        btnYellow = builder.get_object("btnYellow")
        btnOrange = builder.get_object("btnOrange")

        btnRevert.connect("clicked", self.revert)
        btnApply.connect("clicked", self.apply)

        btnNeutral.connect("clicked", self.neutral_filter)
        btnRed.connect("clicked", self.red_filter)
        btnGreen.connect("clicked", self.green_filter)
        btnBlue.connect("clicked", self.blue_filter)
        btnYellow.connect("clicked", self.yellow_filter)
        btnOrange.connect("clicked", self.orange_filter)

        self.windlggray.show()

    def revert(self, widget):
        self.parent.show_image(self.temp_im.convert("RGB"))
        
    def apply(self, widget):
        self.windlggray.destroy()

    def neutral_filter(self, widget):
        self.revert(widget)
        pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.convert_to_gray(pixels, n_channels, width, height, rowstride)
        im = Image.frombytes("RGB", (width, height), pixels)
        self.parent.im_temp = im.copy()
        self.parent.show_image(im)

    def red_filter(self, widget):
        self.revert(widget)
        pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.filter_red(pixels, n_channels, width, height, rowstride)
        im = Image.frombytes("RGB", (width, height), pixels)
        self.parent.im_temp = im.copy()
        self.parent.show_image(im)
        
    def green_filter(self, widget):
        self.revert(widget)
        pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.filter_green(pixels, n_channels, width, height, rowstride)
        im = Image.frombytes("RGB", (width, height), pixels)
        self.parent.im_temp = im.copy()
        self.parent.show_image(im)

    def blue_filter(self, widget):
        self.revert(widget)
        pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.filter_blue(pixels, n_channels, width, height, rowstride)
        im = Image.frombytes("RGB", (width, height), pixels)
        self.parent.im_temp = im.copy()
        self.parent.show_image(im)
        
    def yellow_filter(self, widget):
        self.revert(widget)
        pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.filter_yellow(pixels, n_channels, width, height, rowstride)
        im = Image.frombytes("RGB", (width, height), pixels)
        self.parent.im_temp = im.copy()
        self.parent.show_image(im)
        
    def orange_filter(self, widget):
        self.revert(widget)
        pixels = self.parent.im_temp.tobytes()
        width, height = self.parent.im_temp.size
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        n_channels = pixbuf.get_n_channels()
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        rowstride = pixbuf.get_rowstride()

        self.effects.filter_orange(pixels, n_channels, width, height, rowstride)
        im = Image.frombytes("RGB", (width, height), pixels)
        self.parent.im_temp = im.copy()
        self.parent.show_image(im)
