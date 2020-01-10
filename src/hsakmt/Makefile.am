include $(top_srcdir)/hsakmt/Makefile.sources

ext_inc_dir = $(top_srcdir)/hsakmt/include

# additional include paths necessary to compile the C library
AM_CFLAGS = -I$(ext_inc_dir) @AM_CFLAGS@

###############################################################################
# THE LIBRARIES TO BUILD
###############################################################################

lib_LTLIBRARIES = libhsakmt-1.la

libhsakmt_1_la_LDFLAGS = -version-info $(LT_VERSION_INFO) -no-undefined @PTHREAD_LDFLAGS@ 
libhsakmt_1_la_LIBADD = @PTHREAD_LIBS@ -lm
libhsakmt_1_la_SOURCES = $(libhsakmt_sources) $(libhsakmt_headers)

libhsakmtincludedir = $(includedir)/hsakmt-1
libhsakmtinclude_HEADERS = $(ext_inc_dir)/hsakmt.h $(ext_inc_dir)/hsakmttypes.h
noinst_LTLIBRARIES = 

.c.s : $(libhsakmtinclude_HEADERS)
	$(CC) $(CFLAGS) $(ASM_CFLAGS_$(@:hsakmt-%.s=%)) -DHAVE_CONFIG_H -I$(srcdir) -I$(srcdir)/include -I$(builddir) -I$(top_builddir) -S -o $@ $<
