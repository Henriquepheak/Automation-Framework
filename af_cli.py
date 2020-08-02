import os
import subprocess

# Run tests
#cmd = 'venv/bin/ansible-playbook -i hosts roles/tests/main.yml'
cmd = 'venv/bin/ansible-playbook -i hosts roles/tests/main.yml --step'
subprocess.run(cmd, shell=True)
