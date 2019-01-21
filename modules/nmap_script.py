import nmap


def run_scan(target, arguments):
    nm = nmap.PortScanner()
    scaninfo = nm.scan(hosts=target, arguments=arguments)
    return scaninfo['scan']
