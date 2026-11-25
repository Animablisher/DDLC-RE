# DDLC-RE
An Arabic localization &amp; an Android port of Doki Doki Literature Club!

## Introduction

**Doki Doki Literature Club! RE (DDLC:RE)** is an **Arabic localization** and an **Android port** of *Doki Doki Literature Club!*

I've always wanted to port **Doki Doki Literature Club! (DDLC)** to Android with Arabic support, ever since around 2021. There has already been a localization patch, and I initially intended to port **it** to Android. However, it was bad; it was poorly-handled, it censored certain dialogue lines, and even failed to get some important points across.

Therefore, I, **Amine Oussous, the Ultimate Weeb**, took it upon myself to restart from zero, retranslating the whole game myself (yes, I am also a translator, I just didn't plan on translating the game at first), maintaining the original vision of the developer, fixing all issues, and adding or improving things that the old localization didn't.

The first version of my localization (**v1.0.0**) launched on **24 July 2026**. There were issues, but it was **finished** and fully playable. All that mattered at the time was releasing the project and avoiding further delays. As of **06 November 2026**, the latest version (**v1.0.7**) is the most stable and bug-free release, fixing all of the issues. But that's not the end, as many extra features are planned for the unknown future.

---

## Features

- **Full Arabic translation**: The whole game is fully localized to Arabic, dialogues and menus alike, with the ability to switch into English at any time from the game settings.
- **Full Android support**: The code has been modified to support Android, and it plays exactly like the PC version, and supports **all** Android versions (including Android 14+).
- **Basic Android modding support**: It's still very basic, but it lets you put custom `.rpy` files in the `mods` folder to override the game's script and change or add features. You can add images and audio there as well. Basically, you can manipulate the game on Android however you like if you know how to write Ren'Py code. Everything you need to know is available on the [Ren'Py Documentation](https://www.renpy.org/doc/html/index.html)
- **Ease of patching**: Reformatted the poems and some lines to make patching and localization much easier. I even made a translation template if you want, [here](https://github.com/Animablisher/DDLC-RE/releases/download/v1.0.7/DDLC-RE.Translation.Template.zip)
- **Subtitles for the end credits.**

---

## Downloads

> ⚠️ **Don't download anything yet!**
> Read what's below first, then come back to download (or download this README file for later).

There are three ways to download as of now, choose the one that you like:

1. [GitHub Releases](https://github.com/Animablisher/DDLC-RE/releases)
2. [My Neocities website](https://animablisher.neocities.org/ddlc_re)
3. **Torrent**: do you like torrents? Because I made one! [Torrent link](https://archive.org/download/ddlc-re-1.0.7/ddlc-re-1.0.7_archive.torrent)
   - On PC, I use [qBittorrent](https://www.qbittorrent.org/).
   - On Android, I use [LibreTorrent](https://github.com/proninyaroslav/libretorrent).
   - **Please seed the torrent if you care.**

---

## How to Install on Windows

1. Download the game from [Dan Salvato's itch.io store page](https://teamsalvato.itch.io/ddlc).
2. Download the **`DDLC-RE v1.0.7.zip`** file from the [Releases](https://github.com/Animablisher/DDLC-RE/releases/download/v1.0.7/DDLC-RE.v1.0.7.zip).
3. Extract the game.
4. Extract the file and copy its content (`DDLCRE.exe`, `game`, `lib`, ...) into the game's main directory.

And that's it!

---

## How to Install on Android

### 1. Choosing the right APK

What's your Android version?

- **Android 14 or above:** download **`DDLC-RE r7 v1.0.7.apk`** from [here](https://github.com/Animablisher/DDLC-RE/releases/download/v1.0.7/DDLC-RE.r7.v1.0.7.apk).
- **Below Android 14:** download **`DDLC-RE r6 v1.0.7.apk`** from [here](https://github.com/Animablisher/DDLC-RE/releases/download/v1.0.7/DDLC-RE.r6.v1.0.7.apk).

### 2. Game crash issue

On some devices, the game might crash immediately after choosing a language. You can fix that by downloading [this file](https://github.com/Animablisher/DDLC-RE/releases/download/v1.0.7/r7.crash.fix.zip), extracting **`options.rpy`** from it, and putting it into the `renpy/ddlc/mods` directory.

---

## How to Build

*(Skip this section if you're not a developer.)*

The files in this repo can easily be patched into the game, allowing you to export a PC or Android build right off the bat.

### What you need

- The original game
- [**rpaExtract**](https://iwanplays.itch.io/rpaex)
- [**unrpyc**](https://github.com/CensoredUsername/unrpyc)
- The patch files [**here**](https://github.com/Animablisher/DDLC-RE/releases/download/v1.0.7/DDLC-RE.v1.0.7.Decompiled.zip)
- [Ren'Py **6.99.14.3**](https://www.renpy.org/release/6.99.14.3) — **do NOT use Ren'Py 7 or 8 unless you know what you're doing!!**

### Steps

1. Decompile the `.RPA` archives using **rpaExtract**.
2. Decode the `.RPYC` files into `.RPY` using **unrpyc**.
3. Copy the patch files into the game's directory (all of them **except** `_Engine Patches`).
4. The `_Engine Patches` folder contains **necessary** files that you should copy to Ren'Py's main directory. Take the `renpy` folder (from the `Ren'Py v6.99.14` folder) and copy it to the `renpy-6.99.14.3-sdk` directory. It should overwrite three `.py` files.

Those three files are an **Android compatibility patch** for Ren'Py 6. They change where native files (such as `log.txt` and `traceback.txt`) are saved, and also bypass **Scoped Storage** limitations (Thanks, Google, but you can't "protect the users" from me).

And that's it! Very easy! Once you open Ren'Py, you can launch the project and it will work with no issues.

---

## Conclusion

The DDLC:RE project is planned to be maintained every now and then (or once every blood moon). So, if you coded any feature you think I should add, open a **Pull Request**, or you can DM me on [Facebook](https://www.facebook.com/AmineOussousWeeb).

Suggestions are welcome as well, as long as they're reasonable and not drastic changes or additions.

