import numpy as np

class euler2s:
    def __init__(self, x, u1_init, u2_init , du1dx, du2dx):
        self.x = x
        self.u1_init = u1_init
        self.u2_init = u2_init
        self.du1dx = du1dx
        self.du2dx = du2dx
        self.h = x[1] - x[0]
        self.u1 = np.array([u1_init])
        self.u2 = np.array([u2_init])
        self.solve()

    def solve(self):

        for i in range(0,len(self.x)- 1):

            

            u1_next = self.u1[i] + self.h * self.du1dx(self.x[i],self.u1[i],self.u2[i])
            u2_next = self.u2[i] + self.h * self.du2dx(self.x[i],self.u1[i],self.u2[i])

            self.u1 = np.append(self.u1, u1_next)
            self.u2 = np.append(self.u2, u2_next)

           