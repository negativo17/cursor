# Download URL, version and hash from:
# https://github.com/oslook/cursor-ai-downloads/blob/main/version-history.json
%global dl_hash 07aa3b4519da4feab4761c58da3eeedd253a1671

%global desktop_id co.anysphere.cursor

%global debug_package %{nil}

# Build id links are sometimes in conflict with other RPMs.
%define _build_id_links none

# Remove bundled libraries from requirements/provides
%global __requires_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libvk_swiftshader\\.so.*|libvulkan\\.so.*|/usr/bin/node)$
%global __provides_exclude ^(libffmpeg\\.so.*|libEGL\\.so.*|libGLESv2\\.so.*|libvk_swiftshader\\.so.*|libvulkan\\.so.*|/usr/bin/node)$

Name:       cursor
Version:    1.4.2
Release:    1%{?dist}
Summary:    AI-first coding environment
License:    Proprietary
URL:        https://www.cursor.com/

Source0:    https://downloads.cursor.com/production/%{dl_hash}/linux/x64/Cursor-%{version}-x86_64.AppImage
Source1:    https://downloads.cursor.com/production/%{dl_hash}/linux/arm64/Cursor-%{version}-aarch64.AppImage
Source2:    %{name}-wrapper
Source3:    %{desktop_id}.appdata.xml

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:   hicolor-icon-theme

# Bundled libraries in AppImage's /usr/lib:
Requires:   GConf2
Requires:   libappindicator
Requires:   libnotify
Requires:   libXScrnSaver
Requires:   libXtst

%description
Cursor AI is an AI-powered code editor that aims to enhance developer
productivity by offering features like AI-driven code suggestions, codebase
understanding, and natural language code editing.

%prep
%setup -c -T

%ifarch x86_64
chmod +x %{SOURCE0}
%{SOURCE0} --appimage-extract
%endif

%ifarch aarch64
chmod +x %{SOURCE1}
%{SOURCE1} --appimage-extract
%endif

# Throw away unused stuff:
rm -fr \
  squashfs-root%{_prefix}/bin \
  squashfs-root%{_prefix}/lib \
  squashfs-root%{_datadir}/appdata

# Adjust paths:
mkdir -p squashfs-root%{_libdir}
mv squashfs-root%{_datadir}/%{name} squashfs-root%{_libdir}/%{name}
mv squashfs-root%{_datadir}/zsh/vendor-completions squashfs-root%{zsh_completions_dir}
sed -i -e 's|Exec=%{_datadir}/%{name}|Exec=%{_libdir}/%{name}|g' squashfs-root%{_datadir}/applications/*

%install
mkdir -p %{buildroot}%{_prefix}
cp -fra squashfs-root%{_prefix}/* %{buildroot}%{_prefix}/

mkdir %{buildroot}%{_bindir}
cat %{SOURCE2} | sed -e 's|INSTALL_DIR|%{_libdir}/%{name}|g' \
    > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

install -p -m 0644 -D %{SOURCE3} %{buildroot}%{_metainfodir}/%{desktop_id}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.appdata.xml

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-url-handler.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/mime/packages/%{name}-workspace.xml
%{_datadir}/pixmaps/%{desktop_id}.png
%{_libdir}/%{name}
%{_metainfodir}/%{desktop_id}.appdata.xml
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}

%changelog
* Thu Aug 07 2025 Simone Caronni <negativo17@gmail.com> - 1.4.2-1
- Update to version 1.4.2.

* Fri Aug 01 2025 Simone Caronni <negativo17@gmail.com> - 1.3.8-1
- Update to version 1.3.8.

* Sun Jul 27 2025 Simone Caronni <negativo17@gmail.com> - 1.3.3-1
- Update to version 1.3.3.

* Thu Jul 24 2025 Simone Caronni <negativo17@gmail.com> - 1.3.0-1
- Update to version 1.3.0.

* Mon Jul 14 2025 Simone Caronni <negativo17@gmail.com> - 1.2.4-1
- Update to version 1.2.4.

* Thu Jul 10 2025 Simone Caronni <negativo17@gmail.com> - 1.2.3-1
- Update to version 1.2.3.

* Tue Jul 08 2025 Simone Caronni <negativo17@gmail.com> - 1.2.2-1
- Update to version 1.2.2.

* Thu Jul 03 2025 Simone Caronni <negativo17@gmail.com> - 1.2.1-1
- Update to version 1.2.1.

* Wed Jun 25 2025 Simone Caronni <negativo17@gmail.com> - 1.1.6-1
- Update to version 1.1.6.

* Tue Jun 24 2025 Simone Caronni <negativo17@gmail.com> - 1.1.5-1
- Update to version 1.1.5.

* Thu Jun 19 2025 Simone Caronni <negativo17@gmail.com> - 1.1.4-1
- Update to version 1.1.4.

* Fri Jun 13 2025 Simone Caronni <negativo17@gmail.com> - 1.1.2-1
- Update to version 1.1.2.

* Sat Jun 07 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0-1
- Update to version 1.0.0.

* Mon May 26 2025 Simone Caronni <negativo17@gmail.com> - 0.50.7-1
- Update to version 0.50.7.

* Mon May 19 2025 Simone Caronni <negativo17@gmail.com> - 0.50.5-1
- Update to version 0.50.5.

* Sat Apr 26 2025 Simone Caronni <negativo17@gmail.com> - 0.49.6-1
- Update to version 0.49.6.

* Tue Apr 22 2025 Simone Caronni <negativo17@gmail.com> - 0.49.4-1
- Update to version 0.49.4.

* Mon Apr 14 2025 Simone Caronni <negativo17@gmail.com> - 0.48.9-1
- Update to version 0.48.9.

* Mon Apr 07 2025 Simone Caronni <negativo17@gmailc.om> - 0.48.7-1
- First build.
