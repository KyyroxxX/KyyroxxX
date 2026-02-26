#!/bin/bash
# Script: user_manager.sh
# Propósito: Crear y eliminar usuarios automáticamente en Linux
# Uso: sudo ./user_manager.sh add|del username

ACTION=$1
USER=$2

if [[ -z "$ACTION" || -z "$USER" ]]; then
    echo "Uso: $0 add|del username"
    exit 1
fi

case "$ACTION" in
    add)
        sudo useradd -m -s /bin/bash "$USER"
        sudo passwd "$USER"
        echo "Usuario $USER creado."
        ;;
    del)
        sudo userdel -r "$USER"
        echo "Usuario $USER eliminado."
        ;;
    *)
        echo "Acción inválida: usar add o del"
        exit 1
        ;;
esac
