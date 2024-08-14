#!/bin/bash

# Define package names
PROJECT_NAME="cvtease"
MAIN_PACKAGES=("click" "colorama" "opencv-python" "opencv-python-headless")
SEPARATE_PACKAGES=("mediapipe" "PySide6")

# Function to check if a package is installed
check_package_installed() {
    pip show "$1" &>/dev/null
}

# Function to install packages using pip
install_packages() {
    echo "Installing main packages: ${MAIN_PACKAGES[*]}"
    pip install "${MAIN_PACKAGES[@]}"
}

# Function to check and prompt installation of separate packages
check_and_prompt_installation() {
    for package in "${SEPARATE_PACKAGES[@]}"; do
        if ! check_package_installed "$package"; then
            echo "The package '$package' is not installed."
            echo "Please install it using the appropriate command for your OS:"
            case "$OSTYPE" in
                linux*)
                    echo "For Linux, use: pip install $package"
                    ;;
                darwin*)
                    echo "For macOS, use: pip install $package"
                    ;;
                msys*|cygwin*|win32)
                    echo "For Windows (WSL), use: pip install $package"
                    ;;
                *)
                    echo "Your OS is not recognized. Use: pip install $package"
                    ;;
            esac
        fi
    done
}

# Function to display the usage of cvtease if packages are missing
display_usage() {
    echo -e "\nUsage of $PROJECT_NAME:"
    echo -e "  $PROJECT_NAME [command] [options]\n"
    echo "Please ensure the following packages are installed separately:"
    for package in "${SEPARATE_PACKAGES[@]}"; do
        echo "  - $package"
    done
}

# Install main packages
install_packages

# Check and prompt installation of separate packages
check_and_prompt_installation

# Check if cvtease can run
if ! command -v $PROJECT_NAME &>/dev/null; then
    echo -e "\n$PROJECT_NAME is not installed or not in your PATH."
    echo "Please install the package using the appropriate method for your OS."
else
    # Check if separate packages are installed
    for package in "${SEPARATE_PACKAGES[@]}"; do
        if ! check_package_installed "$package"; then
            display_usage
            exit 1
        fi
    done
    echo "$PROJECT_NAME is ready to use!"
fi
