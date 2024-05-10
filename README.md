# Install_linux_packages
Python script to install my packages on Ubuntu

**SNAP -**
- vs code - sudo snap install code --classic
- sudo snap install chromium-ffmpeg

**APT ­-**
First run
- sudo apt autoclean ; sudo apt autoremove

> Check if FLATHUB IS INSTALLED. If not, do following

    - sudo apt install flatpak
    - sudo apt install gnome-software-plugin-flatpak
    - flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

- sudo apt install chromium-codecs-ffmpeg-extra -y
- Ulauncher
    * sudo add-apt-repository universe -y && sudo add-apt-repository ppa:agornostal/ulauncher -y && sudo apt install ulauncher -y
- sudo apt install curl -y
- sudo apt install gnome-tweaks -y
- sudo apt install git-all -y
- sudo apt install gh -y
- sudo apt install autokey-gtk -y
- sudo apt install nemo followed by
    * xdg-mime default nemo.desktop inode/directory application/x-gnome-saved-search
    * gsettings set org.gnome.desktop.background show-desktop-icons false
    * gsettings set org.nemo.desktop show-desktop-icons true
    * use xdg-open $HOME to ensure it is the default
- sudo apt install terminator
- sudo apt install clamav
- sudo apt install clamtk


**Flatpak -**
- flatpak install flathub one.ablaze.floorp
- flatpak install flathub com.brave.Browser
- flatpak install flathub net.giuspen.cherrytree
- flatpak install flathub org.gnome.DejaDup
- flatpak install flathub com.mattjakeman.ExtensionManager
- flatpak install flathub org.keepassxc.KeePassXC
- flatpak install flathub org.signal.Signal
- flatpak install flathub us.zoom.Zoom
- flatpak install flathub org.gnome.SimpleScan
- flatpak install flathub org.libreoffice.LibreOffice

**Manual -**
- Bleachbit as root - install via Software app
- Proton Mail - .deb
- Proton VPN - install via Software app
