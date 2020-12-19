# Orka Ansible Dynamic Inventory Script

## Usage
1. Log in to the Orka CLI
2. Clone the repo
3. Test the script by running: `python3 orka_inventory.py`
It should print JSON output representing your current Orka inventory.
4. Make the file executable by running: `chmod +x orka_inventory.py`
5. Set the environment variables `ANSIBLE_SSH_USER` and `ANSIBLE_SSH_PASS`
6. Test the dynamic inventory by running: `sudo ansible all -i orka_inventory.py -m ping`

## Optional Args
Optional arguments to be passed as environment variables:

`ANSIBLE_NAME_CONTAINS`: a string by which to filter running VMs. 

Example usage:
`export ANSIBLE_NAME_CONTAINS=prod`

Only running VMs with `prod` in the VM name will be added to the inventory.

## Troubleshooting:
If the file appears to run, but produces no output
