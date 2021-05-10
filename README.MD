# LBChallenge.py Overview

The LBChallenge Python module simulates a load balancer, reverse proxying traffic to a backend pool member that is available each run.

### Key features include:
-------------------------
* Ingesting a yaml file with the VIP name and its associated pool members
* Performing a TCP Healthcheck on the backend pool member port
* Implementing the 'round-robin' load balancing algorithm with a pickled file containing the service name to persist member state
* With a current version of Python (3.9), the LBChallenge module should be OS agnostic.

### How to:
-----------
* Clone the "LBChallenge" repository. Specifically, you will need to pull the 'LBChallenge.py' and 'observabilityplatforms.com.yaml' files.
```
gh repo clone joegarcia12/LBChallenge
git@github.com:joegarcia12/LBChallenge.git
```
* Each LBChallenge.py run will generate a 'rr_state.pk' and error.html file in the current working directory. Delete the 'rr_state.pk' file in the event you modify the members within the YAML file.
```
#### Example run, all members up ####
josephrgarcia-mbp:LBChallenge josephrgarcia$ python3 LBChallenge.py
Service name: observabilityplatforms.com
Connection to 142.251.33.110 port 443 [tcp/https] succeeded!
Connection to 52.5.196.118 port 443 [tcp/https] succeeded!
Connection to 52.84.169.4 port 443 [tcp/https] succeeded!
Your VIP returned member: newrelic.com:443

#### First member is unavailable, other 2 members are available. ####
josephrgarcia-mbp:LBChallenge josephrgarcia$ python3 LBChallenge.py
Service name: observabilityplatforms.com
nc: connectx to 100.251.33.110 port 443 (tcp) failed: Operation timed out
Connection to 52.5.196.118 port 443 [tcp/https] succeeded!
Connection to 52.84.169.4 port 443 [tcp/https] succeeded!
Your VIP returned member: splunk.com:443

#### where only 1 member is available ####
josephrgarcia-mbp:LBChallenge josephrgarcia$ python3 LBChallenge.py
Service name: observabilityplatforms.com
Connection to 142.251.33.110 port 443 [tcp/https] succeeded!
nc: connectx to 100.15.196.118 port 443 (tcp) failed: Operation timed out
nc: connectx to 100.84.169.4 port 443 (tcp) failed: Operation timed out
Your VIP returned member: newrelic.com:443

```

### Improvements, given more time:
----------------------------------
* Print a more user-friendly output than the standard nc output when a member passes/fails healthcheck.
* LBChallenge.py returns a 'EOFError: Ran out of input' exception if the 'rr_state.pk' file exists but is empty. The 'else' condition iterates self.rr_count beyond the number of available members.  A try/except code block fixed this, but it doesn't consider the corner case where the pickle byte stream is modified and interrupts the dictionary 'list' calls in Roundrobin().
* There is a "ValueError: 'newrelic.com' is not in list" if, for example, 'newrelic.com' is a member defined in the YAML file, removed from the YAML file, and 'newrelic.com' is the string stored in the pickled file. Members are hot-swappable, but I recommend deleting the 'rr_state.pk' file to workaround this corner case or any other potential corner cases that could appear.
* No need to waste CPU and Disk I/O when overwriting the existing error.html page, if it already exists.
* The end goal was not to be a fully-featured load balancer, but the VIP address and listener_port are inconsequential for each run. I ended up not needing them in this application, but I left them there to demonstrate how additional properties in the YAML file could be configured.
* This script was limited to load balancing HTTPS websites, when we could load balance any service (LDAP, SMTP, mysql, etc). I focused on HTTPS since they are the most prevalent use case for load balancers, and it's easy to determine whether a website is available programmatically and visually. The '503' response handling mentioned in the LBChallenge.md file pushed me to focus on HTTPS.
* Haven't tested on Windows, but it should work if one could get the Linux Subsystem configured and running, along with installing the latest Python version.
* The YAML-defined websites use round-robin DNS, but this program only healthchecked 1 of the A records. The public addresses resolve to different IPs, from when I initially started working on this project.
* 'Picklelint' function was named since I initially intended on testing corner cases within this function. It'd be more apt to rename as 'Picklemember' or 'Picklerr'.
