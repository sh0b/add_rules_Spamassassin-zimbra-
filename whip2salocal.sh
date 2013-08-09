#!/bin/bash
#===============================================================================
#
#          FILE:  whip2salocal.sh
# 
#         USAGE:  ./whip2salocal.sh 
# 
#   DESCRIPTION:  whiptail front-end for psalocal.py 
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Sebastian Batalla (sh0b), sbbt.uy@gmail.com
#       COMPANY:  Netlabs SRL
#       VERSION:  1.0
#       CREATED:  08/08/13 14:48:48 UYT
#      REVISION:  ---
#===============================================================================

if [ -x "`which resize 2>/dev/null`" ]; then
        eval `resize`
else
        SIZE=`stty size`
        LINES=${SIZE%% *}
        COLUMNS=${SIZE##* }
fi


function Menu () {
        while [ -z "$MENU" ]; do
                MENU=$(whiptail --nocancel --title "Menu" --menu "Realizar una accion sobre el salocal Zimbra" \
                        $LINES $COLUMNS $(( $LINES - 8 )) \
                        "FraseMedio" "Frase nivel medio" "FraseAlto" "Frase nivel alto" "blacklistEmail" "Blacklistear un e-mail" "exit" "Exit" 3>&1 1>&2 2>&3)
	
	if [[ $MENU == "exit" ]]; then exit ;fi
	done
}

function SpamPhrase () {
        while [ -z "$PHRASE" ]; do
                PHRASE=$(whiptail --nocancel --inputbox "Ingrese la frase a blacklistear" $LINES $COLUMNS --title "Spam Phrase" 3>&1 1>&2 2>&3)
        done
}

function SpamMail () {
        while [ -z "$MAIL" ]; do
                MAIL=$(whiptail --nocancel --inputbox "Ingrese el e-mail a blacklistear" $LINES $COLUMNS --title "Spam Mail" 3>&1 1>&2 2>&3)
        done
}


Menu

if [[ $MENU == 'FraseMedio' ]] 
then
	SpamPhrase
	./psalocal.py -o 0 -p "$PHRASE"
	
elif [[ $MENU == 'FraseAlto' ]]
then
	SpamPhrase
	./psalocal.py -o 1 -p "$PHRASE"
else
	SpamMail
	./psalocal.py -o 2 -p "$MAIL"

fi


exit


