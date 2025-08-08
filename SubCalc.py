# Import the sys module to access command-line arguments
import sys

# Function to convert an IP address string to a 32-bit integer
def ip_to_int(ip):
    # Split the IP string into individual octets
    octets = ip.split('.')
    # Combine octets into a single 32-bit integer using bit shifting
    return (int(octets[0]) << 24) | (int(octets[1]) << 16) | (int(octets[2]) << 8) | int(octets[3])

# Function to convert a 32-bit integer back to dotted-decimal IP format
def int_to_ip(ip_int):
    # Extract each octet using bit masking and shifting
    return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"

# Function to convert CIDR notation to subnet mask integer
def cidr_to_mask(cidr):
    # Create mask by shifting 1s to the left and applying 32-bit mask
    return (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF

# Function to determine IP address class
def get_ip_class(ip_int):
    # Extract the first octet
    first_octet = (ip_int >> 24) & 0xFF
    
    # Class A: 1-126
    if 1 <= first_octet <= 126:
        return 'A'
    # Class B: 128-191
    elif 128 <= first_octet <= 191:
        return 'B'
    # Class C: 192-223
    elif 192 <= first_octet <= 223:
        return 'C'
    # Class D (Multicast): 224-239
    elif 224 <= first_octet <= 239:
        return 'D'
    # Class E (Reserved): 240-255
    elif 240 <= first_octet <= 255:
        return 'E'
    # Special cases (0, 127, etc.)
    else:
        return 'Special'

# Function to calculate subnet properties
def calculate_subnet(ip_int, mask_int):
    # Network address is IP AND mask
    network = ip_int & mask_int
    # Broadcast address is network OR inverted mask
    broadcast = network | (0xFFFFFFFF ^ mask_int)
    return network, broadcast

# Main function to handle program execution
def main():
    # Check for CIDR format input (single argument with '/')
    if len(sys.argv) == 2 and '/' in sys.argv[1]:
        # Split input into IP and CIDR parts
        ip_str, cidr_str = sys.argv[1].split('/')
        cidr = int(cidr_str)
        mask_int = cidr_to_mask(cidr)
    # Check for IP + subnet mask format
    elif len(sys.argv) == 3:
        ip_str = sys.argv[1]
        mask_str = sys.argv[2]
        mask_int = ip_to_int(mask_str)
        # Validate subnet mask pattern
        mask_bin = bin(mask_int)[2:].zfill(32)
        if '01' in mask_bin:
            print("Error: Invalid subnet mask (non-contiguous 1s)")
            return
    # Handle invalid input formats
    else:
        print("Usage:")
        print("  CIDR: python subnet_calculator.py <IP/CIDR>")
        print("  Mask: python subnet_calculator.py <IP> <SUBNET_MASK>")
        print("\nExamples:")
        print("  python subnet_calculator.py 192.168.1.100/26")
        print("  python subnet_calculator.py 10.0.0.5 255.255.255.0")
        return

    try:
        # Convert IP string to integer
        ip_int = ip_to_int(ip_str)
    except Exception as e:
        print(f"Invalid IP address: {e}")
        return

    # Detect IP class
    ip_class = get_ip_class(ip_int)
    
    # Calculate network and broadcast addresses
    network, broadcast = calculate_subnet(ip_int, mask_int)
    
    # Count number of 1s in mask for CIDR notation
    cidr = bin(mask_int).count('1')
    
    # Handle special cases for small subnets
    if cidr == 32:  # Single host subnet
        first_host = network
        last_host = network
        hosts = 1
    elif cidr == 31:  # Point-to-point link (RFC 3021)
        first_host = network
        last_host = broadcast
        hosts = 2
    else:  # Standard subnets
        first_host = network + 1
        last_host = broadcast - 1
        hosts = last_host - first_host + 1

    # Display results
    print(f"\nIP Address Class:   {ip_class}")
    print(f"CIDR Notation:      /{cidr}")
    print(f"Subnet Mask:        {int_to_ip(mask_int)}")
    print(f"Network Address:    {int_to_ip(network)}")
    print(f"Broadcast Address:  {int_to_ip(broadcast)}")
    print(f"First Usable Host:  {int_to_ip(first_host)}")
    print(f"Last Usable Host:   {int_to_ip(last_host)}")
    print(f"Usable Hosts:       {hosts}")

# Execute main function when script is run directly
if __name__ == "__main__":
    main()