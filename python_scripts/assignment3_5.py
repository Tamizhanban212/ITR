import math as m
from pprint import pprint

l2 = 3
l3 = 4
q1 = float(input("Enter the joint angle 1: "))
q1 = q1*m.pi/180
q2 = float(input("Enter the joint angle 2: "))
q2 = q2*m.pi/180
J = [[-l3*m.sin(q1+q2)-l2*m.sin(q1), -m.sin(q1)*(l3*m.cos(q2)+l2)-m.cos(q1)*l3*m.sin(q2), -l3*m.sin(q1+q2)], [l3*m.cos(q1+q2)+l2*m.cos(q1), m.cos(q1)*(l3*m.cos(q2)+l2)-m.sin(q1)*l3*m.sin(q2), l3*m.cos(q1+q2)], [0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1]]

pprint(J)