import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
// Use the container's pre-installed Chromium; never download a browser.
Config.setBrowserExecutable(
  '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'
);
Config.setChromiumOpenGlRenderer('angle-egl');
