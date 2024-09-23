def parse_adif(adif_file_path):
    """Parse ADIF file and return a list of QSO dictionaries."""
    qsos = []
    qso_data = {}
    
    with open(adif_file_path, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        line = line.strip()  # Remove any leading/trailing whitespace
        
        # Debugging: print each line as it's being processed
        print(f"Processing line {i + 1}: {line}")
        
        if not line:  # Skip empty lines
            print(f"Skipping empty line {i + 1}")
            continue
        
        if line.upper() == "<EOH>":  # Skip the end of header marker
            print(f"Skipping EOH at line {i + 1}")
            continue
        
        if line.upper() == "<EOR>":  # End of QSO record
            if qso_data:  # Only append if there's valid data
                qsos.append(qso_data)
                print(f"QSO added: {qso_data}")
            else:
                print(f"No valid QSO data found at line {i + 1}, skipping...")
            qso_data = {}  # Reset for next QSO
            continue
        
        # Process fields within the line
        while '<' in line and '>' in line:
            field_start = line.find('<')
            field_end = line.find('>')
            
            # Ensure the tag contains a valid structure (e.g., "<CALL:6>")
            tag_content = line[field_start + 1:field_end]
            if ':' not in tag_content:
                print(f"Invalid tag structure: {tag_content}, skipping line {i + 1}")
                break
            
            field_info = tag_content.split(':')
            field_name = field_info[0].lower()

            # Ensure the field has a length part and is an integer
            try:
                field_length = int(field_info[1])
            except (IndexError, ValueError):
                print(f"Error parsing field length for {field_name} at line {i + 1}, skipping...")
                break

            field_value = line[field_end + 1:field_end + 1 + field_length].strip()
            
            # Map 'call' to 'callsign'
            if field_name == 'call':
                field_name = 'callsign'
                
            qso_data[field_name] = field_value.strip()
            line = line[field_end + 1 + field_length:]

    print(f"Total QSOs parsed: {len(qsos)}")
    return qsos
