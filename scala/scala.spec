%global debug_package %{nil}

Name:           scala3
Version:        3.2.0
Release:        1%{?dist}
Summary:        A next-generation compiler for Scala
License:        ASL 2.0
URL:            https://github.com/lampepfl/dotty
Source:         https://github.com/lampepfl/dotty/archive/%{version}.tar.gz

BuildRequires:  pkg-config sbt java-17-openjdk

Requires:       java-17-openjdk

%description
A next-generation compiler for Scala

%prep
%autosetup -n dotty-%{version}

%build
export JAVA_HOME=$HOME/jdk
export PATH=$JAVA_HOME/bin
sbt dist/packArchive

%install
mkdir -p %{buildroot}/opt/scala3
cp -a dist/target/pack/* %{buildroot}/opt/scala3

rm %{buildroot}/opt/scala3/bin/*.bat

#mkdir -p %{buildroot}/etc/profile.d/
# add path
#echo "export PATH=$PATH:/opt/scala3/bin" > %{buildroot}/etc/profile.d/scala3.sh

%check

%files
%dir /opt/scala3
/opt/scala3/*

%ghost /usr/bin/scala3
%ghost /usr/bin/scalac3
%ghost %{buildroot}/usr/bin/scala3doc
%post
ln -s /opt/scala3/bin/scala3 /usr/bin/scala3
ln -s /opt/scala3/bin/scalac3 /usr/bin/scalac3
ln -s /opt/scala3/bin/scala3doc /usr/bin/scala3doc

%changelog
