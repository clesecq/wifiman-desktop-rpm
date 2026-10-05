%global _hardened_build 1
%define _build_id_links none
%define debug_package %{nil}
%global selinuxtype targeted
%global modulename wifiman_desktop

Name:          wifiman-desktop
Version:       1.3.0
Release:       2
Summary:       Discover devices and access Teleport VPNs
License:       LicenseRef-Proprietary AND MIT AND GPL-2.0-only
Vendor:        Ubiquiti Inc. <monitoring@wifiman.com>
URL:           https://wifiman.com/
ExclusiveArch: x86_64

# tito generates Source0 from the git tree; it carries the SELinux module
Source0:  %{name}-%{version}.tar.gz
Source1:  https://desktop.wifiman.com/wifiman-desktop-%{version}-amd64.deb

BuildRequires: binutils
BuildRequires: bzip2
BuildRequires: desktop-file-utils
BuildRequires: gzip
BuildRequires: selinux-policy-devel
BuildRequires: systemd-rpm-macros
BuildRequires: tar

Requires: net-tools
Requires: iw
%{?systemd_requires}
%{?selinux_requires}
# tray icon library is dlopen()ed, so it is not picked up automatically
Requires: libayatana-appindicator-gtk3

%description
WiFiman is here to save your home or office network from sluggish surfing, endless buffering, and congested data channels.
With this free-to-use (and ad-free) app you can:

- Detect and connect to all available Wi-Fi networks devices instantly.
- Scan network subnet for details on available devices, using Bonjour, SNMP, NetBIOS, and Ubiquiti discovery protocols.
- Conduct download/upload speed tests, store results, compare network performance, and share your insights with others.
- Relocate your access points (APs) to nearby data channels to instantly increase signal strength and reduce traffic volume.
- Connect remotely to your UniFi network via Teleport VPN.

%prep
%setup -cT
tar xf %{SOURCE0} --strip-components=1
ar x %{SOURCE1}
tar xf data.tar.gz

%build
make -C selinux -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 selinux/%{modulename}.pp

%install
install -m 0755 -vd %{buildroot}%{_datadir}
cp -R usr/share/* %{buildroot}%{_datadir}/

install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp usr/bin/wifiman-desktop %{buildroot}%{_bindir}/

install -m 0755 -vd %{buildroot}%{_prefix}/lib/wifiman-desktop
install -m 0755 -vp usr/lib/wifiman-desktop/wg %{buildroot}%{_prefix}/lib/wifiman-desktop/
install -m 0755 -vp usr/lib/wifiman-desktop/wg-quick %{buildroot}%{_prefix}/lib/wifiman-desktop/
install -m 0755 -vp usr/lib/wifiman-desktop/wifiman-desktopd %{buildroot}%{_prefix}/lib/wifiman-desktop/
install -m 0755 -vp usr/lib/wifiman-desktop/wireguard-go %{buildroot}%{_prefix}/lib/wifiman-desktop/
install -m 0644 -vp usr/lib/wifiman-desktop/.env %{buildroot}%{_prefix}/lib/wifiman-desktop/

install -m 0644 -vpD usr/lib/wifiman-desktop/wifiman-desktop.service %{buildroot}%{_unitdir}/%{name}.service

install -m 0644 -vpD selinux/%{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/wifiman-desktop.desktop

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
# files were unpacked before the module loaded, so they still carry lib_t
restorecon -R %{_prefix}/lib/wifiman-desktop &> /dev/null || :
%systemd_post %{name}.service

%preun
if [ $1 -eq 0 ] ; then
  pkill -SIGTERM -f '^(%{_bindir}/)?wifiman-desktop( |$)' &> /dev/null || :
fi
%systemd_preun %{name}.service

%postun
%selinux_modules_uninstall -s %{selinuxtype} %{modulename}
%systemd_postun_with_restart %{name}.service

%files
%dir %attr(755, root, root) %{_prefix}/lib/wifiman-desktop
%attr(644, root, root) %{_prefix}/lib/wifiman-desktop/.env
%attr(755, root, root) %{_prefix}/lib/wifiman-desktop/wg
%attr(755, root, root) %{_prefix}/lib/wifiman-desktop/wg-quick
%attr(755, root, root) %{_prefix}/lib/wifiman-desktop/wifiman-desktopd
%attr(755, root, root) %{_prefix}/lib/wifiman-desktop/wireguard-go
%attr(755, root, root) %{_bindir}/wifiman-desktop
%attr(644, root, root) %{_unitdir}/%{name}.service
%attr(644, root, root) %{_datadir}/applications/wifiman-desktop.desktop
%attr(644, root, root) %{_datadir}/icons/hicolor/*/apps/wifiman-desktop.png
%attr(644, root, root) %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Mon Oct 05 2026 Charles LESECQ <charles@lesecq.eu> 1.3.0-2
- docs: move Copr to coles/wifiman-desktop and document GitHub releases
  (charles@lesecq.eu)
- feat(selinux): run daemon as unconfined_service_t (charles@lesecq.eu)

* Mon Oct 05 2026 Charles LESECQ <charles@lesecq.eu> 1.3.0-1
- ci: build RPM with tito and publish releases on tag (charles@lesecq.eu)
- fix(spec): match only the app process in %%preun pkill (charles@lesecq.eu)
- refactor(spec): unpack in %%prep and drop obsolete scriptlets
  (charles@lesecq.eu)
- fix(spec): tidy dependencies (charles@lesecq.eu)
- fix(spec): only kill running app on package removal (charles@lesecq.eu)
- fix(spec): drop destructive %%postun cleanup (charles@lesecq.eu)
- fix(spec): package systemd unit in %%{_unitdir} (charles@lesecq.eu)
- fix(spec): declare actual license of packaged software (charles@lesecq.eu)
- fix(spec): use wifiman-desktop paths from 1.x deb (charles@lesecq.eu)
- feat(spec): add ExclusiveArch (charles@lesecq.eu)
- feat(spec): upgrade webkit2gtk (charles@lesecq.eu)
- fix(spec): typo in group (charles@lesecq.eu)
- feat(spec): update to 1.3.0 (charles@lesecq.eu)
- spec: update spec to support 1.x.x versions (etienne.barbier@eviden.com)
- doc: daemon start instructions (arun.neelicattu@gmail.com)
- doc: improve readme (arun.neelicattu@gmail.com)

* Thu Sep 05 2024 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.3.0-3
- spec: include all arch debs in srpm (arun.neelicattu@gmail.com)

* Thu Sep 05 2024 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.3.0-2
- tito: fetch sources for build (arun.neelicattu@gmail.com)

* Thu Sep 05 2024 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.3.0-1
- Release 0.30.0 package built with tito
