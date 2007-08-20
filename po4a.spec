Name: po4a
Version: 0.32
Release: 4%{?dist}
Summary: A tool maintaining translations anywhere
Group: Applications/System
License: GPL
URL: http://alioth.debian.org/projects/po4a/
Source0: http://alioth.debian.org/download.php/1798/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: perl(Module::Build)
BuildRequires: perl(Text::WrapI18N)
BuildRequires: perl(SGMLS) >= 1.03ii
BuildRequires: perl(Locale::gettext) >= 1.01, gettext
BuildRequires: perl(Term::ReadKey)
Requires: gettext

%description
The po4a (po for anything) project goal is to ease translations (and
more interestingly, the maintenance of translations) using gettext
tools on areas where they were not expected like documentation.

%prep
%setup -q

%build
perl Build.PL --installdirs vendor
./Build

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -or -name perllocal.pod \
  -or \( -name '*.bs' -a -empty \) \) -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \;
chmod -R u+w %{buildroot}

%find_lang %{name}

# ugly fix to get the translated man pages in utf-8
for file in  %{buildroot}%{_mandir}/*/man*/*.gz; do
  gunzip -c $file | iconv -f latin1 -t utf8 | gzip -c > $file.new
  mv -f $file.new $file
done

%check || :
# check is currently broken due to absence of data-23/fonts
#./Build test verbose=1

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README* COPYING TODO
%{_bindir}/po4a*
%{_bindir}/msguntypot
%{perl_vendorlib}/Locale/Po4a
%{_mandir}/man1/po4a*.1*
%{_mandir}/man1/msguntypot.1*
%{_mandir}/man3/Locale::Po4a::*.3pm*
%{_mandir}/man7/po4a.7*
%{_mandir}/*/man1/po4a*.1p*
%{_mandir}/*/man1/msguntypot.1*
%{_mandir}/*/man3/Locale::Po4a::*.3pm*
%{_mandir}/*/man7/po4a.7*


%changelog
* Mon Aug 20 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.32-4
- Update to 0.32.
- fixes a possible race condition under /tmp (no CVE yet).

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.29-3
- Update to 0.29.

* Sat Feb 18 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

