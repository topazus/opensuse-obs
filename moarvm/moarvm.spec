%global year    2022
%global month   12

Name:           moarvm
Version:        %{year}.%{month}
Release:        0
Summary:        Virtual machine for Rakudo and NQP

License:        Artistic-2.0
URL:            https://moarvm.org/
Source:         https://moarvm.org/releases/MoarVM-%{version}.tar.gz

%if 0%{?fedora} >= 33 || 0%{?mageia} >= 8 || 0%{?rhel} >= 8 || 0%{?suse_version} > 1500
%define has_libuv      1
%else
%define has_libuv      0
%endif

%if 0%{?fedora} >= 33 || 0%{?mageia} >= 8 || 0%{?suse_version} > 1500
%define has_libtommath 1
%else
%define has_libtommath 0
%endif

%if 0%{?rhel} > 0 && 0%{?rhel} < 8
%define has_libzstd    0
%else
%define has_libzstd    1
%endif

%define moar_libdir %{_libdir}/moar

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconfig(libffi)
Requires:       pkgconfig(libffi)
%if %{?has_libzstd}
BuildRequires:  pkgconfig(libzstd)
Requires:       pkgconfig(libzstd)
%endif
%if %{?has_libtommath}
BuildRequires:  pkgconfig(libtommath) >= 1.2
Requires:       pkgconfig(libtommath) >= 1.2
%endif
%if %{?has_libuv}
BuildRequires:  pkgconfig(libuv) >= 1.26
Requires:       pkgconfig(libuv) >= 1.26
%endif

%undefine _package_note_file

%description
MoarVM, short for "Metamodel On A Runtime Virtual Machine", is a virtual
machine for the Rakudo compiler and the NQP compiler toolchain.

%package        devel
Summary:        Header files for MoarVM development

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(libffi)
%if %{?has_libzstd}
Requires:       pkgconfig(libzstd)
%endif
%if %{?has_libtommath}
Requires:       pkgconfig(libtommath) >= 1.2
%endif
%if %{?has_libuv}
Requires:       pkgconfig(libuv) >= 1.26
%endif

%description devel
This package contains header files for building Rakudo with MoarVM.

%prep
%autosetup -n MoarVM-%{version}

%build
%if %{undefined build_cflags}
%define build_cflags %{optflags}
%endif
%if %{undefined build_ldflags}
%define build_ldflags %{nil}
%endif
CFLAGS="%{build_cflags}" \
LDFLAGS="%{build_ldflags} -Wl,-rpath=%{moar_libdir}" \
perl Configure.pl \
    --prefix=%{_usr} \
    --libdir=%{moar_libdir} \
    --has-libffi \
%if %{?has_libtommath}
    --has-libtommath \
%endif
%if %{?has_libuv}
    --has-libuv \
%endif
    --mastdir=%{_datadir}/nqp/lib/MAST
%{make_build}

%install
%{make_install}
chmod +x %{buildroot}%{moar_libdir}/libmoar.so

# Move the 3rd party include files into the moar subdirectory. We don't want
# to clash with include files that are provided by the operating system.
# Rakudo and NQP prepend the moar subdirectory to their include path.
for i in libatomic_ops libtommath libuv mimalloc; do
    if [ -d %{buildroot}%{_includedir}/$i ]; then
        mv %{buildroot}%{_includedir}/$i/* %{buildroot}%{_includedir}/moar/
        rmdir %{buildroot}%{_includedir}/$i
    fi
done

%files
%defattr(-, root, root)
%license Artistic2.txt LICENSE
%doc CREDITS docs/ChangeLog
%{_bindir}/moar
%{_datadir}/nqp
%{moar_libdir}

%files devel
%defattr(-, root, root)
%{_includedir}/moar
%{_datadir}/pkgconfig/moar.pc

%changelog
