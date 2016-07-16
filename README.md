# x10_any

Wrapper module to control X10 devices.


### Table of Contents
* [Information](#information)
* [Getting Started](#getting-started)


## Information

Initial focus is supporting:
  * CM17A serial Firecracker X10 unit
      * http://www.averdevelopment.com/python/x10.html can be made to work with Python 3
      * https://bitbucket.org/cdelker/python-x10-firecracker-interface can be used on RaspberryPy to control GPIO, not (yet) Python 3 compatible and does not support ALL on/off
  * Mochad (or compatible) servers to control 
      * https://sourceforge.net/projects/mochad/ for CM15A RF (radio frequency) and PL (power line) controller and the CM19A RF controller
      * https://bitbucket.org/clach04/mochad_firecracker/ works under Windows and Linux and can control CM17A serial Firecracker

Implemented in pure Python. Known to work with:

  * Python 2.7
  * Python 3.5

## Getting Started

To get started:

    pip install -r requirements.txt

And manually get an X10 library, example:

    wget https://bitbucket.org/cdelker/python-x10-firecracker-interface/raw/46b300343d3faa148e17479487581a28ebdfac0e/firecracker.py


### Permissions under Linux

Under Linux most users do not have serial port permissions,
either:

  * give user permission (e.g. add to group "dialout") - RECOMMENDED
  * run this demo as root - NOT recommended!

Giver user dialout (serial port) access:

    # NOTE requires logout/login to take effect
    sudo usermod -a -G dialout $USER

### Sample


    import.....
