dnl  Copyright 2015 Red Hat, Inc.
dnl 
dnl  Permission to use, copy, modify, distribute, and sell this software and its
dnl  documentation for any purpose is hereby granted without fee, provided that
dnl  the above copyright notice appear in all copies and that both that
dnl  copyright notice and this permission notice appear in supporting
dnl  documentation, and that the name of Red Hat not be used in
dnl  advertising or publicity pertaining to distribution of the software without
dnl  specific, written prior permission.  Red Hat makes no
dnl  representations about the suitability of this software for any purpose.  It
dnl  is provided "as is" without express or implied warranty.
dnl 
dnl  RED HAT DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
dnl  INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
dnl  EVENT SHALL RED HAT BE LIABLE FOR ANY SPECIAL, INDIRECT OR
dnl  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
dnl  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
dnl  TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
dnl  PERFORMANCE OF THIS SOFTWARE.
dnl
dnl Process this file with autoconf to create configure.

AC_PREREQ([2.57])

#   hsakmt versioning scheme
#
#   - The version in git has an odd MICRO version number
#
#   - Released versions, have an even MICRO version number
#
#   - Versions that break ABI must have a new MAJOR number
#
#   - If you break the ABI, then at least this must be done:
#
#        - increment MAJOR
#
#        - In the first development release where you break ABI, find
#          all instances of "hsakmt-n" and change them to hsakmt-(n+1)
#
#          This needs to be done at least in 
#                    configure.ac
#                    all Makefile.am's
#                    hsakmt-n.pc.in
#
#      This ensures that binary incompatible versions can be installed
#      in parallel.  See http://www106.pair.com/rhp/parallel.html for
#      more information
#

m4_define([hsakmt_major], 1)
m4_define([hsakmt_minor], 0)
m4_define([hsakmt_micro], 0)

m4_define([hsakmt_version],[hsakmt_major.hsakmt_minor.hsakmt_micro])

AC_INIT(hsakmt, hsakmt_version, [oded.gabbay@gmail.com], hsakmt)
AM_INIT_AUTOMAKE([foreign dist-bzip2])

# Suppress verbose compile lines
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_CONFIG_HEADERS(config.h)

# Checks for programs.
AC_CANONICAL_HOST
AC_PROG_AWK
test_CFLAGS=${CFLAGS+set} # We may override autoconf default CFLAGS.
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_LIBTOOL
AC_PROG_MAKE_SET
dnl HSAKMT_LINK_WITH_ENV(env-setup, program, true-action, false-action)
dnl
dnl Compiles and links the given program in the environment setup by env-setup
dnl and executes true-action on success and false-action on failure.
AC_DEFUN([HSAKMT_LINK_WITH_ENV],[dnl
	save_CFLAGS="$CFLAGS"
	save_LDFLAGS="$LDFLAGS"
	save_LIBS="$LIBS"
	CFLAGS=""
	LDFLAGS=""
	LIBS=""
	$1
	CFLAGS="$save_CFLAGS $CFLAGS"
	LDFLAGS="$save_LDFLAGS $LDFLAGS"
	LIBS="$save_LIBS $LIBS"
	AC_LINK_IFELSE(
		[AC_LANG_SOURCE([$2])],
		[hsakmt_cc_stderr=`test -f conftest.err && cat conftest.err`
		 hsakmt_cc_flag=yes],
		[hsakmt_cc_stderr=`test -f conftest.err && cat conftest.err`
		 hsakmt_cc_flag=no])

	if test "x$hsakmt_cc_stderr" != "x"; then
		hsakmt_cc_flag=no
	fi

	if test "x$hsakmt_cc_flag" = "xyes"; then
		ifelse([$3], , :, [$3])
	else
		ifelse([$4], , :, [$4])
	fi
	CFLAGS="$save_CFLAGS"
	LDFLAGS="$save_LDFLAGS"
	LIBS="$save_LIBS"
])

dnl Find a -Werror for catching warnings.
WERROR=
for w in -Werror -errwarn; do
    if test "z$WERROR" = "z"; then
        AC_MSG_CHECKING([whether the compiler supports $w])
        HSAKMT_LINK_WITH_ENV(
		[CFLAGS=$w],
		[int main(int c, char **v) { (void)c; (void)v; return 0; }],
		[WERROR=$w; yesno=yes], [yesno=no])
	AC_MSG_RESULT($yesno)
    fi
done

dnl HSAKMT_CHECK_CFLAG(flag, [program])
dnl  Adds flag to CFLAGS if the given program links without warnings or errors.
AC_DEFUN([HSAKMT_CHECK_CFLAG], [dnl
	AC_MSG_CHECKING([whether the compiler supports $1])
	HSAKMT_LINK_WITH_ENV(
		[CFLAGS="$WERROR $1"],
		[$2
		 int main(int c, char **v) { (void)c; (void)v; return 0; }
		],
		[_yesno=yes],
		[_yesno=no])
	if test "x$_yesno" = xyes; then
	   CFLAGS="$CFLAGS $1"
	fi
	AC_MSG_RESULT($_yesno)
])

AC_CHECK_SIZEOF(long)

# Checks for Sun Studio compilers
AC_CHECK_DECL([__SUNPRO_C], [SUNCC="yes"], [SUNCC="no"])
AC_CHECK_DECL([__amd64], [AMD64_ABI="yes"], [AMD64_ABI="no"])

# Default CFLAGS to -O -g rather than just the -g from AC_PROG_CC
# if we're using Sun Studio and neither the user nor a config.site
# has set CFLAGS.
if test $SUNCC = yes &&			\
   test "x$test_CFLAGS" = "x" &&	\
   test "$CFLAGS" = "-g"
then
  CFLAGS="-O -g"
fi

# 
# We ignore hsakmt_major in the version here because the major version should
# always be encoded in the actual library name. Ie., the soname is:
#
#      hsakmt-$(hsakmt_major).0.minor.micro
#
m4_define([lt_current], [hsakmt_minor])
m4_define([lt_revision], [hsakmt_micro])
m4_define([lt_age], [hsakmt_minor])

LT_VERSION_INFO="lt_current:lt_revision:lt_age"

HSAKMT_VERSION_MAJOR=hsakmt_major()
AC_SUBST(HSAKMT_VERSION_MAJOR)
HSAKMT_VERSION_MINOR=hsakmt_minor()
AC_SUBST(HSAKMT_VERSION_MINOR)
HSAKMT_VERSION_MICRO=hsakmt_micro()
AC_SUBST(HSAKMT_VERSION_MICRO)

AC_SUBST(LT_VERSION_INFO)

# Check for dependencies

HSAKMT_CHECK_CFLAG([-Wall])
HSAKMT_CHECK_CFLAG([-Wdeclaration-after-statement])
HSAKMT_CHECK_CFLAG([-Wno-unused-local-typedefs])
HSAKMT_CHECK_CFLAG([-fno-strict-aliasing])

# Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_HEADER_STDBOOL
AC_TYPE_INT16_T
AC_TYPE_INT32_T
AC_TYPE_INT64_T
AC_TYPE_INT8_T
AC_TYPE_UINT16_T
AC_TYPE_UINT32_T
AC_TYPE_UINT64_T
AC_TYPE_UINT8_T

dnl =====================================
dnl posix_memalign, sigaction, alarm, gettimeofday

AC_CHECK_FUNC(posix_memalign, have_posix_memalign=yes, have_posix_memalign=no)
if test x$have_posix_memalign = xyes; then
   AC_DEFINE(HAVE_POSIX_MEMALIGN, 1, [Whether we have posix_memalign()])
fi

AC_CHECK_FUNC(sigaction, have_sigaction=yes, have_sigaction=no)
if test x$have_sigaction = xyes; then
   AC_DEFINE(HAVE_SIGACTION, 1, [Whether we have sigaction()])
fi

AC_CHECK_FUNC(alarm, have_alarm=yes, have_alarm=no)
if test x$have_alarm = xyes; then
   AC_DEFINE(HAVE_ALARM, 1, [Whether we have alarm()])
fi

AC_CHECK_HEADER([sys/mman.h],
   [AC_DEFINE(HAVE_SYS_MMAN_H, [1], [Define to 1 if we have <sys/mman.h>])])

AC_CHECK_FUNC(mmap, have_mmap=yes, have_mmap=no)
if test x$have_mmap = xyes; then
   AC_DEFINE(HAVE_MMAP, 1, [Whether we have mmap()])
fi

AC_CHECK_FUNC(mprotect, have_mprotect=yes, have_mprotect=no)
if test x$have_mprotect = xyes; then
   AC_DEFINE(HAVE_MPROTECT, 1, [Whether we have mprotect()])
fi

AC_CHECK_FUNC(getpagesize, have_getpagesize=yes, have_getpagesize=no)
if test x$have_getpagesize = xyes; then
   AC_DEFINE(HAVE_GETPAGESIZE, 1, [Whether we have getpagesize()])
fi

AC_CHECK_FUNC(gettimeofday, have_gettimeofday=yes, have_gettimeofday=no)
AC_CHECK_HEADER(sys/time.h, have_sys_time_h=yes, have_sys_time_h=no)
if test x$have_gettimeofday = xyes && test x$have_sys_time_h = xyes; then
   AC_DEFINE(HAVE_GETTIMEOFDAY, 1, [Whether we have gettimeofday()])
fi

AC_DEFUN([HSAKMT_CHECK_PTHREAD],[dnl
    if test "z$support_for_pthreads" != "zyes"; then
	HSAKMT_LINK_WITH_ENV(
		[$1], [pthread_test_program],
		[PTHREAD_CFLAGS="$CFLAGS"
		 PTHREAD_LIBS="$LIBS"
		 PTHREAD_LDFLAGS="$LDFLAGS"
		 support_for_pthreads=yes])
    fi
])

support_for_pthreads=no

AC_MSG_CHECKING(for pthreads)

HSAKMT_CHECK_PTHREAD([CFLAGS="-pthread"; LDFLAGS="-pthread"])
HSAKMT_CHECK_PTHREAD([CFLAGS="-D_REENTRANT"; LIBS="-lpthread"])
HSAKMT_CHECK_PTHREAD([CFLAGS="-D_REENTRANT"; LDFLAGS="-lroot"])
    
if test $support_for_pthreads = yes; then
    AC_DEFINE([HAVE_PTHREADS], [], [Whether pthreads is supported])
    if test $ac_cv_tls = none ; then
        CFLAGS="$CFLAGS $PTHREAD_CFLAGS"
    fi
fi

AC_MSG_RESULT($support_for_pthreads)

# distribute additional compiler and linker flags among Makefiles
# --> set and change these variables instead of CXXFLAGS or LDFLAGS (for user only)
AC_SUBST(TOOLCHAIN_SUPPORTS__THREAD)
AC_SUBST(HAVE_PTHREADS)
AC_SUBST(PTHREAD_LDFLAGS)
AC_SUBST(PTHREAD_LIBS)
AC_SUBST(PTHREAD_CFLAGS)
AC_SUBST(AM_CFLAGS)

# Checks for library functions.

AC_FUNC_MALLOC
AC_FUNC_MMAP
AC_CHECK_FUNCS([memchr memset strstr])

AC_OUTPUT([hsakmt-1.pc
           hsakmt-1-uninstalled.pc
           Makefile
	   hsakmt/Makefile
	   hsakmt/hsakmt-version.h])
