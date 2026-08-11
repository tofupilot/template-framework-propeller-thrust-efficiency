import numpy as np

from utils.propulsion import figure_of_merit, system_efficiency


def compute_efficiency(bench, measurements, log):
    data = bench.last_sweep()
    throttle = data["throttle"]

    eff = system_efficiency(data)
    md = measurements.efficiency_curve
    md.x_axis = throttle
    md.y_axis.efficiency = eff

    # Hover point: thrust per motor equals 1/4 AUW of a 1.6 kg quad.
    hover_thrust = 400.0
    hover_idx = int(np.argmin(np.abs(np.asarray(data["thrust_g"]) - hover_thrust)))
    measurements.hover_efficiency_gw = eff[hover_idx]
    log.info(f"Hover point at {throttle[hover_idx]}% throttle, "
             f"{eff[hover_idx]:.1f} g/W")

    measurements.peak_thrust_g = max(data["thrust_g"])

    fom = figure_of_merit(data, prop_diameter_m=0.240)
    measurements.figure_of_merit = fom
    log.info(f"Figure of merit at WOT: {fom:.2f}")
