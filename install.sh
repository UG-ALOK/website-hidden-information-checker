#!/data/data/com.termux/files/usr/bin/bash

# ==========================================
# Website Hidden Information Checker
# Developer:
# Main File: WHIC.py
# ==========================================

RESET='\033[0m'
RED='\033[1;31m'
GREEN='\033[1;32m'
GOLD='\033[1;33m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'

MAIN_FILE="admin.py"

clear

echo -e "${RED}========================================${RESET}"
echo -e "${WHITE}          Website Hidden Information Checker${RESET}"
echo -e "${GOLD}           TERMUX SETUP${RESET}"
echo -e "${RED}========================================${RESET}"
echo

if ! command -v pkg >/dev/null 2>&1; then
    echo -e "${RED}[ERROR] Termux package manager not found.${RESET}"
    exit 1
fi

echo -e "${CYAN}[1/4] Updating Termux...${RESET}"
if ! pkg update -y; then
    echo -e "${RED}[ERROR] Update failed.${RESET}"
    exit 1
fi

echo -e "${CYAN}[2/4] Installing Python...${RESET}"
if ! pkg install -y python; then
    echo -e "${RED}[ERROR] Python installation failed.${RESET}"
    exit 1
fi

echo -e "${CYAN}[3/4] Installing Git...${RESET}"
if ! pkg install -y git; then
    echo -e "${RED}[ERROR] Git installation failed.${RESET}"
    exit 1
fi

echo -e "${CYAN}[4/4] Requesting storage permission...${RESET}"

if ! command -v termux-setup-storage >/dev/null 2>&1; then
    echo -e "${GOLD}[INFO] Storage setup command is unavailable.${RESET}"
    echo -e "${GOLD}Install Termux:API/storage support if needed.${RESET}"
else
    termux-setup-storage
fi

echo
echo -e "${GREEN}========================================${RESET}"
echo -e "${GREEN}       BASIC SETUP COMPLETED${RESET}"
echo -e "${GREEN}========================================${RESET}"
echo
echo -e "${WHITE}Python:${RESET}"
python --version
echo
echo -e "${WHITE}Git:${RESET}"
git --version
echo
echo -e "${CYAN}Main file: ${WHITE}${MAIN_FILE}${RESET}"
echo -e "${GOLD}Run command: python WHIC.py${RESET}"
echo