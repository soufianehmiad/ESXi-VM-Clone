import os

# Clear the command-line interface
os.system('clear')

# ANSI color codes for text formatting
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # Reset to default color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_clone_commands(selected_file_info, new_clone_name):
    """
    Print the commands for cloning the selected VM.

    Args:
        selected_file_info (dict): Information about the selected VM.
        new_clone_name (str): Name for the new clone.
    """
    vmx_file = selected_file_info['file_name'] + ".vmx"
    vmdk_file = selected_file_info['file_name'] + ".vmdk"
    folder_path = selected_file_info['folder_path']
    new_folder_path = "/vmfs/volumes/vms_datastore/" + new_clone_name

    try:
        # Create new folder for the clone
        os.makedirs(new_folder_path, exist_ok=True)

        # Clone the virtual disk
        os.system(f"vmkfstools -i {folder_path}/{vmdk_file} -d thin {new_folder_path}/{new_clone_name}.vmdk")

        # Copy the VMX file
        os.system(f"cp {folder_path}/{vmx_file} {new_folder_path}/{new_clone_name}.vmx")

        # Replace old VM name with new clone name in the VMX file
        os.system(f"sed -i 's/{selected_file_info['file_name']}/{new_clone_name}/g' {new_folder_path}/{new_clone_name}.vmx")

        # Register the new clone
        register_output = os.popen(f"vim-cmd solo/registervm {new_folder_path}/{new_clone_name}.vmx").read()
        vm_id = register_output.splitlines()[-1]  # Extracting the VM ID from the output

        print(f"\n{Color.OKGREEN}Cloning completed successfully.{Color.ENDC}")
        return vm_id.strip()
    except Exception as e:
        print(f"\n{Color.FAIL}An error occurred during cloning. Rolling back...{Color.ENDC}")
        # Remove the newly created folder and files
        if os.path.exists(new_folder_path):
            os.system(f"rm -rf {new_folder_path}")
        print(f"{Color.FAIL}Rollback completed. Error message: {str(e)}{Color.ENDC}")
        return None

def list_vmx_files():
    """
    List all .vmx files with assigned numbers.

    Returns:
        dict: Dictionary containing VM information with assigned numbers.
    """
    vmx_files = {}
    count = 1

    # Loop through each .vmx file and store it in the dictionary
    for root, _, files in os.walk("/vmfs/volumes/vms_datastore/"):
        for file in files:
            if file.endswith(".vmx"):
                file_name = os.path.splitext(file)[0]
                vmx_files[count] = {
                    "file_name": file_name,
                    "folder_path": root
                }
                count += 1

    return vmx_files

# Main script
vm_files = list_vmx_files()

# Calculate the width of the longest VM name
max_name_length = max(len(vm_info["file_name"]) for vm_info in vm_files.values())

# Print the available VMs with numbers
print("\nAvailable VMs:")
for num, file_info in vm_files.items():
    # Format the VM name and folder path with appropriate spacing
    name = file_info['file_name']
    folder_path = file_info['folder_path']
    print(f"{num:2}. {Color.OKBLUE}{name:<{max_name_length + 2}}{Color.ENDC} ({Color.OKGREEN}{folder_path}{Color.ENDC})")

# Get user input for the VM to clone
while True:
    try:
        selected_num = int(input("\nEnter the number of the VM you want to clone: "))
        selected_file_info = vm_files.get(selected_num)
        if selected_file_info:
            break
        else:
            print(f"{Color.FAIL}Invalid input. Please enter a valid VM number.{Color.ENDC}")
    except ValueError:
        print(f"{Color.FAIL}Invalid input. Please enter a valid integer.{Color.ENDC}")

# Get user input for the name of the new clone
while True:
    new_clone_name = input("\nEnter the name for the new clone: ")
    new_folder_path = "/vmfs/volumes/vms_datastore/" + new_clone_name
    if os.path.exists(new_folder_path):
        print(f"{Color.WARNING}Error: The specified folder already exists.{Color.ENDC}")
        choice = input(f"Do you want to choose a different name or exit? (type '{Color.BOLD}name{Color.ENDC}' to choose a different name or '{Color.BOLD}exit{Color.ENDC}' to exit): ")
        if choice.lower() == "exit":
            exit()
    else:
        break

# Confirm details before cloning
print("\nConfirmation:")
print(f"Selected VM: {Color.OKBLUE}{selected_file_info['file_name']}{Color.ENDC}")
print(f"New clone name: {Color.OKBLUE}{new_clone_name}{Color.ENDC}")

# Prompt user for confirmation to proceed with cloning
confirmation = input("\nDo you want to proceed with cloning? (yes/no): ").lower()

# If user confirms, proceed with cloning
if confirmation == "yes":
    print(f"\n{Color.BOLD}Cloning in progress...{Color.ENDC}")
    vm_id = print_clone_commands(selected_file_info, new_clone_name)
    
    # if vm_id:
        # # Prompt user to power on the machine
        # power_on = input("\nDo you want to power on the cloned machine? (yes/no): ").lower()
        # if power_on == "yes":
            # print(f"{Color.BOLD}Powering on the machine...{Color.ENDC}")
            # os.system(f"vim-cmd vmsvc/power.on {vm_id}")
        # else:
            # print(f"{Color.BOLD}The cloned machine is not powered on.{Color.ENDC}")
else:
    print("\nCloning aborted.")
