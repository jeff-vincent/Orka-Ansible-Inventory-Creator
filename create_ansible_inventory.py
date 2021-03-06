import argparse
import ast
import os
import subprocess


class OrkaAnsibleInventory:

    def __init__(self, output_dir):
        self.vm_data = None
        self.sorted_data = None
        self.output_dir = output_dir
        self.inventory_header = ('[all:vars]\nanisble_connection=ssh\n'
                                'ansible_ssh_user=<ssh user>\n'
                                'ansible_ssh_pass=<ssh password>\n\n'
                                '[hosts]\n')


    def get_current_vm_data(self):
        """Get current VM data related to the current CLI user.

        Note
        ----

        The user must be logged in to the Orka CLI.
        """
        completed_process = subprocess.run(
            ['orka', 'vm', 'list', '--json'], 
            capture_output=True)
        dict_string = completed_process.stdout.decode('utf-8')
        data = ast.literal_eval(dict_string)
        self.vm_data = data['virtual_machine_resources']


    def sort_vm_data(self, sort_key):
        """Sort current VM data related to the current CLI user.
        
        Parameters
        ----------
        
        sort_key: str
            One of the `sort_key` values listed in the README.
            
        Note
        ----
        
        `sort_key` is passed as a command line arg with the flag
        `--sort-key`. See README for example usage.
        """
        self.sorted_data = sorted(
            self.vm_data, key = lambda vm: vm['status'][0][sort_key])


    def write_inventory(self, data):
        """Write current VM data -- sorted or not -- to an 
        Ansible inventory file.
        
        Parameters
        ----------
        
        data: list
            A list of Python dicts that represent Orka VMs.
        """
        inventory_path = os.path.join(self.output_dir, 'inventory')
        with open(inventory_path, 'w+') as f:
            f.write(self.inventory_header)
            for vm in data:
                line = '{}   ansible_ssh_port={}   ansible_ssh_host={}'.format(
                    vm['virtual_machine_name'],
                    vm['status'][0]['ssh_port'],
                    vm['status'][0]['virtual_machine_ip'])
                f.write(line + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', 
        help='The path to the directory \
        where the inventory file will be written.')
    parser.add_argument('--sort-key', action='store', 
        dest='sort_key', help='Optional. The key in the VM \
        dict by which to sort the VMs.')
    args = parser.parse_args()
    inventory_creator = OrkaAnsibleInventory(args.output_dir)
    inventory_creator.get_current_vm_data()
    if args.sort_key:
        inventory_creator.sort_vm_data(args.sort_key)
        inventory_creator.write_inventory(
            inventory_creator.sorted_data)
    else:
        inventory_creator.write_inventory(
            inventory_creator.vm_data)
