#!/bin/bash
# Script: backup.sh
# Propósito: Realizar backup de carpetas importantes
# Uso: ./backup.sh

SRC="/home/alejandro/Documentos"
DEST="/home/alejandro/Backups"
DATE=$(date +%Y-%m-%d_%H-%M)

mkdir -p "$DEST"
tar -czvf "$DEST/backup_$DATE.tar.gz" "$SRC"

echo "Backup completado: $DEST/backup_$DATE.tar.gz"
