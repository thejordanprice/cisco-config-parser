import sys
import re
import json

def parse_cisco_config(filename):
    config = {}
    current_interface = None
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if re.match(r'^hostname\s+(.+)$', line):
            match = re.match(r'^hostname\s+(.+)$', line)
            config['hostname'] = match.group(1)
        
        elif re.match(r'^interface\s+(.+)$', line):
            match = re.match(r'^interface\s+(.+)$', line)
            current_interface = match.group(1)
            if 'interfaces' not in config:
                config['interfaces'] = {}
            if current_interface not in config['interfaces']:
                config['interfaces'][current_interface] = {}
        
        elif current_interface:
            match = re.match(r'^\s*(\S+)\s+(.+)$', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                config['interfaces'][current_interface][key] = value

    return config

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parser.py <filename>")
        return
    
    filename = sys.argv[1]
    config = parse_cisco_config(filename)
    json_config = json.dumps(config, indent=2)
    print(json_config)

if __name__ == '__main__':
    main()