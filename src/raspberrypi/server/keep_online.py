# -*- coding:utf-8 -*-
import re
import subprocess
import tornado.ioloop


def icache(iterate, n):
    res = []
    for e in iterate:
        res.append(e)
        if len(res) >= n:
            yield res
            res = []
    if len(res) > 0:
        yield res + [None] * (n - len(res))



def get_interface_information():
    m = {}
    split_tab_block_cmd = lambda x: [block.strip() for block in re.split(r"^(\w+)", x, flags=re.M) if block.strip()]
    addr_info = split_tab_block_cmd(subprocess.check_output(["ifconfig"]))
    for interface, info in icache(addr_info, 2):
        ipv4s = re.findall(r"inet\s+(?:addr:)?\s*((?:\d{1,3}\.){3}\d{1,3}).*?(?:Bcast:|broadcast)\s*((?:\d{1,3}\.){3}\d{1,3})", info)
        if len(ipv4s) > 0:
            m[interface] = ipv4s
    return m

def get_route_information():
    res = {}
    try:
        route_info = subprocess.check_output(["ip", "route"]).split("\n")
    except OSError:
        return res
    for line in route_info:
        r_route = re.search("via\s+((?:\d{1,3}\.){3}\d{1,3}).*dev\s+([\w\d]+)", line)
        if r_route:
            ip, dev = r_route.groups()
            if ip in res:
                res[ip]['interface'].append(dev)
            else:
                res[ip]={
                        "default": False,
                        "interface": [dev]
                    }
                if line.startswith("default"):
                    res[ip]['default'] = True
    return res


def icmp_loss_rate(ip, n=5):
    try:
        ping_info = subprocess.check_output(["ping", "-c", str(n), ip])
    except subprocess.CalledProcessError, e:
        ping_info = e.output
    r_ping = re.search(r"\s+(\d{1,3}(?:\.\d+)?)% packet loss", ping_info)
    if r_ping:
        percent, = r_ping.groups()
        return float(percent)
    else:
        raise OSError


def wifi_status():
    try:
        return subprocess.check_output(['wpa_cli', 'status'])
    except OSError:
        print("get wifi status failure")
        return ""

def wifi_reconnect():
    try:
        print subprocess.check_output(['wpa_cli', 'reconnect'])
    except OSError:
        print "reconnect failure"
    try:
        print subprocess.check_output(['wpa_cli', 'reassociate'])
    except OSError:
        print ('reassociate failure')


def check_and_reconnect():
    route_table = {}
    route_table.update(get_route_information())
    for ip, conf in route_table.items():
        if 'wlan0' in conf['interface']:
            rate = icmp_loss_rate(ip)
            if rate > 80:
                wifi_reconnect()


def console_run():
    tornado.ioloop.PeriodicCallback(check_and_reconnect, 1000 * 60).start()
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    console_run()