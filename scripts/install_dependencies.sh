#!/bin/bash
# Install system dependencies

dnf update -y
dnf install -y epel-release
dnf groupinstall -y "Development Tools"
dnf install -y cmake gcc-c++ make git wget curl net-tools \
    xorg-x11-xauth mariadb-server mariadb java-11-openjdk

# Add MAX IV repo
cat > /etc/yum.repos.d/maxiv.repo << 'MAXIV'
[maxiv-public]
name=MAX IV public RPM Packages
baseurl=http://pubrepo.maxiv.lu.se/rpm/el9/\$basearch
gpgcheck=0
enabled=1
MAXIV

dnf install -y tango-db tango-starter tango-test
