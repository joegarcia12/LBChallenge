# LBChallenge.py Overview
=========================

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

```

### Improvements, given more time:
----------------------------------
* LBChallenge.py returns a 'EOFError: Ran out of input' exception if the 'rr_state.pk' file exists but is empty. The 'else' condition iterates self.rr_count beyond the number of available members.  A try/except code block fixed this, but it doesn't consider the corner case where the pickle byte stream is modified and interrupts the dictionary 'list' calls in Roundrobin().
* There is a "ValueError: 'newrelic.com' is not in list" if, for example, 'splunk.com' is a member defined in the YAML file, removed from the YAML file, and 'splunk.com' is the string stored in the pickled file. Members are hot-swappable, but I recommend deleting the 'rr_state.pk' file to workaround this corner case or any other potential corner cases that could appear.
* No need to waste CPU and Disk I/O when overwriting the existing error.html page, if it already exists.
* The end goal was not to be a fully-featured load balancer, but the VIP address and listener_port are inconsequential for each run. I ended up not needing them in this application, but I left them there to demonstrate how additional properties in the YAML file could be added.
* This script was limited to load balancing HTTPS websites, when we could load balance any service (LDAP, SMTP, mysql, etc). I focused on HTTPS since they are the most prevalent use case for load balancers, and it's easy to determine whether a website is available programmatically and visually. The '503' response in the LBChallenge.md file pushed me in that direction as well.
* Print a more user-friendly output than the standard nc output when a member passes/fails healthcheck.
