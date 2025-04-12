# JetMaple Mono

Fusion of [JetBrains Mono](https://www.jetbrains.com/lp/mono/) and [Maple Mono](https://github.com/subframe7536/Maple-font).

**JetMaple Mono is currently built with:**

- JetBrains Mono: v2.304
- Maple Mono CN unhinted: V7.0

## Features

1. JetBrains Mono for regular text with Maple Mono for italics.
2. Ligatures support.
3. Chinese and Japanese support from Maple Mono.

## Installation

**Option 1: Download the Pre-built Fonts**

Download the latest releases from the [Releases](https://github.com/yilinfang/JetMaple-Mono/releases) and install the TTF files.

**Option 2: Build from Source**

**Prerequisites:**

- Python 3.8 or later

```bash
# Clone the repository
git clone https://github.com/yilinfang/JetMaple-Mono.git
cd JetMaple-Mono

# Set up Python environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build the fonts
chmod +x build.sh
./build.sh
```

The built fonts will be located in the `output` directory.

## Usage

After installing the TTF font files, you can use JetMaple Mono by setting your favorite code editor or terminal emulator' font to `JetMaple Mono`.

## License

This project is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).

This project combines two fonts with their own licenses:

- JetBrains Mono: [SIL Open Font License 1.1](https://github.com/JetBrains/JetBrainsMono/blob/master/OFL.txt)
- Maple Mono: [SIL Open Font License 1.1](https://github.com/subframe7536/maple-font/blob/variable/OFL.txt)

## Credit

- [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono)
- [Maple Mono](https://github.com/subframe7536/Maple-font)
