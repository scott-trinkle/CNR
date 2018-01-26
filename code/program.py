import cnr_tools as cnr


def main_menu():

    # Main menu will refresh until kill = True
    main_kill = False

    print('Welcome to the microCT CNR calculator!\n')

    while main_kill == False:

        # Options for two variable parameters, the rest will be fixed
        print('1 - Energy\n2 - Contrast material\n3 - Contrast thickness\n4 - Contrast density')
        print('5 - Background material\n6 - Background density\n7 - Total thickness')
        print('0 - Exit\n')

        param_input = input(
            'Please enter comma-separated integers corresponding to two parameters to manipulate: ')

        try:
            # splits input into two integers
            var1, var2 = [int(i) for i in param_input.split(',')]
        except ValueError:  # called if input is anything other than two comma-separated integers
            if param_input == '0':
                print('\nGoodbye!')
                return
            else:
                print('\nError - Please type two comma separated integer values.\n')
        else:
            if (var1 < 0 or var1 > 7) or (var2 < 0 or var2 > 7):
                print('\nError - Please choose values from 0-7\n')
            elif var1 == 0 or var2 == 0:
                print('\nGoodbye!')
                return
            elif var1 == var2:
                print('\n Error - Please choose two separate values\n')
            else:
                second_menu(var1, var2)


def second_menu(var1, var2):

    print('\nYou chose to manipulate: {} and {}\n'.format(
        cnr.parameter_string(var1), cnr.parameter_string(var2)))

    var_1_values = cnr.get_param_range(var1)

    return


main_menu()
