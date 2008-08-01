
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
Release:	%mkrel 6
License:	GPL
Group:		Networking/Other
URL:		http://www.atstake.com/research/tools/info_gathering/
Source0:	%{name}.%{version}.tar.bz2
Patch0:		%{name}-%{version}-optflags.patch
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
