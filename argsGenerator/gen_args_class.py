#!/usr/bin/env python

import sys

input = sys.stdin
output = sys.stdout


def read_line():
    """
    Returns the next line from the input, including the EOL sequence.
    Throws StopIteration on EOF.
    
    Skips comment lines automatically.
    """
    while True:
        line = next(input)
        if line.startswith('#'):
            continue
        return line


def lowercase_first_letter(string):
    return string[0].lower() + string[1:]


output.write("""    /* BEGIN AUTOGENERATED CODE */
    
""")

ignore_duplicates = False
args_already_seen = set()
ignored_machine_names = set()

try:
    while True:
        machine_name = read_line()[:-1]
        if machine_name.startswith('!'):
            # Actually this is a directive. Process it.
            directive = machine_name
            if directive == '!SET ignore_duplicates 1':
                ignore_duplicates = True
            elif directive.startswith('!SUPPRESS '):
                machine_name = directive[len('!SUPPRESS '):]
                ignored_machine_names.add(machine_name)
            else:
                sys.exit("Unknown directive: %s" % directive)
            continue
        java_name = read_line()[:-1]
        type = read_line()[:-1]
        
        description_lines = []
        reading_description = True
        code_lines = None
        while True:
            line = read_line()
            if line.startswith('!CODE'):
                code_lines = []
                reading_description = False
                continue
            if line.startswith('='):
                break
            
            if reading_description:
                description_lines.append(line)
            else:
                code_lines.append(line)
        
        if not java_name[0].isupper():
            sys.exit("Expected first letter to be uppercase: %s" % java_name)
        java_name_lower = lowercase_first_letter(java_name)
        
        # Generate the setter code
        if code_lines is not None:
            # Custom code for this setter
            code = ''.join(code_lines)[:-1];
        else:
            # Standard code for this setter, depending on its parameter type
            code = """        this.put("%s", %s);""" % (machine_name, java_name_lower)
            if '[]' in type or type == 'Date':
                if type == 'String[]-MULTIPLE':
                    type = 'String[]'
                    code = """        this.put("%s", %s);""" % (machine_name, java_name_lower)
                elif type == 'String[]-CSV':
                    type = 'String[]'
                    code = """        StringBuilder csv = new StringBuilder();
        for (int i = 0, n = %s.length; i < n; i++) {
            if (i != 0) {
                csv.append(",");
            }
            csv.append(%s[i]);
        }
        
        this.put("%s", String.valueOf(csv));""" % (java_name_lower, java_name_lower, machine_name)
                else:
                    sys.exit("Don't know how to encode an array of type: %s" % type);
        
        # Split description_lines -> {method_description_lines, param_description_lines}
        method_description_lines = []
        param_description_lines = []
        saw_description_separator = False
        for line in description_lines:
            if line.startswith('-'):
                saw_description_separator = True
                continue
            
            if not saw_description_separator:
                method_description_lines.append(line)
            else:
                param_description_lines.append(line)
        
        if not saw_description_separator:
            print ('WARNING: No separate method description found for ' +
                'argument %s. This is against convention.') % machine_name
            param_description_lines = method_description_lines
            method_description_lines = []
        
        # Format method_description_lines
        method_description_formatted = ''
        if method_description_lines != []:
            for line in method_description_lines:
                method_description_formatted += '     * %s' % line
            method_description_formatted += '     * \n'
        
        # Format param_description_lines
        param_description_formatted = ''
        for line in param_description_lines:
            param_description_formatted += '     *      %s' % line
        
        cur_arg = (machine_name, type)
        if cur_arg in args_already_seen:
            if ignore_duplicates:
                continue
            else:
                sys.exit("Multiple definitions for argument: %s %s" % (
                    type, machine_name));
        else:
            args_already_seen.add(cur_arg)
        
        # Output the current argument
        if machine_name not in ignored_machine_names:
            output.write("""    /**
%s     * @param %s
%s     */
    public void set%s(%s %s) {
%s
    }
    
""" % (method_description_formatted,
       java_name_lower, param_description_formatted,
       java_name, type, java_name_lower,
       code))
    
except StopIteration:
    # Done!
    pass

output.write("""    /* END AUTOGENERATED CODE */
""")