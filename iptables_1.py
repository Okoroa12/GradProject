import subprocess

# Function to execute iptables command
def execute_iptables_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e}")

# List of iptables rules
iptables_rules = [
    # 1: Drop invalid packets
    "/sbin/iptables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP",

    # 2: Drop TCP packets that are new and are not SYN
    "/sbin/iptables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP",

    # 3: Drop SYN packets with suspicious MSS value
    "/sbin/iptables -t mangle -A PREROUTING -p tcp -m conntrack --ctstate NEW -m tcpmss ! --mss 536:65535 -j DROP",

    # 4: Block packets with bogus TCP flags
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN,RST,PSH,ACK,URG NONE -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN FIN,SYN -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,RST SYN,RST -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,RST FIN,RST -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,ACK FIN -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,URG URG -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,FIN FIN -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,PSH PSH -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL ALL -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL NONE -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL FIN,PSH,URG -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL SYN,FIN,PSH,URG -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP",

    # 5: Block spoofed packets
    "/sbin/iptables -t mangle -A PREROUTING -s 224.0.0.0/3 -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -s 169.254.0.0/16 -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -s 192.0.2.0/24 -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -s 0.0.0.0/8 -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -s 240.0.0.0/5 -j DROP",
    "/sbin/iptables -t mangle -A PREROUTING -s 127.0.0.0/8 ! -i lo -j DROP",

    # 6: Drop ICMP
    "/sbin/iptables -t mangle -A PREROUTING -p icmp -j DROP",

    # 7: Drop fragments in all chains
    "/sbin/iptables -t mangle -A PREROUTING -f -j DROP",

    # 8: Limit connections per source IP
    "/sbin/iptables -A INPUT -p tcp -m connlimit --connlimit-above 111 -j REJECT --reject-with tcp-reset",

    # 9: Limit new TCP connections per second per source IP
    "/sbin/iptables -A INPUT -p tcp -m conntrack --ctstate NEW -m limit --limit 60/s --limit-burst 20 -j ACCEPT",
    "/sbin/iptables -A INPUT -p tcp -m conntrack --ctstate NEW -j DROP",

    # 10: Protection against port scanning
    "/sbin/iptables -N port-scanning",
    "/sbin/iptables -A port-scanning -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s --limit-burst 2 -j RETURN",
    "/sbin/iptables -A port-scanning -j DROP",
]

# Execute each iptables rule
for rule in iptables_rules:
    execute_iptables_command(rule)
