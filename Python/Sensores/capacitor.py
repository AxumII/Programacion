
class Capacitor:
    def __init__(self,d_S,h_left,h_right,width = 10):
        self.d_S = d_S
        self.h_left = h_left
        self.h_right = h_right
        self.widht = width
        self.Ea = 1.0001
        self.Ev = 8.854e-12
        
    def area(self):
        t1 = self.widht*self.h_left / 2
        t2 = self.widht*self.h_right / 2
        return t1 + t2
    
    def cap(self):
        return (self.Ea*self.Ev*self.area())/self.d
        
        
d_S = 10/1000 #mm
h_left = 40/1000 #mm
h_right = 40/1000 #mm


c1 = Capacitor(d_S = d_S, h_left = h_left, h_right=h_right )
print(c1.cap())