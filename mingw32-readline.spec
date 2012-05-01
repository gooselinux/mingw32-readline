%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-readline
Version:        5.2
Release:        7%{?dist}.4
Summary:        MinGW port of readline for editing typed command lines


License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source0:        ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:         readline-5.2-shlib.patch
Patch2:         readline-5.2-001.patch
Patch3:         readline-5.2-002.patch
Patch4:         readline-5.2-003.patch
Patch5:         readline-5.2-004.patch
Patch6:         readline-5.2-005.patch
Patch7:         readline-5.2-006.patch
Patch8:         readline-5.2-007.patch
Patch9:         readline-5.2-008.patch
Patch10:        readline-5.2-009.patch
Patch11:        readline-5.2-010.patch
Patch12:        readline-5.2-011.patch
Patch13:        readline-5.2-redisplay-sigint.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 49
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-termcap >= 1.3.1-3


%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

This is a port of the library and development tools to Windows.


%prep
%setup -q -n readline-%{version}
%patch1 -p1 -b .shlib
%patch2 -p0 -b .001
%patch3 -p0 -b .002
%patch4 -p0 -b .003
%patch5 -p0 -b .004
%patch6 -p0 -b .005
%patch7 -p0 -b .006
%patch8 -p0 -b .007
%patch9 -p0 -b .008
%patch10 -p0 -b .009
%patch11 -p0 -b .010
%patch12 -p0 -b .011
%patch13 -p1 -b .redisplay-sigint

pushd examples
rm -f rlfe/configure
iconv -f iso8859-1 -t utf8 -o rl-fgets.c{_,}
touch -r rl-fgets.c{,_}
mv -f rl-fgets.c{_,}
popd


%build
%{_mingw32_configure} --enable-shared
make SHLIB_LIBS=-ltermcap

# Rebuild the DLLs correctly and create implibs.
pushd shlib
%{_mingw32_cc} -shared -o readline.dll -Wl,--out-implib,libreadline.dll.a readline.so vi_mode.so funmap.so keymaps.so parens.so search.so rltty.so complete.so bind.so isearch.so display.so signals.so util.so kill.so undo.so macro.so input.so callback.so terminal.so text.so nls.so misc.so xmalloc.so history.so histexpand.so histfile.so histsearch.so shell.so mbutil.so tilde.so compat.so -ltermcap
%{_mingw32_cc} -shared -o history.dll -Wl,--out-implib,libhistory.dll.a history.so histexpand.so histfile.so histsearch.so shell.so mbutil.so xmalloc.so
popd


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove the fake .so files and install our DLLs and implibs.
pushd shlib
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/lib*.so.*
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
install readline.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install libreadline.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}
install history.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install libhistory.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}
popd

# Don't want the info files or manpages which duplicate the native package.
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}

# Don't want the static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libhistory.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libreadline.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/readline.dll
%{_mingw32_bindir}/history.dll
%{_mingw32_libdir}/libreadline.dll.a
%{_mingw32_libdir}/libhistory.dll.a
%{_mingw32_includedir}/readline/


%changelog
* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 5.2-7.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 5.2-7.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 5.2-7.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 5.2-7.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 5.2-5
- Rebuild for mingw32-gcc 4.4

* Sat Nov 22 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-4
- Rename *.dll.a to lib*.dll.a so that libtool can use these libraries.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-3
- Fix paths to mandir, infodir.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-2
- Rebuild against latest termcap.

* Thu Sep 25 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-1
- Initial RPM release.
