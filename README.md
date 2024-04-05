# ESXi VM Clone Script

## Introduction
This script allows you to clone a virtual machine (VM) on an ESXi host. It lists the available VMs, prompts you to select one for cloning, and then guides you through the cloning process.

## Prerequisites
- Python 3.x
- ESXi host with SSH enabled
- Access to the ESXi datastore where VMs are stored

## Usage
1. Clone or download the script.
2. Modify the `datastore_path` variable in the script to match your ESXi datastore path.
3. Run the script using Python (`python vm-clone.py`) on your local machine or directly on the ESXi server.

## Features
- Interactive command-line interface for selecting VMs and providing clone names.
- Automatic detection of existing VMs in the datastore to prevent name conflicts.
- Step-by-step guidance through the cloning process.
- Error handling and rollback in case of cloning failures.

## License
This script is provided under the [MIT License](LICENSE).
