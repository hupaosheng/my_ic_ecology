class Signal:
    def __init__(self, name, width=None, kind=None, default=None, comment=""):
        self.name = name
        self.width = width
        self.kind = kind
        self.default = default
        self.comment = comment
        
class Block:
    def __init__(self, name:str, kind="as"):
        self.name = name
        self.kind = kind
        self.signals:List[Signal] = []
        self.texts: List[str] = []
        self.textkinds: List[str] = []
    
    def add_signal(self, signal):
        self.signals.append(signal)
        
    def add_text(self, text, textkind):
        self.texts.append(text)
        self.textkinds.append(textkind)

class Connect:
    def __init__(self, moduleinster,signal):
        self.moduleinster = moduleinster
        self.signal = signal
        
class Connecter:
    def __init__(self, name:str):
        self.name = name
        self.connects: List[Connect] = []
    
    def add_signal(self, module, signal):
        self.connects.append(Connect(module,signal))
        module.signals.append(signal)
        module.connecters.append(self)
        
    def add_param(self, module, signal):
        self.connects.append(Connect(module,signal))
        module.parasignals.append(signal)
        module.paraconnecters.append(self)
        
class HDLmodule:
    def __init__(self, name: str, path: str, header=None):
        self.header:ModuleHeader = header
        self.path = path
        self.signals:List[Signal] = []
        self.blocks:List[Block] = []
        self.connecters:List[Connecter] = []
        self.moduleinsters:List[ModuleInster] = []
        
    def update(self):
        for block in self.blocks:
            for signal in block.signals:
                print(signal.name + signal.kind)
                signal_mergemark(signal,self.header.signals,self.signals)
        for connecter in self.connecters:
            signal_mergemark(Signal(connecter.name,width = connecter.connects[0].signal.width,kind = "wire"),self.header.signals,self.signals)

    def write_v(self):
        self.update()
        with open(self.path, 'w', encoding='utf-8') as f:
            if(self.header.headparams):
                f.write("module " + self.header.name + "#(" + "\n")
                for i,para in  enumerate(self.header.headparams):
                    if i == len(self.header.headparams) -1 :
                        f.write("    parameter " + para.name + "=" + para.default +"\n")
                    else:
                        f.write("    parameter " + para.name + "=" + para.default + "," +"\n")
                f.write(")("+"\n")
            else:
                f.write("module " + self.header.name + "(" + "\n")
            for i,signal in  enumerate(self.header.signals):
                if(i == len(self.header.signals) -1):
                    if(signal.width == "0"):
                        f.write("    " + signal.kind + " " + signal.name + "\n")
                    else:
                        f.write("    " + signal.kind + " " + "[" + signal.width + ":0] " + signal.name + "\n")
                else:
                    if(signal.width == "0"):
                        f.write("    " + signal.kind + " " + signal.name + "," + "\n")
                    else:
                        f.write("    " + signal.kind + " " + "[" + signal.width + ":0] " + signal.name + "," + "\n")
            f.write(");\n\n")
            for signal in self.signals:
                if(signal.width == "0"):
                    f.write("    " + signal.kind + " " + signal.name + ";" + "\n")
                else:
                    f.write("    " + signal.kind + " " + "[" + signal.width + ":0] " + signal.name + ";" + "\n")
            f.write("\n")
            for block in self.blocks:
                for text in block.texts:
                    f.write("    " + text + "\n")
                f.write("\n")
            for moduleinster in self.moduleinsters:
                if(moduleinster.hdlmodule.header.headparams):
                    f.write("    " + moduleinster.hdlmodule.header.name + " #( " + "\n")
                    for i,connecter in enumerate(moduleinster.paraconnecters):
                        if(i == len(moduleinster.paraconnecters) -1):
                            for connect in connecter.connects:
                                if(connect.moduleinster is moduleinster):
                                    f.write("    " + "    " + "." + connect.signal.name + "(" + connecter.name + ")" +"\n")
                        else:
                            for connect in connecter.connects:
                                if(connect.moduleinster is moduleinster):
                                    f.write("    " + "    " + "." + connect.signal.name + "(" + connecter.name + ")," +"\n")
                    f.write("    " + ") " + moduleinster.name + " ("+"\n")
                else:
                    f.write("    " + moduleinster.hdlmodule.header.name + " (" + "\n")
                for i,connecter in enumerate(moduleinster.connecters):
                    if(i == len(moduleinster.connecters) -1):
                        for connect in connecter.connects:
                            if(connect.moduleinster is moduleinster):
                                f.write("    " + "    " + "." + connect.signal.name + "(" + connecter.name + ")" +"\n")
                    else:
                        for connect in connecter.connects:
                            if(connect.moduleinster is moduleinster):
                                f.write("    " + "    " + "." + connect.signal.name + "(" + connecter.name + ")," +"\n")
                f.write("    " + ");\n\n")
            f.write("endmodule")
                    
class ModuleHeader:
    def __init__(self, name: str):
        self.name = name
        self.headparams: List[Signal] = []
        self.signals: List[Signal] = []

    def add_param(self, signal):
        self.headparams.append(signal)
        return self

    def add_signal(self, signal):
        self.signals.append(signal)
        return self

        
class ModuleInster:
    def __init__(self, name: str, hdlmodule):
        self.name = name
        self.hdlmodule: HDLmodule = hdlmodule
        self.signals: List[Signal] = []
        self.connecters: List[Connecter] = []
        self.parasignals: List[Signal] = []
        self.paraconnecters: List[Connecter] = []
        
def signal_mergemark(signal,signals1,signals2):
    mark = 1
    for signal_old in signals1:
        
        if(signal.name == signal_old.name):
            print("   " + signal_old.name + signal_old.kind)
            if(signal_old.kind == "output" and signal.kind == "reg"):
                signal_old.kind = "output reg"
            mark = 0
    for signal_old in signals2:
        if(signal.name == signal_old.name):
            mark = 0
    if(mark):
        signals2.append(signal)
    
    
