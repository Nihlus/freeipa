Name:           ipa-server
Version:        0.5.0
Release:        1%{?dist}
Summary:        Ipa authentication server

Group:          System Environment/Base
License:        GPL
URL:            http://www.freeipa.org
Source0:        %{name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: fedora-ds-base-devel >= 1.1
BuildRequires: mozldap-devel
BuildRequires: openssl-devel
BuildRequires: openldap-devel
BuildRequires: krb5-devel
BuildRequires: nss-devel
BuildRequires: libcap-devel

Requires: ipa-python
Requires: ipa-admintools
Requires: fedora-ds-base >= 1.1
Requires: openldap-clients
Requires: nss
Requires: nss-tools
Requires: krb5-server
Requires: krb5-server-ldap
Requires: cyrus-sasl-gssapi
Requires: ntp
Requires: httpd
Requires: mod_python
Requires: mod_auth_kerb
Requires: mod_nss >= 1.0.7-2
Requires: python-ldap
Requires: python
Requires: python-krbV
Requires: TurboGears
Requires: python-tgexpandingformwidget
Requires: acl
Requires: freeradius
Requires: pyasn1
Requires: libcap

%define httpd_conf /etc/httpd/conf.d
%define plugin_dir %{_libdir}/dirsrv/plugins

%description
Ipa is a server for identity, policy, and audit.

%prep
%setup -q
./configure --prefix=%{buildroot}/usr --libdir=%{buildroot}/%{_libdir} --sysconfdir=%{buildroot}/etc

%build

make

%install
rm -rf %{buildroot}

make install

# Remove .la files from libtool - we don't want to package
# these files
rm %{buildroot}/%{plugin_dir}/libipa_pwd_extop.la
rm %{buildroot}/%{plugin_dir}/libipa-memberof-plugin.la
rm %{buildroot}/%{plugin_dir}/libipa-dna-plugin.la

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add ipa-kpasswd
    /sbin/chkconfig --add ipa-webgui
fi

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del ipa-kpasswd
    /sbin/chkconfig --del ipa-webgui
    /sbin/service ipa-kpasswd stop >/dev/null 2>&1 || :
    /sbin/service ipa-webgui stop >/dev/null 2>&1 || :
fi

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service ipa-kpasswd condrestart >/dev/null 2>&1 || :
    /sbin/service ipa-webgui condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_sbindir}/ipa-server-install
%{_sbindir}/ipa-replica-install
%{_sbindir}/ipa-replica-prepare
%{_sbindir}/ipa_kpasswd
%{_sbindir}/ipa-webgui
%attr(4750,root,apache) %{_sbindir}/ipa-keytab-util
%attr(755,root,root) %{_initrddir}/ipa-kpasswd
%attr(755,root,root) %{_initrddir}/ipa-webgui

%dir %{_usr}/share/ipa
%{_usr}/share/ipa/*

%attr(755,root,root) %{plugin_dir}/libipa_pwd_extop.so
%attr(755,root,root) %{plugin_dir}/libipa-memberof-plugin.so
%attr(755,root,root) %{plugin_dir}/libipa-dna-plugin.so


%changelog
* Wed Nov 21 2007 Karl MacMillan <kmacmill@mentalrootkit.com> - 0.5.0-1
- Preverse mode on ipa-keytab-util
- Version bump for relase and rpm name change

* Thu Nov 15 2007 Rob Crittenden <rcritten@redhat.com> - 0.4.1-2
- Broke invididual Requires and BuildRequires onto separate lines and
  reordered them
- Added python-tgexpandingformwidget as a dependency
- Require at least fedora-ds-base 1.1

* Thu Nov  1 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.1-1
- Version bump for release

* Wed Oct 31 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.0-6
- Add dep for freeipa-admintools and acl

* Wed Oct 24 2007 Rob Crittenden <rcritten@redhat.com> - 0.4.0-5
- Add dependency for python-krbV

* Fri Oct 19 2007 Rob Crittenden <rcritten@redhat.com> - 0.4.0-4
- Require mod_nss-1.0.7-2 for mod_proxy fixes

* Thu Oct 18 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.0-3
- Convert to autotools-based build

* Tue Sep 25 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.0-2
- Package ipa-webgui

* Fri Sep 7 2007 Karl MacMillan <kmacmill@redhat.com> - 0.3.0-1
- Added support for libipa-dna-plugin

* Fri Aug 10 2007 Karl MacMillan <kmacmill@redhat.com> - 0.2.0-1
- Added support for ipa_kpasswd and ipa_pwd_extop

* Mon Aug  5 2007 Rob Crittenden <rcritten@redhat.com> - 0.1.0-3
- Abstracted client class to work directly or over RPC

* Wed Aug  1 2007 Rob Crittenden <rcritten@redhat.com> - 0.1.0-2
- Add mod_auth_kerb and cyrus-sasl-gssapi to Requires
- Remove references to admin server in ipa-server-setupssl
- Generate a client certificate for the XML-RPC server to connect to LDAP with
- Create a keytab for Apache
- Create an ldif with a test user
- Provide a certmap.conf for doing SSL client authentication

* Fri Jul 27 2007 Karl MacMillan <kmacmill@redhat.com> - 0.1.0-1
- Initial rpm version
