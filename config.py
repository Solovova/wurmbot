import configparser
import codecs
import mouse
from gtts import gTTS
from pygame import mixer
import time
import os

class Config:
    def __init__(self):
        path = "config.ini"
        conf = configparser.ConfigParser()
        conf.readfp(codecs.open(path, "r", "utf8"))
        
        self.operations = [st.strip() for st in conf['Main']['operations'].split(',')]
        self.nameLog = conf['Main']['nameLog'].strip()
        self.operationsToDo   = []
        self.operationsPointName = []
        self.operationsPoint = []
        for iOperation in self.operations:
            self.operationsToDo.append(conf[iOperation]['ToDo'])
            try:
                tmpPointName = [name.strip() + '...1...2...3' for name in conf[iOperation]['Point'].split(',')]
            except:
                tmpPointName = []
            self.operationsPointName.append(tmpPointName)
            tmpOperationsPoint = [[0,0] for i in range(len(tmpPointName))]
            self.operationsPoint.append(tmpOperationsPoint)
        self.activeOperation = 0
        
        pathw = "configw.ini"
        if os.path.isfile(pathw):
            confw = configparser.ConfigParser()
            confw.readfp(codecs.open(pathw, "r", "utf8"))
            try:
                self.activeOperation = int(confw['Main']['activeOperation'].strip())
            except:
                self.activeOperation = 0
            
            for ind0 in range(len(self.operationsPoint)):
                for ind1 in range(len(self.operationsPoint[ind0])):
                    for ind2 in range(2):
                        try:
                            PointsName = str(ind0)+'_'+str(ind1)+'_'+str(ind2)
                            tmpcoord = int(confw['Points'][PointsName])
                            self.operationsPoint[ind0][ind1][ind2] = tmpcoord
                        except:
                            ''' '''
        
    def save(self):
        configw = configparser.ConfigParser()
        configw.add_section("Main")
        configw.set("Main", "activeOperation", str(self.activeOperation))
        
        configw.add_section("Points")
        for ind0 in range(len(self.operationsPoint)):
            for ind1 in range(len(self.operationsPoint[ind0])):
                for ind2 in range(len(self.operationsPoint[ind0][ind1])):
                    if type(self.operationsPoint[ind0][ind1][ind2]) == type(0):
                        PointsName = str(ind0)+'_'+str(ind1)+'_'+str(ind2)
                        configw.set("Points", PointsName, str(self.operationsPoint[ind0][ind1][ind2]))
        
        with open("configw.ini", "w") as config_file:
            configw.write(config_file)
        
    
    def getCoordinates(self):   
        self.operationsPoint[self.activeOperation]  = []
        for i in range(len(self.operationsPointName[self.activeOperation])):
            tts = gTTS(text=self.operationsPointName[self.activeOperation][i], lang='en', slow=False)
            fname = str(i) + '.mp3'
            tts.save(fname)
            mixer.init()
            mixer.music.load(fname)
            mixer.music.play()
            while mixer.music.get_busy() == 1:
                time.sleep(0.1)
            mixer.quit()
            tmpspis = mouse.get_position()
            tmpmas = [tmpspis[0],tmpspis[1]]
            self.operationsPoint[self.activeOperation].append(tmpmas)