#
# AF
# **
#
# Created by Kevin Thomas 09/09/20
# Modified by Kevin Thomas 09/09/20
# 
# Copyright: (c) 2020, Kevin Thomas <kevin@mytechnotalent.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# An open-source Automation Framework.
# 
# required modules
# pip install ansible
# pip install selenium
#
# Version 0.0.1 Alpha
#


import os
import subprocess

# Run tests
#cmd = 'venv/bin/ansible-playbook -i hosts roles/tests/main.yml'
cmd = 'venv/bin/ansible-playbook -i hosts roles/tests/main.yml --step'
subprocess.run(cmd, shell=True)
