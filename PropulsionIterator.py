"""
Determines the wet mass of a rocket propulsion system via iteration.
Each iteration updates tankage and propellant mass.
Handles bipropellant and monopropellant systems.
Does not currently handle blow-down propellant storage considerations.
"""
import math
from tkinter import DoubleVar, IntVar


class PropInputs:
    def __init__(self):
        self.thruster_mass = DoubleVar()         # kg, Mass of the thruster itself.
        self.isp = DoubleVar()                   # sec
        self.delta_v = DoubleVar()               # m/sec
        self.contingency = DoubleVar()
        self.ox_fuel_ratio = DoubleVar()         # Ratio of bipropellant oxidizer to fuel, by mass. 0 if monopropellant.
        self.payload = DoubleVar()               # kg, All mass above this stage - the "first guess" for dry mass.
        self.fuel_density = DoubleVar()          # kg/m^3
        self.ox_density = DoubleVar()            # kg/m^3, set 1 if monopropellant
        self.aspect_ratio = DoubleVar()
        self.mass_factor = DoubleVar()
        self.wall_density = DoubleVar()          # kg/m^3
        self.wall_s_ult = DoubleVar()            # MPa
        self.safety_factor = DoubleVar()
        self.op_pressure = DoubleVar()           # MPa
        self.prop_type = IntVar()                # 1 if monoprop, 2 if biprop
        self.fuel_tank_shape = IntVar()          # 1 if spherical, 2 if cylindrical
        self.ox_tank_shape = IntVar()            # 1 if spherical, 2 if cylindrical

    def calculate(self):
        result = PropOutputs()
        result.iterations = IntVar()
        m_f = self.payload.get()
        m_f_last = 0

        while abs(m_f - m_f_last) > 0.01:
            # Fuel Calculations
            m_p = m_f*(math.exp(self.delta_v.get()/(self.isp.get()*9.8))-1)*self.contingency.get()
            result.fuel_mass.set(m_p/(self.ox_fuel_ratio.get()+1))
            result.oxidizer_mass.set(m_p-result.fuel_mass.get())
            result.fuel_volume.set(result.fuel_mass.get()/self.fuel_density.get())
            result.oxidizer_volume.set(result.oxidizer_mass.get()/self.ox_density.get())

            # Tank Calculations
            if self.fuel_tank_shape == 1:
                result.fuel_tank_radius.set((result.fuel_volume.get()/(math.pi*4/3)) ** (1/3))
                thickness_fuel_sph = self.safety_factor.get()*self.op_pressure.get()*result.fuel_tank_radius/(2*self.wall_s_ult.get())
                result.fuel_tank_mass.set(self.mass_factor.get()*self.wall_density.get()*(4/3*math.pi*((result.fuel_tank_radius.get()+thickness_fuel_sph)**3-result.fuel_tank_radius.get()**3)))
            elif self.fuel_tank_shape == 2:
                result.fuel_tank_radius.set((result.fuel_volume.get()/(math.pi*(self.aspect_ratio.get()+4/3)) ) ** (1/3))
                thickness_fuel_cyl = self.safety_factor.get()*2*self.op_pressure.get()*result.fuel_tank_radius.get()/self.wall_s_ult.get()
                thickness_fuel_cyl_caps = thickness_fuel_cyl/2
                result.fuel_tank_mass.set(self.mass_factor.get()*self.wall_density.get()*math.pi*(4/3*((result.fuel_tank_radius.get()+thickness_fuel_cyl_caps)**3-result.fuel_tank_radius.get()**3)+self.aspect_ratio.get()*result.fuel_tank_radius*(2*result.fuel_tank_radius.get()*thickness_fuel_cyl+thickness_fuel_cyl**2)))
            if result.oxidizer_tank_mass == 1:
                result.oxidizer_tank_radius.set((result.oxidizer_volume.get()/(math.pi*4/3)) ** (1/3))
                thickness_ox_sph = self.safety_factor.get()*self.op_pressure.get()*result.oxidizer_tank_radius/(2*self.wall_s_ult.get())
                result.oxidizer_tank_mass.set(self.mass_factor.get()*self.wall_density.get()*(4/3*math.pi*((result.oxidizer_tank_radius.get()+thickness_ox_sph)**3-result.oxidizer_tank_radius.get()**3)))
            elif result.oxidizer_tank_mass == 2:
                result.oxidizer_tank_radius.set((result.oxidizer_volume.get()/(math.pi*(self.aspect_ratio.get()+4/3)) ) ** (1/3))
                thickness_ox_cyl = self.safety_factor.get()*2*self.op_pressure.get()*result.oxidizer_tank_radius.get()/self.wall_s_ult.get()
                thickness_ox_cyl_caps = thickness_ox_cyl/2
                result.oxidizer_mass.set(self.mass_factor.get()*self.wall_density.get()*math.pi*(4/3*((result.oxidizer_tank_radius.get()+thickness_ox_cyl_caps)**3-result.oxidizer_tank_radius.get()**3)+self.aspect_ratio.get()*result.oxidizer_tank_radius.get()*(2*result.oxidizer_tank_radius.get()*thickness_ox_cyl+thickness_ox_cyl**2)))

            m_f_last, m_f = m_f, self.payload.get() + result.fuel_tank_mass.get() + result.oxidizer_tank_mass.get() + self.thruster_mass.get()
            result.iterations.set(result.iterations.get()+1)

        result.sys_dry_mass.set(self.thruster_mass.get() + result.fuel_tank_mass.get() + result.oxidizer_tank_mass.get())
        result.sys_wet_mass.set(result.sys_dry_mass.get() + result.fuel_mass.get() + result.oxidizer_mass.get())
        result.vehicle_wet_mass.set(m_f + result.fuel_mass.get() + result.oxidizer_mass.get())



class PropOutputs:
    def __init__(self):
        self.iterations = IntVar()
        self.fuel_mass = DoubleVar()
        self.oxidizer_mass = DoubleVar()
        self.fuel_volume = DoubleVar()
        self.oxidizer_volume = DoubleVar()
        self.fuel_tank_mass = DoubleVar()
        self.oxidizer_tank_mass = DoubleVar()
        self.fuel_tank_radius = DoubleVar()
        self.oxidizer_tank_radius = DoubleVar()
        self.sys_dry_mass = DoubleVar()
        self.sys_wet_mass = DoubleVar()
        self.vehicle_wet_mass = DoubleVar()