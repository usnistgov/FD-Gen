import argparse
import os
import script_engine_main
import sys
from version import VERSION, RELEASE_DATE

# ask a Y/N question; with --yes the answer is Y without asking. 'N' or invalid input ends the program.
def confirm(question, assume_yes):
    if assume_yes:
        print(question + 'Y (--yes)')
        return
    user_input = input(question).strip().lower()
    if user_input == 'y':
        return
    elif user_input == 'n':
        print("Operation aborted.")
        sys.exit()
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")
        sys.exit()

def FDSdata(path, assume_yes=False, sample_only=False):
    script_file = path
    with open(script_file, 'rb') as file:
        user_script = file.readlines()

    "Step 1 basic information."
    print('\n')
    print('**********************************************')
    print(f'* Fire Data Generator (FD-Gen) Version {VERSION} *')
    print(f' release date {RELEASE_DATE} '.center(46, '*'))
    print('**********************************************')
    print('\n')
    project_name = script_engine_main.project_name(user_script)
    if project_name is not None and os.path.exists(os.path.join(os.getcwd(), project_name)):
        confirm(f"Project folder '{project_name}' already exists. Delete it and continue? (Y/N): ", assume_yes)
    print('========================================')
    script_engine_main.execute_MHDR_script(user_script)
    print('========================================\n')

    "Step 2 main program."
    print('\n')
    print('========================================')
    script_engine_main.execute_checking_script(user_script)
    print('========================================\n')
    confirm("Do you want to proceed to the SAMPLING step? (Y/N): ", assume_yes)
    print('\n')
    print('\n')
    parameter_outputs, parameter_sample_generator_outputs=script_engine_main.execute_sampling_script(user_script)
    print('\n')
    if sample_only:
        print("Sampling finished (--sample-only): no FDS case files or plots written.")
        return
    confirm("Do you want to proceed to the WRAPPING step? (Y/N): ", assume_yes)
    print('\n')
    print('\n')
    script_engine_main.execute_wrapping_script(user_script, parameter_outputs)


    "Step 3 Plot the data."
    print('\n')
    print('========================================')
    script_engine_main.execute_plotting_script(user_script, parameter_outputs, parameter_sample_generator_outputs)
    print('========================================\n')


    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='FD-Gen', description='Fire Data Generator: generate multiple FDS case input files from one FD-Gen input file.')
    parser.add_argument('script_file_path', help='FD-Gen input file (.fds)')
    parser.add_argument('-y', '--yes', action='store_true', help='answer Y to all prompts and run every step without asking')
    parser.add_argument('--sample-only', action='store_true', help='stop after the sampling step (no FDS case files or plots)')
    parser.add_argument('--version', action='version', version=f'FD-Gen {VERSION} ({RELEASE_DATE})')
    args = parser.parse_args()

    FDSdata(args.script_file_path, assume_yes=args.yes, sample_only=args.sample_only)
