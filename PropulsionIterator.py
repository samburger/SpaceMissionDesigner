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

        def calculate(prop_inputs):
            result = PropOutputs()
            result.iterations = 0
            m_f = prop_inputs.payload
            m_f_last = 0

            while abs(m_f - m_f_last) > 0.01:
                # Fuel Calculations
                m_p = m_f*(math.exp(prop_inputs.delta_v.get()/(prop_inputs.isp.get()*9.8))-1)*prop_inputs.contingency.get()
                result.fuel_mass = m_p/(prop_inputs.ox_fuel_ratio.get()+1)
                result.oxidizer_mass = m_p-result.fuel_mass
                result.fuel_volume = result.fuel_mass/prop_inputs.fuel_density.get()
                result.oxidizer_volume = result.oxidizer_mass/prop_inputs.ox_density.get()

                # Tank Calculations
                if prop_inputs.fuel_tank_shape == 1:
                    result.fuel_tank_radius = (result.fuel_volume/(math.pi*4/3)) ** (1/3)
                    thickness_fuel_sph = prop_inputs.safety_factor.get()*prop_inputs.op_pressure.get()*result.fuel_tank_radius/(2*prop_inputs.wall_s_ult.get())
                    result.fuel_tank_mass = prop_inputs.mass_factor.get()*prop_inputs.wall_density.get()*(4/3*math.pi*((result.fuel_tank_radius+thickness_fuel_sph)**3-result.fuel_tank_radius**3))
                elif prop_inputs.fuel_tank_shape == 2:
                    result.fuel_tank_radius = (result.fuel_volume/(math.pi*(prop_inputs.aspect_ratioget()+4/3)) ) ** (1/3)
                    thickness_fuel_cyl = prop_inputs.safety_factor.get()*2*prop_inputs.op_pressure.get()*result.fuel_tank_radius/prop_inputs.wall_s_ult.get()
                    thickness_fuel_cyl_caps = thickness_fuel_cyl/2
                    result.fuel_tank_mass = prop_inputs.mass_factor.get()*prop_inputs.wall_density.get()*math.pi*(4/3*((result.fuel_tank_radius+thickness_fuel_cyl_caps)**3-result.fuel_tank_radius**3)+prop_inputs.aspect_ratio.get()*result.fuel_tank_radius*(2*result.fuel_tank_radius*thickness_fuel_cyl+thickness_fuel_cyl**2))
                if prop_inputs.oxidizer_tank_mass == 1:
                    result.oxidizer_tank_radius = (result.oxidizer_volume/(math.pi*4/3)) ** (1/3)
                    thickness_ox_sph = prop_inputs.safety_factor.get()*prop_inputs.op_pressure.get()*result.oxidizer_tank_radius/(2*prop_inputs.wall_s_ult.get())
                    result.oxidizer_tank_mass = prop_inputs.mass_factor.get()*prop_inputs.wall_density.get()*(4/3*math.pi*((result.oxidizer_tank_radius+thickness_ox_sph)**3-result.oxidizer_tank_radius**3))
                elif prop_inputs.oxidizer_tank_mass == 2:
                    result.oxidizer_tank_radius = (result.oxidizer_volume/(math.pi*(prop_inputs.aspect_ratioget()+4/3)) ) ** (1/3)
                    thickness_ox_cyl = prop_inputs.safety_factor.get()*2*prop_inputs.op_pressure.get()*result.oxidizer_tank_radius/prop_inputs.wall_s_ult.get()
                    thickness_ox_cyl_caps = thickness_ox_cyl/2
                    result.oxidizer_mass = prop_inputs.mass_factor.get()*prop_inputs.wall_density.get()*math.pi*(4/3*((result.oxidizer_tank_radius+thickness_ox_cyl_caps)**3-result.oxidizer_tank_radius**3)+prop_inputs.aspect_ratio.get()*result.oxidizer_tank_radius*(2*result.oxidizer_tank_radius*thickness_ox_cyl+thickness_ox_cyl**2))

                m_f_last, m_f = m_f, prop_inputs.payload.get() + result.fuel_tank_mass + result.oxidizer_tank_mass + prop_inputs.thruster_mass.get()
                result.iterations += 1

            result.sys_dry_mass = prop_inputs.thruster_mass.get() + result.fuel_tank_mass + result.oxidizer_tank_mass
            result.sys_wet_mass = result.sys_dry_mass + result.fuel_mass + result.oxidizer_mass
            result.vehicle_wet_mass = m_f + result.fuel_mass + result.oxidizer_mass
            return result


class PropOutputs:
    def __init__(self):
        self.iterations = 0
        self.fuel_mass = 0
        self.oxidizer_mass = 0
        self.fuel_volume = 0
        self.oxidizer_volume = 0
        self.fuel_tank_mass = 0
        self.oxidizer_tank_mass = 0
        self.fuel_tank_radius = 0
        self.sys_dry_mass = 0
        self.sys_wet_mass = 0
        self.vehicle_wet_mass = 0