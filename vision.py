#!/usr/bin/env python

import cv2
import numpy as np

import itertools
from networktables.util import ntproperty

INF = float('inf')

# -m cscore.local

class ImageProcessor(object):
    '''
        Stuff here.
    '''
    
    if False:
        # Values for the lifecam-3000
        VFOV = 45.6
        HFOV = 61 # Camera's horizontal field of view
    elif True:
        # Values for the Logitech C930e
        VFOV = 61.9
        HFOV = 77.3
        
    VFOV_2 = VFOV / 2.0
    HFOV_2 = HFOV / 2.0
    
    # Useful BGR colors
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    MOO = (255, 255, 0)
    
    enabled = ntproperty('/camera/enabled', False, writeDefault=True)
    tuning = ntproperty('/camera/tuning', False, writeDefault=True)
    logging_enabled = ntproperty('/camera/logging_enabled', False, writeDefault=True)
    
    target = ntproperty('/camera/target', (0, 0, INF), writeDefault=True)
    
    # TODO:
    # Amber: 0,255 . 70/191 . 252/255?
    # Green:
    # Blue:
    
    # boston 2013: 30 75 188 255 16 255
    # virginia 2014: ?
    # test image:  43 100 0 255 57 255
    
    thresh_hue_p = ntproperty('/camera/thresholds/hue_p', 0)
    thresh_hue_n = ntproperty('/camera/thresholds/hue_n', 255)
    thresh_sat_p = ntproperty('/camera/thresholds/sat_p', 145)
    thresh_sat_n = ntproperty('/camera/thresholds/sat_n', 255)
    thresh_val_p = ntproperty('/camera/thresholds/val_p', 80)
    thresh_val_n = ntproperty('/camera/thresholds/val_n', 255)
    
    draw = ntproperty('/camera/draw_targets', True)
    draw_thresh = ntproperty('/camera/draw_thresh', False)
    draw_c1 = ntproperty('/camera/draw_c1', False)
    
    def __init__(self):
        
        self.lower = np.array([self.thresh_hue_p, self.thresh_sat_p, self.thresh_val_p], dtype=np.uint8)
        self.upper = np.array([self.thresh_hue_n, self.thresh_sat_n, self.thresh_val_n], dtype=np.uint8)
        
        self.size = None
        
    
    def preallocate(self, img):
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            
            self.out = np.empty((h, w, 3), dtype=np.uint8)
            self.bin = np.empty((h, w, 1), dtype=np.uint8)
            self.hsv = np.empty((h, w, 3), dtype=np.uint8)
            
            self.subr = np.empty((h, w, 1), dtype=np.uint8)
            self.addr = np.empty((h, w, 1), dtype=np.uint8)
            
            # for drawing
            self.zeros = np.zeros((h, w, 1), dtype=np.bool)
            self.black = np.zeros((h, w, 3), dtype=np.uint8)
            
            k = 3
            offset = (0,0)
            self.morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k,k), anchor=offset)
            self.morphIterations = 1
            
        # Copy input image to output
        cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=self.RED, dst=self.out)
    
    def process(self, img):
        
        #
        # Standard stuff
        #
        
        self.preallocate(img)
        
        if False:
            # Convert to HSV
            cv2.cvtColor(img, cv2.COLOR_BGR2HLS, dst=self.hsv)
            
            if self.tuning:
                self.lower = np.array([self.thresh_hue_p, self.thresh_sat_p, self.thresh_val_p], dtype=np.uint8)
                self.upper = np.array([self.thresh_hue_n, self.thresh_sat_n, self.thresh_val_n], dtype=np.uint8)
            
            # Threshold
            cv2.inRange(self.hsv, self.lower, self.upper, dst=self.bin)
        else:
            # experimental thresholding from frc900:
            # - Add blue and red channels
            # - Subtract them from green
            # - Run otsu's threshold on it and use that
            
            cv2.add(img[:,:,0], img[:,:,2], dst=self.addr)
            cv2.subtract(img[:,:,1], self.addr, dst=self.subr)
            
            r,_ = cv2.threshold(self.subr, 0, 255,
                                cv2.THRESH_BINARY+cv2.THRESH_OTSU,
                                dst=self.bin)
            if r < 1:
                return self.out, None
        
        # Fill in the gaps
        cv2.morphologyEx(self.bin, cv2.MORPH_CLOSE, self.morphKernel, dst=self.bin,
                         iterations=self.morphIterations)
        
        if self.draw_thresh:
            b = (self.bin != 0)
            cv2.copyMakeBorder(self.black, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=self.RED, dst=self.out)
            self.out[np.dstack((b, b, b))] = 255
        
        # Find contours
        _, contours, _ = cv2.findContours(self.bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        #
        # Game-specific target processing
        #
        # Portions of the processing code below was borrowed from code by Amory
        # Galili and Carter Fendley
        #
        
        square_contours = []
        results = []
        target = None
        
        for cnt in contours:
            # 7% arc length... removes sides in the shapes to detects rectangles
            epsilon = 0.07 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4:
                if self.draw_c1:
                    cv2.drawContours(self.out, [approx], -1, self.BLUE, 2, lineType=8)
                
                # Compute and store data for later    
                (cx, cy), (rw, rh), r = cv2.minAreaRect(approx)
                x, y, w, h = cv2.boundingRect(approx)
                    
                square_contours.append((approx, cx, cy, w, h))
        
        #
        # Find contours that are similar shapes/sizes, and group them together
        #
        
        for (c1, cx1, cy1, cw1, ch1), \
            (c2, cx2, cy2, cw2, ch2)  \
                in itertools.combinations(square_contours, 2):
            
            # Constraints:
            
            # * about the same size
            about_the_same_size = (.5 < cw1/cw2 < 2 and .8 < ch1/ch2 < 1.2)
            
            # * at about the same place on the Y axis
            at_same_y = abs(cy1 - cy2) < 10.0
            
            # * separated by at least 2 widths
            correct_separation = abs(cx1 - cx2) > 2*cw1
            
            if not (about_the_same_size and at_same_y and correct_separation):
                continue
                
            # generate a combined target
            c = np.concatenate([c1, c2])
            
            hull = cv2.convexHull(c)
            c = cv2.approxPolyDP(hull, 0.07*cv2.arcLength(hull, True), True)
            
            (cx, cy), (rw, rh), r = cv2.minAreaRect(c)
            h, w = img.shape[:2]
            h = float(h)
            w = float(w)
            
            results.append({
                'c': c,
                'angle': self.HFOV * cx / w - (self.HFOV_2)
            })
        
        # select the target that's closest to the center, and send it out
        # sort the returned data, tend to prefer the 'closest' gate to the center
        if results:
            results.sort(key=lambda r: abs(r['angle']))
            target = results[0]

            if self.draw:
                cv2.drawContours(self.out, [target['c']], -1, self.RED, 2, lineType=8)
        
        return self.out, target

def main():
    
    # TODO: get rid of this boilerplate, or make it easier to do
    
    from cscore import CameraServer
    from cscore.imagewriter import ImageWriter
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)
    cvSink = cs.getVideo()
    outputStream = cs.putVideo("CV", 320, 240)
    
    #c = cs.startAutomaticCapture(dev=1)
    #c.setResolution(320, 240)
    
    proc = ImageProcessor()
    writer = ImageWriter()
    
    enabled = None
    
    img = None
    while True:
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError());
            # skip the rest of the current iteration
            continue
        
        en = proc.enabled
        if en != enabled:
            enabled = en
            if enabled:
                camera.setExposureManual(0)
            else:
                camera.setExposureAuto()
        
        if enabled:
            if proc.logging_enabled:
                writer.setImage(img)
            
            out, target = proc.process(img)
        else:
            out = img
            target = None
        
        if target:
            proc.target = (1, time, target['angle'])
        else:
            proc.target = (0, time, INF)
        
        outputStream.putFrame(out)

if __name__ == '__main__':
    
    # Need to be able to run this on a single image
    # or on a selected image
    # or on a directory of images
    # shouldn't require imshow due to opencv-python
    # .. what if it were an ipython notebook? maybe add an %imshow magic?
    
    #_run()
    pass
