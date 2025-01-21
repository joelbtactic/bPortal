# Progressive Web APP Setup

This document explains how to configure the PWA settings for your bPortal.

## bPortal Settings

### Core Settings

These are the **essential settings** that define the behavior and appearance of your PWA:

1. **`PWA_APP_NAME`**
   - The name displayed on the home screen when the app is installed.
   - Default: `bPortal`.

2. **`PWA_APP_DESCRIPTION`**
   - A short description displayed in installation dialogs or app details.
   - Default: `Your bPortal`.

3. **`PWA_APP_DISPLAY`**
   - Determines how the app appears when launched:
     - `standalone`: Launches like a native app.
     - `fullscreen`: Covers the entire screen.
     - `minimal-ui`: Shows minimal browser UI.
   - Default: `standalone`. Modify only if necessary.

4. **`PWA_APP_ORIENTATION`**
   - Controls screen orientation:
     - `portrait`: Locked to portrait mode.
     - `landscape`: Locked to landscape mode.
     - `any`: Supports both orientations.
   - Default: `any`.

### Icons and Splash Screens

These settings are used for branding your app on devices. By default, it uses bTactic logos and icons:

7. **`PWA_APP_ICONS`**
   - Configures the icons of your **bPortal** in different sizes for various devices and screen resolutions.
   - Refer to the **official documentation** for size and format guidelines.

8. **`PWA_APP_ICONS_APPLE`**
   - Provides Apple-specific icons for devices like iPhones and iPads.
   - Refer to Apple's requirements for icon dimensions and specifications.

9. **`PWA_APP_SPLASH_SCREEN`**
   - Configures images for the splash screen displayed when the app is launched.
   - Ensure the images match the recommended dimensions for a seamless experience.

10. **`PWA_APP_SCREENSHOTS`**
    - Specifies screenshots shown in app store-like environments or browser install prompts.
    - Use screenshots that showcase key app features.

### Debugging and Development Settings

11. **`PWA_APP_DEBUG_MODE`**
    - Enables debugging mode for PWA settings. This is useful during development to quickly validate changes without relying on cached files.
    - **Only enable this setting if you are a developer.**

## Modifying PWA Settings
To modify any of the above settings, open the `settings.py` file and adjust the corresponding variables.

### Updating Icons
Default icons are located in `bPortal/portal/static/portal/img/icons/`. To change them:
1. Replace existing icons with new ones of the correct size and format.
2. Update the configuration in `settings.py`.

#### Apply Changes
If you are working in **development mode**, no additional steps are required.

To apply the changes in production, reload Apache with the following command:

```sh
service apache2 reload
```

## Install bPortal as an Application
To install bPortal as an application on your desktop or mobile devices, refer to the [pwa_installation.md](pwa_installation.md) document.
