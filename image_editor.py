#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, Gio
import os
from PIL import Image, ImageOps, ImageChops, ExifTags, ImageFilter, ImageDraw, ImageFont
from dialog import Dialog
from dlggray import DialogGray
from ctypes import *

class ImageEditor(Gtk.Application):
    def __init__(self):
        self.so_file = "./effects.so"
        self.effects = CDLL(self.so_file)

        self.effects.convert_to_sepia.argtypes = [c_char_p, c_int, c_int, c_int, c_int]
        self.effects.invert.argtypes = [c_char_p, c_int, c_int, c_int, c_int]
        self.effects.convert_to_gray.argtypes = [c_char_p, c_int, c_int, c_int, c_int]
        
        Gtk.Application.__init__(self, application_id="apps.image_editor", flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_activate)

    def on_activate(self, data=None):
        sinais = {
            "on_itmSair_activate":self.sair,
            "on_itmOpenImage_activate":self.open_image,
            "on_itmP&B_activate":self.black_and_white,
            "on_itmInvert_activate":self.invert,
            "on_itmBlur_activate":self.blur,
            "on_itmUndo_activate":self.undo,
            "on_itmBrightness_activate":self.brightness,
            "on_itmContrast_activate":self.contrast,
            "on_itmSaturation_activate":self.saturation,
            "on_itmSalvarImagem_activate":self.save_image,
            "on_itmSharpness_activate":self.sharpness,
            "on_itmGaussianBlur_activate":self.gaussian_blur,
            "on_itmAutoContrast_activate":self.auto_contrast,
            "on_itmFlip_activate":self.flip,
            "on_itmMirror_activate":self.mirror,
            "on_itmPosterize_activate":self.posterize,
            "on_itmSolarize_activate":self.solarize,
            "on_itmBlend_activate":self.blend,
            "on_itmSepia_activate":self.sepia,
            "on_itmFilters_activate":self.pb_filter,
        }

        self.path = os.getcwd()
        self.angle = 0
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("image_editor.glade")

        self.main_window = self.builder.get_object("mainwindow")
        self.image1 = self.builder.get_object("image1")
        self.popoverBlur = self.builder.get_object("popoverBlur")
        self.popoverBrightness = self.builder.get_object("popoverBrightness")
        self.popoverContrast = self.builder.get_object("popoverContrast")
        self.popoverSaturation = self.builder.get_object("popoverSaturation")
        self.popoverSharpness = self.builder.get_object("popoverSharpness")
        self.popoverGaussianBlur = self.builder.get_object("popoverGaussianBlur")
        self.img_label = self.builder.get_object("img_label")

        self.builder.connect_signals(sinais)

        self.box1 = self.builder.get_object("box1")

        screen = Gdk.Screen.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.main_window.show()

        self.add_window(self.main_window)

    def open_image(self, widget):
        dialog = Gtk.FileChooserDialog(title="Abrir Arquivo", parent=self.main_window, action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        self.add_filters(dialog)

        dialog.set_local_only(False)
        dialog.set_current_folder(self.path)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            self.path = dialog.get_current_folder()

            self.title = self.filename.split('/')
            self.title.reverse()
            self.main_window.set_title('Editor de Imagens - ' + self.title[0])

            self.im = Image.open(self.filename)
            self.im_temp = Image.open(self.filename)
            self.im_converted = self.im_temp.convert(mode="RGB")

            self.show_image(self.im_converted)
            
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

    def show_image(self, im:Image):
        self.exif_data = {}
        
        exif_data = self.getExif()

        (width, height) = im.size

        self.img_label.set_text(self.title[0] + " " + str(width) + " X " + str(height))
        
        ratio = width/height
        
        if width > 1024:
            width = 1024
            height = int(1024/ratio)
            im = im.resize((width,height))
        else:
            self.resized = im
        
        self.resized = im.tobytes()

        for keys, val in exif_data.items():
            if keys == 'Orientation':
                if val == 1:
                    self.angle = 0
                elif val == 2:
                    self.angle == 180
                elif val == 3:
                    self.angle = 180
                elif val == 4:
                    self.angle = 90
                elif val == 5:
                    self.angle = 270
                elif val == 6:
                    self.angle = 270
                elif val == 7:
                    self.angle = 90
                elif val == 8:
                    self.angle = 270
           
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_data(self.resized, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
        self.pixbuf = self.pixbuf.rotate_simple(self.angle)
        self.image1.set_from_pixbuf(self.pixbuf)

    def getExif(self):
        info = self.im._getexif()
        
        if info == None:
            self.angle = 0
            return self.exif_data
        
        for key, val in info.items():
            if key in ExifTags.TAGS:
                self.exif_data[ExifTags.TAGS[key]] = val
                
        return self.exif_data
    
    def black_and_white(self, widget):
        try:
            pixels = self.im_temp.tobytes()
            width, height = self.im_temp.size
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
            n_channels = pixbuf.get_n_channels()
            width = pixbuf.get_width()
            height = pixbuf.get_height()
            rowstride = pixbuf.get_rowstride()
            
            self.effects.convert_to_gray(pixels, n_channels, width, height, rowstride)
            im = Image.frombytes("RGB", (width, height), pixels)
            self.im_temp = im.copy()
            self.show_image(self.im_temp)    
        except:
            self.open_image(widget)
        
    def invert(self, widget):
        try:
            pixels = self.im_temp.tobytes()
            width, height = self.im_temp.size
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
            n_channels = pixbuf.get_n_channels()
            width = pixbuf.get_width()
            height = pixbuf.get_height()
            rowstride = pixbuf.get_rowstride()
            
            self.effects.invert(pixels, n_channels, width, height, rowstride)
            im = Image.frombytes("RGB", (width, height), pixels)
            self.im_temp = im.copy()
            self.show_image(self.im_temp)    
        except:
            self.open_image(widget)

    def blur(self, widget):
        try:
            dialog = Dialog(self, "blur", self.im_temp)
            dialog.windialog.set_title("Desfoque")
        except:
            self.open_image(widget)
    
    def brightness(self, widget):
        try:
            dialog = Dialog(self, "brightness", self.im_temp)
            dialog.windialog.set_title("Brilho")
            dialog.adjustment.set_value(1.00)
        except:
            self.open_image(widget)

    def contrast(self, widget):
        try:
            dialog = Dialog(self, "contrast", self.im_temp)
            dialog.windialog.set_title("Contraste")
            dialog.adjustment.set_value(0.00)
        except:
            self.open_image(widget)

    def saturation(self, widget):
        try:
            dialog = Dialog(self, "saturation", self.im_temp)
            dialog.windialog.set_title("Saturação")
        except:
            self.open_image(widget)

    def sharpness(self, widget):
        try:
            dialog = Dialog(self, "sharpness", self.im_temp)
            dialog.windialog.set_title("Nitidez")
        except:
            self.open_image(widget)

    def gaussian_blur(self, widget):
        try:
            dialog = Dialog(self, "gaussian_blur", self.im_temp)
            dialog.windialog.set_title("Desfoque Gaussiano")
        except:
            self.open_image(widget)

    def auto_contrast(self, widget):
        try:
            dialog = Dialog(self, "autocontrast", self.im_temp)
            dialog.windialog.set_title("Auto Contraste")
        except:
            self.open_image(widget)

    def flip(self, widget):
        try:
            im_flip = self.im_temp.copy()
            im_flip = ImageOps.flip(im_flip)
            self.show_image(im_flip.convert("RGB"))
            self.im_temp = im_flip
        except:
            self.open_image(widget)

    def mirror(self, widget):
        try:
            im_mirror = self.im_temp.copy()
            im_mirror = ImageOps.mirror(im_mirror)
            self.show_image(im_mirror.convert("RGB"))
            self.im_temp = im_mirror
        except:
            self.open_image(widget)

    def posterize(self, widget):
        try:
            dialog = Dialog(self, "posterize", self.im_temp)
            dialog.windialog.set_title("Posterizar")
        except:
            self.open_image(widget)
        
    def solarize(self, widget):
        try:
            dialog = Dialog(self, "solarize", self.im_temp)
            dialog.windialog.set_title("Solarizar")
        except:
            self.open_image(widget)

    def blend(self, widget):
        try:
            dialog = Dialog(self, "blend", self.im_temp)
            dialog.windialog.set_title("Dupla Exposição")
        except:
            self.open_image(widget)
        
    def sepia(self,widget):
        try:
            pixels = self.im_temp.tobytes()
            width, height = self.im_temp.size
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(pixels, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3, None, None)
            n_channels = pixbuf.get_n_channels()
            width = pixbuf.get_width()
            height = pixbuf.get_height()
            rowstride = pixbuf.get_rowstride()
            
            self.effects.convert_to_sepia(pixels, n_channels, width, height, rowstride)
            im = Image.frombytes("RGB", (width, height), pixels)
            self.im_temp = im.copy()
            self.show_image(self.im_temp)
        except:
            self.open_image(widget)

    def pb_filter(self, widget):
        try:
            dialog = DialogGray(self.im_temp, self)
            dialog.windlggray.set_title("Filtros P&B")
        except:
            self.open_image(widget)

    def undo(self, widget):
        try:
            self.im_temp = Image.open(self.filename)
            self.im_converted = self.im_temp.convert(mode="RGB")
            self.show_image(self.im_converted)
        except:
            pass

    def save_image(self, widget):
        dialog = Gtk.FileChooserDialog(title="Salvar Arquivo", parent=self.main_window, action=Gtk.FileChooserAction.SAVE)

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        
        self.add_filters(dialog)

        dialog.set_filename(self.filename)
        
        dialog.set_local_only(False)

        dialog.set_current_folder(self.path)

        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file = dialog.get_filename()
            self.path = dialog.get_current_folder()

            self.im_temp.save(file)

            dialog.destroy()
            self.info_message("Arquivo salvo no disco.")

        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def windlg_close(self,widget,user_data):
        print(widget)
        widget.hide()

    def cancel(self, widget):
        self.show_image(self.im_temp)
        self.windlg.close()
    
    def info_message(self, message):
        messagedialog = Gtk.MessageDialog( parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, message_format=message)

        messagedialog.set_title("Salvar Arquivo")

        messagedialog.connect("response", self.info_dialog_response)

        messagedialog.show()

    def info_dialog_response(self, widget, response_id):
        if response_id == Gtk.ResponseType.OK:
            widget.destroy()

    def sair(self, widget):
        self.main_window.destroy()

if __name__ == "__main__":
    app = ImageEditor()
    app.run(None)
