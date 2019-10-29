"""
This example illustrates how to update a VM's tags
"""
import os
from datetime import datetime
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_active_directory import ServicePrincipalCredentials

def get_credentials():
  credentials = ServicePrincipalCredentials(
    os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"], tenant=os.environ["TENANT_ID"]
  ) 
  return credentials 

def get_compute_management_client():
  subscription_id = os.environ["SUBSCRIPTION_ID"]
  credentials = get_credentials()
  return ComputeManagementClient(credentials, subscription_id)

def get_vm_details(compute_client, vm_resource_group, vm_name):
  vm = compute_client.virtual_machines.get(
    vm_resource_group,
    vm_name
  )
  return vm

def update_vm(compute_client, resource_group, name, tags, location):
  async_vm_update = compute_client.virtual_machines.update(
    resource_group,
    name,
    {
      'location': location,
      'tags': tags
    }
  )

def add_ansible_tags(vm):
  epochTime = int(datetime.now().timestamp())
  tags = vm.tags
  vm.tags['ansible-complete']=1
  vm.tags['ansible-complete-time']=epochTime
  return tags

def remove_tag_if_exists(tags, tag_to_remove):
  tags.pop(tag_to_remove,None)
  return tags

def main():
  compute_client = get_compute_management_client()  
  vm_resource_group =os.environ["VM_RESOURCE_GROUP"]
  vm_name = "hattantest400"
  
  vm = get_vm_details(compute_client, vm_resource_group, vm_name)
  tags = add_ansible_tags(vm)
  
  update_vm(compute_client, vm_resource_group, vm_name, tags, vm.location)

if __name__ == "__main__":
  main()

