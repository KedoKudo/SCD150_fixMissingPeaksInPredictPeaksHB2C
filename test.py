from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# data IPTS and run numbers ----------------------------------------------------
data_ipts = 25156
data_runs = [543722, 545522]  #[325670, 327470]

# vandium IPTS and run number --------------------------------------------------
van_ipts = 23858
van_run = 531821  #320259

# wavelength (angstrom) --------------------------------------------------------
wavelength = 1.486

# minimum and maximum values for Q sample --------------------------------------
min_values = [-7.5, -0.65, -4.4]
max_values = [6.8, 0.65, 7.5]

# obliquity parallax coefficient
cop = 1.0

# detector grouping for loading data faster ------------------------------------
grouping = '4x4'  # '2x2', 'None', '4x4'

# ---

# predict peak centering -------------------------------------------------------
reflection_condition = 'Primitive'

# ---

norm = LoadWANDSCD(IPTS=van_ipts, RunNumbers=van_run, Grouping=grouping)

data = LoadWANDSCD(IPTS=data_ipts,
                   RunNumbers='{}-{}'.format(*data_runs),
                   Grouping=grouping)

norm_replicated = ReplicateMD(ShapeWorkspace=data, DataWorkspace=norm)
data = DivideMD(LHSWorkspace=data, RHSWorkspace=norm_replicated)

scale = 1

data.setSignalArray(data.getSignalArray() / scale)
data.setErrorSquaredArray(data.getErrorSquaredArray() / scale**2)

data_norm = ConvertHFIRSCDtoMDE(data,
                                Wavelength=wavelength,
                                ObliquityParallaxCoefficient=cop,
                                MinValues='{},{},{}'.format(*min_values),
                                MaxValues='{},{},{}'.format(*max_values))

bragg = PredictPeaks(InputWorkspace=data_norm,
                     ReflectionCondition=reflection_condition,
                     CalculateGoniometerForCW=True,
                     MinAngle=-90,
                     MaxAngle=90,
                     Wavelength=wavelength,
                     OutputType='Peak')
