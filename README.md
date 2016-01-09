# remote-dpkg
remote install packages with dpkg
usage: remote-dpkg.py -s 127.0.0.1 localhost -u root -i ./*.deb
This script uses dpkg over fabric in order to allow the installation of multiple deb packages to multiple hosts
IMPORTANT: dpkg is used with the --force-all parameter, this might cause issues in some cases, so test it manually before
