#!/bin/bash


CSV="mutations.csv"


ROSETTA="rosetta_scripts.static.linuxgccrelease"


TEMPLATE_XML="template.xml"


tail -n +2 $CSV | while read mut
do
    echo "Processing $mut"


    WT=${mut:0:1}
    POS=$(echo $mut | sed 's/[^0-9]//g')
    MUT=${mut: -1}


    case $MUT in
        A) AA3="ALA";;
        R) AA3="ARG";;
        N) AA3="ASN";;
        D) AA3="ASP";;
        C) AA3="CYS";;
        Q) AA3="GLN";;
        E) AA3="GLU";;
        G) AA3="GLY";;
        H) AA3="HIS";;
        I) AA3="ILE";;
        L) AA3="LEU";;
        K) AA3="LYS";;
        M) AA3="MET";;
        F) AA3="PHE";;
        P) AA3="PRO";;
        S) AA3="SER";;
        T) AA3="THR";;
        W) AA3="TRP";;
        Y) AA3="TYR";;
        V) AA3="VAL";;
        *) echo "Unknown AA: $MUT"; exit 1;;
    esac


    mkdir -p $mut
    cd $mut


    ln -sf ../A5-FPP.pdb .
    ln -sf ../flags .
    ln -sf ../X00.params .
    ln -sf ../Y00.params .
    ln -sf ../Z00.params .
    ln -sf ../dock.cst .

    TARGET="${POS}A"

    sed "
    s/__MUT_NAME__/$mut/g;
    s/__TARGET__/$TARGET/g;
    s/__NEW_RES__/$AA3/g
    " ../$TEMPLATE_XML > ks_dock.xml


    $ROSETTA @flags -parser:protocol ks_dock.xml -nstruct 10 -ignore_zero_occupancy F > log.txt

    cd ..
done