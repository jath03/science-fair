import serial, threading, websockets, asyncio, webbrowser, server, pickle
from tkinter import *

serial_port = 'COM4'

class Project:
    pass



class Gui(Project):
    def __init__(self):
        self.ser = serial.Serial(serial_port, 9600)
        self.canvases = list()
        self.tk = Tk()
        self.frame = Frame(master=self.tk, width=5, bd=2)
        self.canvas = Canvas(self.frame, height=480, width=640)
        self.graph = Canvas(self.frame, height=220, width=640, bd=3, relief='flat')
        self.var = self.canvas.create_text(1, 1, anchor='nw', text='', font=('Comic Sans MS', 30))
        self.quit = Button(self.frame, text="quit", anchor='ne', command=self.tk.destroy)
        self.re = Button(self.frame, text="restart", anchor='ne', command=self.restart)
        self.canvases.append(self.canvas)
        self.canvases.append(self.graph)
        self.quit.pack(side='top')
        self.re.pack(side='top')
        self.canvas.pack(side='top')
        self.graph.pack(side='bottom')
        self.frame.pack()
        self.count = 0
        self.last_coords = (0, 200)
        self.tk.title(string="Science Project")
        self.graphLines = list()

    def plot(self, value, last_coords, count):
        try:
            new_coords = (count * 5), (200 - float(value))
            self.graphLines.append(self.graph.create_line(last_coords[0], last_coords[1], new_coords[0], new_coords[1], fill='green'))
            count += 1
            return new_coords, count
        except ValueError as err:
            print(err)
            return None

    def stop(self):
        for can in self.canvases:
            can.quit()
        sys.exit(0)

    def restart(self):
        for x in self.graphLines:
            self.graph.delete(x)
        self.count = 0
        self.last_coords = (0, 200)

    def myMainLoop(self):
        try:
            val = self.ser.readline().decode()
            self.last_coords, self.count = self.plot(val, self.last_coords, self.count)
            self.canvas.itemconfig(self.var, text=val)
            self.tk.update()
            self.tk.after(1000, self.myMainLoop)
        except (serial.SerialTimeoutException) as err:
            print('error: {} \n Data could not be read'.format(err))
            self.tk.after(100, self.myMainLoop)


class Web(Project):
    def __init__(self):
        print("Web mode running...")
        self.ser = serial.Serial(serial_port, 9600)
        start_server = websockets.serve(self.handler, 'localhost', 5678)
        asyncio.get_event_loop().run_until_complete(start_server)
        webbrowser.open('http://localhost:9898')
        asyncio.get_event_loop().run_forever()

    async def getVal(self):
        val = self.ser.readline().decode()
        return val

    async def handler(self, websocket, path):
        while True:
            val = await self.getVal()
            await websocket.send(val)
            await asyncio.sleep(.1)


i = input("Gui mode(1) or webbrower mode(2): ")
while i != '1' and i != '2':
    print('Please answer with \"1\" or \"2\"')
    i = input("Gui mode(1) or webbrower mode(2): ")
if i == '1':
    p = Gui()
    myMainloop = threading.Thread(target=p.myMainLoop)
    myMainloop.start()
    p.tk.mainloop()
else:
    server.bg_server.start()
    p = Web()
