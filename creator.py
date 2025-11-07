#!/usr/bin/env python3
import os

def write_file(path, content):
    """Create file and write content to it"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

def create_ansible_project(project_name):
    print(f"📁 Creating Ansible project: {project_name}")
    base = os.path.abspath(project_name)

    # Directory structure
    dirs = [
        "inventories/dev",
        "inventories/stage",
        "inventories/prod",
        "group_vars",
        "host_vars",
        "playbooks",
        "roles/common/tasks",
        "roles/common/handlers",
        "roles/common/vars",
        "roles/common/defaults",
        "roles/common/templates",
        "roles/common/meta",
        "roles/webserver/tasks",
        "roles/webserver/handlers",
        "roles/webserver/templates",
        "roles/webserver/meta"
    ]
    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    # ────────────────────────────────────────────────
    # Inventories
    inventory_content = """[webservers]
# web1 ansible_host=10.0.0.1

[dbservers]
# db1 ansible_host=10.0.0.2
"""
    for env in ["dev", "stage", "prod"]:
        write_file(f"{base}/inventories/{env}/hosts.ini", inventory_content)

    # ────────────────────────────────────────────────
    # group_vars & host_vars
    write_file(f"{base}/group_vars/all.yml", """---
ansible_user: ubuntu
ansible_become: true
package_state: present
""")

    write_file(f"{base}/host_vars/sample_host.yml", """---
example_var: value
""")

    # ────────────────────────────────────────────────
    # Playbook
    write_file(f"{base}/playbooks/site.yml", """---
- name: Apply common configuration
  hosts: all
  become: true
  roles:
    - role: common
    - role: webserver
""")

    # ────────────────────────────────────────────────
    # Common role
    write_file(f"{base}/roles/common/tasks/main.yml", """---
- name: Ensure basic packages are installed
  ansible.builtin.package:
    name: "{{ item }}"
    state: "{{ package_state }}"
  loop:
    - vim
    - curl
    - git
""")

    write_file(f"{base}/roles/common/handlers/main.yml", """---
- name: Restart SSH
  ansible.builtin.service:
    name: ssh
    state: restarted
""")

    write_file(f"{base}/roles/common/defaults/main.yml", """---
timezone: UTC
""")

    write_file(f"{base}/roles/common/vars/main.yml", """---
motd_message: "Welcome to your server"
""")

    write_file(f"{base}/roles/common/templates/motd.j2", """{{ motd_message }}
Managed by Ansible.
""")

    write_file(f"{base}/roles/common/meta/main.yml", """---
galaxy_info:
  author: you
  description: Common setup role
  license: MIT
  min_ansible_version: 2.10
dependencies: []
""")

    # ────────────────────────────────────────────────
    # Webserver role
    write_file(f"{base}/roles/webserver/tasks/main.yml", """---
- name: Install Nginx
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy Nginx config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx
""")

    write_file(f"{base}/roles/webserver/handlers/main.yml", """---
- name: Restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
""")

    write_file(f"{base}/roles/webserver/templates/nginx.conf.j2", """user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
  worker_connections 768;
}

http {
  server {
    listen 80;
    location / {
      return 200 'Hello from Ansible!';
    }
  }
}
""")

    write_file(f"{base}/roles/webserver/meta/main.yml", """---
galaxy_info:
  author: you
  description: Simple nginx webserver
  license: MIT
  min_ansible_version: 2.10
dependencies:
  - role: common
""")

    # ────────────────────────────────────────────────
    # ansible.cfg
    write_file(f"{base}/ansible.cfg", """[defaults]
inventory = inventories/dev/hosts.ini
roles_path = roles
host_key_checking = False
retry_files_enabled = False
""")

    # README
    write_file(f"{base}/README.md", f"""# {project_name}

Standardized Ansible project generated automatically.

## Structure
- playbooks/: entry point playbooks
- roles/: reusable role logic (common, webserver)
- inventories/: environment-specific hosts
- group_vars & host_vars/: variable definitions
""")

    print(f"✅ Project '{project_name}' created successfully at {base}")

# ────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 create_ansible_project.py <project_name>")
        sys.exit(1)
    create_ansible_project(sys.argv[1])




