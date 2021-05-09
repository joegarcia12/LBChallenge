#!/usr/bin/env python3
import yaml
import os
from os import path
import pickle
#from collections import OrderedDict

class VIP:
    def __init__(self):
        self.config_path='observabilityplatforms.com.yaml'
        self.vip_yaml=yaml.load(open(self.config_path, 'r'))

        #assign values of yaml file to variables
        self.service_name = self.vip_yaml['service']
        self.vip_ip = self.vip_yaml['vip']['ip']
        self.vip_port = self.vip_yaml['vip']['listener_port']
        self.member_dict = self.vip_yaml['vip']['pool']['members']
        self.pool_healthcheck = self.vip_yaml['vip']['pool']['healthcheck']

    def Healthcheck(self):
        self.avail_member_dict = {}
        for k, v in self.member_dict.items():
            self.member_dict[k].append(os.system("nc -vw5 -L 1 {} {} ".format(v[0], v[1])))  # takes 1 min and 15 sec for nc to timeout, not 5 sec as I desired. else this would be set to 5/15
            if self.member_dict[k][2] == 0:         # instantiate new dictionary with only available members
                self.avail_member_dict[k] = v

        if len(self.avail_member_dict) != 0:   # pass traffic to backend pool member if at least one available member
            return self.Picklelint()
        else:
            return self.Errorpage()    # return error page if no available members

    def Picklelint(self):
        self.pickle_filename = '/rr_state.pk'
        self.pickle_cwd = os.getcwd() + self.pickle_filename    # current working directory and filename for last served member

        if path.exists(self.pickle_cwd) == False:          # instantiate pickle file, and write first available member to first line
            with open(self.pickle_cwd, 'wb') as write_pickle:
                self.picklelint_dump = pickle.dump(list(self.avail_member_dict)[0], write_pickle)
                print(self.picklelint_dump)
            return self.picklelint_dump

        else:       # pickle file already instantiated
            self.rr_member = self.Roundrobin()
            return self.rr_member

    def Errorpage(self):
        print("Sorry, no members are available.")

    def Roundrobin(self):
        self.pickle_open = open(self.pickle_cwd, 'wb+')
        self.pickle_data = pickle.load(self.pickle_open)
        self.member_total = len(list(self.member_dict))

        # RR Case 1: return the same member if only 1  is available
        if len(self.avail_member_dict) == 1:
            self.pickle_open.close()
            return list(self.avail_member_dict)[0]

        # RR Case 2: return first available member to complete the 'round-robin' cycle
        elif self.avail_member_dict[self.pickle_data] == list(self.avail_member_dict)[self.member_total - 1]:
            self.pickle_open.close()
            return list(self.avail_member_dict)[0]

        # RR Case 3: return next available member between the first and last available member
        else:
            self.rr_count = 0
            for service_name in list(self.avail_member_dict):
                if service_name == list(self.avail_member_dict)[self.rr_count]:
                    pickle.dump(list(self.avail_member_dict)[self.rr_count + 1], self.pickle_open)
                    self.pickle_open.close()
                    return list(self.avail_member_dict)[self.rr_count]
                self.rr_count += 1

        # return next available member, depending on state of pickle file
       # for i in range(0, self.member_total):
        #    if self.member_dict[self.pickle_readline] == list(self.member_dict)[i]
         #       return list(self.member_dict)[i+1]

if __name__ == "__main__":
    a = VIP()
    print(a.service_name)
    a.Healthcheck()
#a =VIP()
#print(a.vip_ip)
