"""Simulated flight stand with thrust, torque, RPM, and electrical metrology.

Swap for a real Tyto Robotics / RCbenchmark driver to run on hardware. The
config mapping in procedure.yaml is passed as keyword arguments here. The
simulated propulsion follows momentum theory for a 9-inch prop with a rotor
figure of merit of 0.72 and a combined motor + ESC efficiency of 0.75.
"""

import numpy as np

RHO = 1.225  # air density kg/m^3
G = 9.80665
PROP_DIAMETER_M = 0.240  # 9.45 inch (PROP-9450)
DISC_AREA = np.pi * PROP_DIAMETER_M**2 / 4
MAX_THRUST_G = 1840.0
MAX_RPM = 10500.0
ROTOR_FOM = 0.72
DRIVE_EFFICIENCY = 0.75  # motor + ESC


class MockFlightStand:
    def __init__(self, address, sample_rate_hz):
        self.address = address
        self.sample_rate_hz = sample_rate_hz
        self.rng = np.random.default_rng(7)
        self.armed = False
        self._last_sweep = None
        print(f"Flight stand at {address}, {sample_rate_hz} Hz")

    def zero_offsets(self):
        return {"thrust_g": 0.6, "torque_mnm": 1.8}

    def arm(self):
        self.armed = True

    def disarm(self):
        self.armed = False
        print("Bench disarmed, outputs off")

    def sweep(self, start_pct, stop_pct, step_pct):
        """Return dict of lists: throttle, thrust_g, torque_nm, rpm, volts, amps."""
        throttle = list(range(start_pct, stop_pct + 1, step_pct))
        out = {"throttle": throttle, "thrust_g": [], "torque_nm": [],
               "rpm": [], "volts": [], "amps": []}
        for t in throttle:
            x = t / 100.0
            thrust_g = MAX_THRUST_G * x**2 + float(self.rng.normal(0, 4))
            thrust_n = max(thrust_g, 1.0) / 1000.0 * G
            rpm = MAX_RPM * x
            n = max(rpm / 60.0, 1.0)

            # Momentum theory: ideal induced power, then rotor FoM losses.
            p_ideal = thrust_n**1.5 / np.sqrt(2 * RHO * DISC_AREA)
            p_mech = p_ideal / ROTOR_FOM
            torque = p_mech / (2 * np.pi * n)

            volts = 24.0 - 0.9 * x
            amps = (p_mech / DRIVE_EFFICIENCY) / volts

            out["thrust_g"].append(round(max(thrust_g, 0.0), 1))
            out["torque_nm"].append(round(max(torque, 0.0), 4))
            out["rpm"].append(round(rpm, 0))
            out["volts"].append(round(volts, 2))
            out["amps"].append(round(max(amps, 0.02), 3))
        self._last_sweep = out
        return out

    def last_sweep(self):
        return self._last_sweep
