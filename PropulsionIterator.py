"""
Determines the wet mass of a rocket propulsion system via iteration.
Each iteration updates tankage and propellant mass.
Handles bipropellant and monopropellant systems.
Does not currently handle blow-down propellant storage considerations.
"""
import math

# Rocket Equation Inputs
thruster_mass = 54       # kg, Mass of the thruster itself.
isp = 340                # sec
delta_v = 1470          # m/sec
contingency_factor = 1.1
ox_fuel_ratio = 1.41     # Ratio of bipropellant oxidizer to fuel, by mass.  0 if monopropellant.
m_f_initial = 2500+381.86    # kg, All mass above this stage - the "first guess" for dry mass.


# Prop Tank Sizing Inputs
density_fuel = 1008.3    # kg/m^3
density_ox = 2720      # kg/m^3, set 1 if monopropellant
aspect_ratio = 3.5
mass_factor = 1.25
wall_density = 4430.0      # kg/m^3
wall_s_ult = 900.0         # MPa
safety_factor = 2.0
op_pressure = 6.89      # MPa


count_sph = 0
count_cyl = 0


# Spherical Tank

m_f_sph = m_f_initial
m_f_last_sph = 0

while abs(m_f_sph - m_f_last_sph) > 0.01:
    # Fuel Mass Calculations
    m_i = m_f_sph*math.exp(delta_v/(isp*9.8))
    m_p = m_f_sph*(math.exp(delta_v/(isp*9.8))-1)*contingency_factor
    m_fuel = m_p/(ox_fuel_ratio+1)
    m_ox = m_p-m_fuel


    # Tank Mass Calculations
    volume_fuel = m_fuel/density_fuel
    volume_ox = m_ox/density_ox

    radius_fuel_sph = ( volume_fuel/(math.pi*4/3) ) ** (1/3)
    radius_ox_sph = ( volume_ox/(math.pi*4/3) ) ** (1/3)

    thickness_fuel_sph = safety_factor*op_pressure*radius_fuel_sph/(2*wall_s_ult)
    thickness_ox_sph = safety_factor*op_pressure*radius_ox_sph/(2*wall_s_ult)

    tank_mass_fuel_sph = mass_factor*wall_density*(4/3*math.pi*((radius_fuel_sph+thickness_fuel_sph)**3-radius_fuel_sph**3))
    tank_mass_ox_sph = mass_factor*wall_density*(4/3*math.pi*((radius_ox_sph+thickness_ox_sph)**3-radius_ox_sph**3))

    m_f_last_sph = m_f_sph
    m_f_sph = m_f_initial + tank_mass_fuel_sph + tank_mass_ox_sph + thruster_mass
    count_sph += 1

print("Spherical tank:")
print("Converged after " + str(count_sph) + " iterations with difference of " + str(round(abs(m_f_sph - m_f_last_sph),4)) + "kg from previous iteration.")
print("Fuel tank radius = " + str(round(radius_fuel_sph, 4)))
print("Oxidizer tank radius = " + str(round(radius_ox_sph, 4)))
print("System dry mass = " + str(round(tank_mass_fuel_sph + tank_mass_ox_sph + thruster_mass, 4)))
print("System wet mass = " + str(round(tank_mass_fuel_sph + tank_mass_ox_sph + thruster_mass + m_fuel + m_ox, 4)))
print("Fuel mass = " + str(round(m_fuel,4)))
print("Oxidizer mass = " + str(round(m_ox,4)))
print("Fuel tank mass = " + str(round(tank_mass_fuel_sph,4)))
print("Oxidizer tank mass = " + str(round(tank_mass_ox_sph,4)))
print("Stage dry mass = " + str(round(m_f_sph, 4)))
print("Stage wet mass = " + str(round(m_f_sph + m_fuel + m_ox, 4)) + "\n")


# Cylindrical Tank

m_f_cyl = m_f_initial
m_f_last_cyl = 0

while abs(m_f_cyl - m_f_last_cyl) > 0.01:
    # Fuel Mass Calculations
    m_i = m_f_cyl*math.exp(delta_v/(isp*9.8))
    m_p = m_f_cyl*(math.exp(delta_v/(isp*9.8))-1)*contingency_factor
    m_fuel = m_p/(ox_fuel_ratio+1)
    m_ox = m_p-m_fuel

    # Tank Mass Calculations
    volume_fuel = m_fuel/density_fuel
    volume_ox = m_ox/density_ox

    radius_fuel_cyl = ( volume_fuel/(math.pi*(aspect_ratio+4/3)) ) ** (1/3)
    radius_ox_cyl = ( volume_ox/(math.pi*(aspect_ratio+4/3)) ) ** (1/3)

    thickness_fuel_cyl = safety_factor*2*op_pressure*radius_fuel_cyl/wall_s_ult
    thickness_ox_cyl = safety_factor*2*op_pressure*radius_ox_cyl/wall_s_ult
    thickness_fuel_cyl_caps = thickness_fuel_cyl/2
    thickness_ox_cyl_caps = thickness_ox_cyl/2

    tank_mass_fuel_cyl = mass_factor*wall_density*math.pi*(4/3*((radius_fuel_cyl+thickness_fuel_cyl_caps)**3-radius_fuel_cyl**3)+aspect_ratio*radius_fuel_cyl*(2*radius_fuel_cyl*thickness_fuel_cyl+thickness_fuel_cyl**2))
    tank_mass_ox_cyl = mass_factor*wall_density*math.pi*(4/3*((radius_ox_cyl+thickness_ox_cyl_caps)**3-radius_ox_cyl**3)+aspect_ratio*radius_ox_cyl*(2*radius_ox_cyl*thickness_ox_cyl+thickness_ox_cyl**2))

    m_f_last_cyl = m_f_cyl
    m_f_cyl = m_f_initial + tank_mass_fuel_cyl + tank_mass_ox_cyl + thruster_mass
    count_cyl += 1

print("Cylindrical tank:")
print("Converged after " + str(count_cyl) + " iterations with difference of " + str(round(abs(m_f_cyl - m_f_last_cyl),4)) + "kg from previous iteration.")
print("Fuel tank radius = " + str(round(radius_fuel_cyl, 4)))
print("Oxidizer tank radius = " + str(round(radius_ox_cyl, 4)))
print("System dry mass = " + str(round(tank_mass_fuel_cyl + tank_mass_ox_cyl + thruster_mass, 4)))
print("System wet mass = " + str(round(tank_mass_fuel_cyl + tank_mass_ox_cyl + thruster_mass + m_fuel + m_ox, 4)))
print("Stage dry mass = " + str(round(m_f_cyl, 4)))
print("Stage wet mass = " + str(round(m_f_cyl + m_fuel + m_ox, 4)))