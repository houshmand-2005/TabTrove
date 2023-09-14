<p align="center">
      <img width="140" height="140" src="readme_files/logo.jpg">
</p>
<h1 align="center"/>TabTrove</h1>
<p align="center">
    A Browser Collection Manager
</p>
<hr/>

**Table of Contents**

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Browsers Notes](#browsers-notes)
- [Supported Browsers](#supported-browsers)

## Description

TabTrove is a Browser Collection Manager that allows you to manage collections of browser tabs and open them in your preferred web browser. You can create, organize, and open collections of URLs, making it easy to access your favorite websites or work-related tabs with just a few clicks.

## Requirements

To use this program, you need the following:

- Python 3.10+
- Python packages: `lz4`, `rich`

## Installation

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/houshmand-2005/TabTrove.git
   ```

2. Navigate to the project directory:

   ```shell
   cd TabTrove
   ```

3. Install the required Python packages using pip:

   ```shell
   pip install lz4 rich
   ```

## Usage

You can run the program by executing the `tabtrove.py` script. It provides a menu-based interface with the following options:

1. **Open a Collection:** Open a previously created collection of URLs in your web browser.
2. **Add a Collection:** Create a new collection of URLs.

Follow the on-screen prompts to use the program effectively.

## Configuration

The program uses a `config.json` file to store browser and collection information. You can configure your browser paths and manage collections through this file. Here's an example of the `config.json` structure:

```json
{
  "browsers": {
    "firefox": {
      "excitable_path": "",
      "profile_path": ""
    },
    "edge": {
      "excitable_path": ""
    }
  },
  "collections": {}
}
```

- `browsers`: Configure your preferred web browsers, specifying the executable paths and profile paths <sub>(to read your open tabs)</sub>.
- `collections`: Manage your collections of URLs within this section.

**Note**: Be careful when editing the `config.json` file, read [here](#browsers-notes) for more details

## Browsers Notes

if you don't know where is your browser profile path you can read this:

windows:

```shell
C:\Users\<username>\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.default
```

linux:

```shell
/home/<username>/.mozilla/firefox/xxxxxxxx.default
```

## Supported Browsers

There is no limit to open tabs in other browsers, and you can add the executable file of your favorite browser to the [config](#configuration) and open tabs inside it.
But for reading open tabs and saving them, only **Firefox** browser is currently supported.
<br>
Other browsers don't make their session files easily available and sometimes they encrypt them, so it takes a lot of time to support the rest of the browsers.

<hr>
<div align="center">
<img src="readme_files/tabtrove.gif" width="710" height="380"/>
</div>
