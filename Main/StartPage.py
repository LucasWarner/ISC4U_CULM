class StartPage(object):
    def __init__ (self,textS,tx,ty,x,y,s,FS):
        startPage = loadImage("Cover.jpeg")
        yes = loadImage("CheckMark.png")
        no = loadImage("RedNo.png")
        textSize(textS)
        image(startPage,0,0,width,height)
        if FS == "True":
            image(yes,x,y,s,s)
        else:
            image(no,x,y,s,s)
        text("FullScreen:",tx,ty)
    def Del(self):
        del self
        clear()
    
        
    
