%define gcj_support             0
%define sname                   postgresql
%define postgresql_version      8.3
%define postgresql_jdbc_release 603

Name:           postgresql-jdbc
Version:        %{postgresql_version}.%{postgresql_jdbc_release}
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        PostgreSQL JDBC driver
License:        BSD
Group:          Development/Java
URL:            http://jdbc.postgresql.org/
Source0:        http://jdbc.postgresql.org/download/postgresql-jdbc-%{postgresql_version}-%{postgresql_jdbc_release}.src.tar.gz
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps
BuildRequires:  ant-trax
BuildRequires:  docbook-style-xsl
BuildRequires:  java-devel >= 0:1.4.0
BuildRequires:  jaxp_transform_impl
# GNU jaxp_transform_impl doesn't work
BuildRequires:  xalan-j2
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The PostgreSQL JDBC driver allows Java programs to connect to a
PostgreSQL database using standard, database independent Java code.
The driver provides are reasonably complete implementation of the
JDBC 3 specification in addition to some PostgreSQL specific
extensions.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.

%prep
%setup -q -n %{name}-%{postgresql_version}-%{postgresql_jdbc_release}.src 
%{_bindir}/find . -type f -name "*.class" | %{_bindir}/xargs -t %{__rm}
#%{__perl} -pi -e 's/<xslt/<xslt processor="trax"/' build.xml

%build
export CLASSPATH=
export OPT_JAR_LIST=
sh ./update-translations.sh
%{ant} -Dbuild.compiler=modern -Dant.build.javac.source=1.5

DOCBOOK_STYLESHEET=`rpm -ql docbook-style-xsl | %{__grep} /html/chunk.xsl`
DOCBOOK_XSL=`echo ${DOCBOOK_STYLESHEET} | %{__sed} 's|/html/chunk.xsl||'`

if test ! -d "${DOCBOOK_XSL}"; then
  echo "Unable to find docbook xsl directory"
  exit 1
fi

if test ! -f "${DOCBOOK_STYLESHEET}"; then
  echo "Unable to find docbook xsl stylesheet"
  exit 1
fi

if [ -z "$SGML_CATALOG_FILES" -a -e %{_sysconfdir}/sgml/catalog ] ; then
  export SGML_CATALOG_FILES=%{_sysconfdir}/sgml/catalog
fi

export OPT_JAR_LIST="ant/ant-nodeps ant/ant-trax xalan-j2 xalan-j2-serializer"
%{ant} -Ddocbook.stylesheet=${DOCBOOK_STYLESHEET} -Ddocbook.xsl=${DOCBOOK_XSL} doc

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a jars/%{sname}.jar %{buildroot}%{_javadir}/%{sname}-%{version}.jar
(cd %{buildroot}%{_javadir} && %{__ln_s} %{sname}-%{version}.jar %{sname}.jar)
%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE README
%{_javadir}/*.jar
%{gcj_files}

%files manual
%defattr(0644,root,root,0755)
%doc build/doc/build/doc/*


