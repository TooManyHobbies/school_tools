#!/usr/bin/env python3
import sys, getopt, os, argparse, random, subprocess


# Read CSV file into a list
def read_csv(file_to_read):

    list_built_from_file = []

    # read each line of file in to list
    csv_file = open(file_to_read, "r")

    for line in csv_file:
        list_built_from_file.append(line)

    csv_file.close()

    return(list_built_from_file)

# Popoulate an empty list with items from CSV string. This will take one record 
# which corresponds to a line form the CSV file, and place each field into
# a member of a list. 
def create_list_from_line(line_string):

    line_list = []
    index_number = 0
    value = ""
    inside_quotes = False

    # Build up value a character at a time.  A "," marks the end of the value.
    for i in range(len(line_string)-1):
    
       if line_string[i] == '"':
            inside_quotes = not inside_quotes
    
       if line_string[i] != "," : 
           value = value + line_string[i]
       else:
           if inside_quotes == False:
               line_list.append(value)
               index_number = index_number + 1
               value = ""
           else:
               value = value + line_string[i]

    return(line_list)

def create_list_of_first_names(list_built_from_file):

    # Test generating list of first names.  The first three lines ommitted since
    # aren't records.  The 5th item in the record is the name.
    first_name_list = []

    for i in range (3, len(list_built_from_file) -1):
        
        value_list = []
        value_list = create_list_from_line(list_built_from_file[i])
        full_name = value_list[name_position]
        
        # make a string called last_first, then slice (str[:2] for example.
        # Remove characters from start until space after the comma.
        # End of last name is at the comma.  Find that position
        last_name_end_pos = 0
        while (full_name[last_name_end_pos] != ','):
           last_name_end_pos = last_name_end_pos + 1 
        
        # move forward 2 characters to get rid of the comma and space
        last_name_end_pos = last_name_end_pos + 2
        first_and_middle = full_name[last_name_end_pos:]
        # print (first_and_middle)


        # now trim off any trailing characters or middle initials
        # to do this, start at the end of the string, and work
        # left, looking for a space.
        first_name_end_pos = 0
        for i in range (len(first_and_middle)):
            if (first_and_middle[i] != ' ') and (first_and_middle[i] != '"') :
                first_name_end_pos = first_name_end_pos + 1
            else:
                 break

        first_name = first_and_middle[:first_name_end_pos]
        first_name_list.append(first_name)


    return(first_name_list)




def create_list_of_last_names(list_built_from_file):

    # The name field is formatted as Last, First.  We want First Last. 
    last_name_list = []
    
    for i in range (3, len(list_built_from_file) -1):

        value_list = []
        value_list = create_list_from_line(list_built_from_file[i])
        full_name = value_list[name_position]
        
        # Find the first comma
        last_name_end_pos = 0
        for last_name_end_pos in range (len(full_name) -1):
            if full_name[last_name_end_pos] == ',' :
                break
        # Strip out the leading quotation mark, and first name    
        last_name = full_name[1:last_name_end_pos]
        last_name_list.append(last_name)
        # print (last_name)

    return(last_name_list)

def create_list_gender(list_built_from_file):

    gender_list = []
    for i in range (3, len(list_built_from_file) -1):
        value_list = []
        value_list = create_list_from_line(list_built_from_file[i])
        gender_list.append(value_list[gender_position])

    return(gender_list)


def create_heading(list_built_from_file):
    header_line = 1
    heading_string = ''
    line_list = create_list_from_line(list_built_from_file[header_line])
    days_raw = line_list[8]
    days = days_raw[1:len(days_raw)-1]
    days_formatted = days.replace(",", "&")
    heading_string = line_list[0]+ " Days "+ days_formatted 
    return(heading_string) 

##### Execution Starts Here #####


#Global Variables
name_position = 4
gender_position = 10
list_built_from_file = []




# Argumentsj
#   -f          first name 
#   -l          last name
#   -fl         first name last name
#   -lf         last name, first name
#   -g          print gender
#   -a          alphabetize, cannot use with - r
#   -r          randomize, cannot use with -a

# Parse Arguemnts


parser = argparse.ArgumentParser(description='List student names from CSV file.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', action='store_true', help="first names only")
group.add_argument('-l', action='store_true', help="last names only")
group.add_argument('-fl', action='store_true', help="first last")
group.add_argument('-lf', action='store_true', help="last, first")
parser.add_argument("-g", help="include gender", action="store_true")
parser.add_argument("-c", help="convert xlsx files to csv", action="store_true")
group_sort = parser.add_mutually_exclusive_group()
group_sort.add_argument('-a', action='store_const', dest='sort_type', const='a', help="alphabetize names", default='a')
group_sort.add_argument('-r', action='store_const', dest='sort_type', const='r', help="randomize names")
args = parser.parse_args()

if args.c:
    print("Converting .xlsx files to .csv files")
    directory = os.getcwd()
    for entry in os.scandir(directory):
        if (entry.path.endswith(".xlsx")  and entry.is_file()):
            subprocess.call(['libreoffice', '--headless', '--convert-to','csv', entry.path]) 


if args.f:
    print("first names only")
    output_list = []
    directory = os.getcwd()


    for entry in os.scandir(directory):
        if (entry.path.endswith(".csv")  and entry.is_file()):
            
            print(entry.path)
            output_file_prefix = entry.path
            output_file = output_file_prefix[:len(output_file_prefix)-3] + "txt" 
            text_file = open(output_file, "w")
            list_built_from_file = read_csv(entry.path)
            first_name_list = create_list_of_first_names(list_built_from_file)
            
            if args.g:
                gender_list = create_list_gender(list_built_from_file)
                for i in range (len(first_name_list)):
                    output_list.append(first_name_list[i]+" "+gender_list[i]) 
            else:
                for i in range (len(first_name_list)):
                    output_list.append(first_name_list[i]) 
            
            if args.sort_type == "a":
                output_list.sort() 
            elif args.sort_type == "r":
                random.shuffle(output_list)

            heading =create_heading(list_built_from_file)
            print (heading)
            text_file.write(heading+"\n")
            
            for i in range (len(first_name_list)):
                print(output_list[i])
                text_file.write(output_list[i]+"\n")

            text_file.close()
 
if args.l:
    print("last names only")
    output_list = []
    directory = os.getcwd()

    for entry in os.scandir(directory):
        if (entry.path.endswith(".csv")  and entry.is_file()):
            
            print(entry.path)
            output_file_prefix = entry.path
            output_file = output_file_prefix[:len(output_file_prefix)-3] + "txt" 
            text_file = open(output_file, "w")
            list_built_from_file = read_csv(entry.path)
            last_name_list = create_list_of_last_names(list_built_from_file)
            
            if args.g:
                gender_list = create_list_gender(list_built_from_file)
                for i in range (len(last_name_list)):
                    output_list.append(last_name_list[i]+" "+gender_list[i]) 
            else:
                for i in range (len(last_name_list)):
                    output_list.append(last_name_list[i]) 
            
            if args.sort_type == "a":
                output_list.sort() 
            elif args.sort_type == "r":
                random.shuffle(output_list)
            
            heading =create_heading(list_built_from_file)
            print (heading)
            text_file.write(heading+"\n")
            
            for i in range (len(last_name_list)):
                print(output_list[i])
                text_file.write(output_list[i]+"\n")
     
            text_file.close()
    
if args.fl:
    print("first last")
    output_list = []
    directory = os.getcwd()

    for entry in os.scandir(directory):
        if (entry.path.endswith(".csv")  and entry.is_file()):
            
            print(entry.path)
            output_file_prefix = entry.path
            output_file = output_file_prefix[:len(output_file_prefix)-3] + "txt" 
            text_file = open(output_file, "w")
            list_built_from_file = read_csv(entry.path)
            first_name_list = create_list_of_first_names(list_built_from_file)
            last_name_list = create_list_of_last_names(list_built_from_file)
            
            if args.g:
                gender_list = create_list_gender(list_built_from_file)
                for i in range (len(last_name_list)):
                    output_list.append(first_name_list[i]+" "+last_name_list[i]+" "+gender_list[i]) 
            else:
                for i in range (len(last_name_list)):
                    output_list.append(first_name_list[i]+" "+last_name_list[i]) 

            if args.sort_type == "a":
                output_list.sort() 
            elif args.sort_type == "r":
                random.shuffle(output_list)

            heading =create_heading(list_built_from_file)
            print (heading)
            text_file.write(heading+"\n")
 

            
            for i in range (len(first_name_list)):
                print(output_list[i])
                text_file.write(output_list[i]+"\n")

            text_file.close()
    
if args.lf:
    print("last, first")
    output_list = []
    directory = os.getcwd()

    for entry in os.scandir(directory):
        if (entry.path.endswith(".csv")  and entry.is_file()):
            
            print(entry.path)
            output_file_prefix = entry.path
            output_file = output_file_prefix[:len(output_file_prefix)-3] + "txt" 
            text_file = open(output_file, "w")
            list_built_from_file = read_csv(entry.path)
            first_name_list = create_list_of_first_names(list_built_from_file)
            last_name_list = create_list_of_last_names(list_built_from_file)
            
            if args.g:
                gender_list = create_list_gender(list_built_from_file)
                for i in range (len(last_name_list)):
                    output_list.append(last_name_list[i]+", "+first_name_list[i]+" "+gender_list[i]) 
            else:
                for i in range (len(last_name_list)):
                    output_list.append(last_name_list[i]+", "+first_name_list[i]) 
            
            if args.sort_type == "a":
                output_list.sort() 
            elif args.sort_type == "r":
                random.shuffle(output_list)

            heading =create_heading(list_built_from_file)
            print (heading)
            text_file.write(heading+"\n")
            
            for i in range (len(first_name_list)):
                print(output_list[i])
                text_file.write(output_list[i]+"\n")
   
            text_file.close()

