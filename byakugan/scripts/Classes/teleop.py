
#!/usr/bin/env python
import rospy 
import curses
import os
from cmdGarras import CmdGarras  
from cmdMotores import CmdMotores
from byakugan.msg import CtrlMotores, BoolGarras

class Teleop:
   def __init__(self):
      rospy.init_node("Teleop", anonymous=True)
      self.pubMotores = rospy.Publisher("cmdMotores", CtrlMotores, queue_size=10)
      self.pubGarras = rospy.Publisher("cmdGarras", BoolGarras, queue_size=10)
      self.cmdGarras = CmdGarras(self.pubGarras)
      self.cmdMotores = CmdMotores(self.pubMotores)
      curses.wrapper(self.main)

   def main(self, win):
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:")
    while 1:          
        try:                 
           key = win.getkey()         
           win.clear()                
           win.addstr("Detected key:")
           
           if(key == 'KEY_UP'):
              win.addstr("cima")
           elif(key == 'KEY_DOWN'):
              win.addstr("baixo")
           elif(key == 'KEY_LEFT'):
              win.addstr("esquerda")
           elif(key == 'KEY_RIGHT'):
              win.addstr("direita")
           elif(key == 'q'):
              win.addstr("abaixa")
           elif(key == 'r'):
              win.addstr("levanta")
              

           if key == os.linesep:
              break           
        except Exception as e:
           # No input   
           pass         


if __name__ == "__main__":
   t = Teleop()
   rospy.spin()

