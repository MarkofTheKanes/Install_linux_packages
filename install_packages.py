# TO DO
# check if packages already installed - install if not
# check sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo has already been done
# add support for installing .deb files
# add option uninstall

import subprocess
import os
import sys
import logging

def check_arguments(file_name):
    """
    Check script has been called correctly. If not, return syntax for using it and exits.
    """
    if len(sys.argv) == 1:
        print(f"\nUsage: {file_name} [option]\n\n\
    -i - install all applications\n\
    -u - uninstall all applications\n\
    -l - list installed applications\n\n\
Example: {file_name} -i = install ALL packages")
        logging.info("No argument provided with '%s'. Exited script", file_name)
        sys.exit()
    else:
        option1 = sys.argv[1]
        return (option1)

def check_files_exists(src_filenames):
    """
    Check source files with apps to be installed exist. If not, exit with relevant error.
    """
    print(f"\nChecking if files lising apps to install exist.\n")

    try:
        for file_name in src_filenames:
            file_exists = os.path.exists(file_name)
            if file_exists:
                print(f"> Source apps file '{file_name}' found ok.")
            else:
                print(f"*** Source apps file '{file_name}' not found ***.")
    except:
        print(f"File '{file_name}' not found.\n")
        logging.info("*** Source apps file '%s' not found. Exited script.***", file_name)
        sys.exit()

def check_pkgmgr_installed(pkgmgr_name):
    """
    Check if the required package managers are installed on Ubuntu.

    Args:
        pkgmgr_name (str): The name of the package manager to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    
    STATUS: needs fixing - if 1st package not installed, ignores checking others
    """
    print(f"\nChecking if required package managers are installed.\n")
    try:
        for pkgname in pkgmgr_name:
            subprocess.run(['dpkg-query', '-l', pkgname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if subprocess:
                print(f"> Package manager '{pkgname}' is installed.")
        return True  # If the package is installed, dpkg-query will exit with status 0
    except subprocess.CalledProcessError:
        print(f"*** Package manager '{pkgname}' is not installed.***")
        install_pkgmgr(pkgname)
        return False  # If the package is not installed, dpkg-query will exit with a non-zero status

def install_pkgmgr(pkg_mgrname2):
    """
    Install package manager.

    Args:
        pkg_mgrname2 (string): the name of the package manager to install
    """
    print(f"\nInstalling missing package manager(s).\n") 

    try:
        print(f"packagemgr =", pkg_mgrname2)
        if pkg_mgrname2 == "flatpak":
            print(f"Installing package Manager {pkg_mgrname2}.")
            os.system('flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo')
            subprocess.run(['sudo', 'apt', 'install', pkg_mgrname2, '-y'], check=True, shell=False)
            subprocess.run(['sudo', 'apt', 'install', 'gnome-software-plugin-flatpak'], check=True, shell=False)
            print(f">Package {pkg_mgrname2} installed successfully.")
        elif pkg_mgrname2 == "nix":
            subprocess.run(['sudo', 'apt', 'install', pkg_mgrname2, '-y'], check=True, shell=False)
            print(f">Package {pkg_mgrname2} installed successfully.")
        elif pkg_mgrname2 == "snap":
            subprocess.run(['sudo', 'snap', 'install', pkg_mgrname2, '-y'], check=True, shell=False)
            print(f">Package {pkg_mgrname2} installed successfully.")
    except subprocess.CalledProcessError as e:
            (f"Error: Failed to install package manager {pkg_mgrname2}. {e}")

def process_packages(pckg_type, packages, pckg_cmd):
    """
    Process required packages.

    Args:
        pckg_type (string): defines the package type to (un)install and the command to run
        packages (list): List of package names to install.
        pckg_cmd (string): command to run e.g. install or uninstall
    """
    print(f"\nProcessing '{pckg_cmd}' application request.\n")
    print(f"pckg_type = '{pckg_type}'\n")
    print(f"packages = '{packages}'\n")
    print(f"pckg_cmd = '{pckg_cmd}'\n")

    try:
        for package in packages:
            if pckg_type == "snap":
                subprocess.run(['sudo', 'snap', pckg_cmd, package,'-y'], check=True, shell=False)
            elif pckg_type == "flatpak":
                subprocess.run(['sudo', 'flatpak', pckg_cmd, 'flathub','-y', package], check=True, shell=False)
            elif pckg_type == "apt":
                if pckg_cmd == "uninstall":
                    pckg_cmd = "remove"
                subprocess.run(['sudo', 'apt', pckg_cmd,'-y', package], check=True, shell=False)
            print(f"Package {package} installed successfully.")
    except subprocess.CalledProcessError as e:
            (f"Error: Failed to {pckg_cmd} package {package}. {e}")

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
    option_selected = check_arguments(script_name)

    # check if source files listing apps to be installed
    # exist
    source_file_names = ["./snap_apps", "./flatpak_apps", "./other_apps"]
    check_files_exists(source_file_names)    

    ## check if package Managers are installed. If not, install them
    #pkgmgr_to_check = ["snap", "flatpak", "apt", "tester"]
    pkgmgr_to_check = ["nix", "snap", "flatpak", "apt"]  # Add package manager names here
    check_pkgmgr_installed(pkgmgr_to_check)

    # 
    match option_selected:
        case "-i":
            ## Install all packages
            pkg_cmd = "install"
            print(f"\nInstalling all applications...")

        case "-u":
            ## Uninstall all packages
            print(f"\nUninstalling all applications...")
            pkg_cmd = "uninstall"
    
        case "-l":
            ## List installed packages
            print(f"\nListing installed applications...")
            commands_to_run = ["snap list", "flatpak list", "apt list --manual-installed=true"]
            list_packages(commands_to_run)
    
        case _:
            ## List installed packages
            commands_to_run = ["snap list", "flatpak list", "apt list --manual-installed=true"]           
            
    if option_selected == "-i" or option_selected == "-u":
        ## Install SNAP packages
        pkg_type = "snap"
        packages_to_process = ["code --classic"]  # Add your SNAP package names here
        #process_packages(pkg_type, packages_to_process, pkg_cmd)
        
        ## Install FLATPAK packages
        pkg_type = "flatpak"
        packages_to_process = ["one.ablaze.floorp", "org.gnome.DejaDup"]  # Add your FLATPAK package names here
        process_packages(pkg_type, packages_to_process, pkg_cmd)
        
        ## Install with apt
        pkg_type = "apt"
        packages_to_process = ["chromium-codecs-ffmpeg-extra", "curl", "terminator"]  # Add name of packages to install using apt
        process_packages(pkg_type, packages_to_process, pkg_cmd)

    print(f"\n**** FINISHED *****")

if __name__ == "__main__":
    main()


