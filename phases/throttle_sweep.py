import numpy as np


def throttle_sweep(bench, temp_stator, temp_esc, measurements, log):
    bench.arm()
    log.info("Sweeping throttle 10-100% in 10% steps")
    data = bench.sweep(10, 100, 10)

    md = measurements.thrust_curve
    md.x_axis = data["throttle"]
    md.y_axis.thrust = data["thrust_g"]

    temps = temp_stator.read_series(len(data["throttle"]))
    esc_temps = temp_esc.read_series(len(data["throttle"]))
    log.info(f"Stator {temps[-1]}°C, ESC {esc_temps[-1]}°C at end of sweep")

    measurements.stator_temp_c = temps
    aggs = measurements.stator_temp_c.aggregations
    aggs.min = float(np.min(temps))
    aggs.max = float(np.max(temps))
    aggs.mean = float(np.mean(temps))
    aggs.p2p = float(np.ptp(temps))
