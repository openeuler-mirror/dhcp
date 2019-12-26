%global nmconfdir %{_sysconfdir}/NetworkManager
%global dhcpconfdir %{_sysconfdir}/dhcp

Name:      dhcp
Version:   4.3.6
Release:   33
Summary:   Dynamic host configuration protocol software
#Please don't change the epoch on this package
Epoch:     12
License:   ISC
URL:       https://www.isc.org/dhcp/
Source0:   http://ftp.isc.org/isc/dhcp/%{version}/dhcp-%{version}.tar.gz
#Source1~8 copy from fedora
Source1:   dhclient-script
Source2:   README.dhclient.d
Source3:   11-dhclient
Source4:   12-dhcpd
Source5:   56dhclient
Source6:   dhcpd.service
Source7:   dhcpd6.service
Source8:   dhcrelay.service

#patch18,20,39,40,41,,42,43 from upstream,other from fedora
Patch0:    dhcp-remove-bind.patch

Patch1:    dhcp-sharedlib.patch

Patch2:    dhcp-dhclient-options.patch
Patch3:    dhcp-release-by-ifup.patch
Patch4:    dhcp-dhclient-decline-backoff.patch
Patch5:    dhcp-unicast-bootp.patch
Patch6:    dhcp-default-requested-options.patch

Patch7:    dhcp-manpages.patch
Patch8:    dhcp-paths.patch
Patch9:    dhcp-CLOEXEC.patch
Patch10:   dhcp-garbage-chars.patch
Patch11:   dhcp-add_timeout_when_NULL.patch
Patch12:   dhcp-64_bit_lease_parse.patch
Patch13:   dhcp-capability.patch

Patch14:   dhcp-sendDecline.patch
Patch15:   dhcp-rfc3442-classless-static-routes.patch
Patch16:   dhcp-honor-expired.patch
Patch17:   dhcp-PPP.patch

Patch18:   dhcp-lpf-ib.patch
Patch19:   dhcp-IPoIB-log-id.patch
Patch20:   dhcp-improved-xid.patch

Patch21:   dhcp-client-request-release-bind-iface.patch
Patch22:   dhcp-no-subnet-error2info.patch
Patch23:   dhcp-sd_notify.patch

Patch24:   dhcp-option97-pxe-client-id.patch
Patch25:   dhcp-stateless-DUID-LLT.patch
Patch26:   dhcp-dhclient-preinit6s.patch
Patch27:   dhcp-handle_ctx_signals.patch
Patch28:   dhcp-4.3.6-omapi-leak.patch
Patch29:   dhcp-4.3.6-isc-util.patch
Patch30:   dhcp-4.3.6-options_overflow.patch
Patch31:   dhcp-4.3.6-reference_count_overflow.patch
Patch32:   dhcp-iface_hwaddr_discovery.patch

Patch6000: Correct-BIND9-dns-API-call-constant.patch
Patch6001: Corrected-dhclient-command-line-parsing-of-dad-wait-.patch
Patch6002: CVE-2019-6470.patch
Patch6003: bugfix-dhcp-4.2.5-check-dhclient-pid.patch
Patch6004: bugfix-reduce-getifaddr-calls.patch

Patch9000: dhcp-fix-dhclient-default-len-64-to-128.patch
Patch9001: bugfix-dhcpd-2038-problem.patch
Patch9002: adds-address-prefix-len-to-dhclient-cli.patch

BuildRequires: gcc autoconf automake libtool openldap-devel krb5-devel libcap-ng-devel bind-export-devel
BuildRequires: systemd systemd-devel

Requires: shadow-utils coreutils grep sed systemd gawk ipcalc iproute iputils


Provides:  %{name}-common %{name}-libs %{name}-server %{name}-relay %{name}-compat %{name}-client
Obsoletes: %{name}-common %{name}-libs %{name}-server %{name}-relay %{name}-compat %{name}-client


Provides:  dhcp = %{epoch}:%{version}-%{release}
Obsoletes: dhcp < %{epoch}:%{version}-%{release}

Provides: dhclient = %{epoch}:%{version}-%{release}
Obsoletes: dhclient < %{epoch}:%{version}-%{release}


%description
The Dynamic Host Configuration Protocol (DHCP) is a network management protocol used on UDP/IP networks whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on a network so they can communicate with other IP networks.

%package devel
Summary: Development headers and libraries for interfacing to the DHCP server
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for using the ISC DHCP libraries.  The
libdhcpctl and libomapi static libraries are also included in this package.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
rm bind/bind.tar.gz

sed -i -e 's|/var/db/|%{_localstatedir}/lib/dhcpd/|g' contrib/dhcp-lease-list.pl


%build
autoreconf --verbose --force --install

CFLAGS="%{optflags} -fno-strict-aliasing" \
%configure --with-srv-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd.leases \
    --with-srv6-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd6.leases \
    --with-cli-lease-file=%{_localstatedir}/lib/dhclient/dhclient.leases \
    --with-cli6-lease-file=%{_localstatedir}/lib/dhclient/dhclient6.leases \
    --with-srv-pid-file=%{_localstatedir}/run/dhcpd.pid \
    --with-srv6-pid-file=%{_localstatedir}/run/dhcpd6.pid \
    --with-cli-pid-file=%{_localstatedir}/run/dhclient.pid \
    --with-cli6-pid-file=%{_localstatedir}/run/dhclient6.pid \
    --with-relay-pid-file=%{_localstatedir}/run/dhcrelay.pid \
    --with-libbind=/usr/bin/isc-export-config.sh \
    --with-ldap --with-ldapcrypto --with-ldap-gssapi --disable-static  --enable-log-pid --enable-paranoia --enable-early-chroot \
    --enable-binary-leases --with-systemd
%make_build

%install
%make_install

install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/dhclient-script

install -p -m 0644 %{SOURCE2} .

mkdir -p $RPM_BUILD_ROOT%{dhcpconfdir}/dhclient.d

mkdir -p $RPM_BUILD_ROOT%{nmconfdir}/dispatcher.d
install -p -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{nmconfdir}/dispatcher.d
install -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{nmconfdir}/dispatcher.d

install -D -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/56dhclient

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpd/
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpd/dhcpd6.leases
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dhclient/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcpd
# WARNING: This file is NOT used anymore.

# If you are here to restrict what interfaces should dhcpd listen on,
# be aware that dhcpd listens *only* on interfaces for which it finds subnet
# declaration in dhcpd.conf. It means that explicitly enumerating interfaces
# also on command line should not be required in most cases.

# If you still insist on adding some command line options,
# copy dhcpd.service from /lib/systemd/system to /etc/systemd/system and modify
# it there.
# https://fedoraproject.org/wiki/Systemd#How_do_I_customize_a_unit_file.2F_add_a_custom_unit_file.3F

# example:
# $ cp /usr/lib/systemd/system/dhcpd.service /etc/systemd/system/
# $ vi /etc/systemd/system/dhcpd.service
# $ ExecStart=/usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid <your_interface_name(s)>
# $ systemctl --system daemon-reload
# $ systemctl restart dhcpd.service
EOF

mkdir -p $RPM_BUILD_ROOT%{dhcpconfdir}
cat << EOF > %{buildroot}%{dhcpconfdir}/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
EOF
cat << EOF > %{buildroot}%{dhcpconfdir}/dhcpd6.conf
#
# DHCPv6 Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd6.conf.example
#   see dhcpd.conf(5) man page
#
EOF

rm -f $RPM_BUILD_ROOT/usr/lib/debug/usr/sbin/dhcrelay-4.3.6-28.7.aarch64.debug
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dhclient.conf.example
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dhcpd.conf.example



mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-client
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-server
install -p -m 0755 doc/examples/dhclient-dhcpv6.conf $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-client/dhclient6.conf.example
install -p -m 0755 doc/examples/dhcpd-dhcpv6.conf $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-server/dhcpd6.conf.example

install -D -p -m 0644 contrib/ldap/dhcp.schema $RPM_BUILD_ROOT%{_sysconfdir}/openldap/schema/dhcp.schema

find $RPM_BUILD_ROOT -type f -name "*.la" -delete -print

%check

%pre
%global gid_uid 177
if ! getent group dhcpd > /dev/null ; then
    groupadd --force --gid %{gid_uid} --system dhcpd
fi

if ! getent passwd dhcpd >/dev/null ; then
    if ! getent passwd %{gid_uid} >/dev/null ; then
      useradd --system --uid %{gid_uid} --gid dhcpd --home / --shell /sbin/nologin --comment "DHCP server" dhcpd
    else
      useradd --system --gid dhcpd --home / --shell /sbin/nologin --comment "DHCP server" dhcpd
    fi
fi



exit 0

%preun
%systemd_preun dhcpd.service dhcpd6.service dhcrelay.service


%post
/sbin/ldconfig
%systemd_post dhcpd.service dhcpd6.service dhcrelay.service

for servicename in dhcpd dhcpd6 dhcrelay; do
  etcservicefile=%{_sysconfdir}/systemd/system/${servicename}.service
  if [ -f ${etcservicefile} ]; then
    grep -q Type= ${etcservicefile} || sed -i '/\[Service\]/a Type=notify' ${etcservicefile}
    sed -i 's/After=network.target/Wants=network-online.target\nAfter=network-online.target/' ${etcservicefile}
  fi
done
exit 0

%postun
/sbin/ldconfig
%systemd_postun_with_restart dhcpd.service dhcpd6.service dhcrelay.service

%files
%defattr(-,root,root)
%license LICENSE
%doc README RELNOTES doc/References.txt
%doc README.dhclient.d client/dhclient.conf.example
%doc contrib/ldap/ contrib/dhcp-lease-list.pl
%{_datadir}/doc/dhcp-client/dhclient6.conf.example
%{_datadir}/doc/dhcp-server/dhcpd6.conf.example
%dir %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/schema/dhcp.schema
%attr(0750,root,root) %dir %{dhcpconfdir}
%dir %{dhcpconfdir}/dhclient.d
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%{_sysconfdir}/NetworkManager/dispatcher.d/11-dhclient
%{_sysconfdir}/NetworkManager/dispatcher.d/12-dhcpd
%attr(0644,root,root)   %{_unitdir}/dhcpd.service
%attr(0644,root,root)   %{_unitdir}/dhcpd6.service
%attr(0644,root,root) %{_unitdir}/dhcrelay.service
%attr(0644,dhcpd,dhcpd) %verify(mode) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd.leases
%attr(0644,dhcpd,dhcpd) %verify(mode) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd6.leases
%config(noreplace) %{_sysconfdir}/sysconfig/dhcpd
%config(noreplace) %{dhcpconfdir}/dhcpd.conf
%config(noreplace) %{dhcpconfdir}/dhcpd6.conf
%{_sbindir}/dhcpd
%{_sbindir}/dhclient
%{_sbindir}/dhclient-script
%{_sbindir}/dhcrelay
%{_bindir}/omshell
%{_libdir}/libdhcpctl.so.*
%{_libdir}/libomapi.so.*
%{_libdir}/libdhcpctl.so
%{_libdir}/libomapi.so
%attr(0755,root,root) %{_libdir}/pm-utils/sleep.d/56dhclient

%files  devel
%defattr(-,root,root)
%doc doc/IANA-arp-parameters doc/api+protocol
%{_includedir}/dhcpctl
%{_includedir}/omapip
%{_includedir}/isc-dhcp


%files help
%defattr(644,root,root)
%doc doc/*
%{_mandir}/man1/omshell.1.gz
%{_mandir}/man5/dhcpd.conf.5.gz
%{_mandir}/man5/dhcpd.leases.5.gz
%{_mandir}/man8/dhcpd.8.gz
%{_mandir}/man5/dhcp-options.5.gz
%{_mandir}/man5/dhcp-eval.5.gz
%{_mandir}/man5/dhclient.conf.5.gz
%{_mandir}/man5/dhclient.leases.5.gz
%{_mandir}/man8/dhclient.8.gz
%{_mandir}/man8/dhclient-script.8.gz
%{_mandir}/man8/dhcrelay.8.gz
%{_mandir}/man3/dhcpctl.3.gz
%{_mandir}/man3/omapi.3.gz

%changelog
* Tue Dec 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-33
- rename doc subpackage as help subpackage

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-32
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix dhcpd 2038 problem;
       Adds address prefix len to dhclient cli

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-31
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: reducing getifaddrs calls and improving code performance

* Mon Sep 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-30
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Fix dhcp package installation failed

* Thu Sep 5 2019 hufeng <solar.hu@huawei.com> - 4.3.6-29
-Create dhcp spec
