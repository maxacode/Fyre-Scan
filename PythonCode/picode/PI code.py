# Import necessary libraries
import nmap  # Import nmap library for network exploration
import configparser  # Import configparser for parsing configuration files
from tqdm import tqdm  # Import tqdm for displaying progress bars

# Function to read IP ranges and exceptions from a configuration file
def read_config_file(file_path):
    config = configparser.ConfigParser()  # Create a configparser object
    config.read(file_path)  # Read the configuration file
    ip_ranges = config['IP_RANGES']  # Get the IP ranges from the configuration
    exceptions = config['EXCEPTIONS']  # Get the exceptions from the configuration
    return ip_ranges, exceptions  # Return the IP ranges and exceptions

# Function to discover hosts in the specified IP ranges
def discover_hosts(ip_ranges):
    nm = nmap.PortScanner()  # Create an nmap PortScanner object

    discovered_hosts = {}  # Initialize an empty dictionary for discovered hosts

    # Discover hosts in each IP range
    for key, value in tqdm(ip_ranges.items(), desc="Discovering Hosts"):  # Iterate through the IP ranges
        nm.scan(hosts=value, arguments='-sn')  # Perform a ping scan for each IP range

        # Add discovered hosts to the dictionary
        for host in nm.all_hosts():  # Iterate through the discovered hosts
            discovered_hosts[host] = nm[host]['status']['state']  # Add the host and its status to the dictionary

    return discovered_hosts  # Return the discovered hosts

# Function to scan services on discovered hosts
def scan_services(discovered_hosts, exceptions, output_file):
    nm = nmap.PortScanner()  # Create a new nmap PortScanner object

    with open(output_file, 'w') as f:  # Open the output file for writing
        pbar = tqdm(total=len(discovered_hosts), desc="Scanning Services")  # Create a progress bar

        # Scan services for discovered hosts
        for host in discovered_hosts:  # Iterate through the discovered hosts
            if host not in exceptions:  # Check if the host is not in the exceptions
                f.write(f"### Scanning services on host: {host}\n")  # Write the host header to the output file
                nm.scan(hosts=host, arguments='-A')  # Use aggressive scan mode to scan the host

                if host in nm.all_hosts():  # Check if the host exists in the scan result
                    for proto in nm[host].all_protocols():  # Iterate through the protocols
                        f.write(f"- Host: {host} Protocol: {proto}\n")  # Write the host and protocol to the output file
                        print(f"- Host: {host} Protocol: {proto}")  # Print the host and protocol

                        ports = nm[host][proto].keys()  # Get the list of ports for the host and protocol
                        for port in ports:  # Iterate through the ports
                            service_name = nm[host][proto][port]['name']  # Get the service name
                            service_version = nm[host][proto][port]['version']  # Get the service version
                            result_line = f"  - Port: {port} \t Service: {service_name} \t Version: {service_version}\n"  # Format the result line
                            f.write(result_line)  # Write the result line to the output file
                            print(result_line.strip())  # Print the result line

                            vulnerabilities = nm[host]['tcp'][port].get('script', {}).get('vulners', None)  # Check if vulnerabilities are found for the port
                            if vulnerabilities:  # If vulnerabilities are found
                                f.write("\t Vulnerabilities:\n")  # Write the vulnerabilities header to the output file
                                for vuln in vulnerabilities:  # Iterate through the vulnerabilities
                                    f.write(f"\t\t {vuln}\n")  # Write the vulnerability to the output file
                                    print(f"\t Vulnerability: {vuln}")  # Print the vulnerability

            pbar.update(1)  # Update the progress bar

        print("\033[92mScan completed!\033[0m")  # Set the color of the console output to green to indicate completion

if __name__ == "__main__":
    config_file_path = "config.conf"  # Change this to your config file path
    output_file = "scan_results.md"   # Change this to your desired output file
    ip_ranges, exceptions = read_config_file(config_file_path)  # Read the IP ranges and exceptions from the config file
    discovered_hosts = discover_hosts(ip_ranges)  # Discover hosts in the specified IP ranges
    scan_services(discovered_hosts, exceptions, output_file)  # Scan services for discovered hosts