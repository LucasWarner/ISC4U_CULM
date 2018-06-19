class Checkbox(object):
    __init__(self,x,y)
    self.over=False
    self.x = _x;
    self.y = _y;
    self.clicked = False;
  }
  void render(){
    stroke(255);
    fill(isOver()?128:64);
    rect(x, y, 20, 20);
    if(b){
      line(x, y, x+20, y+20);
      line(x, y+20, x+20, y);
    }
  }
  void click(){
    if(isOver()){
      b=!b;
    }
  }
  boolean isOver(){
    return(mouseX>x&&mouseX<x+20&&mouseY>y&&mouseY<y+20);
  }
}
