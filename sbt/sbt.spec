%global debug_package %{nil}

Name:           sbt
Version:        1.8.0
Release:        1%{?dist}
Summary:        the interactive build tool
License:        ASL 2.0
URL:            https://github.com/sbt/sbt
Source:         https://github.com/sbt/sbt/releases/download/v%{version}/sbt-%{version}.tgz

BuildRequires:  pkg-config

%description
the interactive build tool

%prep
%autosetup -n sbt

%build

%install
mkdir -p %{buildroot}/opt/sbt
cp -r * %{buildroot}/opt/sbt

%check


%files
%dir /opt/sbt
/opt/sbt/*
/etc/profile.d/sbt.sh

%ghost /usr/bin/sbt
%post
ln -sf /opt/sbt/bin/sbt /usr/bin/sbt

%changelog
