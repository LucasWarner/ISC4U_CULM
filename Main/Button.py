class Button(object):
    def __init__ (self,Xpos,Ypos,wid,high,rad,tex="null",ist=False,rotri=False, texSiz=18):
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
        self.lst = ist
        self.rotation = rotri
        self.tS=texSiz
        
    def display(self,inRed=210,inGreen=215,inBlue=45,textColour=0,inStrokeW=1,outStrokeW=2,inStroke=240,outStroke=240):#,outred=inRed,outGreen=inGreen,outBlue=inBlue):
        if inRed!=0 and inGreen!=0 and inBlue!=0:
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
        if self.lst:
            if self.rotation:
                fill(255)
                triangle(self.x+10, self.y+5, self.x+10, self.y+self.h/2, self.x+20, self.y+2.5+self.h/4)
            elif self.rotation==False:
                fill(255)
                triangle(self.x+10, self.y+5, self.x+20, self.y+5, self.x+15, self.y+self.h/2)
        fill(textColour)
        noStroke()
        textSize(self.tS)
        text(self.text, self.tx, self.ty)
    def Del(self):
        del self
