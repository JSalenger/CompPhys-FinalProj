from graphics import GraphWin

class WindowSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(WindowSingleton, cls).__new__(cls)
            print("new window made")
            cls.win = GraphWin("GNA", 900, 900, autoflush=False)
            cls.win.setCoords(-10, -10, 10, 10)

        return cls.instance

    def __call__(self):
        return self.getWindow()

    def getWindow(self):
        return self.win
