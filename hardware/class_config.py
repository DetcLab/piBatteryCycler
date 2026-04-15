class ConfigCharge:
    def __init__(self, ilimit, vlow, vreg, ichg, iterm, vdpm, vsafe, isafe, lowchg):
        self.ilimit = ilimit
        self.vlow = vlow
        self.vreg  = vreg
        self.ichg = ichg
        self.iterm = iterm
        self.vdpm = vdpm
        self.vsafe = vsafe
        self.isafe = isafe
        self.lowchg = lowchg
    
    def __repr__(self):
        return f"{self.__class__.__name__} | (ILIMIT: {self.ilimit}, VLOW: {self.vlow}, VREG: {self.vreg}, ICHG: {self.ichg}, ITERM: {self.iterm}, VDPM: {self.vdpm}, VSAFE: {self.vsafe}, ISAFE: {self.isafe}, LOWCHG: {self.lowchg})"

class ConfigLoad:
    def __init__(self, iload):
        self.iload = iload
    
    def __repr__(self):
        return f"{self.__class__.__name__} | (ILOAD: {self.iload})"