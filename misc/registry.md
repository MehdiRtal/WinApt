# Registry

The registry file is a JSON document with a single top-level JSON object which follows the schema
described in [packages.schema.json](../packages.schema.json). This document roughly
describes the format of the registry file for humans :smile:

There are no examples in this document, [the registry file](../packages.schema.json) itself is a
living example of what you can do.

## Top Level

The top-level JSON object must contain two keys:

- `version`: Contains the version of the registry file and is used to prompt upgrades from older
  versions of just-install. The version is bumped each time we make a backward-incompatible change
  to the file format.
- `packages`: This is a JSON object. Each key represents a package name and the value is itself a
  JSON object that contains the software version and instructions to get the installer. See "Package
  Entry" below for a description.

## Package Entry

Each entry is a JSON object that must contain at least the following two keys:

- `installer`: A JSON object which describes where the installer is and how to run it once
  downloaded. See "Installer Options" below for a description.
- `version`: The software's version. If you are adding an unversioned link that always points to the
  latest stable version use `latest` here.

The following key is optional:

- `skipAudit`: A boolean value that indicates whether CI should skip audits for this package. Use
  with care.

## Installer

This JSON object must contain at least the following two keys:

- `installer`: It can be one of the following:
  - `advancedinstaller`: Silently installs Advanced Installer packages;
  - `as-is`: Will run the executable as-is;
  - `copy`: Copy the file according to the `destination` parameter;
  - `custom`: Allows you to specify how to call the installer according to the `arguments` parameter;
  - `innosetup`: Silently installs InnoSetup packages;
  - `msi`: Silently installs Windows Installer packages;
  - `nsis`: Silently installs NSIS packages;
  - `squirrel`: Silently installs Squirrel packages;
