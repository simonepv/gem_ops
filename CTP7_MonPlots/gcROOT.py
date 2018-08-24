import ROOT

# keep a pointer to the original TCanvas constructor
caninit = ROOT.TCanvas.__init__

# define a new TCanvas class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(ROOT.TCanvas):
  def __init__(self, *args):
    caninit(self,*args)
    ROOT.SetOwnership(self,False)

# keep a pointer to the original TPad constructor
padinit = ROOT.TPad.__init__

# define a new TPad class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentPad(ROOT.TPad):
  def __init__(self, *args):
    padinit(self,*args)
    ROOT.SetOwnership(self,False)

# keep a pointer to the original TLine constructor
lineinit = ROOT.TLine.__init__

# define a new TLine class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentLine(ROOT.TLine):
  def __init__(self, *args):
    lineinit(self,*args)
    ROOT.SetOwnership(self,False)

# keep a pointer to the original TH1D constructor
th1dinit = ROOT.TH1D.__init__

# define a new TH1D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTH1D(ROOT.TH1D):
  def __init__(self, *args):
    th1dinit(self,*args)
    ROOT.SetOwnership(self,False)

# keep a pointer to the original TH2D constructor
th2dinit = ROOT.TH2D.__init__

# define a new TH2D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentTH2D(ROOT.TH2D):
  def __init__(self, *args):
    th2dinit(self,*args)
    ROOT.SetOwnership(self,False)

# replace the old TCanvas class by the new one
ROOT.TCanvas = GarbageCollectionResistentCanvas
# replace the old TLine class by the new one
ROOT.TLine = GarbageCollectionResistentLine
# replace the old TH1D class by the new one
ROOT.TH1D = GarbageCollectionResistentTH1D
# replace the old TH2D class by the new one
ROOT.TH2D = GarbageCollectionResistentTH2D
