import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import sys
import signal

# Parameters
x_len = 200         # Number of points to display
y_range = [8000, 10000]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

# Initialize communication with TMP102
port = int(input("Input the port: "))
file = input("Input the file location: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("10.45.72.154", port))
print("Connecting to port " + str(port))
sock.settimeout(15)
file = open(f"{file}-{port}.csv", 'w')

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('Encoder Values over Time')
plt.xlabel('Time')
plt.ylabel('Speed(U)')

# This function is called periodically from FuncAnimation
def animate(i, ys):
    dat = sock.recv(1024)
    print(dat)
    data = dat.decode("utf-8")
    try:
        file.write(data + "\n")
        print(data)
    except socket.timeout:
        print("Socket timed out!")
        signal_handler(None, None)
    encoder = float(data.split(",")[1])

    # Add y to list
    ys.append(encoder)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

def signal_handler(self,sig, frame):
   self.file.close()
   sys.exit(0)

# Set up plot to call animate() function periodically
signal.signal(signal.SIGINT, signal_handler)
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
plt.show()
