def power_down(bench, log):
    # Teardown always runs, even when a main phase fails.
    bench.disarm()
    log.info("Bench powered down")
