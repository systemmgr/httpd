#!/usr/bin/env bash
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
APPNAME="httpd"
USER="${SUDO_USER:-${USER}}"
HOME="${USER_HOME:-${HOME}}"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#set opts

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
##@Version       : 020820211604-git
# @Author        : Jason Hempstead
# @Contact       : jason@casjaysdev.com
# @License       : LICENSE.md
# @ReadME        : README.md
# @Copyright     : Copyright: (c) 2021 Jason Hempstead, CasjaysDev
# @Created       : Tuesday, Feb 09, 2021 20:59 EST
# @File          : install.sh
# @Description   :
# @TODO          :
# @Other         :
# @Resource      :
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Import functions
CASJAYSDEVDIR="${CASJAYSDEVDIR:-/usr/local/share/CasjaysDev/scripts}"
SCRIPTSFUNCTDIR="${CASJAYSDEVDIR:-/usr/local/share/CasjaysDev/scripts}/functions"
SCRIPTSFUNCTFILE="${SCRIPTSAPPFUNCTFILE:-app-installer.bash}"
SCRIPTSFUNCTURL="${SCRIPTSAPPFUNCTURL:-https://github.com/dfmgr/installer/raw/main/functions}"
connect_test() { ping -c1 1.1.1.1 &>/dev/null || curl --disable -LSs --connect-timeout 3 --retry 0 --max-time 1 1.1.1.1 2>/dev/null | grep -e "HTTP/[0123456789]" | grep -q "200" -n1 &>/dev/null; }
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if [ -f "$PWD/$SCRIPTSFUNCTFILE" ]; then
  . "$PWD/$SCRIPTSFUNCTFILE"
elif [ -f "$SCRIPTSFUNCTDIR/$SCRIPTSFUNCTFILE" ]; then
  . "$SCRIPTSFUNCTDIR/$SCRIPTSFUNCTFILE"
elif connect_test; then
  curl -LSs "$SCRIPTSFUNCTURL/$SCRIPTSFUNCTFILE" -o "/tmp/$SCRIPTSFUNCTFILE" || exit 1
  . "/tmp/$SCRIPTSFUNCTFILE"
else
  echo "Can not load the functions file: $SCRIPTSFUNCTDIR/$SCRIPTSFUNCTFILE" 1>&2
  exit 1
fi
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Call the main function
system_installdirs
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Make sure the scripts repo is installed
scripts_check
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Defaults
APPNAME="${APPNAME:-httpd}"
APPDIR="/usr/local/etc/$APPNAME"
INSTDIR="$SYSSHARE/CasjaysDev/systemmgr/$APPNAME"
REPO_BRANCH="${GIT_REPO_BRANCH:-master}"
REPO="${SYSTEMMGRREPO:-https://github.com/systemmgr}/$APPNAME"
REPORAW="$REPO/raw/$REPO_BRANCH"
APPVERSION="$(__appversion "$REPORAW/version.txt")"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Setup plugins
PLUGNAMES=""
PLUGDIR="${SHARE:-$HOME/.local/share}/$APPNAME"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Require a version higher than
systemmgr_req_version "$APPVERSION"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Call the systemmgr function
systemmgr_install
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Script options IE: --help
show_optvars "$@"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Requires root - no point in continuing
sudoreq # sudo required
#sudorun # sudo optional
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Do not update - add --force to overwrite
#installer_noupdate "$@"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# initialize the installer
systemmgr_run_init
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# end with a space
APP="$APPNAME "
PERL=""
PYTH=""
PIPS=""
CPAN=""
GEMS=""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# install packages - useful for package that have the same name on all oses
install_packages "$APP"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# install required packages using file
install_required "$APP"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# check for perl modules and install using system package manager
install_perl "$PERL"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# check for python modules and install using system package manager
install_python "$PYTH"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# check for pip binaries and install using python package manager
install_pip "$PIPS"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# check for cpan binaries and install using perl package manager
install_cpan "$CPAN"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# check for ruby binaries and install using ruby package manager
install_gem "$GEMS"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Other dependencies
dotfilesreq
dotfilesreqadmin
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Ensure directories exist
ensure_dirs
ensure_perms
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Backup if needed
if [ -d "$APPDIR" ]; then
  execute "backupapp $APPDIR $APPNAME" "Backing up $APPDIR"
fi
# Main progam
if am_i_online; then
  if [ -d "$INSTDIR/.git" ]; then
    execute "git_update $INSTDIR" "Updating $APPNAME configurations"
  else
    execute "git_clone $REPO $INSTDIR" "Installing $APPNAME configurations"
  fi
  # exit on fail
  failexitcode $? "Git has failed"
fi
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# run post install scripts
run_postinst() {
  systemmgr_run_post
  local apache2user sitename
  sitename="$(hostname -f)"
  if [[ -f "$(builtin type -P pacman)" ]]; then
    local apache2user="http"
    cp_rf "$INSTDIR/src/etc-httpd/." /etc/httpd
    cp_rf "$INSTDIR/src/etc-httpd/conf/httpd-arch.conf" "/etc/httpd/conf/httpd.conf"
  elif [ -d /etc/httpd ]; then
    local apache2user="httpd"
    cp_rf "$INSTDIR/src/etc-httpd/." /etc/httpd
  elif [ -d /etc/httpd ]; then
    local apache2user="www-data"
    cp_rf "$INSTDIR/src/etc-apache2/." /etc/apache2
  fi
  if [ -d "/usr/share/httpd/.git" ]; then
    git -C /usr/share/httpd reset --hard &>/dev/null
    if ! git -C /usr/share/httpd pull -q &>/dev/null; then
      rm_rf "/usr/share/httpd"
      git clone "https://github.com/casjay-templates/default-web-assets" "/usr/share/httpd" &>/dev/null
    fi
    [ -f "/usr/share/httpd/setup.sh" ] && STATICSITE="$sitename" bash -c "/usr/share/httpd/setup.sh"
  else
    mkd /usr/share/httpd
    cp_rf "$INSTDIR/src/etc-apache2/." /usr/share/httpd/
  fi
  if [ "$(command -v yum >/dev/null 2>&1)" ] || [ "$(command -v dnf >/dev/null 2>&1)" ]; then
    find /usr/share/httpd -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -iname "*.md" -iname "*.css" -exec sed -i 's#static.casjay.net#'$sitename'#g' {} \; >/dev/null 2>&1
    find /usr/share/httpd -not -path "./git/*" -type f -iname "*.sh" -iname "*.pl" -iname "*.cgi" -exec chmod 755 -Rf {} \; >/dev/null 2>&1
  elif [ "$(command -v apt-get >/dev/null 2>&1)" ]; then
    find /usr/share/httpd -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#Redhat based system#Debian based system#g' {} \; >/dev/null 2>&1
    find /usr/share/httpd -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#href="https://redhat.com"> <img border="0" alt="Redhat/CentOS/Fedora/SL Linux" src="/default-icons/powered_by_redhat.jpg">#href="https://debian.com"> <img border="0" alt="Debian/Ubuntu/Mint" src="/default-icons/powered_by_debian.jpg"#g' {} \; >/dev/null 2>&1
    find /var/www -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#Redhat based system#Debian based system#g' {} \; >/dev/null 2>&1
    find /var/www -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#href="https://redhat.com"> <img border="0" alt="Redhat/CentOS/Fedora/SL Linux" src="/default-icons/powered_by_redhat.jpg">#href="https://debian.com"> <img border="0" alt="Debian/Ubuntu/Mint" src="/default-icons/powered_by_debian.jpg"#g' {} \; >/dev/null 2>&1
  elif [ "$(command -v pacman >/dev/null 2>&1)" ]; then
    find /usr/share/httpd -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#Redhat based system#Debian based system#g' {} \; >/dev/null 2>&1
    find /usr/share/httpd -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#href="https://redhat.com"> <img border="0" alt="Redhat/CentOS/Fedora/SL Linux" src="/default-icons/powered_by_redhat.jpg">#href="https://debian.com"> <img border="0" alt="Debian/Ubuntu/Mint" src="/default-icons/powered_by_debian.jpg"#g' {} \; >/dev/null 2>&1
    find /var/www -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#Redhat based system#Arch based system#g' {} \; >/dev/null 2>&1
    find /var/www -not -path "./git/*" -type f -iname "*.php" -iname ".*html" -exec sed -i 's#href="https://redhat.com"> <img border="0" alt="Redhat/CentOS/Fedora/SL Linux" src="/default-icons/powered_by_redhat.jpg">#href="https://archlinux.org"> <img border="0" alt="ArchLinux" src="/default-icons/powered_by_archlinux.png"#g' {} \; >/dev/null 2>&1
  fi
  if [ -n "$apache2user" ]; then
    chown -Rf "$apache2user":"$apache2user" /var/www /usr/share/httpd
  fi
}
#
execute "run_postinst" "Running post install scripts"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# create version file
systemmgr_install_version
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# run exit function
run_exit
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# End application
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# lets exit with code
exit ${exitCode:-$?}
