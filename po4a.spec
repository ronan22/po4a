Name: po4a
Version: 0.35
Release: 13%{?dist}
Summary: A tool maintaining translations anywhere
Group: Applications/System
# Nothing in the source tree specifies a version of the GPL.
License: GPL+
URL: http://alioth.debian.org/projects/po4a/
Source0: http://alioth.debian.org/frs/download.php/2809/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: perl(Module::Build)
BuildRequires: perl(Text::WrapI18N)
BuildRequires: perl(SGMLS) >= 1.03ii
BuildRequires: perl(Locale::gettext) >= 1.01, gettext
BuildRequires: perl(Term::ReadKey)

# Required by the tests.
BuildRequires: perl(Test::More)
BuildRequires: docbook-dtds

Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
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
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}

%find_lang %{name}

# ugly fix to get the translated man pages in utf-8
for file in  %{buildroot}%{_mandir}/*/man*/*.gz; do
  gunzip -c $file | iconv -f latin1 -t utf8 | gzip -c > $file.new
  mv -f $file.new $file
done

%check
# The tests are unclean
./Build test ||:

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README* COPYING TODO
%{_bindir}/po4a*
%{_bindir}/msguntypot
%{perl_vendorlib}/Locale
%{_mandir}/man1/po4a*.1*
%{_mandir}/man1/msguntypot.1*
%{_mandir}/man3/Locale::Po4a::*.3pm*
%{_mandir}/man7/po4a.7*
%{_mandir}/*/man1/po4a*.1*
%{_mandir}/*/man1/msguntypot.1*
%{_mandir}/*/man3/Locale::Po4a::*.3pm*
%{_mandir}/*/man7/po4a.7*


%changelog
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.35-11
- Update to 0.35.

* Tue Jan 13 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.34-10
- Add BuildRequires: perl(Test::More), BuildRequires: docbook-dtds.
- Activate tests.
- Fix Source0:-URL.
- Spec file cosmetics.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.34-9
- Update to 0.34.

* Sun Jun 01 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-8
- Let package own %%{perl_vendorlib}/Locale (BZ 449258).

* Thu May 22 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-7
- Remove || : in %%check due to rpm not accepting it anymore.

* Thu May 22 2008 Ralf Corsépius <rc040203@freenet.de> - 0.32-6
- Add: "Requires: perl(:MODULE_COMPAT_...)" (BZ 442548).

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.32-5
- fix license tag

* Mon Aug 20 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.32-4
- Update to 0.32.
- fixes a possible race condition under /tmp (no CVE yet).

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.29-3
- Update to 0.29.

* Sat Feb 18 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

