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
# @Contact       : jason@casjaysdev.pro
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
REPO_BRANCH="${GIT_REPO_BRANCH:-main}"
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
  local apache2user sitename httpd_dir httpd_shared httpd_web httpd_log httpd_src GET_OSNAME GET_OSVER
  GET_OSNAME="$(grep -s 'NAME=' /etc/*-release | awk -F '=' '{print $2}' | head -n1)"
  GET_OSVER="$(grep -s 'BUILD_ID' /etc/*-release | awk -F '=' '{print $2}' | head -n1)"
  sitename="$(hostname -f)"
  httpd_web="/var/www/html"
  httpd_shared="/usr/local/share/httpd"
  if [[ -d "/etc/httpd" ]]; then
    apache2user="httpd"
    httpd_src="etc-httpd"
    httpd_dir="/etc/httpd"
    httpd_log="/var/log/httpd"
  elif [[ -d "/etc/apache2" ]]; then
    apache2user="www-data"
    httpd_src="etc-apache2"
    httpd_dir="/etc/apache2"
    httpd_log="/var/log/apache2"
    a2enmod access_compat alias asis auth_basic authn_core authn_file authz_core authz_host authz_user autoindex \
      brotli cgi cgid charset_lite data deflate dir env expires fcgid filter geoip headers lbmethod_bybusyness \
      lua mime mpm_prefork negotiation php7.4 proxy proxy_balancer reqtimeout request rewrite session \
      session_dbd setenvif slotmem_shm socache_shmcb speling status userdir vhost_alias xml2enc
  fi
  [[ -d "$httpd_dir" ]] || mkd "$httpd_dir"
  [[ -d "$httpd_log" ]] || mkd "$httpd_log"
  [[ -d "$httpd_web/unknown" ]] || mkd "$httpd_web/unknown"
  [[ -d "$httpd_web/default" ]] || mkd "$httpd_web/default"
  [[ -L "$httpd_dir/logs" ]] || ln_sf "$httpd_log" "$httpd_dir/logs"
  cp_rf "$INSTDIR/src/$httpd_src/." "$httpd_dir"
  if [[ -f "$(builtin type -P pacman 2>/dev/null)" ]]; then
    apache2user="http"
    cp_rf "$INSTDIR/src/etc-httpd/conf/httpd-arch.conf" "/etc/httpd/conf/httpd.conf"
  fi

  STATICSITE="$sitename"
  sudo -HE STATICSITE="$sitename" bash -c "$(curl -LSs https://github.com/casjay-templates/default-web-assets/raw/main/setup.sh)"

  [ -e "$httpd_web/default/index.default.php" ] || ln_sf "$httpd_shared/html/index.default.php" "$httpd_web/default/index.default.php"
  [ -e "$httpd_web/unknown/index.unknown.php" ] || ln_sf "$httpd_shared/html/index.unknown.php" "$httpd_web/unknown/index.unknown.php"
  if [ -n "$apache2user" ]; then
    sed -i "s|replace_apache|$apache2user|g" "$APPDIR/src/php/php-fpm.conf"
    chown -Rf "$apache2user":"$apache2user" "$httpd_web" "$httpd_shared" "$httpd_log" "$httpd_dir"
  fi
  cmd_exists changeip && changeip &>/dev/null
  mkd /run/mod_fcgid
  systemctl enable --now httpd || systemctl enable --now apache2
  systemctl restart httpd || systemctl restart apache2
  if [ -n "$GET_OSNAME" ] && [ -n "$GET_OSVER" ]; then
    printf '%s\n' "$GET_OSNAME $GET_OSVER" >"/etc/casjaysdev/updates/versions/osver.txt"
  elif [ -n "$GET_OSNAME" ]; then
    printf '%s\n' "$GET_OSNAME" >"/etc/casjaysdev/updates/versions/osver.txt"
  elif [ -n "$GET_OSVER" ]; then
    printf '%s\n' "$GET_OSVER" >"/etc/casjaysdev/updates/versions/osver.txt"
  else
    printf '%s\n' 'Unknown' >"/etc/casjaysdev/updates/versions/osver.txt"
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
