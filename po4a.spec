Name: po4a
Version: 0.40.1
Release: 1%{?dist}
Summary: A tool maintaining translations anywhere
Group: Applications/System
# Nothing in the source tree specifies a version of the GPL.
License: GPL+
URL: http://alioth.debian.org/projects/po4a/
Source0: http://alioth.debian.org/frs/download.php/3341/%{name}-v%{version}.tar.gz
Patch0: %{name}-%{version}.diff

BuildArch: noarch
BuildRequires: perl(Module::Build)
BuildRequires: perl(Text::WrapI18N)
BuildRequires: perl(SGMLS) >= 1.03ii
BuildRequires: perl(Locale::gettext) >= 1.01
BuildRequires: perl(Term::ReadKey)
BuildRequires: /usr/bin/xsltproc
BuildRequires: gettext
BuildRequires: docbook-style-xsl

# Requires a pod2man which support --utf8
# Seemingling added in perl-5.10.1
BuildRequires: perl >= 4:5.10.1

# Required by the tests.
BuildRequires: perl(Test::More)
BuildRequires: /usr/bin/kpsewhich

Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: gettext

# Optional, used by Locale/Po4a/TeX.pm
# Requires: /usr/bin/kpsewhich
# Optional, used by po4a-build
# Requires: /usr/bin/xsltproc
# Optional, but package is quite useless without
Requires: perl(Locale::gettext) >= 1.01

%description
The po4a (po for anything) project goal is to ease translations (and
more interestingly, the maintenance of translations) using gettext
tools on areas where they were not expected like documentation.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1
# Get rid of /usr/bin/env
sed -i -e 's,#! /usr/bin/env perl,#!/usr/bin/perl,' \
po4a po4a-gettextize po4a-translate po4a-updatepo po4a-normalize scripts/msguntypot

%build
# Propagate %%{_prefix}
sed -i -e 's,^prefix =.*$,prefix = %{_prefix},' po/bin/Makefile
# Install to vendor dirs
sed -i -e 's,perl Build.PL,perl Build.PL --installdirs vendor,' Makefile
make

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -or -name perllocal.pod \
  -or \( -name '*.bs' -a -empty \) \) -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}

%find_lang %{name}

%check
./Build test

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
%{_mandir}/man3/Locale::Po4a::*.3*
%{_mandir}/man5/po4a-build.conf*.5*
%{_mandir}/man7/po4a-runtime.7*
%{_mandir}/man7/po4a.7*
%{_mandir}/*/man1/po4a*.1*
%{_mandir}/*/man1/msguntypot.1*
%{_mandir}/*/man3/Locale::Po4a::*.3*
%{_mandir}/*/man5/po4a-build.conf.5*
%{_mandir}/*/man7/po4a.7*
%{_mandir}/*/man7/po4a-runtime.7*

%changelog
* Fri Oct 15 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.40.1-1
- Upstream update.
- Add po4a-v0.40.1.diff (add missing file t/compare-po.pl)
- Make testsuite working.
- Spec overhaul.
- Eliminate /usr/bin/env perl.
- Require perl >= 5.10.1

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.35-15
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.35-14
- rebuild against perl 5.10.1

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

