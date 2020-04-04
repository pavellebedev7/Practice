from tkinter import *
import numpy as np
from numpy import linalg as la

Ts = 63                 # Simulation time, s
dTs = 0.001             # Simulation time interval, s
Td = 1                  # Display time, s
dTd = 1                 # Display time interval, ms
n = 0                   # First simulation step
N = int(Ts / dTs)       # Last simulation step
k = 20                  # Display time interval multiplier
j = 1                   # First display step
J = N/k                 # Last display step

A = 596                 # Canvas side, m
a = 10                  # Text padding
D = 8                   # Object diameter, m
G = 6.674484*10**-11    # Gravitational constant, m^3 / (S^2 * kg^1)
limit = D               # Collision detection distance
w = 12
h = 2

# Output format
location = "x:{x:.1f} vx:{vx:.1f}\ny:{y:.1f} vy:{vy:.1f}"
status = "T:{T:d}s, multiplier:{k:d}\nn:{n:d} out of {N:d}"


def main():
    class Body(object):
        def __init__(self, m, x, y, vx, vy):
            self.m = m
            # With respect to canvas
            self.position = np.zeros((N, 2))
            self.velocity = np.zeros((N, 2))
            self.d_position = np.zeros((N, 2))
            self.d_velocity = np.zeros((N, 2))
            self.position[0] = [canvas.winfo_width() / 2 + x, canvas.winfo_height() / 2 - y]
            self.velocity[0] = [vx, -vy]
            self.d_position[0] = [0, 0]
            self.d_velocity[0] = [0, 0]
            self.D_position = [0, 0]

            # With respect to grid
            self.velocity0 = np.zeros((N, 2))
            self.position0 = np.zeros((N, 2))
            self.d_position0 = np.zeros((N, 2))
            self.d_velocity0 = np.zeros((N, 2))
            self.velocity0[0] = [vx, vy]
            self.position0[0] = [x, y]
            self.d_position0[0] = [0, 0]
            self.d_velocity0[0] = [0, 0]
            self.D_position0 = [0, 0]

    def gravity_motion(body1, body2, body3):
        global n
        for n in range(N):
            if n > 0:
                # Position change
                body1.d_position[n] = body1.velocity[n-1] * dTs
                body2.d_position[n] = body2.velocity[n-1] * dTs
                body3.d_position[n] = body3.velocity[n-1] * dTs
                body1.d_position0[n] = [body1.d_position[n][0], -body1.d_position[n][1]]
                body2.d_position0[n] = [body2.d_position[n][0], -body2.d_position[n][1]]
                body3.d_position0[n] = [body3.d_position[n][0], -body3.d_position[n][1]]

                # Current position
                body1.position[n] = body1.position[n-1] + body1.d_position[n-1]
                body2.position[n] = body2.position[n-1] + body2.d_position[n-1]
                body3.position[n] = body3.position[n-1] + body3.d_position[n-1]
                body1.position0[n] = body1.position0[n-1] + body1.d_position0[n-1]
                body2.position0[n] = body2.position0[n-1] + body2.d_position0[n-1]
                body3.position0[n] = body3.position0[n-1] + body3.d_position0[n-1]

                # Collision detection
                if la.norm(body1.position[n] - body2.position[n]) < limit:
                    n = N
                    l11['text'] = "Collision 1 and 2"
                elif la.norm(body2.position[n] - body3.position[n]) < limit:
                    n = N
                    l11['text'] = "Collision 2 and 3"
                elif la.norm(body3.position[n] - body1.position[n]) < limit:
                    n = N
                    l11['text'] = "Collision 3 and 1"

                # Velocity change
                body1.d_velocity[n] = G * dTs * (body2.m * (body2.position[n-1] - body1.position[n-1]) / (
                            (la.norm((body2.position[n-1] - body1.position[n-1]))) ** 3) + body3.m * (body3.position[n-1] - body1.position[n-1]) / (
                                                             (la.norm((body3.position[n-1] - body1.position[n-1]))) ** 3))
                body2.d_velocity[n] = G * dTs * (body1.m * (body1.position[n-1] - body2.position[n-1]) / (
                            (la.norm((body1.position[n-1] - body2.position[n-1]))) ** 3) + body3.m * (body3.position[n-1] - body2.position[n-1]) / (
                                                             (la.norm((body3.position[n-1] - body2.position[n-1]))) ** 3))
                body3.d_velocity[n] = G * dTs * (body1.m * (body1.position[n-1] - body3.position[n-1]) / (
                            (la.norm((body1.position[n-1] - body3.position[n-1]))) ** 3) + body2.m * (body2.position[n-1] - body3.position[n-1]) / (
                                                             (la.norm((body2.position[n-1] - body3.position[n-1]))) ** 3))
                body1.d_velocity0[n] = [body1.d_velocity[n][0], -body1.d_velocity[n][1]]
                body2.d_velocity0[n] = [body2.d_velocity[n][0], -body2.d_velocity[n][1]]
                body3.d_velocity0[n] = [body3.d_velocity[n][0], -body3.d_velocity[n][1]]

                # Current velocity
                body1.velocity[n] = body1.velocity[n-1] + body1.d_velocity[n-1]
                body2.velocity[n] = body2.velocity[n-1] + body2.d_velocity[n-1]
                body3.velocity[n] = body3.velocity[n-1] + body3.d_velocity[n-1]
                body1.velocity0[n] = body1.velocity0[n-1] + body1.d_velocity0[n-1]
                body2.velocity0[n] = body2.velocity0[n-1] + body2.d_velocity0[n-1]
                body3.velocity0[n] = body3.velocity0[n-1] + body3.d_velocity0[n-1]

    def start_simulation():
        # Get initial condition
        b1 = Body(float(entry_m1.get()), float(entry_x1_0.get()), float(entry_y1_0.get()), float(entry_vx1_0.get()), float(entry_vy1_0.get()))
        b2 = Body(float(entry_m2.get()), float(entry_x2_0.get()), float(entry_y2_0.get()), float(entry_vx2_0.get()), float(entry_vy2_0.get()))
        b3 = Body(float(entry_m3.get()), float(entry_x3_0.get()), float(entry_y3_0.get()), float(entry_vx3_0.get()), float(entry_vy3_0.get()))
        global n
        l11['text'] = " "
        gravity_motion(b1, b2, b3)
        n = 0

        # Grid plot
        canvas.delete("all")
        canvas.create_line(0, canvas.winfo_height() / 2, canvas.winfo_width(), canvas.winfo_height() / 2)
        canvas.create_line(canvas.winfo_width() / 2, 0, canvas.winfo_width() / 2, canvas.winfo_height())

        # Initial objects plot
        object1 = canvas.create_oval(b1.position[n][0] - D/2, b1.position[n][1] - D/2, b1.position[n][0] + D/2, b1.position[n][1] + D/2, fill='red')
        object2 = canvas.create_oval(b2.position[n][0] - D/2, b2.position[n][1] - D/2, b2.position[n][0] + D/2, b2.position[n][1] + D/2, fill='green')
        object3 = canvas.create_oval(b3.position[n][0] - D/2, b3.position[n][1] - D/2, b3.position[n][0] + D/2, b3.position[n][1] + D/2, fill='blue')
        text1 = canvas.create_text(b1.position[n][0] + a, b1.position[n][1] + a, text=str(b1.position0[n][0]) + '\n' + str(b1.position0[n][1]), anchor=NW, font="Verdana 8", fill='red')
        text2 = canvas.create_text(b2.position[n][0] + a, b2.position[n][1] + a, text=str(b2.position0[n][0]) + '\n' + str(b2.position0[n][1]), anchor=NW, font="Verdana 8", fill='green')
        text3 = canvas.create_text(b3.position[n][0] + a, b3.position[n][1] + a, text=str(b3.position0[n][0]) + '\n' + str(b3.position0[n][1]), anchor=NW, font="Verdana 8", fill='blue')
        stat = canvas.create_text(a, a, text=status.format(T=Ts, k=k, n=int(n), N=int(N)), anchor=NW, font="Verdana 8")

        # Simulation function
        def motion():
            global n
            global j

            canvas.itemconfig(stat, text=status.format(T=Ts, k=k, n=int(j), N=int(J)))

            b1.D_position = b1.position[j*k] - b1.position[(j-1)*k]
            b2.D_position = b2.position[j*k] - b2.position[(j-1)*k]
            b3.D_position = b3.position[j*k] - b3.position[(j-1)*k]

            canvas.move(object1, b1.D_position[0], b1.D_position[1])
            canvas.move(object2, b2.D_position[0], b2.D_position[1])
            canvas.move(object3, b3.D_position[0], b3.D_position[1])

            canvas.move(text1, b1.D_position[0], b1.D_position[1])
            canvas.move(text2, b2.D_position[0], b2.D_position[1])
            canvas.move(text3, b3.D_position[0], b3.D_position[1])

            canvas.itemconfig(text1, text=location.format(x=b1.position0[j*k][0], y=b1.position0[j*k][1], vx=b1.velocity0[j*k][0], vy=b1.velocity0[j*k][1]))
            canvas.itemconfig(text2, text=location.format(x=b2.position0[j*k][0], y=b2.position0[j*k][1], vx=b2.velocity0[j*k][0], vy=b2.velocity0[j*k][1]))
            canvas.itemconfig(text3, text=location.format(x=b3.position0[j*k][0], y=b3.position0[j*k][1], vx=b3.velocity0[j*k][0], vy=b3.velocity0[j*k][1]))

            canvas.create_line(b1.position[j*k][0], b1.position[j*k][1], b1.position[j*k][0] + b1.D_position[0], b1.position[j*k][1] + b1.D_position[1], fill='red')
            canvas.create_line(b2.position[j*k][0], b2.position[j*k][1], b2.position[j*k][0] + b2.D_position[0], b2.position[j*k][1] + b2.D_position[1], fill='green')
            canvas.create_line(b3.position[j*k][0], b3.position[j*k][1], b3.position[j*k][0] + b3.D_position[0], b3.position[j*k][1] + b3.D_position[1], fill='blue')

            j += 1
            if j < J:
                root.after(dTd, motion)

        motion()

    def stop_simulation():
        global n
        n = N-1

    # Interface
    root = Tk()
    root.title("Three-body problem simulation")
    root.geometry("1000x700")

    # Initial condition
    x1_0 = StringVar(root, value='0')
    y1_0 = StringVar(root, value='0')
    vx1_0 = StringVar(root, value='0')
    vy1_0 = StringVar(root, value='0')
    m1 = StringVar(root, value='1.498e14')

    x2_0 = StringVar(root, value='100')
    y2_0 = StringVar(root, value='0')
    vx2_0 = StringVar(root, value='0')
    vy2_0 = StringVar(root, value='-10')
    m2 = StringVar(root, value='1e0')

    x3_0 = StringVar(root, value='-100')
    y3_0 = StringVar(root, value='0')
    vx3_0 = StringVar(root, value='0')
    vy3_0 = StringVar(root, value='10')
    m3 = StringVar(root, value='1e0')

    entry_x1_0 = Entry(root, textvariable=x1_0, width=w)
    entry_x1_0.grid(row=1, column=1)
    entry_y1_0 = Entry(root, textvariable=y1_0, width=w)
    entry_y1_0.grid(row=2, column=1)
    entry_vx1_0 = Entry(root, textvariable=vx1_0, width=w)
    entry_vx1_0.grid(row=3, column=1)
    entry_vy1_0 = Entry(root, textvariable=vy1_0, width=w)
    entry_vy1_0.grid(row=4, column=1)
    entry_m1 = Entry(root, textvariable=m1, width=w)
    entry_m1.grid(row=5, column=1)

    entry_x2_0 = Entry(root, textvariable=x2_0, width=w)
    entry_x2_0.grid(row=1, column=2)
    entry_y2_0 = Entry(root, textvariable=y2_0, width=w)
    entry_y2_0.grid(row=2, column=2)
    entry_vx2_0 = Entry(root, textvariable=vx2_0, width=w)
    entry_vx2_0.grid(row=3, column=2)
    entry_vy2_0 = Entry(root, textvariable=vy2_0, width=w)
    entry_vy2_0.grid(row=4, column=2)
    entry_m2 = Entry(root, textvariable=m2, width=w)
    entry_m2.grid(row=5, column=2)

    entry_x3_0 = Entry(root, textvariable=x3_0, width=w)
    entry_x3_0.grid(row=1, column=3)
    entry_y3_0 = Entry(root, textvariable=y3_0, width=w)
    entry_y3_0.grid(row=2, column=3)
    entry_vx3_0 = Entry(root, textvariable=vx3_0, width=w)
    entry_vx3_0.grid(row=3, column=3)
    entry_vy3_0 = Entry(root, textvariable=vy3_0, width=w)
    entry_vy3_0.grid(row=4, column=3)
    entry_m3 = Entry(root, textvariable=m3, width=w)
    entry_m3.grid(row=5, column=3)

    l1 = Label(text="1 - Red", width=w, height=h)
    l1.grid(row=0, column=1)
    l2 = Label(text="2 - Green", width=w, height=h)
    l2.grid(row=0, column=2)
    l3 = Label(text="3 - Blue", width=w, height=h)
    l3.grid(row=0, column=3)

    l4 = Label(text="x0", width=w, height=h)
    l4.grid(row=1, column=0)
    l5 = Label(text="y0", width=w, height=h)
    l5.grid(row=2, column=0)
    l6 = Label(text="vx0", width=w, height=h)
    l6.grid(row=3, column=0)
    l7 = Label(text="vy0", width=w, height=h)
    l7.grid(row=4, column=0)
    l10 = Label(text="m", width=w, height=h)
    l10.grid(row=5, column=0)

    l11 = Label(text="0", width=w, height=h)
    l11.grid(row=6, column=0)

    canvas = Canvas(width=A, height=A, bg="white")
    canvas.grid(row=1, column=5, rowspan=10)

    # Start and stop
    button1 = Button(text="Start", command=start_simulation, width=w, height=h)
    button1.grid(row=6, column=1)
    button2 = Button(text="Stop", command=stop_simulation, width=w, height=h)
    button2.grid(row=6, column=2)

    root.mainloop()


main()
