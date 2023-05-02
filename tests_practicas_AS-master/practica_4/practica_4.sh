#!/bin/bash
#845097, Valle Morenilla, Juan, T, 1, A
#839757, Ye, Ming Tao, T, 1, A

# Comprobamos que el usuario tiene privilegios de administrador
if [ "$EUID" -ne 0 ]; then
    echo "Este script necesita privilegios de administracion"
    exit 1
fi

# Comprobamos si el número de parámetros es el correcto (3)
if [ "$#" -ne 3 ]; then
    echo "Numero incorrecto de parametros">&2
    exit 1
fi

# Leer fichero de usuarios y comprobar que exista
if [ ! -f "$2" ]; then
    echo "Error: No se encontró el fichero de usuarios"
    exit 1
fi

# Leer fichero de máquinas y comprobar que exista
if [ ! -f "$3" ]; then
    echo "Error: No se encontró el fichero de máquinas"
    exit 1
fi

if [ "$1" = "-a" ]; then
    while read ip
    do
        while IFS=',' read nombre contrasena nombreCompleto
        do
            # Comprobamos que los campos no son la cadena vacía
            if [ "$nombre" = "" -o "$contrasena" = "" -o "$nombreCompleto" = "" ]; then
                echo "Campo invalido"
                exit 1
            fi

            ssh -n -i /home/as/.ssh/id_as_ed25519 as@"$ip" "sudo useradd -U -m -c \"$nombreCompleto\" -K UID_MIN=1815 $nombre"
            if [ "$?" -eq 0 ]; then
                ssh -n -i /home/as/.ssh/id_as_ed25519 as@"$ip" "echo "$nombre:$contrasena" | 
                sudo chpasswd ; sudo chage -M 30 $nombre ; echo "$nombreCompleto ha sido creado." "
            else
                echo "El usuario $nombre ya existe"
            fi

            # Comprobamos si el ssh ha ido correctamente
            if [ "$?" -ne 0 ]; then
                echo "$ip no es accesible"
                exit 1
            fi
        done < "$2"     # La stdIn del bucle es el fichero de usuarios pasado por parámetro
    done < "$3"         # La stdIn del bucle es el fichero de ip's pasado por parámetro

# Borramos usuarios
elif [ "$1" = "-s" ]; then
    while read ip
    do
        ssh -n -i /home/as/.ssh/id_as_ed25519 as@"$ip" "mkdir -p /extra/backup" # Creamos el directorio backup si no existe
        if [ "$?" -ne 0 ]; then
            echo "$ip no es accesible"
            exit 1
        fi
        while IFS=',' read nombre contrasena nombreCompleto
        do
            if [ "$nombre" = "" ]; then
                echo "Campo invalido"
                exit 1
            fi

            home=$(ssh -n -i /home/as/.ssh/id_as_ed25519 as@"$ip" "grep $nombre /etc/passwd | cut -d: -f6")
            if [ "$home" != "" ]; then
                ssh -n -i /home/as/.ssh/id_as_ed25519 as@"$ip" "sudo tar czpf /extra/backup/"$nombre".tar "$home" 
                2>/dev/null && sudo userdel -r "$nombre" 2>/dev/null"
            fi
        done < "$2"   # La stdIn del bucle es el fichero de usuarios pasado por parámetro
    done < "$3"     # La stdIn del bucle es el fichero de ip's pasado por parámetro

# Parámetros incorrectos
else
    echo "Opcion invalida" >&2
    exit 1
fi
