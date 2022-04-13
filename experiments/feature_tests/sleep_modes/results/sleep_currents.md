# Active current

The active current of the device is around 40mA ± 2mA.

## Active current with voltage

The voltage was altered in the range of 3.3V - 3.7V and the active current didn't significantly change.

-   3.3V -> 40mA
-   3.4V -> 41mA
-   3.5V -> 41.5mA
-   3.7V -> 40mA

# Sleep mode currents

## time.sleep

Current was identical to the device's active current.

## machine.sleep

Current went down to 7mA ± 0.1mA

## machine.deepsleep

Current went down to 4.4mA ± 0.1mA

## pycom.go_to_sleep()

Current went down to 18μA ± 1μA

## pycom.go_to_sleep(false)

Current went down to 9μA ± 1μA
