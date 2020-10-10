# Orka-Ansible-Inventory-Creator

A simple script to generate an Ansible inventory for Orka VMs. 

## Usage

1. Install and set up the Orka CLI.
1. Run `create_ansible_inventory.py path/to/output_dir`

## Examples

Create an unsorted inventory of all VMs associated with CLI user.
`python3 create_ansible_inventory.py ~/MacStadium/ansible_dir`

Create an inventory in which VMs are sorted by name. 
`python3 create_ansible_inventory.py ~/MacStadium/ansible_dir --sort-key virtual_machine_name`

## Available `sort_key` Values

owner,virtual_machine_name,virtual_machine_id,node_location,node_status,virtual_machine_ip,vnc_port,screen_sharing_port,ssh_port,cpu,vcpu,RAM,base_image,image,configuration_template,vm_status 