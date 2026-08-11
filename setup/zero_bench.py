def zero_bench(bench, measurements, log, run):
    log.info("Zeroing thrust and torque with motor un-energized")
    offsets = bench.zero_offsets()
    measurements.thrust_zero_g = offsets["thrust_g"]
    measurements.torque_zero_mnm = offsets["torque_mnm"]

    # Run metadata is filterable on the dashboard.
    run.metadata["line"] = "EOL-2"
    run.metadata["prop_lot"] = "PL-2620-A"
    run.metadata["ambient_temp_c"] = 22.4
