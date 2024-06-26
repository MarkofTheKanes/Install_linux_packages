# TO DO
# add support for installing .deb files
#   .debs - Wave terminal emulator
# add support for apps requiring additional configs
# Pull list of apps to process from a file
# Fix checking issue with pkg_mg install check - stops checking if a package
# has not been installed


import subprocess
import os
import sys
import logging


def check_arguments(file_name):
    """
    Check script has been called correctly. If not, returns syntax for using
    it and exits.
    """
    if len(sys.argv) == 1:
        print(f"\nUsage: {file_name} [option]\n\n\
    -i - install all applications\n\
    -u - uninstall all applications\n\
    -l - list installed applications\n\
Example: {file_name} -i = install ALL packages\n")
        logging.info(
            "No argument provided with '%s'. Exited script", file_name)
        sys.exit()
    else:
        option1 = sys.argv[1]
        return (option1)


def check_files_exists(src_filenames):
    """
    Check source files with apps to be installed exist. If not, exit with
    relevant error.
    """
    print("\nChecking if files lising apps to install exist.\n")

    try:
        for file_name in src_filenames:
            file_exists = os.path.exists(file_name)
            if file_exists:
                print(f"> Source apps file '{file_name}' found ok.")
            else:
                print(f"*** Source apps file '{file_name}' not found ***.")
    except:
        # except FileNotFoundError:
        print(f"File '{file_name}' not found.\n")
        logging.info(
            "*** Source file '%s' not found. Exited script.***", file_name)
        sys.exit()


def check_pkgmgr_installed(pkgmgr_name):
    """
    Check if the required package managers are installed on Ubuntu.

    Args:
        pkgmgr_name (str): The name of the package manager to check.

    Returns:
        bool: True if the package is installed, False otherwise.

    STATUS: needs fixing - if 1st package not installed, ignores checking
            others
    """
    print("\nChecking if required package managers are installed.\n")
    try:
        for pkgname in pkgmgr_name:
            subprocess.run(['dpkg-query', '-l', pkgname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if subprocess:
                print(f"> Package manager '{pkgname}' is installed.")
        return True
        # If the package is installed, dpkg-query will exit with status 0
    except subprocess.CalledProcessError:
        print(f"*** Package manager '{pkgname}' is not installed.***")
        install_pkgmgr(pkgname)
        return False
        # If the package is not installed, dpkg-query will exit with a
        # non-zero status


def install_pkgmgr(pkg_mgrname2):
    """
    Install package manager.

    Args:
        pkg_mgrname2 (string): the name of the package manager to install
    """
    print("\nInstalling missing package manager(s).\n")

    try:
        print("packagemgr =", pkg_mgrname2)
        if pkg_mgrname2 == "flatpak":
            print(f"Installing package Manager {pkg_mgrname2}.")
            os.system(
                'flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo')
            subprocess.run(['sudo', 'apt', 'install',
                           pkg_mgrname2, '-y'], check=True, shell=False)
            subprocess.run(
                ['sudo', 'apt', 'install', 'gnome-software-plugin-flatpak'], check=True, shell=False)
            print(f">Package {pkg_mgrname2} installed successfully.")
        elif pkg_mgrname2 == "nix":
            subprocess.run(['sudo', 'apt', 'install',
                           pkg_mgrname2, '-y'], check=True, shell=False)
            print(f">Package {pkg_mgrname2} installed successfully.")
        elif pkg_mgrname2 == "snap":
            subprocess.run(['sudo', 'snap', 'install',
                           pkg_mgrname2, '-y'], check=True, shell=False)
            print(f">Package {pkg_mgrname2} installed successfully.")
    except subprocess.CalledProcessError as e:
        (f"Error: Failed to install package manager {pkg_mgrname2}. {e}")


def process_snap_packages(pckg_type, packages, pckg_cmd):
    """
    Process required packages.

    Args:
        pckg_type (string): defines the package type to (un)install and
                            the command to run
        packages (list): List of package names to install.
        pckg_cmd (string): command to run e.g. install or uninstall
    """
    print(f"\nProcessing '{pckg_cmd}' application request.")
    print(f">Packages Type = '{pckg_type}'.")
    print(f">Packages = '{packages}'.\n")
    if pckg_cmd == "uninstall":
        pckg_cmd = "remove"
    try:
        for pkg_name in packages:
            # Process Snap packages
  
            print(f"> Package to be processed = '{pkg_name}'")
            subprocess.run(['sudo', 'snap', pckg_cmd, pkg_name], check=True, shell=False, stderr=subprocess.DEVNULL)
            print(f"> Processing '{pckg_cmd}' of package '{pkg_name}' using '{pckg_type}'\n")
            print(f"The '{pckg_cmd}' command for package '{pkg_name}' has completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"*** Error: Failed to '{pckg_cmd}' package {pkg_name}. {e} ***")


def process_flatpak_packages(pckg_type, packages, pckg_cmd):
    """
    Process required packages.

    Args:
        pckg_type (string): defines the package type to (un)install and
                            the command to run
        packages (list): List of package names to install.
        pckg_cmd (string): command to run e.g. install or uninstall
    """
    print(f"\nProcessing '{pckg_cmd}' application request.")
    print(f">Packages Type = '{pckg_type}'.")
    print(f">Packages = '{packages}'.\n")
    try:
        for pkg_name in packages:
            # Install FLATPAK packages
            if pckg_cmd == "install":
                print(f"> Package = '{pkg_name}'")
                print(f"> Processing '{pckg_cmd}' of package '{pkg_name}' using '{pckg_type}'\n")
                subprocess.run(['sudo', 'flatpak', pckg_cmd, 'flathub', pkg_name, '-y'], check=True, shell=False, stderr=subprocess.DEVNULL)
            # Uninstall FLATPAK packages
            elif pckg_cmd == "uninstall":
                print(f"> Package = '{pkg_name}'")
                print(f"> Processing '{pckg_cmd}' of package '{pkg_name}' using '{pckg_type}'\n")
                subprocess.run(['sudo', 'flatpak', pckg_cmd, pkg_name, '-y', ], check=True, shell=False, stderr=subprocess.DEVNULL)
                print(f"The '{pckg_cmd}' command for package '{pkg_name}' has completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"*** Error: Failed to {pckg_cmd} package {pkg_name}. {e} ***")


def process_apt_packages(pckg_type, packages, pckg_cmd):
    """
    Process required packages.

    Args:
        pckg_type (string): defines the package type to (un)install and
                            the command to run
        packages (list): List of package names to install.
        pckg_cmd (string): command to run e.g. install or purge
    """
    if pckg_cmd == "uninstall":
        pckg_cmd = "purge"
    print(f"\nProcessing '{pckg_cmd}' application request.")
    print(f">Packages Type = '{pckg_type}'.")
    print(f">Packages = '{packages}'.\n")
    try:
        for pkg_name in packages:
            print(f"> Package = '{pkg_name}'")
            print(f"> Processing '{pckg_cmd}' of package '{pkg_name}' using '{pckg_type}'\n")
            subprocess.run(['sudo', 'apt', pckg_cmd, '-y', pkg_name], check=True, shell=False, stderr=subprocess.DEVNULL)
            print(f"The '{pckg_cmd}' command for package '{pkg_name}' has completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"*** Error: Failed to {pckg_cmd} package {pkg_name}. {e} ***")


def process_brave(pckg_cmd):
    """
    Process required packages.

    Args:
        pckg_cmd (string): command to run e.g. install or purge
    """
    pkg_name = "brave-browser"
    pckg_type = "apt"
    if pckg_cmd == "uninstall":
        pckg_cmd = "purge" 
    try:
        print(f"> Processing '{pckg_cmd}' for package '{pkg_name}' using '{pckg_type}'\n")
        subprocess.run(['sudo', 'curl', '-fsSLo', '/usr/share/keyrings/brave-browser-archive-keyring.gpg', 'https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'], check=True, shell=False, stderr=subprocess.DEVNULL)

        subprocess.run(['echo', '"deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"', '|sudo', 'tee', '/etc/apt/sources.list.d/brave-browser-release.list' ], check=True, shell=False, stderr=subprocess.DEVNULL)
        
        subprocess.run(['sudo', 'apt', pckg_cmd, '-y', pkg_name], check=True, shell=False, stderr=subprocess.DEVNULL)

        print(f"The '{pckg_cmd}' command for package '{pkg_name}' has completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"*** Error: Failed to {pckg_cmd} package {pkg_name}. {e} ***")


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

    # check user has included an argument when calling the script.
    option_selected = check_arguments(script_name)
    match option_selected:
        case "-i":
            # Install all packages
            pkg_cmd = "install"
            # print(f"\nInstalling all applications...")

        case "-u":
            # Uninstall all packages
            pkg_cmd = "uninstall"
            # print(f"\nUninstalling all applications...")

        case "-c":
            # Clean up unused  packages - TO DO
            pkg_cmd = "uninstall"
            # print(f"\nUninstalling all applications...")

        case "-l":
            # List installed packages
            print("\nListing installed applications...")
            commands_to_run = ["snap list", "flatpak list",
                               "apt list --manual-installed=true"]
            list_packages(commands_to_run)

        case _:
            # List installed packages
            commands_to_run = ["snap list", "flatpak list", "apt list --manual-installed=true"]
            list_packages(commands_to_run)
    if option_selected == "-i" or option_selected == "-u":
        # check if source files listing apps to be installed exist
        # source_file_names = ["./snap_apps", "./flatpak_apps", "./other_apps"]
        # check_files_exists(source_file_names)

        # check if package Managers are installed. If not, install them
        # Add package manager names here
        pkgmgr_to_check = ["snap", "flatpak", "apt"]
        check_pkgmgr_installed(pkgmgr_to_check)

        # Process SNAP packages
        pkg_type = "snap"
        # Add your SNAP package names here
        #packages_to_process = ["code --classic", "chromium-ffmpeg"]
        packages_to_process = ["chromium-ffmpeg","standard-notes"]
        #process_snap_packages(pkg_type, packages_to_process, pkg_cmd)

        # Process FLATPAK packages
        pkg_type = "flatpak"
        # Add your FLATPAK package names here
        packages_to_process = ['one.ablaze.floorp', 'org.gnome.DejaDup', 'net.giuspen.cherrytree','com.mattjakeman.ExtensionManager', 'org.signal.Signal', 'us.zoom.Zoom', 'org.gnome.SimpleScan', 'org.libreoffice.LibreOffice']
        #process_flatpak_packages(pkg_type, packages_to_process, pkg_cmd)

        # Process with apt
        pkg_type = "apt"
        # Add name of packages to be processed using apt here
        # Note: curl needs to be installed before Brave
        packages_to_process = ["chromium-codecs-ffmpeg-extra", "curl", "terminator", 'gnome-tweaks', 'git-all', 'gh', 'autokey-gtk', 'nemo','ubuntu-restricted-extras', 'tlp']
        #packages_to_process = ['brave-browser', "chromium-codecs-ffmpeg-extra", "curl", "terminator", 'gnome-tweaks', 'git-all', 'gh', 'autokey-gtk', 'nemo', 'clamav', 'clamtk', 'ubuntu-restricted-extras', 'tlp']
        #process_apt_packages(pkg_type, packages_to_process, pkg_cmd)

        # Special installs 
        ## Brave Browser
        process_brave(pkg_cmd)
        

    print("\nRun 'sudo snap install code --classic' to manually install VS Code")
    print("\n**** FINISHED *****")


if __name__ == "__main__":
    main()