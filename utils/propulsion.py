import numpy as np

RHO = 1.225  # air density kg/m^3
G = 9.80665


def system_efficiency(data):
    """Thrust (g) per electrical watt at each sweep step."""
    thrust = np.asarray(data["thrust_g"], dtype=float)
    p_elec = np.asarray(data["volts"], dtype=float) * np.asarray(
        data["amps"], dtype=float
    )
    return [round(float(t / max(p, 0.1)), 2) for t, p in zip(thrust, p_elec)]


def figure_of_merit(data, prop_diameter_m):
    """FoM = C_T^1.5 / (C_P * sqrt(2)) at wide-open throttle (rotorcraft hover convention, see McCormick)."""
    n = data["rpm"][-1] / 60.0  # rev/s
    d = prop_diameter_m
    thrust_n = data["thrust_g"][-1] / 1000.0 * G
    torque_nm = data["torque_nm"][-1]
    p_mech = torque_nm * 2 * np.pi * n

    c_t = thrust_n / (RHO * n**2 * d**4)
    c_p = p_mech / (RHO * n**3 * d**5)
    return float(c_t**1.5 / (c_p * np.sqrt(2)))
