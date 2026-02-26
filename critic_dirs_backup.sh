#!/bin/bash
# Script: backup.sh
# Propósito: Realizar backup de carpetas importantes
# Uso: ./backup.sh

# Tienes que cambiar las siguientes variables= SRC: A lo que quieres hacerle Backup, DEST: Donde quieres que se guarde el backup, te recomiendo usar crontab para automatizarlo.
SRC="/home/alejandro/Documentos"
DEST="/home/alejandro/Backups"
DATE=$(date +%Y-%m-%d_%H-%M)

mkdir -p "$DEST"
tar -czvf "$DEST/backup_$DATE.tar.gz" "$SRC"

echo "Backup completado: $DEST/backup_$DATE.tar.gz"
