from sys import stdout as outfile    # added stdout as outfile from sys module


roll_num, name = int(input("Enter roll number :"), input("Enter name :")          # took user input for roll number and name
print("Hello World," + name + "your roll number is" + str(roll_num), sep = ' ', end = '\n', flush = True, file = outfile)
                  # multiline comment
''' print name and roll number on standard output without loading it into buffer '''
