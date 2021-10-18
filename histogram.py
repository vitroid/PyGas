from nodebox_wrapper import *
import numpy as np

class Hist:
    def __init__(self,vmin,vmax,interval,colorscheme=None):
        self.vmin = vmin
        self.vmax = vmax
        self.interval = interval
        self.Ndata = 0
        self.Nbin = int((vmax-vmin)/interval)
        self.histo = np.zeros(self.Nbin)
        self.colorscheme = colorscheme
    def accum(self,value,weight=1):
        bin = int((value - self.vmin) / self.interval + 0.5)
        if 0 <= bin < self.histo.shape[0]:
            self.histo[bin] += weight
        self.Ndata += weight
    def draw(self,x,y,width,height,vertical=False):
        nofill()
        stroke(0)
        if self.Ndata == 0:
            return
        if vertical:
            dy = height / self.Nbin
            for i in range(self.Nbin):
                if self.colorscheme is not None:
                    center = (i-0.5)*self.interval+self.vmin
                    h,s,b = self.colorscheme.getHSB(center)
                    fill(h,s,b)
                dx = int(width*self.histo[i]/self.Ndata/self.interval+0.5)
                rect(x-dx,y-i*dy,dx,dy)
        else:
            dx = width / self.Nbin
            for i in range(self.Nbin):
                if self.colorscheme is not None:
                    center = (i-0.5)*self.interval+self.vmin
                    h,s,b = self.colorscheme.getHSB(center)
                    fill(h,s,b)
                dy = int(height*self.histo[i]/self.Ndata/self.interval+0.5)
                rect(i*dx+x,y-dy,dx,dy)
