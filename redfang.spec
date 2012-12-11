
# OE: conditional switches
#
#(ie. use with rpm --rebuild):
#
#	--with diet	Compile dcetest against dietlibc
#
# 

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary: 	The Bluetooth Hunter
Name:		redfang
Version:	2.5
Release:	%mkrel 9
License:	GPL
Group:		Networking/Other
URL:		http://www.atstake.com/research/tools/info_gathering/
Source0:	%{name}.%{version}.tar.bz2
Patch0:		%{name}-%{version}-optflags.patch
Patch1:		%{name}-2.5-fix-format-errors.patch
Patch2:		%{name}-2.5-fix-missing-header.patch
BuildRequires:	bluez-devel
%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Redfang v2.5 is an enhanced version of the original application
that finds non-discoverable Bluetooth devices by brute-forcing the
last six bytes of the device's Bluetooth address and doing a
read_remote_name(). This new version has streamlined code,
enumerates service information, and supports multiple threads for
substantial speed gains using multiple devices (maximum
theoretical limit of 127 USB devices). This release of Redfang was
developed in collaboration with QinetiQ as part of their work in
the DTI Next Wave Technologies project FORWARD. (For more
information about the underlying concepts of Bluetooth discovery,
read our research report War Nibbling: Bluetooth Insecurity.)

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .optflags
%patch1 -p1 -b .format
%patch2 -p1 -b .header

%build

%if %{build_diet}
# OE: use the power of dietlibc
make CC="diet gcc -D_BSD_SOURCE -D_GNU_SOURCE -s -static"
%else
%make
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

install -m755 fang %{buildroot}%{_bindir}/fang
install -m644 fang.1 %{buildroot}%{_mandir}/man1/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG INSTALL OTHERS README
%{_bindir}/fang
%{_mandir}/man1/fang.1*


%changelog
* Tue Sep 15 2009 Thierry Vignaud <tvignaud@mandriva.com> 2.5-9mdv2010.0
+ Revision: 442672
- rebuild

* Tue Mar 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.5-8mdv2009.1
+ Revision: 347712
- rebuild for latest bluez libs
- fix format errors
- fix build error

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 2.5-3mdv2008.1
+ Revision: 140744
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5-3mdv2008.0
+ Revision: 66680
- Import redfang



* Fri Jul 14 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5-3mdv2007.0
- rebuild

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.5-2mdk
- rebuild

* Mon May 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.5-1mdk
- initial cooker contrib
- added P0
