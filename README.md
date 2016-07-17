# x10_any

Wrapper module to control X10 devices.

[ ![Codeship Status for clach04/x10_any](https://codeship.com/projects/f7535da0-2dd5-0134-789e-12bd9e093a4a/status?branch=master)](https://codeship.com/projects/163630)

### Table of Contents
* [Information](#information)
* [Getting Started](#getting-started)


## Information

Initial focus is supporting:
  * Mochad (or compatible) servers to control
      * https://sourceforge.net/projects/mochad/ for CM15A RF (radio frequency) and PL (power line) controller and the CM19A RF controller
      * https://bitbucket.org/clach04/mochad_firecracker/ works under Windows and Linux and can control CM17A serial Firecracker
  * CM17A serial Firecracker X10 unit, builtin support fot CM17A over regular serial port. For control via GPIO on Raspberry Pi manually install:
      * https://bitbucket.org/cdelker/python-x10-firecracker-interface can be used on Raspberry Pi to control GPIO, not (yet) Python 3 compatible and does not support ALL on/off

Implemented in pure Python. Known to work with:

  * Python 2.7
  * Python 3.5

## Getting Started

To get started:

    pip install -r requirements.txt

### Serial Port Permissions under Linux

Under Linux most users do not have serial port permissions,
either:

  * give user permission (e.g. add to group "dialout") - RECOMMENDED
  * run this demo as root - NOT recommended!

Giver user dialout (serial port) access:

    # NOTE requires logout/login to take effect
    sudo usermod -a -G dialout $USER

### Sample

Mochad

    import x10_any
    
    x10_any.default_logger.setLevel(x10_any.logging.DEBUG) # DEBUG
    
    dev = x10_any.MochadDriver()
    dev.x10_command('A', 1, x10_any.ON)
    dev.x10_command('A', 1, x10_any.OFF)

Firecracker

    import x10_any
    
    x10_any.default_logger.setLevel(x10_any.logging.DEBUG) # DEBUG
    
    dev = x10_any.FirecrackerDriver()
    #dev = x10_any.FirecrackerDriver('COM11')
    #dev = x10_any.FirecrackerDriver('/dev/ttyUSB0')
    dev.x10_command('A', 1, x10_any.ON)
    dev.x10_command('A', 1, x10_any.OFF)
