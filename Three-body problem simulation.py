from tkinter import *
import numpy as np
from numpy import linalg as la

T = 60                  # Simulation time, s
dT = 1                  # Time interval, ms
dTs = dT / 1000         # Time interval, s
A = 396                 # Canvas side, m
D = 8                   # Object diameter, m
n = 0                   # First step
N = T / dTs             # Last step
G = 6.674484*10**-11    # Gravitational constant, m^3 / (S^2 * kg^1)
limit = D               # Collision detection distance
k = 10                  # Time interval multiplier
dTs *= k

output_text = "x:{x:.1f} vx:{vx:.1f}\ny:{y:.1f} vy:{vy:.1f}"


def main():
    class Body(object):
        def __init__(self, m, x, y, vx, vy):
            self.m = m
            self.position = np.array([canvas.winfo_width() / 2 + x, canvas.winfo_height() / 2 - y])
            self.velocity = np.array([vx, -vy])
            self.d_position = np.array([0, 0])

    def gravity_motion(body1, body2, body3):
        global n
        # Position change
        body1.d_position = body1.velocity * dTs
        body2.d_position = body2.velocity * dTs
        body3.d_position = body3.velocity * dTs

        # Current position
        body1.position += body1.d_position
        body2.position += body2.d_position
        body3.position += body3.d_position

        # Collision detection
        if la.norm(body1.position - body2.position) < limit:
            n = N
            l11['text'] = "Collision 1 and 2"
        elif la.norm(body2.position - body3.position) < limit:
            n = N
            l11['text'] = "Collision 2 and 3"
        elif la.norm(body3.position - body1.position) < limit:
            n = N
            l11['text'] = "Collision 3 and 1"

        # Current velocity
        body1.velocity += G * dTs * (body2.m * (body2.position - body1.position) / (
                    (la.norm((body2.position - body1.position))) ** 3) + body3.m * (body3.position - body1.position) / (
                                                     (la.norm((body3.position - body1.position))) ** 3))
        body2.velocity += G * dTs * (body1.m * (body1.position - body2.position) / (
                    (la.norm((body1.position - body2.position))) ** 3) + body3.m * (body3.position - body2.position) / (
                                                     (la.norm((body3.position - body2.position))) ** 3))
        body3.velocity += G * dTs * (body1.m * (body1.position - body3.position) / (
                    (la.norm((body1.position - body3.position))) ** 3) + body2.m * (body2.position - body3.position) / (
                                                     (la.norm((body2.position - body3.position))) ** 3))

    def start_simulation():
        # Get initial condition
        b1 = Body(float(entry_m1.get()), float(entry_x1_0.get()), float(entry_y1_0.get()), float(entry_vx1_0.get()), float(entry_vy1_0.get()))
        b2 = Body(float(entry_m2.get()), float(entry_x2_0.get()), float(entry_y2_0.get()), float(entry_vx2_0.get()), float(entry_vy2_0.get()))
        b3 = Body(float(entry_m3.get()), float(entry_x3_0.get()), float(entry_y3_0.get()), float(entry_vx3_0.get()), float(entry_vy3_0.get()))
        global n
        n = 0
        l11['text'] = " "

        # Grid plot
        canvas.delete("all")
        canvas.create_line(0, canvas.winfo_height() / 2, canvas.winfo_width(), canvas.winfo_height() / 2)
        canvas.create_line(canvas.winfo_width() / 2, 0, canvas.winfo_width() / 2, canvas.winfo_height())

        # Initial objects plot
        object1 = canvas.create_oval(b1.position[0] - D/2, b1.position[1] - D/2, b1.position[0] + D/2, b1.position[1] + D/2, fill='red')
        object2 = canvas.create_oval(b2.position[0] - D/2, b2.position[1] - D/2, b2.position[0] + D/2, b2.position[1] + D/2, fill='green')
        object3 = canvas.create_oval(b3.position[0] - D/2, b3.position[1] - D/2, b3.position[0] + D/2, b3.position[1] + D/2, fill='blue')
        text1 = canvas.create_text(b1.position[0] + 10, b1.position[1] + 10, text=str(b1.position[0]) + '\n' + str(b1.position[1]), anchor=NW, font="Verdana 8", fill='red')
        text2 = canvas.create_text(b2.position[0] + 10, b2.position[1] + 10, text=str(b2.position[0]) + '\n' + str(b2.position[1]), anchor=NW, font="Verdana 8", fill='green')
        text3 = canvas.create_text(b3.position[0] + 10, b3.position[1] + 10, text=str(b3.position[0]) + '\n' + str(b3.position[1]), anchor=NW, font="Verdana 8", fill='blue')

        # Simulation function
        def motion():
            global n

            n += 1
            gravity_motion(b1, b2, b3)
            canvas.move(object1, b1.d_position[0], b1.d_position[1])
            canvas.itemconfig(text1, text=output_text.format(x=b1.position[0], y=b1.position[1], vx=b1.velocity[0], vy=b1.velocity[1]))
            canvas.move(text1, b1.d_position[0], b1.d_position[1])

            canvas.move(object2, b2.d_position[0], b2.d_position[1])
            canvas.itemconfig(text2, text=output_text.format(x=b2.position[0], y=b2.position[1], vx=b2.velocity[0], vy=b2.velocity[1]))
            canvas.move(text2, b2.d_position[0], b2.d_position[1])

            canvas.move(object3, b3.d_position[0], b3.d_position[1])
            canvas.move(text3, b3.d_position[0], b3.d_position[1])
            canvas.itemconfig(text3, text=output_text.format(x=b3.position[0], y=b3.position[1], vx=b3.velocity[0], vy=b3.velocity[1]))

            if n < N:
                root.after(dT, motion)
        motion()

    def stop_simulation():
        global n
        n = N

    # Interface
    root = Tk()
    root.title("Three-body problem simulation")
    root.geometry("1000x500")

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

    entry_x1_0 = Entry(root, textvariable=x1_0)
    entry_x1_0.grid(row=1, column=1)
    entry_y1_0 = Entry(root, textvariable=y1_0)
    entry_y1_0.grid(row=2, column=1)
    entry_vx1_0 = Entry(root, textvariable=vx1_0)
    entry_vx1_0.grid(row=3, column=1)
    entry_vy1_0 = Entry(root, textvariable=vy1_0)
    entry_vy1_0.grid(row=4, column=1)
    entry_m1 = Entry(root, textvariable=m1)
    entry_m1.grid(row=5, column=1)

    entry_x2_0 = Entry(root, textvariable=x2_0)
    entry_x2_0.grid(row=1, column=2)
    entry_y2_0 = Entry(root, textvariable=y2_0)
    entry_y2_0.grid(row=2, column=2)
    entry_vx2_0 = Entry(root, textvariable=vx2_0)
    entry_vx2_0.grid(row=3, column=2)
    entry_vy2_0 = Entry(root, textvariable=vy2_0)
    entry_vy2_0.grid(row=4, column=2)
    entry_m2 = Entry(root, textvariable=m2)
    entry_m2.grid(row=5, column=2)

    entry_x3_0 = Entry(root, textvariable=x3_0)
    entry_x3_0.grid(row=1, column=3)
    entry_y3_0 = Entry(root, textvariable=y3_0)
    entry_y3_0.grid(row=2, column=3)
    entry_vx3_0 = Entry(root, textvariable=vx3_0)
    entry_vx3_0.grid(row=3, column=3)
    entry_vy3_0 = Entry(root, textvariable=vy3_0)
    entry_vy3_0.grid(row=4, column=3)
    entry_m3 = Entry(root, textvariable=m3)
    entry_m3.grid(row=5, column=3)

    l1 = Label(text="1 - Red", width=20, height=2)
    l1.grid(row=0, column=1)
    l2 = Label(text="2 - Green", width=20, height=2)
    l2.grid(row=0, column=2)
    l3 = Label(text="3 - Blue", width=20, height=2)
    l3.grid(row=0, column=3)

    l4 = Label(text="x0", width=10, height=2)
    l4.grid(row=1, column=0)
    l5 = Label(text="y0", width=10, height=2)
    l5.grid(row=2, column=0)
    l6 = Label(text="vx0", width=10, height=2)
    l6.grid(row=3, column=0)
    l7 = Label(text="vy0", width=10, height=2)
    l7.grid(row=4, column=0)
    l10 = Label(text="m", width=10, height=2)
    l10.grid(row=5, column=0)

    l11 = Label(text="0", width=15, height=2)
    l11.grid(row=6, column=0)

    canvas = Canvas(width=A, height=A, bg="white")
    canvas.grid(row=1, column=5, rowspan=10)

    # Start and stop
    button1 = Button(text="Start", command=start_simulation, width=15, height=2)
    button1.grid(row=6, column=1)
    button2 = Button(text="Stop", command=stop_simulation, width=15, height=2)
    button2.grid(row=6, column=2)

    root.mainloop()


main()
