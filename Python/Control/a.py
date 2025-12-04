import scipy.signal as sg
num = [1.0]
den = [1.0, 2.0, 2.0]
wn, zeta, poles = sg.damp((num, den))
print("Polos:", poles)
print("wn:", wn)
print("zeta:", zeta)
