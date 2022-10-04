import subprocess

commands = ["sudo apt-get -y install postgresql-12",
            "sudo service postgresql-12 initdb",
            "sudo service postgresql-12 start"]
for command in commands:
    process = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
    output, error = process.communicate()