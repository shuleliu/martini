#!/usr/bin/python

# generate parameters needed for packmol building a cylindrical vesicle
# modified to add cap

# original surface area per lipid is 0.56 nm^2
# here I use larger value to avoid steric collision

# the length of lipid is 1.95 = 3.9/2 originally
# here I used larger value to avoid steric collision

import math

from math import pi,sqrt,acos,sin,cos

f = open('cylpara_cap.txt','w')

R = float(raw_input("Cylinder Radius, in unit of nm, should be larger than 8.0 nm: "))

L = float(raw_input("Length of Cylinder, in unit of nm: "))

Lz=float(raw_input("Length of box in z direction, must be greater than twice of cylinder radius: "))

c_salt=float(raw_input("salt concentration in unit of mol/L: "))

water_thickness = float(raw_input("water thickness on one side of the tube in unit of nm: "))

while Lz/2.0<=R:
      print "Twice radius is %f" %(2.0*R)
      print "Lz must be greater than this value"
      Lz=float(raw_input("Reenter Lz in unit of nm: "))

r = R - 8.0  #radius of water cylinder

print>>f, "Radius of cylinder: %f nm" %R
print>>f, "Length of cylinder: %f nm" %L
print>>f, "Length in the z direction: %f nm" %Lz
print>>f, "Radius of water cylinder: %f nm" %r
print>>f, "Radius of the center of the lipid bilayer: %f nm" %((R+r)/2.0)

Lx = L + 2.0*R + 2.0*water_thickness
print>>f, "Estimated Lx in unit of nm: %.5f" %Lx

surf_area = 1.0  # GCER/DPGS surface area

n_outer = int(2.0*math.pi*R*L/surf_area)
n_inner = int(2.0*math.pi*(R+r)/2.0*L/surf_area)

print>>f, "Number of lipids in outer leaflet: %d" %n_outer
print>>f, "Number of lipids in inner leaflet: %d" %n_inner

# calculate the number of lipids in the cap
# this is manually manipulated to reduce the cap density
n_outer_cap = int(4.0*pi*(r+4.0)*(r+4.0)/surf_area)
n_inner_cap = int(4.0*pi*r*r/surf_area)

print>>f, "Number of lipids in outer leaflet of the cap: %d" %n_outer_cap
print>>f, "Number of lipids in inner leaflet of the cap: %d" %n_inner_cap

l_lipid = sqrt(surf_area)

d_costheta_outer = l_lipid/(r+4.0)
nbintheta_cap_outer = int(2.0/d_costheta_outer) + 1
d_phi_outer = l_lipid/(r+4.0)
nbinphi_cap_outer = int(2.0*pi/d_phi_outer) + 1

# make sure there is enough grids
while nbintheta_cap_outer*nbinphi_cap_outer<n_outer_cap:
      print "Not enough grid!"
      print "n_outer_cap = %d" %n_outer_cap
      print "Current number of grids: %d" %(nbintheta_cap_outer*nbinphi_cap_inner)
      print "Will update grids"
      nbintheta_cap_outer+=1 
      nbinphi_cap_outer+=1

print>>f,"Number of bins in cos(theta) for outer cap: %d" %nbintheta_cap_outer
print>>f,"Number of bins in phi for outer cap: %d" %nbinphi_cap_outer

d_costheta_inner = l_lipid/r
nbintheta_cap_inner = int(2.0/d_costheta_inner) + 1
d_phi_inner = l_lipid/r
nbinphi_cap_inner = int(2.0*pi/d_phi_inner) + 1

# make sure there is enough grids
while nbintheta_cap_inner*nbinphi_cap_inner<n_inner_cap:
      print "Not enough grid!"
      print "n_inner_cap = %d" %n_inner_cap
      print "Current number of grids: %d" %(nbintheta_cap_inner*nbinphi_cap_inner)
      print "Will update grids"
      nbintheta_cap_inner+=1 
      nbinphi_cap_inner+=1

print>>f,"Number of bins in cos(theta) for inner cap: %d" %nbintheta_cap_inner
print>>f,"Number of bins in phi for inner cap: %d" %nbinphi_cap_inner

 
r_water = 0.47/2.0   # radius of the martini water
v_water = 4.0/3.0*math.pi*r_water**3
n_water_inner = int(2.0*math.pi*r*L/v_water)
n_water_outer = int((Lz*Lz*Lx - 2.0*pi*R*R*L - 4.0/3.0*pi*R*R*R)/v_water)
print>>f, "Number of water inside the vesicle: %d" %n_water_inner
print>>f, "Number of water outside the vesicle: %d" %n_water_outer

n_avgadro = 6.02e23

# volume of the box in unit of m^3
V_box = Lx*Lz*Lz*1.0e-27

n_salt = c_salt*1.0e3*V_box*n_avgadro

n_na = int(n_salt)
n_cl = int(n_salt)

print>>f, " Salt concentraiton is: %f mol/L" %c_salt
print>>f, " number of Na ions: %d" %n_na 
print>>f, " number of Cl  ions: %d" %n_cl


print>>f,"\n"

# start writing the input parameter part

#DPGS
pdbname='DPGS-em.pdb'
n_i = n_inner/6
n_o = n_outer/6
n_i_c = n_inner_cap/6
n_o_c = n_outer_cap/6
print>>f, "%-20s %5d %5d %5d %5d" %(pdbname,n_i,n_o,n_o_c,n_i_c)

 
#POPE
pdbname='POPE-em.pdb'
n_i = n_inner/6
n_o = n_outer/6
n_i_c = n_inner_cap/6
n_o_c = n_outer_cap/6
print>>f, "%-20s %5d %5d %5d %5d" %(pdbname,n_i,n_o,n_o_c,n_i_c)

#CHOL
pdbname='CHOL-em.pdb'
n_i = n_inner/3
n_o = n_outer/3
n_i_c = n_inner_cap/3
n_o_c = n_outer_cap/3
print>>f, "%-20s %5d %5d %5d %5d" %(pdbname,n_i,n_o,n_o_c,n_i_c)

#DPPC
pdbname='DPPC-em.pdb'
n_i = n_inner/3
n_o = n_outer/3
n_i_c = n_inner_cap/3
n_o_c = n_outer_cap/3
print>>f, "%-20s %5d %5d %5d %5d" %(pdbname,n_i,n_o,n_o_c,n_i_c)

print>>f,"output   cyl_py_cap.gro"
print>>f,"r_inner  %.4f" %r
print>>f,"r_outer  %.4f" %R
print>>f,"Lx       %.4f" %L     # note the we print L rather than Lx
print>>f,"Lz       %.4f" %Lz
print>>f,"nwater_inside  %d" %n_water_inner
print>>f,"nwater_outside  %d" %n_water_outer
print>>f,"nNa  %d" %n_na
print>>f,"nCl  %d" %n_cl
print>>f,"nbintheta_cap_outer  %d" %nbintheta_cap_outer
print>>f,"nbinphi_cap_outer  %d" %nbinphi_cap_outer
print>>f,"nbintheta_cap_inner  %d" %nbintheta_cap_inner
print>>f,"nbinphi_cap_inner  %d" %nbinphi_cap_inner
print>>f, "water_thickness %.5f" %water_thickness

f.close() 
