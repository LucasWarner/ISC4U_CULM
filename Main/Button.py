class Button(object):
    def __init__ (self,Xpos,Ypos,wid,high,rad,tex="null"):
        self.x = Xpos
        self.y = Ypos
        self.w = wid
        self.h = high
        self.rad = rad
        self.text = tex
        self.tx = self.x + self.w/4
        self.ty = self.y + self.h/1.65
        self.ix = self.x + self.w/8
        self.iy = self.y + self.h/8
        self.iw = self.w - self.w/4
        self.ih = self.h - self.h/4
        
    def display(self,inRed=210,inGreen=215,inBlue=45,textColour=0,inStrokeW=1,outStrokeW=2,inStroke=240,outStroke=240):#,outred=inRed,outGreen=inGreen,outBlue=inBlue):
        strokeJoin(ROUND)
        hint(ENABLE_STROKE_PURE)
        
        strokeWeight(outStrokeW)
        stroke(outStroke)
        fill(inRed,inGreen,inBlue)
        rect(self.x, self.y, self.w, self.h, self.rad)
        
        strokeWeight(inStrokeW)
        stroke(inStroke)
        fill(inRed,inGreen,inBlue)
        rect(self.ix, self.iy, self.iw, self.ih, self.rad)
    
        fill(textColour)
        noStroke()
        text(self.text, self.tx, self.ty)
    def Del(self):
        del self
