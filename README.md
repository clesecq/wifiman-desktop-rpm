[![Copr Build Status](https://copr.fedorainfracloud.org/coprs/coles/wifiman-desktop/package/wifiman-desktop/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/coles/wifiman-desktop/)

# RPM Package: wifiman-desktop

This repository holds the RPM package source for [wifiman-desktop](https://www.ui.com/download/app/wifiman-desktop).

> WiFiman is here to save your home or office network from sluggish surfing, endless buffering, and congested data 
> channels.

> [!NOTE]  
> This is a wrapper package of the WiFiman Desktop releases for Ubuntu available [here](https://www.ui.com/download/app/wifiman-desktop)
> and is in no way affliated with or maintained by [Ubiquity Inc](https://ui.com/) for any application support or questions please see
> [here](https://help.ui.com/hc/en-us).


## Usage
### From Copr
You can use this package by enabling the copr repository at [coles/wifiman-desktop](https://copr.fedorainfracloud.org/coprs/coles/wifiman-desktop/) as described [here](https://fedorahosted.org/copr/wiki/HowToEnableRepo).

```sh
dnf copr enable coles/wifiman-desktop
dnf install wifiman-desktop
```

### From GitHub releases
Prebuilt RPMs are attached to each [release](https://github.com/clesecq/wifiman-desktop-rpm/releases). Download the `.x86_64.rpm` from the [latest release](https://github.com/clesecq/wifiman-desktop-rpm/releases/latest), or fetch it with the GitHub CLI, then install the local file:

```sh
gh release download --repo clesecq/wifiman-desktop-rpm --pattern '*.x86_64.rpm'
dnf install ./wifiman-desktop-*.x86_64.rpm
```

On rpm-ostree based systems (Silverblue, Kinoite, ...), use `rpm-ostree install ./wifiman-desktop-*.x86_64.rpm` and reboot.

Once installed you can enable and start the daemon using the following command, then launch the application.

```sh
systemctl enable --now wifiman-desktop.service
```

## Release flow
Releases are automated with GitHub Actions and [tito](https://github.com/rpm-software-management/tito):

1. [`check-update.yml`](.github/workflows/check-update.yml) runs daily. It reads the upstream
   [manifest](https://desktop.wifiman.com/wifiman-desktop-linux-manifest.json), verifies the `.deb` checksum and,
   when a newer version is out, opens a pull request bumping `Version` (and resetting `Release` to `1`) in the spec.
2. Merging the pull request triggers [`tag.yml`](.github/workflows/tag.yml), which runs
   `tito tag --keep-version --accept-auto-changelog`, pushes the changelog commit and tag, then calls
   [`build.yml`](.github/workflows/build.yml) to build the RPM and publish the GitHub release.
3. The Copr webhook builds the new tag on [coles/wifiman-desktop](https://copr.fedorainfracloud.org/coprs/coles/wifiman-desktop/).

For packaging changes without a new upstream version, bump the release locally and push the commit and tag together;
the tag push triggers `build.yml`:

```sh
tito tag
git push --follow-tags origin main
```
