# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /usr/bin/amazon-efs-mount-watchdog; \
restorecon -R /usr/lib/systemd/system/amazon-efs-mount-watchdog.service; \
restorecon -R /var/log/amazon/efs; \

%define selinux_policyver 39.1-1

%global selinuxbooleans domain_can_mmap_files=1

Name:   efsutils_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for efsutils

Group:	System Environment/Base
License:	GPLv2+
# This is an example. You will need to change it.
# For a complete guide on packaging your policy
# see https://fedoraproject.org/wiki/SELinux/IndependentPolicy
URL:		http://HOSTNAME
Source0:	efsutils.pp
Source1:	efsutils.if
Source2:	efsutils_selinux.8


Requires: policycoreutils-python-utils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
Requires(post): efs-utils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for efsutils.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/efsutils_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/efsutils.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files
    %selinux_set_booleans -s %{selinuxtype} %{selinuxbooleans}
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r efsutils
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files
       %selinux_unset_booleans -s %{selinuxtype} %{selinuxbooleans}

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/efsutils.pp
%{_datadir}/selinux/devel/include/contrib/efsutils.if
%{_mandir}/man8/efsutils_selinux.8.*


%changelog
* Thu Nov  9 2023 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
- Initial version

