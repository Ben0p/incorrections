# incorrections
Threaded UDP relay for CMR+ GPS corrections

Designed to be a python drop in replacement for [samplicator](https://github.com/sleinen/samplicator)

* Listens on specified udp port for any data from specified source IP
* Sends data to each IP in the IP list on the specified port
* Uses curses module to display statistics



## Usage
Linux only

### IP List File Format
(Default final.conf)
{source IP}:{Destination IP}/{port}
Example:
10.20.23.230:10.20.66.109/5019

Omits any lines beginning with #

This is based on the original samplicator file format

### Running
1. Rename gps3.py to whatever (gps)
2. Copy to /usr/local/bin
3. Type the name in bash terminal and press enter