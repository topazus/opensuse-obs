%global debug_package %{nil}

Name:           clifm
Version:        1.9
Release:        1%{?dist}
Summary:        a CLI-based, shell-like, and non-curses terminal file manager written in C
License:        GPL 2.0
URL:            https://github.com/leo-arch/clifm
Source:         https://github.com/leo-arch/clifm/archive/v%{version}.tar.gz#/v%{version}.tar.gz

BuildRequires:  gcc make pkg-config
BuildRequires:  desktop-file-utils libcap-devel libacl-devel readline-devel
# fix magic.h error
BuildRequires:  file-devel file-libs

Requires:       libcap libacl readline
# for remote filesystems support
Requires:       fuse-sshfs curlftpfs cifs-utils

%description
CliFM is a completely command-line-based, shell-like file manager able to perform all the basic operations you may expect from any other file manager.

%prep
%autosetup -n %{name}-%{version}

%build
#make %{?_smp_mflags}
%make_build

%install
install -pDm755 clifm %{buildroot}%{_bindir}/%{name}
install -pDm644 misc/clifm.desktop %{buildroot}%{_datadir}/applications/*.desktop

install -pDm644 misc/logo/clifm.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/*.svg

install -pDm644 misc/completions.bash %{buildroot}%{_datadir}/bash-completion/completions/clifm
install -pDm644 misc/completions.zsh %{buildroot}%{_datadir}/zsh/site-functions/_clifm


install -pDm644 misc/manpage %{buildroot}%{_datadir}/man/man1/clifm.1

mkdir -p %{buildroot}%{_datadir}/clifm
cp -r plugins functions %{buildroot}%{_datadir}/clifm

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%{_datadir}/bash-completion/completions/clifm
%{_datadir}/zsh/site-functions/_clifm
%{_datadir}/man/man1/clifm.1.gz
%{_datadir}/clifm

%changelog
