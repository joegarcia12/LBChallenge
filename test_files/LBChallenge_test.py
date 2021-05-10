#!/usr/bin/env python3
import yaml
import os
from os import path
import pickle
#from collections import OrderedDict

class VIP:
    def __init__(self):
        self.yaml_filename = '/observabilityplatforms.com.yaml'
        self.config_path= os.getcwd() + self.yaml_filename
        self.vip_yaml=yaml.load(open(self.config_path, 'r'), Loader=yaml.FullLoader)

        #assign values of yaml file to variables
        self.service_name = self.vip_yaml['service']
        self.vip_ip = self.vip_yaml['vip']['ip']
        self.vip_port = self.vip_yaml['vip']['listener_port']
        self.member_dict = self.vip_yaml['vip']['pool']['members']
        self.pool_healthcheck = self.vip_yaml['vip']['pool']['healthcheck']

    def Healthcheck(self):
        self.avail_member_dict = {}
        for k, v in self.member_dict.items():
            self.member_dict[k].append(os.system("nc -vw2 -G2 -L 1 {} {} ".format(v[0], v[1])))  # 2 sec timeout to speed up execution times
            if self.member_dict[k][2] == 0:         # instantiate new dictionary with only available members
                self.avail_member_dict[k] = v

        self.avail_member_total = len(list(self.avail_member_dict))
        if self.avail_member_total != 0:   # pass traffic to backend pool member if at least one available member
            return self.Picklelint()
        else:
            print("Errorpage call, avail_member_total: {}".format(self.avail_member_total))
            return self.Errorpage()    # return error page if no available members

    def Picklelint(self):
        self.pickle_filename = '/rr_state.pk'
        self.pickle_cwd_file = os.getcwd() + self.pickle_filename    # current working directory and filename for last served member
        self.first_rr_member = list(self.avail_member_dict)[0]

        if path.exists(self.pickle_cwd_file) == False:          # instantiate pickle file, and write first available member to first line
            with open(self.pickle_cwd_file, 'wb+') as write_pickle:
                pickle.dump(self.first_rr_member, write_pickle)
            return self.first_rr_member

        else:       # pickle file already instantiated
            self.rr_member = self.Roundrobin()
            return self.rr_member

    def Errorpage(self):
        self.html_text ='''
        <html>
            <body>
                <h1>{}</h1>
                    <p>There are no members available for this service.</p>
            </body>
        </html>
        '''.format(self.service_name)

        self.html_filename = '/error.html'
        self.html_cwd_file = os.getcwd() + self.html_filename

        self.html_write = open(self.html_cwd_file, "w")    # create error page
        self.html_write.write(self.html_text)
        self.html_write.close()

        self.html_read = open(self.html_cwd_file, "r")    # print error page
        print(self.html_read.read())
        self.html_write.close()

        return "Not Available"

    def Roundrobin(self):
        self.pickle_open = open(self.pickle_cwd_file, 'rb')
        try:
            self.pickle_data = pickle.load(self.pickle_open)

        except EOFError:        # handles the corner case where the 'rr_state.pk' file exists, but is empty
            self.pickle_data = self.first_rr_member
            print("Pickle data within Roundrobin function, type:", self.pickle_data, type(self.pickle_data))
        self.pickle_open.close()


        print("If and elif conditions pre-test, self.pickle_data:", self.pickle_data)
        # RR Case 1: return the same member if only 1 member is available
        if len(self.avail_member_dict) == 1:
            return list(self.avail_member_dict)[0]

        # RR Case 2: return first available member to complete the 'round-robin' cycle
        elif self.pickle_data == list(self.avail_member_dict.keys())[int(self.avail_member_total - 1)]:
            self.pickle_open = open(self.pickle_cwd_file, 'wb')
            pickle.dump(list(self.avail_member_dict)[0], self.pickle_open)
            self.pickle_open.close()
            return list(self.avail_member_dict)[0]

        # RR Case 3: return next available member between the first and last available member
        else:
            print("If and elif conditions failed, self.pickle_data:", self.pickle_data)
            self.rr_count = int(list(self.avail_member_dict).index(self.pickle_data))
            print("rr_count value =", self.rr_count)
            for service_name in list(self.avail_member_dict)[self.rr_count : self.avail_member_total]:        # index slicing from current order in dictionary list, to last available member
                print("service_name loop Service, rr_count:", service_name, self.rr_count)
                if service_name == list(self.avail_member_dict)[self.rr_count]:
                    self.pickle_open = open(self.pickle_cwd_file, 'wb')
                    self.rr_member = list(self.avail_member_dict)[self.rr_count + 1]
                    print('Previous member:', list(self.avail_member_dict)[self.rr_count], 'Served member:', self.rr_member)
                    pickle.dump(self.rr_member, self.pickle_open)
                    self.pickle_open.close()
                    return list(self.avail_member_dict)[self.rr_count + 1]
                self.rr_count += 1

if __name__ == "__main__":
    a = VIP()
    print("Service name:", a.service_name)
    print("Your VIP returned member:", a.Healthcheck())
