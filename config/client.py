import subprocess

command = "sudo service postgresql start"
process = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
output, error = process.communicate()