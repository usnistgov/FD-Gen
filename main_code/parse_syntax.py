import re
import numpy as np

"Part 1: General syntax algorithm."
# break the script
def break_script(script):
    output_namelist_lines=[]
    for line,num in zip(script,range(len(script))):
        line=line.decode('UTF-8').strip()
        pattern = r'^&(\w+)\s*(.*)'
        match = re.match(pattern, line)
        if match:
            if len(match.group(1)) != 4:
                raise ValueError(f"Invalid syntax found.")
            else:
                output_namelist_lines.append(num)
    
    # output grouped lines
    valid_line_grouped_list = []
    for index in range(1,len(output_namelist_lines)):
        valid_line_grouped_list.append(list(range(output_namelist_lines[index-1], output_namelist_lines[index])))
    valid_line_grouped_list.append(list(range(output_namelist_lines[-1], len(script))))
    
    # output valid script
    valid_script=[]
    for grouped_lines in valid_line_grouped_list:
        lines=[script[i].decode('UTF-8').strip() for i in grouped_lines]
        temp_script='\n'.join(lines)
        temp_script = temp_script.replace("\n", ", ").strip()
        valid_script.append(temp_script)
    
    return valid_line_grouped_list, valid_script


# parse the valid script lines
def parse_script_lines(line):
    # parse custom syntax using regular expressions
    pattern1 = r'^&(\w+)\s*(.*)'
    match1 = re.match(pattern1, line)
    pattern2 = r'^\s(\s{4})'
    match2 = re.match(pattern2, line)
    
    if match1:
        function_name = match1.group(1)
        params_str = strip_terminator(match1.group(2))
        params = parse_params(params_str)
        # modify
        if 'ID' in params: 
            if isinstance(params['ID'], list):
                params['ID'] =''.join(params['ID'])
        if 'FYI' in params: 
            if isinstance(params['FYI'], list):
                params['FYI'] =''.join(params['FYI'])
        return function_name, params
    
    elif match2:
        function_name = '    '
        params_str = strip_terminator(line[5:])
        params = parse_params(params_str)
        # modify
        if 'ID' in params: 
            if isinstance(params['ID'], list):
                params['ID'] =''.join(params['ID'])
        if 'FYI' in params: 
            if isinstance(params['FYI'], list):
                params['FYI'] =''.join(params['FYI'])
        return function_name, params
    
    else:
        raise ValueError("Invalid script line format")


# text inside '...' blanked out with the same length, so commas, '/', '=' and argument names
# in quoted text are not read as syntax; positions in the masked text match the original.
def mask_quotes(text):
    return re.sub(r"'[^']*'", lambda match: "'" + '\x00' * (len(match.group(0)) - 2) + "'", text)

# drop the closing '/' of a namelist line and what follows it ('/' inside quotes is kept)
def strip_terminator(params_str):
    index = mask_quotes(params_str).find('/')
    return params_str if index == -1 else params_str[:index]

# position of argument ARG_NAME= in a line, ignoring quoted text and longer names ending in ARG_NAME
def find_arg(line, arg_name):
    masked = mask_quotes(line)
    match = re.search(r'(?<![\w(])' + re.escape(arg_name) + r'\s*=', masked)
    return match.start() if match else masked.find(arg_name)

def parse_params(params_str):
    # Parse parameter pair strings -- key-value pairs
    params = {}
    # remove spaces around '=' outside quotes
    pieces, last = [], 0
    for match in re.finditer(r'\s*=\s*', mask_quotes(params_str)):
        pieces += [params_str[last:match.start()], '=']
        last = match.end()
    params_str = ''.join(pieces) + params_str[last:]
    masked = mask_quotes(params_str)
    for part_match in re.finditer(r'\b[\w():,]+=.*?(?=\s*\b[\w():,]+=|\s*$)', masked):
        start, end = part_match.span()
        equal_index = masked.index('=', start)
        key = params_str[start:equal_index].strip()
        string_value = params_str[equal_index+1:end]
        # split values on commas outside quotes
        split_string_value, last = [], 0
        for index, char in enumerate(masked[equal_index+1:end]):
            if char == ',':
                split_string_value.append(string_value[last:index])
                last = index + 1
        split_string_value.append(string_value[last:])
        # Convert to a list of appropriate types
        mapping = {
            '.FALSE.':'.FALSE.',
            '.TRUE.':'.TRUE.',
            "T":'T',
            "F":'F',
            "None": None,
            "true": True,
            "false": False,
            "True": True,
            "False": False,
            "FALSE": False,
            "TRUE": True
            }
        values=[]
        for value in split_string_value:
            if "'" in value:
                match = re.search(r"'([^']*)'", value)
                if match:
                    value = match.group(1)  # Extracted part
                values.append(value)
            elif value.strip():
                if value in mapping:
                    values.append(mapping[value])
                else:
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                        values.append(value)
                    except ValueError:
                        pass 
        if len(values)==1:
            values=values[0]
        params[key] = values
    
    return params

"Part 2: replace the potential sentence."
# format one value as FDS text (numpy scalars -> plain numbers, float noise trimmed to 12 significant digits)
def format_value(value):
    if isinstance(value, np.floating):
        value = float(str(value))
    elif isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float):
        value = float(f'{value:.12g}')
    return repr(value)

def replace_value(line_content, replaced_args, replaced_after_args, replaced_value):
    # prepare the replaced syntax
    line_content_replaced=line_content
    replaced_value_str=', '.join(format_value(value) for value in replaced_value)+','+' '
    combined_str = replaced_args + '=' + replaced_value_str
    current_length = len(combined_str)
    
    index_start = find_arg(line_content, replaced_args)
    if replaced_after_args is not None:
        index_end = find_arg(line_content, replaced_after_args)
        spaces_to_add=len(line_content_replaced[index_start:index_end])-current_length
        final_str = combined_str + ' ' * spaces_to_add
        line_content_replaced=line_content_replaced[:index_start]+final_str+line_content_replaced[index_end:]
    else:
        index_end = mask_quotes(line_content).find('/')
        if index_end != -1:
            spaces_to_add=len(line_content_replaced[index_start:index_end+1])-current_length
            final_str = combined_str + ' ' * spaces_to_add
            line_content_replaced=line_content_replaced[:index_start]+final_str+line_content_replaced[index_end:]
        else:
            spaces_to_add=len(line_content_replaced[index_start:])-current_length
            final_str = combined_str + ' ' * spaces_to_add
            line_content_replaced=line_content_replaced[:index_start]+final_str
    
    return line_content_replaced
