#!/usr/bin/env bash
set -e # Exit on error

# Parse command line arguments
KEEP_TEMP=false
CONFIG_FILE=""

while [[ "$#" -gt 0 ]]; do
  case $1 in
  --keep-temp) KEEP_TEMP=true ;;
  --config)
    CONFIG_FILE="$2"
    shift
    ;;
  *)
    echo "Unknown parameter: $1"
    exit 1
    ;;
  esac
  shift
done

# Font download URLs
JETBRAINS_URL="https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip"
MAPLE_URL="https://github.com/subframe7536/maple-font/releases/download/v7.2/MapleMono-CN-unhinted.zip"

# Default configuration
if [ -z "$CONFIG_FILE" ]; then
  echo "Using default configuration"
  CONFIG_FILE="tmp_config.json"
  cat >"$CONFIG_FILE" <<EOF
{
    "jetbrains_dir": "tmp/jetbrains-mono/fonts/ttf",
    "maple_dir": "tmp/maple-mono",
    "output_dir": "output/fonts"
}
EOF
else
  echo "Using custom configuration: $CONFIG_FILE"
fi

# Create necessary directories
mkdir -p tmp
mkdir -p output/fonts

# Clean up existing directories if they exist
if [ -d "tmp/jetbrains-mono" ]; then
  rm -rf tmp/jetbrains-mono
fi

if [ -d "tmp/maple-mono" ]; then
  rm -rf tmp/maple-mono
fi

# Download font packages
echo "Downloading JetBrains Mono..."
curl -L "$JETBRAINS_URL" -o tmp/jetbrains-mono.zip

echo "Downloading Maple Mono..."
curl -L "$MAPLE_URL" -o tmp/maple-mono.zip

# Extract font packages
echo "Extracting JetBrains Mono..."
mkdir tmp/jetbrains-mono
unzip -q tmp/jetbrains-mono.zip -d tmp/jetbrains-mono

echo "Extracting Maple Mono..."
mkdir -p tmp/maple-mono
unzip -q tmp/maple-mono.zip -d tmp/maple-mono

# Run the merge script
echo "Merging fonts..."
python -m merge "$CONFIG_FILE"

# Clean up if not keeping temp files
if [ "$KEEP_TEMP" = false ]; then
  echo "Cleaning up temporary files..."
  rm -rf tmp

  # Remove temp config if we created it
  if [ "$CONFIG_FILE" = "tmp_config.json" ]; then
    rm -f tmp_config.json
  fi
fi

echo "JetMaple Mono fonts have been generated in: output/fonts"
