# TO DO
# check if snap and flatpak installed - install if not
# check sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo has already been done
# add support for installing .deb files
# add option to install or uninstall

import subprocess
import subprocess
import os
import sys
import subprocess
import logging

def check_arguments(file_name):
    """
    Check script has been called correctly. If not, return syntax for using it and exits.
    """
    if len(sys.argv) < 3:
        print(f"\nUsage: {file_name} [options]\n\
        -i - install applications\n\
        -u - uninstall applications\n\
        -s - (un)install snap packages only\n\
        -f - (un)install flatpack packages only\n\
        -a - (un)install all packages\n\
        -l - list installed applications\n\
        Example: {file_name} -i -s = install snap packages")
        logging.info("No argument provided with '%s'. Exited script", file_name)
        sys.exit()
    else:
        option1 = sys.argv[1]
        option2 = sys.argv[2]
        return (option1, option2)

def check_files_exists(filenames):
    """
    Check source files with apps to be installed exist. If not, exit with relevant error.
    """
    try:
        for file_name in filenames:
            print(f"file_name =",file_name)
            file_exists = os.path.exists(file_name)
            print(f"File '{file_name}' found ok.\n")
    except:
        print(f"File '{filenames}' not found.\n")
        logging.info("File '%s' not found. Exited script", filenames)
        sys.exit()

def check_pkgmgr_installed(pkgmgr_name):
    """
    Check if the required package managers are installed on Ubuntu.

    Args:
        pkgmgr_name (str): The name of the package manager to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    try:
        for pkgname in pkgmgr_name:
            subprocess.run(['dpkg-query', '-l', pkgname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if subprocess:
                print(f"The package manager '{pkgname}' is installed.")
        return True  # If the package is installed, dpkg-query will exit with status 0
    except subprocess.CalledProcessError:
        print(f"The package manager'{pkgname}' is not installed.")
        install_pkgmgr(pkgmgr_name)
        return False  # If the package is not installed, dpkg-query will exit with a non-zero status

def install_pkgmgr(pkg_mgrname):
    """
    Install package manager.

    Args:
        pkg_mgrname (string): the name of the package manager to install
    """
    try:
        for packagemgr in pkg_mgrname:
            if packagemgr == "snap":
                subprocess.run(['sudo', 'snap', 'install', packagemgr], check=True)
            elif packagemgr == "flatpak":
                print(f"Installing package Manager {packagemgr}.\n")
                os.system('flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo')
                subprocess.run(['sudo', 'apt', 'install', pkg_mgrname], check=True)
                print(f"Package {packagemgr} installed successfully.")
    except subprocess.CalledProcessError as e:
            (f"Error: Failed to install package manager {packagemgr}. {e}")

def install_packages(pkg_type, packages):
    """
    Install required packages.

    Args:
        pkg_type (string): defines the package type to install and the command to run
        packages (list): List of package names to install.
    """
    try:
        for package in packages:
            if pkg_type == "snap":
                subprocess.run(['sudo', 'snap', 'install', package], check=True)
            elif pkg_type == "flatpak":
                subprocess.run(['sudo', 'flatpak', 'install', 'flathub','-y', package], check=True)
            print(f"Package {package} installed successfully.")
    except subprocess.CalledProcessError as e:
            (f"Error: Failed to install package {package}. {e}")

def uninstall_packages(pkg_type, packages):
    """
    Uninstall required packages.

    Args:
        pkg_type (string): defines the package type to uninstall and the command to run
        packages (list): List of package names to install.
    """
    try:
        for package in packages:
            if pkg_type == "snap":
                subprocess.run(['sudo', 'snap', 'install', package], check=True)
            elif pkg_type == "flatpak":
                subprocess.run(['sudo', 'flatpak', 'install', 'flathub','-y', package], check=True)
            print(f"Package {package} installed successfully.")
    except subprocess.CalledProcessError as e:
            (f"Error: Failed to install package {package}. {e}")

def list_packages(command):
    """
    List installed packages
       Args:
            commands (list): command to run.
    """
    try:
        for cmd2run in command:
            print(f"\n'{cmd2run}' results:\n")
            result = subprocess.run(cmd2run, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to run command '{cmd2run}'. {e}")
        return None    

def main():
    os.system('clear')

    # Get the full path of the script
    script_path = os.path.abspath(__file__)
    # Extract the script name from the full path
    script_name = os.path.basename(script_path)

    ## check user has included an argument when calling the script.
    check_arguments(script_name)

    # check if source files listing apps to be installed
    # exist
    source_file_names = ["snap_apps", "flatpak_apps"]
    check_files_exists(source_file_names)    

    ## check if package Managers are installed. If not, install them
    pkgmgr_to_check = ["snap", "flatpak", "tester"]  # Add package manager names here
    #pkgmgr_to_check = "snap2"  # Add package manager names here
    check_pkgmgr_installed(pkgmgr_to_check)

    ## Install snap packages
    pkg_type = "snap"
    packages_to_install = ["slack", "package2", "package3"]  # Add your SNAP package names here
    #install_packages(pkg_type, packages_to_install)

    ## Install flatpak packages
    pkg_type = "flatpak"
    packages_to_install = ["slack", "package2", "package3"]  # Add your FLATPAK package names here
    #install_packages(pkg_type, packages_to_install)
    
    ## List installed packages
    commands_to_run = ["snap list", "flatpak list"]
    #list_packages(commands_to_run)

if __name__ == "__main__":
    main()


