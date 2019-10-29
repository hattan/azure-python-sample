"""
This example illustrates how to update a VM's tags
"""
import os
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_active_directory import ServicePrincipalCredentials

def get_compute_management_client():
  credentials = ServicePrincipalCredentials("<CLIENT_ID>", "<CLIENT_SECRET>", "<TENANT_ID>") 
  return ComputeManagementClient(credentials, "<SUBSCRIPTION_ID_ID>")

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

def add_tags(vm):
  tags = vm.tags
  vm.tags['tag1']=1234
  vm.tags['foo']="bar"
  return tags

def remove_tag_if_exists(tags, tag_to_remove):
  tags.pop(tag_to_remove,None)
  return tags

def main():
  compute_client = get_compute_management_client()  
  resource_group = "<RESOURCE_GROUP_NAME>"
  vm_name = "<VM_NAME_HERE>"
  
  vm = get_vm_details(compute_client, resource_group, vm_name)
  tags = add_tags(vm)
  
  update_vm(compute_client, resource_group, vm_name, tags, vm.location)

if __name__ == "__main__":
  main()

