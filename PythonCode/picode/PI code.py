import nmap
import configparser
import re
from tqdm import tqdm

def read_config_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    ip_ranges = config['IP_RANGES']
    exceptions = config['EXCEPTIONS']
    return ip_ranges, exceptions

def discover_hosts(ip_ranges):
    nm = nmap.PortScanner()
    discovered_hosts = {}
    for key, value in tqdm(ip_ranges.items(), desc="Discovering Hosts"):
        nm.scan(hosts=value, arguments='-sn')
        for host in nm.all_hosts():
            discovered_hosts[host] = nm[host]['status']['state']
    return discovered_hosts

def scan_services(discovered_hosts, exceptions, output_file):
    nm = nmap.PortScanner()

    with open(output_file, 'w') as f:
        pbar = tqdm(total=len(discovered_hosts), desc="Scanning Services")

        # Write table headers
        f.write("| IP | Port | Service | Service Version | Vulnerabilities |\n")
        f.write("|----|------|---------|------------------|-----------------|\n")

        for host in discovered_hosts:
            if host not in exceptions:
                f.write(f"### Scanning services on host: {host}\n")
                nm.scan(hosts=host, arguments='-sV --script vuln ')

                if host in nm.all_hosts():
                    for proto in nm[host].all_protocols():
                        for port in nm[host][proto].keys():
                            service_name = nm[host][proto][port]['name']
                            service_version = nm[host][proto][port]['version']
                            vulnerabilities = nm[host]['tcp'][port].get('script', {}).get('vulners', None)
                            cves = re.findall(r'CVE-\d{4}-\d{4,7}', vulnerabilities) if vulnerabilities else []

                            # Start of the service row in the table
                            f.write(f"| {host} | {port} | {service_name} | {service_version} | ")

                            # Write vulnerabilities if found, else write None
                            if cves:
                                f.write(', '.join(cves))
                            else:
                                f.write("None")

                            f.write(" |\n")

            pbar.update(1)

    print("\033[92mScan completed!\033[0m")

if __name__ == "__main__":
    config_file_path = "config.conf"
    output_file = "scan_results.md"
    ip_ranges, exceptions = read_config_file(config_file_path)
    discovered_hosts = discover_hosts(ip_ranges)
    scan_services(discovered_hosts, exceptions, output_file)
