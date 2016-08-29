import random
import os


class FloodingExercise:

    MIN_ID = 10000

    def __init__(self, name="FLOOD", num_aircrafts=50, parent_dir="flood"):

        self.num_aircrafts = num_aircrafts
        self.min_lat = -24.181252
        self.max_lat = -23.012609
        self.min_lon = -47.15538
        self.max_lon = -44.579773

        self.name = name
        self.parent_dir = parent_dir

        self.EXES_DIR = self.parent_dir+os.path.sep+"exes"
        self.PROC_DIR = self.parent_dir+os.path.sep+"proc"
        self.TABS_DIR = self.parent_dir+os.path.sep+"tabs"
        self.TRAF_DIR = self.parent_dir+os.path.sep+"traf"

        if not os.path.exists(self.EXES_DIR):
            os.makedirs(self.EXES_DIR)

        if not os.path.exists(self.PROC_DIR):
            os.makedirs(self.PROC_DIR)

        if not os.path.exists(self.TABS_DIR):
            os.makedirs(self.TABS_DIR)

        if not os.path.exists(self.TRAF_DIR):
            os.makedirs(self.TRAF_DIR)

    def rand_latitude(self):
        return random.uniform(self.min_lat, self.max_lat)

    def rand_longitude(self):
        return random.uniform(self.min_lon, self.max_lon)

    def generate_cfg(self):
        target = open(self.parent_dir + os.path.sep + "tracks.cfg", 'w')
        target.write('[glb]\n')
        target.write('exe = %s\n' % self.name)
        target.write('canal = 4\n')
        target.write('[dir]\n')
        target.write('aer = aers\n')
        target.write('exe = exes\n')
        target.write('fnt = font\n')
        target.write('img = images\n')
        target.write('snd = sound\n')
        target.write('tab = tabs\n')
        target.write('dat = %s%sdata\n' % (self.parent_dir, os.path.sep))
        target.write('[net]\n')
        target.write('cnfg = 227.12.2\n')
        target.write('data = 231.12.2\n')
        target.write('rdar = 235.12.2\n')
        target.write('port = 1970\n')
        target.write('[time]\n')
        target.write('accel = 1.\n')
        target.write('cnfg = 5\n')
        target.write('fgen = 30\n')
        target.write('prox = 1\n')
        target.close()

    def generate_exe_file(self):
        target = open(self.EXES_DIR + os.path.sep + "%s.exe.xml" % self.name, 'w')

        target.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        target.write('<!DOCTYPE exercicios>\n')
        target.write('<exercicios VERSION="0001" CODE="1961" FORMAT="NEWTON">\n')
        target.write('\n')
        target.write('    <exercicio nExe="%s">\n' % self.name)
        target.write('        <descricao>Flooding Exercise</descricao>\n')
        target.write('        <horainicio>06:00</horainicio>\n')
        target.write('    </exercicio>\n')
        target.write('\n')
        target.write('</exercicios>\n')

        target.close()

    def generate_trafic_file(self):

        target = open(self.TRAF_DIR + os.path.sep + "%s.trf.xml" % self.name, 'w')
        target.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        target.write('<!DOCTYPE trafegos>\n')
        target.write('<trafegos VERSION="0001" CODE="1961" FORMAT="NEWTON">\n')

        for i in range(0,self.num_aircrafts):
            target.write('\t<trafego nTrf="%s">\n' % (i+self.MIN_ID))
            target.write('\t\t<designador>B737</designador>\n')
            target.write('\t\t<ssr>7003</ssr>\n')
            target.write('\t\t<indicativo>HCK%04d</indicativo>\n' % (i+1))
            target.write('\t\t<origem>SBBR</origem>\n')
            target.write('\t\t<destino>SBRJ</destino>\n')
            target.write('\t\t<procedimento>TRJ%s</procedimento>\n' %(i+self.MIN_ID))
            target.write('\t\t<temptrafego>0</temptrafego>\n')
            target.write('\t\t<coord>\n')
            target.write('\t\t\t<tipo>L</tipo>\n')
            target.write('\t\t\t<campoA>%s</campoA>\n' % self.rand_latitude())
            target.write('\t\t\t<campoB>%s</campoB>\n' % self.rand_longitude())
            target.write('\t\t</coord>\n')
            target.write('\t\t<velocidade>250</velocidade>\n')
            target.write('\t\t<altitude>3000</altitude>\n')
            target.write('\t\t<proa>%s</proa>\n' % random.randint(0,359))
            target.write('\t</trafego>\n')
            target.write('\n')

        target.write('\n')
        target.write('</trafegos>\n')
        target.close()

    def generate_procedure_file(self):
        target = open(self.PROC_DIR + os.path.sep + "tabTrj.xml", "w")

        target.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        target.write('<!DOCTYPE trajetorias>\n')
        target.write('<trajetorias VERSION="0001" CODE="1961" FORMAT="NEWTON">\n')

        for i in range(0,self.num_aircrafts):

            nbreaks = random.randint(2,5)

            target.write('\t<trajetoria nTrj="%s">\n' % (i+self.MIN_ID) )
            target.write('\t\t<descricao>%04d - FLOODER / RAND</descricao>\n' % (i+1))

            for j in range(1,nbreaks+1):
                target.write('\t\t<breakpoint nBrk="%s">\n' % j)
                target.write('\t\t<coord>\n')
                target.write('\t\t\t<tipo>L</tipo>\n')
                target.write('\t\t\t<campoA>%s</campoA>\n' % self.rand_latitude())
                target.write('\t\t\t<campoB>%s</campoB>\n' % self.rand_longitude())
                target.write('\t\t</coord>\n')
                target.write('\t\t<altitude>10000</altitude>\n')
                target.write('\t\t<velocidade>210</velocidade>\n')
                target.write('\t\t</breakpoint>\n')
                target.write('\n')

            target.write('\t</trajetoria>\n')

        target.write('</trajetorias>\n')
        target.close()

if __name__ == '__main__':

    a = FloodingExercise(name="FLOOD2", parent_dir="flood")

    a.generate_cfg()
    a.generate_exe_file()
    a.generate_trafic_file()
    a.generate_procedure_file()

    print "Fim"
