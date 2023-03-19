import json
import subprocess
import sys

from prettytable import PrettyTable
from termcolor import colored

def is_json(line):
    try:
        json.loads(line)
    except ValueError:
        return False
    return True

command = "kubectl get deployments --all-namespaces -o json"
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True).stdout

deployments = json.loads(result)["items"]

table = PrettyTable()
table.field_names = ["Namespace", "Name", "Desired Pods", "Available Pods", "CPU Request", "Memory Request"]

for deployment in deployments:
    namespace = deployment["metadata"]["namespace"]
    name = deployment["metadata"]["name"]
    desired_pods = deployment["spec"].get("replicas", 0)
    available_pods = deployment["status"].get("availableReplicas", 0)
    resources = deployment["spec"]["template"]["spec"]["containers"][0]["resources"]
    cpu_request = resources["requests"].get("cpu", "N/A") if "requests" in resources else "N/A"
    memory_request = resources["requests"].get("memory", "N/A") if "requests" in resources else "N/A"
   
    if desired_pods == available_pods:
        color = "green"
    elif int(available_pods) > 0:
        color = "yellow"
    else:
        color = "red"

    row = [
        colored(namespace, color),
        colored(name, color),
        colored(desired_pods, color),
        colored(available_pods, color),
        colored(cpu_request, color),
        colored(memory_request, color),
    ]
    table.add_row(row)

print(table)

