Summary:	The LAPACK libraries for numerical linear algebra
Name:		lapack
Version:	3.4.1
Release:	1
License:	freely distributable
Group:		Libraries
Source0:	http://www.netlib.org/lapack/%{name}-%{version}.tgz
# Source0-md5:	44c3869c38c8335c2b9c2a8bb276eb55
Patch0:		%{name}-automake_support.patch
URL:		http://www.netlib.org/lapack/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-fortran
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran77.

%package devel
Summary:	LAPACK development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
LAPACK development files.

%package -n lapacke
Summary:	Native C interface to LAPACK library routines
Group:		Libraries
Requires:	lapack = %{version}-%{release}

%description -n lapacke
This implementation provides a native C interface to LAPACK routines
to facilitate usage of LAPACK functionality for C programmers.

%package -n lapacke-devel
Summary:	Header files for LAPACKE - native C interface to LAPACK
Group:		Development/Libraries
Requires:	lapack-devel = %{version}-%{release}
Requires:	lapacke = %{version}-%{release}

%description -n lapacke-devel
Header files for LAPACKE.

%prep
%setup -q
%patch0 -p1

# directory INSTALL conflicts with file INSTALL needed by automake
mv -f INSTALL INSTALLSRC
# copy selected routines; use INT_ETIME versions of second
cp -f INSTALLSRC/{ilaver,slamch,dlamch,second_INT_ETIME,dsecnd_INT_ETIME}.f SRC

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# present both in blas and lapack
rm -f man/manl/{lsame,xerbla}.l

%clean
rm -fr $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %ghost %{_libdir}/libblas.so.?
%attr(755,root,root) %ghost %{_libdir}/liblapack.so.?
%attr(755,root,root) %{_libdir}/libblas.so.*.*.*
%attr(755,root,root) %{_libdir}/liblapack.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblas.so
%attr(755,root,root) %{_libdir}/liblapack.so
%{_libdir}/libblas.la
%{_libdir}/liblapack.la
%{_pkgconfigdir}/blas.pc
%{_pkgconfigdir}/lapack.pc

%files -n lapacke
%defattr(644,root,root,755)
%doc lapacke/{LICENSE,README}
%attr(755,root,root) %{_libdir}/liblapacke.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblapacke.so.2

%files -n lapacke-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblapacke.so
%{_libdir}/liblapacke.la
%{_includedir}/lapacke*.h
%{_pkgconfigdir}/lapacke.pc

