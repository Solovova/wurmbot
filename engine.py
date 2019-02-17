import keyboard
import mouse
from timeit import default_timer
import time

#KeyPress (press, [waitms])
# MouseClick (press, [waitms]) L-left button
#Label (label)
#GoTo (label)
# WaitTime(waitms)

# LoopSet(iterrstions)
# LoopGoTo(label)

# Stop()

# LogClear()

# WaitText(waitms , label0, label1, text1;text2;...,label2,text1;text2;...,) #label1 if text, label2 if text, label0 if empty

# MouseMoveTo    point,msekwait
# MouseMoveDiff    dx,dy,msekwait
# MouseDragFrom  point,wait before click, wait after click
# MouseDragTo    point,wait before click, wait after click

#TimerSet (ntimer, ms)
#TimerGoTo (ntimer, label)


def isText(text, searches):
    for search in searches.split(':'):
        if search.strip() in text:
            return True
    return False


class Engine():
    def __init__(self):
        self.reset()

    def reset(self):
        self.Procedures = []
        self.Points = []
        self.DoProcedure = 0
        self.DoPreviousProcedure = -1
        self.DoTimer0 = 0
        self.DoTimerMax = 5
        self.DoTimer = [0 for i in range(self.DoTimerMax)]
        self.log = []
        self.lastrow = ''

    def addCommand(self, data, command):
        try:
            ind0 = command.find('(')
            ind1 = command.find(')')
            if ind0 == -1 or ind1 == -1:
                raise Exception('has no ()')
            stCommand = command[0:ind0].strip()
            stData = [el.strip()
                      for el in command[ind0+1:ind1].strip().split(',')]
        except Exception as e:
            data.append(['Error', str(e)])
        else:
            data.append([stCommand, stData])

    def load(self, commands, points):
        self.reset()
        for command in commands.split(';'):
            self.addCommand(self.Procedures, command.strip())
        self.DoLabels = {}
        for ind, procedure in enumerate(self.Procedures):
            if procedure[0] == 'Label':
                self.DoLabels[procedure[1][0]] = ind

        for point in points:
            self.Points.append([point[0], point[1]])

        print(self.Points)

    def run(self):
        ret = []
        if self.DoProcedure >= len(self.Procedures):
            self.DoProcedure = 0  # GoTo Start

        if self.DoPreviousProcedure != self.DoProcedure:
            ret.append(['AddToDo', str(self.DoProcedure), self.Procedures[self.DoProcedure]
                        [0], self.Procedures[self.DoProcedure][1]])
            self.DoPreviousProcedure = self.DoProcedure

        m = globals()['Engine']
        if (self.Procedures[self.DoProcedure][0] == 'Error'):
            self.DoProcedure += 1
            return ret
        func = getattr(m, 'SubProcedure_' +
                       self.Procedures[self.DoProcedure][0])
        result = func(self, self.Procedures[self.DoProcedure][1])
        if result == 1:
            self.DoProcedure += 1
        elif result == -2:
            ret.append(['AddToDo', 'Stop', '', ''])
            ret.append(['Stop', '', '', ''])

        return ret

    def SubProcedure_KeyPress(self, data):
        keyboard.press(data[0])
        time.sleep(0.05)
        keyboard.release(data[0])
        if len(data) > 1:
            time.sleep(float(data[1])/1000)
        return 1

    def SubProcedure_MouseClick(self, data):
        if data[0] == 'L':
            mouse.click()
        elif data[0] == 'R':
            mouse.click(button='right')

        if len(data) > 1:
            time.sleep(float(data[1])/1000)
        return 1

    def SubProcedure_WaitTime(self, data):
        if self.DoTimer0 == 0:
            self.DoTimer0 = default_timer(
            ) + float(data[0])/1000  # время окончания

        if default_timer() > self.DoTimer0:
            self.DoTimer0 = 0
            return 1
        else:
            return 0

    def SubProcedure_Label(self, data):
        return 1

    def SubProcedure_GoTo(self, data):
        try:
            self.DoProcedure = self.DoLabels[data[0]]-1
        except:
            return 1
        return 1

    def SubProcedure_LoopSet(self, data):
        self.DoLoop = int(data[0]) - 1
        return 1

    def SubProcedure_LoopGoTo(self, data):
        if self.DoLoop == 0:
            return 1
        self.DoLoop -= 1
        return self.SubProcedure_GoTo(data)

    def SubProcedure_Stop(self, data):
        return -2

    def SubProcedure_LogClear(self, data):
        self.log = []
        self.lastrow = ''
        return 1

    # WaitText(waitms , label1, text1;text2;...,label2,text1;text2;..., label3 ...)
    def SubProcedure_WaitText(self, data):
        if self.DoTimer0 == 0:
            self.DoTimer0 = default_timer(
            ) + float(data[0])/1000  # время окончания

        if len(self.log) > 0 and self.lastrow == '':
            self.lastrow = self.log.pop(0)
        print(self.lastrow)

        param = 1
        while len(data) > param:
            if isText(self.lastrow, data[param+1]):
                self.DoTimer0 = 0
                if data[param+2] == 'del':
                    self.lastrow = ''
                return self.SubProcedure_GoTo([data[param]])
            param += 3

        self.lastrow = ''

        if default_timer() > self.DoTimer0:
            self.DoTimer0 = 0
            return 1
        else:
            return 0

    def SubProcedure_MouseMoveTo(self, data):
        mouse.move(self.Points[int(data[0])][0], self.Points[int(data[0])][1])
        if len(data) > 1:
            time.sleep(float(data[1])/1000)
        return 1

    def SubProcedure_MouseMoveDiff(self, data):
        pos = mouse.get_position()
        mouse.move(pos[0] + int(data[0]), pos[1] + int(data[1]))
        if len(data) > 2:
            time.sleep(float(data[2])/1000)
        return 1

    def SubProcedure_MouseDragFrom(self, data):
        mouse.move(self.Points[int(data[0])][0], self.Points[int(data[0])][1])
        if len(data) > 1:
            time.sleep(float(data[1])/1000)
        mouse.press(button='left')
        if len(data) > 2:
            time.sleep(float(data[2])/1000)
        return 1

    def SubProcedure_MouseDragTo(self, data):
        mouse.move(self.Points[int(data[0])][0], self.Points[int(data[0])][1])
        if len(data) > 1:
            time.sleep(float(data[1])/1000)
        mouse.release(button='left')
        if len(data) > 2:
            time.sleep(float(data[2])/1000)
        return 1

    def SubProcedure_TimerSet(self, data):
        indTimer = int(data[0])
        if indTimer > self.DoTimerMax:
            return 1
        self.DoTimer[indTimer] = default_timer() + float(data[1]) / \
            1000  # время окончания
        return 1

    def SubProcedure_TimerGoTo(self, data):
        indTimer = int(data[0])
        if default_timer() > self.DoTimer[indTimer] and self.DoTimer[indTimer] != 0:
            self.DoTimer[indTimer] = 0
            return self.SubProcedure_GoTo([data[1]])
        else:
            return 1
