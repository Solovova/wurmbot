import time
from PyQt5.QtCore import QThread, pyqtSignal
from config import Config
from engine import Engine

# TreadWorker
# потоковый процесс, всегда читает log и делает подготовку данных для Engine
# Config
# читает и записывает данные в ini файл


class TreadWorker(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, window):
        QThread.__init__(self)
        self._isRunning = True
        self._isActive = False
        self.window = window
        self.engine = Engine()
        self.reloadConfig()

    def reloadConfig(self):
        self.config = Config()
        self.logfile = open(self.config.nameLog, "r")
        self.logfile.seek(0, 2)
        self.engine.reset()

    def run(self):
        while self._isRunning:
            row = self.logfile.readline()
            while row:
                self.signal.emit(['AddLog', row])
                self.engine.log.append(row)
                row = self.logfile.readline()

            if self._isActive:
                res = self.engine.run()
                for rowres in res:
                    self.signal.emit(rowres)
            time.sleep(0.05)

        self.logfile.close()

    def stop(self):
        self._isRunning = False

    def setActive(self, activate):
        if not self._isActive and activate:  # запуск
            self.config.activeOperation = self.window.comboBox_Process.currentIndex()
            self.engine.load(self.config.operationsToDo[self.config.activeOperation],
                             self.config.operationsPoint[self.config.activeOperation])
        elif self._isActive and not activate:  # остановка
            self.engine.reset()

        self._isActive = activate
        self.signal.emit(['ChangeActive'])

    def getCoordinates(self):
        self.config.activeOperation = self.window.comboBox_Process.currentIndex()
        self.config.getCoordinates()
