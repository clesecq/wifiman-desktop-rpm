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
Prebuilt RPMs are attached to each [release](https://github.com/clesecq/wifiman-desktop-rpm/releases). Install the latest one directly:

```sh
dnf install https://github.com/clesecq/wifiman-desktop-rpm/releases/download/wifiman-desktop-1.3.0-1/wifiman-desktop-1.3.0-1.x86_64.rpm
```

Or download it with the GitHub CLI and install the local file:

```sh
gh release download --repo clesecq/wifiman-desktop-rpm --pattern '*.x86_64.rpm'
dnf install ./wifiman-desktop-*.x86_64.rpm
```

On rpm-ostree based systems (Silverblue, Kinoite, ...), use `rpm-ostree install ./wifiman-desktop-*.x86_64.rpm` and reboot.

Once installed you can enable and start the daemon using the following command, then launch the application.

```sh
systemctl enable --now wifiman-desktop.service
```
