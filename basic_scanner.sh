#!/bin/bash

# =============================
# NMAP Escaaner Basico de Vulnerabilidades con scripts NSE
# =============================

# Para poder hacer ctrl+C
function ctrl_c() {
    echo -e "\n[!] Escaneo interrumpido por el usuario. Saliendo..."
    exit 1
}

trap ctrl_c SIGINT

if [ $# -ne 1 ]; then
    echo "[!] Uso: $0 <IP o red>"
    exit 1
fi

TARGET=$1
DATE=$(date +%Y-%m-%d_%H-%M)
OUTDIR="scan_$DATE"

mkdir -p "$OUTDIR"

echo "[+] Escaneo iniciado contra $TARGET"
echo "[+] Resultados en $OUTDIR"

# =============================
# 1. Descubrimiento hosts vivos
# =============================
echo "[+] Descubriendo hosts activos..."

sudo nmap -sn "$TARGET" -oG "$OUTDIR/hosts.gnmap"

HOSTS=$(grep "Up" "$OUTDIR/hosts.gnmap" | awk '{print $2}')

if [ -z "$HOSTS" ]; then
    echo "[!] No hay hosts activos."
    exit 1
fi

echo "[+] Hosts encontrados:"
echo "$HOSTS"

# =============================
# 2. Escaneo rápido puertos TOP
# =============================
echo "[+] Escaneo rápido (Top 1000)..."

sudo nmap -T4 -sS -Pn -sV \
-oA "$OUTDIR/quick_scan" \
$HOSTS

# =============================
# 3. Escaneo completo TCP
# =============================
echo "[+] Escaneo completo TCP (puede tardar)..."

sudo nmap -p- -T4 -sS -Pn \
-oA "$OUTDIR/full_ports" \
$HOSTS

# =============================
# 4. Scripts NSE vulnerabilidades
# =============================
echo "[+] Ejecutando scripts NSE de vulnerabilidades..."

sudo nmap -sV -Pn \
--script "vuln,safe,auth,default" \
--script-timeout 2m \
-oA "$OUTDIR/vuln_scan" \
$HOSTS

# =============================
# 5. Detección OS + servicios
# =============================
echo "[+] Detectando OS y servicios..."

sudo nmap -A -Pn \
-oA "$OUTDIR/aggressive" \
$HOSTS

echo "[+] Escaneo terminado."
echo "[+] Revisa resultados en $OUTDIR"
