#!/usr/bin/env python3
import os
import sys
import argparse
import json
from fontTools.ttLib import TTFont
from fontTools.merge import Merger

from tqdm import tqdm


def load_config(config_path):
    """Load configuration from a JSON file"""
    file_ext = os.path.splitext(config_path)[1].lower()

    with open(config_path, "rb" if file_ext == ".toml" else "r") as f:
        if file_ext == ".json":
            return json.load(f)
        else:
            print(f"Error: Unsupported configuration file format: {file_ext}")
            print("Supported formats: .json")
            sys.exit(1)


def process_regular_font(jb_path, maple_path, output_path):
    """Process regular fonts by merging JetBrains Mono and Maple Mono"""
    print(
        f"Processing regular: {os.path.basename(jb_path)} + {os.path.basename(maple_path)}"
    )

    try:
        # Use fontTools merger to combine fonts
        # The first font in the list is the "master" font that determines most properties
        merger = Merger()
        merged_font = merger.merge([maple_path, jb_path])

        # Update font names
        style_name = (
            os.path.basename(output_path)
            .replace("JetMapleMono-", "")
            .replace(".ttf", "")
        )
        update_font_names(merged_font, style_name)

        # Save the merged font
        merged_font.save(output_path)
        print(f"  Generated: {output_path}")
    except Exception as e:
        print(f"  Error merging fonts: {e}")


def process_italic_font(maple_path, output_path):
    """Process italic fonts by simply renaming Maple Mono"""
    print(
        f"Processing italic: {os.path.basename(maple_path)} (direct copy with rename)"
    )

    try:
        # Open the Maple Mono font
        font = TTFont(maple_path)

        style_name = (
            os.path.basename(output_path)
            .replace("JetMapleMono-", "")
            .replace(".ttf", "")
        )
        update_font_names(font, style_name)

        # Save the font
        font.save(output_path)
        print(f"  Generated: {output_path}")
    except Exception as e:
        print(f"  Error processing italic font: {e}")


def update_font_names(font, style_name):
    """Update all font name fields to ensure proper classification"""
    family_name = "JetMaple Mono"
    full_name = f"JetMaple Mono {style_name}"
    postscript_name = f"JetMapleMono-{style_name}"

    # Get the name table
    name_table = font["name"]

    # Update ALL relevant name records
    # Name ID meanings:
    # 0: Copyright notice
    # 1: Font Family name
    # 2: Font Subfamily name (style)
    # 3: Unique font identifier
    # 4: Full font name
    # 5: Version string
    # 6: PostScript name
    # 16: Typographic Family name
    # 17: Typographic Subfamily name

    # First, find existing nameIDs and their platform/encoding/language settings
    name_id_settings = {}
    for record in name_table.names:
        name_id_settings[record.nameID] = (
            record.platformID,
            record.platEncID,
            record.langID,
        )

    # Update or add each required name field
    for name_id in [1, 4, 6, 16]:
        if name_id in name_id_settings:
            platform_id, plat_enc_id, lang_id = name_id_settings[name_id]

            # Set the appropriate value based on name ID
            if name_id == 1:  # Family Name
                name_table.setName(
                    family_name, name_id, platform_id, plat_enc_id, lang_id
                )
            elif name_id == 4:  # Full Name
                name_table.setName(
                    full_name, name_id, platform_id, plat_enc_id, lang_id
                )
            elif name_id == 6:  # PostScript Name
                name_table.setName(
                    postscript_name, name_id, platform_id, plat_enc_id, lang_id
                )
            elif name_id == 16:  # Typographic Family name
                name_table.setName(
                    family_name, name_id, platform_id, plat_enc_id, lang_id
                )
        else:
            # If the name ID doesn't exist, add it with standard settings
            # platformID=3, platEncID=1, langID=0x409 is Windows Unicode English
            if name_id == 1:  # Family Name
                name_table.setName(family_name, name_id, 3, 1, 0x409)
            elif name_id == 4:  # Full Name
                name_table.setName(full_name, name_id, 3, 1, 0x409)
            elif name_id == 6:  # PostScript Name
                name_table.setName(postscript_name, name_id, 3, 1, 0x409)
            elif name_id == 16:  # Typographic Family name
                name_table.setName(family_name, name_id, 3, 1, 0x409)

    # Also ensure subfamily names are set correctly
    subfamily = style_name
    for name_id in [2, 17]:  # Subfamily and Typographic Subfamily
        if name_id in name_id_settings:
            platform_id, plat_enc_id, lang_id = name_id_settings[name_id]
            name_table.setName(subfamily, name_id, platform_id, plat_enc_id, lang_id)
        else:
            name_table.setName(subfamily, name_id, 3, 1, 0x409)


def main():
    parser = argparse.ArgumentParser(
        description="Font fusion script using fontTools with configuration file"
    )
    parser.add_argument(
        "config", help="Path to configuration file (TOML, YAML, or JSON)"
    )
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Extract configuration values
    jetbrains_dir = config.get("jetbrains_dir")
    maple_dir = config.get("maple_dir")
    output_dir = config.get("output_dir")
    styles_regular = config.get(
        "styles_regular",
        [
            "Regular",
            "Bold",
            "ExtraBold",
            "ExtraLight",
            "Light",
            "Medium",
            "SemiBold",
            "Thin",
        ],
    )

    styles_italic = config.get(
        "styles_italic",
        [
            "Italic",
            "BoldItalic",
            "ExtraBoldItalic",
            "ExtraLightItalic",
            "LightItalic",
            "MediumItalic",
            "SemiBoldItalic",
            "ThinItalic",
        ],
    )

    # Validate required configuration
    if not all([jetbrains_dir, maple_dir, output_dir]):
        print(
            "Error: Configuration must include 'jetbrains_dir', 'maple_dir', and 'output_dir'"
        )
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process all font regular styles
    for style in tqdm(styles_regular):
        # Process non-italic version
        jb_regular = os.path.join(jetbrains_dir, f"JetBrainsMono-{style}.ttf")
        maple_regular = os.path.join(maple_dir, f"MapleMono-CN-{style}.ttf")
        output_regular = os.path.join(output_dir, f"JetMapleMono-{style}.ttf")

        if os.path.exists(jb_regular) and os.path.exists(maple_regular):
            try:
                process_regular_font(jb_regular, maple_regular, output_regular)
            except Exception as e:
                print(f"Error processing regular font {style}: {e}")
        else:
            print(f"Warning: Missing files for {style} style, skipping")
            print(f"  JetBrains: {os.path.exists(jb_regular)}")
            print(f"  Maple: {os.path.exists(maple_regular)}")

    # Process all italic styles
    for style in tqdm(styles_italic):
        # Process italic version
        maple_italic = os.path.join(maple_dir, f"MapleMono-CN-{style}.ttf")
        output_italic = os.path.join(output_dir, f"JetMapleMono-{style}.ttf")

        if os.path.exists(maple_italic):
            try:
                process_italic_font(maple_italic, output_italic)
            except Exception as e:
                print(f"Error processing italic font {style}: {e}")
        else:
            print(f"Warning: Missing file for {style} style, skipping")
            print(f"  Maple: {os.path.exists(maple_italic)}")
    print("Font fusion completed successfully!")


if __name__ == "__main__":
    main()
