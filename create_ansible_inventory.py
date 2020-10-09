import argparse
import ast
import os
import subprocess


class CreateOrkaAnsibleInventory:

    def __init__(self, output_dir):
        self.raw_data = None
        self.output_dir = output_dir

    def get_current_vm_data(self):
        completed_process = subprocess.run(
            ['orka', 'vm', 'list', '--json'], 
            capture_output=True)
        dict_string = completed_process.stdout.decode('utf-8')
        raw_data = ast.literal_eval(dict_string)
        self.raw_data = raw_data

    def write_inventory(self):
        inventory_path = os.path.join(self.output_dir, 'inventory')
        connection_info = ('[all:vars]\nanisble_connection=ssh\n'
                            'ansible_ssh_user=<ssh user>\n'
                            'ansible_ssh_pass=<ssh password>\n\n'
                            '[hosts]\n')
        with open(inventory_path, 'w+') as f:
            f.write(connection_info)
            for vm in self.raw_data['virtual_machine_resources']:
                line = '{}   ansible_ssh_port={}  ansible_ssh_host={}'.format(
                    vm['virtual_machine_name'],
                    vm['status'][0]['ssh_port'],
                    vm['status'][0]['virtual_machine_ip'])
                f.write(line + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', help='The path to the directory \
        where the inventory file will be written.')
    args = parser.parse_args()
    output_dir = args.output_dir
    inventory_creator = CreateOrkaAnsibleInventory(output_dir)
    inventory_creator.get_current_vm_data()
    inventory_creator.write_inventory()



