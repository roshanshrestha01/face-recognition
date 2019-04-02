import os
from builtins import ord

import gi
import cv2
import numpy as np

from settings import HAAR_CASCADE, CAPTURE_DIR
from utils import check_folder

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

face_cascade = cv2.CascadeClassifier(HAAR_CASCADE)


class FaceRecognitionWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Face Recognition")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.CITY_NAME = None  # for refresh action
        self.gui = self.setup()
        self.add(self.gui)

    def setup(self):
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        subject_name = Gtk.Label(xalign=0)
        subject_name.set_text("Subject name")
        self.subject_name = Gtk.Entry()
        self.subject_name.set_size_request(400, 20)
        self.subject_name.set_text("S1")
        self.subject_name.set_width_chars(40)

        vbox.pack_start(subject_name, False, False, 0)
        vbox.pack_start(self.subject_name, False, False, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.capture_image = Gtk.Button.new_with_label("Capture Image")
        self.capture_image.connect("clicked", self.open_capture_image_window)
        self.capture_image.set_size_request(200, 20)

        self.sort_image = Gtk.Button.new_with_label("Sort Image")
        self.sort_image.connect("clicked", self.sort_images)
        self.sort_image.set_size_request(200, 20)

        hbox.pack_end(self.sort_image, True, True, 0)
        hbox.pack_end(self.capture_image, True, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.traing_model = Gtk.Button.new_with_label("Train Model")
        self.traing_model.connect("clicked", self.training_model)
        self.traing_model.set_size_request(200, 20)

        self.predict_model = Gtk.Button.new_with_label("Predict Video")
        self.predict_model.connect("clicked", self.open_predict_window)
        self.predict_model.set_size_request(200, 20)

        hbox.pack_end(self.predict_model, True, True, 0)
        hbox.pack_end(self.traing_model, True, True, 0)

        listbox.add(row)

        return box_outer

    def open_capture_image_window(self, button):
        subject_name = self.subject_name.get_text()
        print(subject_name)

        cap = cv2.VideoCapture(2)
        count = 1

        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            roi_gray = None
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                # if roi_gray is not None:
                #     check_folder(CAPTURE_DIR)
                #     subject_root = os.path.join(CAPTURE_DIR, subject_name)
                #     check_folder(subject_root)
                #     cv2.imwrite(os.path.join(subject_root, '{}.jpg'.format(count)), roi_gray)
                #     count += 1
                #     print(count)

            cv2.imshow('Video', img)
            k = cv2.waitKey(30) & 0xff
            if k == ord('c'):
                check_folder(CAPTURE_DIR)
                subject_root = os.path.join(CAPTURE_DIR, subject_name)
                check_folder(subject_root)
                count = len(os.listdir(subject_root))
                if roi_gray is not None:
                    cv2.imwrite(os.path.join(subject_root, '{}.jpg'.format(count)), roi_gray)
                    count += 1
                else:
                    print('ROI cannot be found.')
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def sort_images(self, button):
        pass

    def training_model(self, button):
        pass

    def open_predict_window(self, button):
        pass


win = FaceRecognitionWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()