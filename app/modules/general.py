import json
import resource
import itertools
import re
import netaddr

added_ip_re = re.compile(r"(?<=\+)(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?=\D)")
added_net_re = re.compile(r"(?<=\+)(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(/([0-9]|[1-2][0-9]|3[0-2])){1}(?=\D)")
ip_re = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
net_re = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(/([0-9]|[1-2][0-9]|3[0-2]))$")
not_periodic_feed_re = re.compile(r"^(?!.*_\d{1,3}d(\.ipset|\.netset)).*(\.ipset|\.netset)$")
uniq_ips_re = re.compile(r"(?<=\ )(\d*)(?= unique IPs)")


def jsonify(data):
    json_data = json.dumps(data, indent=4, sort_keys=True)
    return json_data


def load_cfg(config):
    with open(config) as f:
        data = json.load(f)
        return data


def read_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip("\n")


def limit_memory(maxsize_g):
    maxsize = maxsize_g * 2 ** 30
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, maxsize))


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def normalize_net4(net_raw):
    for ip in netaddr.IPNetwork(net_raw).iter_hosts():
        yield str(ip)


def validate_input_item(input):
    if net_re.match(input) or ip_re.match(input):
        net = input
        if not netaddr.IPNetwork(net).is_private():
            return True
