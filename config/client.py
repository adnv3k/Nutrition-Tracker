import subprocess

commands = ["sudo service postgresql start"]
for command in commands:
    process = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
    output, error = process.communicate()