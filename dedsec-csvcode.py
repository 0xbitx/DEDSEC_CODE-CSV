#coder: 0xbit
import os, sys, textwrap, csv, binascii

green_dot = '\033[92m●\033[0m'
green_q = '\033[92m?\033[0m'
red_dot = '\033[91m●\033[0m'

os.system('clear')

def banner():
    banner = '''
    
        \033[92m   ⣀⣀⣤⣤⣤⣶⣶⣿⣿⣿\033[0m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        \033[92m⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[0m⠀⠀
        \033[92m⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[0m⠀⠀
        \033[92m⢸⣿⣿⣏⠉⠙⣿⣿⠉⠉⣿⣿⣿\033[0m⠀
        \033[92m⢸⣿⣿⣿⣆⠀⠸⠃⢀⣾⣿⣿⣿\033[0m⠀⠀\033[92mDEDSEC CODE TO CSV GENERATOR\033[0m
        \033[92m⢸⣿⣿⣿⣿⠆⠀⠀⢾⣿⣿⣿⣿\033[0m⠀⠀hide payload inside csv file
        \033[92m⢸⣿⣿⣿⠏⠀⣰⡄⠀⢿⣿⣿⣿\033[0m⠀⠀
        \033[92m⢸⣿⣿⣃⣀⣰⣿⣷⣀⣀⣻⣿⣿\033[0m⠀⠀
        \033[92m⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[0m⠀
        \033[92m⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[0m⠀⠀
        \033[92m⠀⠀⠀⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿\033[0m⠀v.1.0⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Coded: by 0xbit
        
        
          1. INJECT PAYLOAD
          2. EXTRACT PAYLOAD
          3. EXIT'''
    print((banner))
        
all_headers = ['card-id', 
            'door-id', 
            'id-code', 
            'post-id', 
            'card-reader-index', 
            'paytoswipe-id',
            'swipe-index',
            'swipe-addrs-value',
            'cardholder-ssn',
            'cardholder-pan',
            'cardholder-zip',
            'cardholder-idhex',]

class main_code:
    @staticmethod
    def injectcsv(custom_csv, payload_code):
        try:
            with open(custom_csv, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                headers = next(reader) 
                rows = list(reader)  
        except FileNotFoundError:
            sys.exit(f"\n\t [{red_dot}] Custom CSV file not found.\n")

        try:
            with open(payload_code, 'r') as py_file:
                python_code = py_file.read()
        except FileNotFoundError:
            sys.exit(f"\n\t [{red_dot}] Payload file not found.\n")

        hex_code = python_code.encode('utf-8').hex()
        reversed_hex = hex_code[::-1]
        obfuscated_hex = ''.join(f'{int(reversed_hex[i:i+2], 16) ^ 0x5A:02x}' for i in range(0, len(reversed_hex), 2))
        hex_chunks = textwrap.wrap(obfuscated_hex, 5)

        for header in all_headers[1:]:
            if header not in headers:
                headers.append(header)

        num_headers = len(all_headers)
        num_rows = len(rows)
        hex_columns = {header: [] for header in all_headers}

        for idx, chunk in enumerate(hex_chunks):
            header_idx = idx // num_rows  
            row_idx = idx % num_rows      
            if header_idx < num_headers:
                header = all_headers[header_idx]
                hex_columns[header].append((row_idx, chunk))
            else:
                sys.exit(f"\n\t [{red_dot}] Not enough headers to store all hex chunks.\n")
                
        for header, chunks in hex_columns.items():
            for row_idx, chunk in chunks:
                if row_idx < num_rows:
                    rows[row_idx].append(chunk)
                else:
                    sys.exit(f"\n\t [{red_dot}] Row index {row_idx} out of range for header {header}.\n")

        for row in rows:
            while len(row) < len(headers):
                row.append('')
        try:
            file_name = os.path.splitext(os.path.basename(payload_code))[0]
            with open(f'{file_name}.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(headers)  
                writer.writerows(rows)
        except Exception as e:
            sys.exit(f"\n\t [{red_dot}] Error writing to output CSV.\n")
        
        print(f"\n\t [{green_dot}] Code injected to csv file: saved to '{file_name}.csv'.\n")
        
    def extract_code(self, csv_file_path):
        hex_chunks = []
        try:
            with open(csv_file_path, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                headers_in_file = reader.fieldnames
                present_headers = [header for header in all_headers if header in headers_in_file]
                for header in all_headers:
                    if header in present_headers:
                        for row in reader:
                            chunk = row.get(header, "").strip()
                            if chunk:
                                hex_chunks.append(chunk)
                        csv_file.seek(0)
                        next(reader)
                        
        except FileNotFoundError:
            sys.exit(f"\t [{red_dot}] CSV file not found.")
        
        hex_string = ''.join(hex_chunks)
        reversed_hex = ''.join(f'{int(hex_string[i:i+2], 16) ^ 0x5A:02x}' for i in range(0, len(hex_string), 2))
        hex_string = reversed_hex[::-1]
        decoded_code = binascii.unhexlify(hex_string).decode('utf-8')
        
        file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        with open(file_name, 'w') as writer:
            writer.write(decoded_code)
            
        print(f"\n\t [{green_dot}] Code extracted and saved to '{file_name}.'.\n")

def main_builder():
    try:
        select = input(f'\n\t [{green_q}] DEDSEC: ').strip()
        maincode = main_code()
        
        if select == '1':
            custom_file = input(f"\n\t [{green_q}] Custom CSV file: ")
            payload_file = input(f'\t [{green_q}] Payload file: ')
            maincode.injectcsv(custom_file, payload_file)
            
        elif select == '2':
            payload_csv = input(f'\n\t [{green_q}] Payload CSV file: ')
            maincode.extract_code(payload_csv)
        else:
            os.system('clear')
            sys.exit(f"\n\t [{red_dot}] Exiting.\n")
    except KeyboardInterrupt:
        sys.exit(f"\n\n\t [{red_dot}] Operation cancelled by user.\n")

if __name__ == "__main__":
    banner()
    main_builder()
    
