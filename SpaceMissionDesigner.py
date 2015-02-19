from tkinter import *
from tkinter import ttk
from PropulsionIterator import PropInputs


class Application:
    def __init__(self, master):
        self.master = master
        master.title("Space Mission Designer")
        self.inputs = PropInputs()

        self.mainframe = ttk.Frame(master)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # Option Selection
        self.option_frame = ttk.LabelFrame(self.mainframe, text="Options", padding=(5, 5, 5, 5))
        self.option_frame.grid(column=2, row=1, sticky=(N, W, E, S))

        ttk.Label(self.option_frame, text="Propellant Type:").grid(column=1, row=1, sticky=E)
        Radiobutton(self.option_frame, text="Monopropellant", variable=self.inputs.prop_type, value=1).grid(column=2, row=1, sticky=W)
        Radiobutton(self.option_frame, text="Bipropellant", variable=self.inputs.prop_type, value=2).grid(column=3, row=1, sticky=W)
        ttk.Label(self.option_frame, text="Fuel Tank Shape:").grid(column=1, row=2, sticky=E)
        Radiobutton(self.option_frame, text="Spherical", variable=self.inputs.fuel_tank_shape, value=1).grid(column=2, row=2, sticky=W)
        Radiobutton(self.option_frame, text="Cylindrical", variable=self.inputs.fuel_tank_shape, value=2).grid(column=3, row=2, sticky=W)
        ttk.Label(self.option_frame, text="Oxidizer Tank Shape:").grid(column=1, row=3, sticky=E)
        Radiobutton(self.option_frame, text="Spherical", variable=self.inputs.ox_tank_shape, value=1).grid(column=2, row=3, sticky=W)
        Radiobutton(self.option_frame, text="Cylindrical", variable=self.inputs.ox_tank_shape, value=2).grid(column=3, row=3, sticky=W)

        # Propulsion inputs
        self.prop_frame = ttk.LabelFrame(self.mainframe, text="Propulsion inputs", padding=(5, 5, 5, 5))
        self.prop_frame.grid(column=2, row=2, sticky=(N, W, E, S))

        isp_entry = ttk.Entry(self.prop_frame, width=10, textvariable=self.inputs.isp).grid(column=2, row=1, sticky=(W, E))
        delta_v_entry = ttk.Entry(self.prop_frame, width=10, textvariable=self.inputs.delta_v).grid(column=2, row=2, sticky=(W, E))
        m_f_initial_entry = ttk.Entry(self.prop_frame, width=10, textvariable=self.inputs.payload).grid(column=2, row=3, sticky=(W, E))
        contingency_entry = ttk.Entry(self.prop_frame, width=10, textvariable=self.inputs.contingency).grid(column=5, row=1, sticky=(W, E))
        ox_fuel_ratio_entry = ttk.Entry(self.prop_frame, width=10, textvariable=self.inputs.ox_fuel_ratio).grid(column=5, row=2, sticky=(W, E))
        thruster_mass_entry = ttk.Entry(self.prop_frame, width=10, textvariable=self.inputs.thruster_mass).grid(column=5, row=3, sticky=(W, E))

        # Labels
        ttk.Label(self.prop_frame, text="Isp =").grid(column=1, row=1, sticky=E)
        ttk.Label(self.prop_frame, text="sec").grid(column=3, row=1, sticky=W)
        ttk.Label(self.prop_frame, text="Delta V =").grid(column=1, row=2, sticky=E)
        ttk.Label(self.prop_frame, text="m/sec").grid(column=3, row=2, sticky=W)
        ttk.Label(self.prop_frame, text="Mf Initial =").grid(column=1, row=3, sticky=E, padx=(54, 0))
        ttk.Label(self.prop_frame, text="kg").grid(column=3, row=3, sticky=W)
        ttk.Label(self.prop_frame, text="Contingency Factor =").grid(column=4, row=1, sticky=E, padx=(39, 0))
        ttk.Label(self.prop_frame, text="Oxidizer:Fuel Ratio =").grid(column=4, row=2, sticky=E)
        ttk.Label(self.prop_frame, text="Engine Mass =").grid(column=4, row=3, sticky=E)
        ttk.Label(self.prop_frame, text="kg").grid(column=6, row=3, sticky=W)

        # Tank Sizing inputs
        self.tank_frame = ttk.LabelFrame(self.mainframe, text="Propellant Tank Sizing", padding=(5, 5, 5, 5))
        self.tank_frame.grid(column=2, row=3, sticky=(N, W, E, S))

        fuel_density_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.fuel_density).grid(column=2, row=1, sticky=(W ,E))
        ox_density_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.ox_density).grid(column=2, row=2, sticky=(W, E))
        op_pressure_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.op_pressure).grid(column=2, row=3, sticky=(W, E))
        aspect_ratio_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.aspect_ratio).grid(column=2, row=4, sticky=(W, E))
        safety_factor_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.safety_factor).grid(column=5, row=1, sticky=(W, E))
        mass_factor_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.mass_factor).grid(column=5, row=2, sticky=(W, E))
        wall_density_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.wall_density).grid(column=5, row=3, sticky=(W, E))
        wall_s_ult_entry = ttk.Entry(self.tank_frame, width=10, textvariable=self.inputs.wall_s_ult).grid(column=5, row=4, sticky=(W, E))

        ttk.Label(self.tank_frame, text="Fuel Density =").grid(column=1, row=1, sticky=E)
        ttk.Label(self.tank_frame, text="kg/m^3").grid(column=3, row=1, sticky=W)
        ttk.Label(self.tank_frame, text="Oxidizer Density =").grid(column=1, row=2, sticky=E)
        ttk.Label(self.tank_frame, text="kg/m^3").grid(column=3, row=2, sticky=W)
        ttk.Label(self.tank_frame, text="Operating Pressure =").grid(column=1, row=3, sticky=E)
        ttk.Label(self.tank_frame, text="MPa").grid(column=3, row=3, sticky=W)
        ttk.Label(self.tank_frame, text="Aspect Ratio =").grid(column=1, row=4, sticky=E)
        ttk.Label(self.tank_frame, text="Safety Factor =").grid(column=4, row=1, sticky=E)
        ttk.Label(self.tank_frame, text="Mass Factor =").grid(column=4, row=2, sticky=E)
        ttk.Label(self.tank_frame, text="Tank Material Density =").grid(column=4, row=3, sticky=E, padx=(20, 0))
        ttk.Label(self.tank_frame, text="kg/m^3").grid(column=6, row=3, sticky=W)
        ttk.Label(self.tank_frame, text="Tank Material s_ult =").grid(column=4, row=4, sticky=E)
        ttk.Label(self.tank_frame, text="MPa").grid(column=6, row=4, sticky=W)

        # Results
        self.results_frame = ttk.LabelFrame(self.mainframe, text="Results")

root = Tk()
main_gui = Application(root)
root.mainloop()
