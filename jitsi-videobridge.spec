%define author Christopher Miersma
## Tito args --builder=mead --arg "maven_property=assembly.skipAssembly=false"

%define debug_package %{nil}

%{!?local_prefix:%define local_prefix local}
%if "%{local_prefix}" != "false"
%define _prefix /opt/%{local_prefix}
%define _sysconfdir /etc%{_prefix}
%define _datadir %{_prefix}/share
%define _docdir %{_datadir}/doc
%define _mandir %{_datadir}/man
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _libdir %{_prefix}/lib
%define _libexecdir %{_prefix}/libexec
%define _includedir %{_prefix}/include
%endif

Name:		jitsi-videobridge
Version:        1.0.968
Release:        1.local%{?dist}

Summary:	Jitsi Videobridge
Group:		local
License:	Apache
URL:		https://gitlab.com/ccmiersma/%{name}/
Source0:        %{name}-%{version}.tar.gz
BuildArch:      x86_64
BuildRequires:  pandoc


%description
WebRTC compatible Selective Forwarding Unit (SFU)
Jitsi Videobridge is a WebRTC compatible Selective Forwarding Unit
(SFU) for multiuser video communication. It is an essential part
of Jitsi Meet


%prep

%setup



%build

mvn package -D assembly.skipAssembly=false -D skipTests

mkdir extracted-files
unzip target/jitsi-videobridge-linux-x64*.zip -d extracted-files

%install

#raw
mkdir -p %buildroot%_prefix
mkdir -p %buildroot%_datadir
mkdir -p %buildroot%_docdir
mkdir -p %buildroot%_mandir
mkdir -p %buildroot%_bindir
mkdir -p %buildroot%_sbindir
mkdir -p %buildroot%_libdir/scripts
mkdir -p %buildroot%_libexecdir 
mkdir -p %buildroot%_includedir 
mkdir -p %buildroot%_sysconfdir/jitsi-videobridge
mkdir -p %buildroot/var/opt/%{local_prefix}

mkdir -p %buildroot%_mandir/man7
mkdir -p %buildroot%_prefix/app
mkdir -p %buildroot%_prefix/webapps
mkdir -p %buildroot%_prefix/lib64


mkdir -p %buildroot/etc/systemd/system 
mkdir -p %buildroot/etc/sysconfig/local
#end raw

mv extracted-files/* %buildroot%_prefix/app/jitsi-videobridge
cp local/jitsi-videobridge.service %buildroot/etc/systemd/system/
cp local/env.conf %buildroot%_sysconfdir/jitsi-videobridge/env.conf
mv %buildroot%_prefix/app/jitsi-videobridge/lib/logging.properties %buildroot%_sysconfdir/jitsi-videobridge/logging.properties
mv %buildroot%_prefix/app/jitsi-videobridge/lib/videobridge.rc %buildroot%_sysconfdir/jitsi-videobridge/videobridge.rc
ln -s -T %_sysconfdir/jitsi-videobridge/logging.properties %buildroot%_prefix/app/jitsi-videobridge/lib/logging.properties
ln -s -T %_sysconfdir/jitsi-videobridge/videobridge.rc %buildroot%_prefix/app/jitsi-videobridge/lib/videobridge.rc
#raw




##Manually defined files and dirs that need special designation.
##This will end up in the files section.
cat > %{name}-defined-files-list << EOF
%docdir %{_mandir}
%docdir %{_docdir}
%config %_sysconfdir/jitsi-videobridge/env.conf
%config %_sysconfdir/jitsi-videobridge/videobridge.rc 
%config %_sysconfdir/jitsi-videobridge/logging.properties
EOF
##Convoluted stuff to combine the manual list above with any new files we find, into a correct list with no duplicates
find %buildroot -type f -o -type l | sed -e "s#${RPM_BUILD_ROOT}##g"|sed -e "s#\(.*\)#\"\1\"#" > %{name}-all-files-list
cat %{name}-defined-files-list | cut -f2 -d' ' | sed -e "s#\(.*\)#\"\1\"#" | sort > %{name}-defined-files-list.tmp
cat %{name}-all-files-list | sort > %{name}-auto-files-list.tmp
diff -e %{name}-defined-files-list.tmp %{name}-auto-files-list.tmp | grep "^\"" > %{name}-auto-files-list
cat %{name}-defined-files-list %{name}-auto-files-list > %{name}-files-list



%clean
%__rm -rf %buildroot

%files -f %{name}-files-list
%defattr(-,root,root, -)


# The post and postun update the man page database
%post


%postun


%changelog



#end raw
