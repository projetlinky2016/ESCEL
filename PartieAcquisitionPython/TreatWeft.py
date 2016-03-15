# =========================================================================
# Traitement des donnees
# =========================================================================

import MySQLdb
from math import sqrt
import sys

def getAnomalie(stge,date,adresseCompteur):
    scale = 16  ## equals to hexadecimal
    num_of_bits = 32
    stgeInBinary = bin(int(stge, scale))[2:].zfill(num_of_bits)
    reverseBinaryStge = stgeInBinary[::-1]
    sys.stdout.flush()
    bitDeCoupure = reverseBinaryStge[1:4]
    bitSurtension = reverseBinaryStge[6]
    bitDepassementDeLaPuissance = reverseBinaryStge[7]
    nature = None
    if bitDeCoupure == "100":
        nature = "surpuissance"
    if bitDeCoupure == "010":
        nature = "surtension"
    if bitDeCoupure == "110":
        nature = "delestage"
    if bitDeCoupure == "001":
        nature = "overt sur ordre CPL/Euridis"
    if bitDeCoupure == "101":
        nature = "surchauffe : valeur de courant > au courant de commutation maximal"
    if bitDeCoupure == "011":
        nature = "surchauffe : valeur de courant < au courant de commutation maximal"
    if nature == None :
        return None
    else :
        return "INSERT INTO `ProjetERDF_BDD`.`Anomalie` (`AdresseCompteur`, `Date`, `Nature`)VALUES (" + str(adresseCompteur) + ",'" + date.strftime("%Y-%m-%d %H:%M:%S") + "' , '"+ nature +"')"  # =========================================================================


def updateOptionCompteurTable(cursor, numeroCompteur, versionTic, optionTarifaire, pApparenteSouscrite):
    cursor.execute(
        """SELECT IdOptCompteur  FROM `ProjetERDF_BDD`.`OptionCompteur` where AdresseSecCompteur = %s  and VersionTic = %s  and OptTarifaire = %s  and PApparenteSouscrite = %s """,
        (numeroCompteur, versionTic, optionTarifaire, pApparenteSouscrite))
    # recuperer le resultat de la requette
    rows = cursor.fetchall()
    id = -1
    # recuperer le resultat de la requette
    for rec in rows:
        for item in rec:
            id = item
    if id == -1:
        cursor.execute(
            "INSERT INTO `ProjetERDF_BDD`.`OptionCompteur` (AdresseSecCompteur,VersionTic,OptTarifaire,PApparenteSouscrite) VALUES (%s, %s,%s,%s)""",
            (numeroCompteur, versionTic, optionTarifaire, pApparenteSouscrite))
        id = cursor.lastrowid
    return id


def doIt():
    hp = False  # heure pleine
    hc = False  # heure creuse
    lastEnergieVar = 0  # valeur de la derniere variation de l energie
    pActive = 0  # la puissance active
    pReactive = 0  # la puisssance reactive
    lastDate = 0
    db = MySQLdb.connect("localhost", "root", "linky", "ProjetERDF_BDD")
    cursor = db.cursor()
    # recuperer la valeur de
    cursor.execute(
        """ SELECT DATE,Energie FROM ProjetERDF_BDD.`Values` where DATE = (SELECT MAX(date) FROM ProjetERDF_BDD.`Values` where Pactive is not null) """)

    rows2 = cursor.fetchall()
    if len(rows2) != 0:
        lastDate = rows2[0][0]
        lastEnergieVar = float(rows2[0][1])

    while 1:
        # recuperer la tram la plus ancienne pour la traitee

        cursor.execute(
            """ SELECT DATE ,EAST ,IRMS1 ,URMS1 , SINST1 , LTARF , VTIC , ADSC , PCOUP,STGE FROM `ProjetERDF_BDD`.`BufferTrame` where DATE = (SELECT MIN(DATE)  FROM `ProjetERDF_BDD`.`BufferTrame`) """)
        rows = cursor.fetchall()
        if len(rows) != 0:
            dateCourante = rows[0][0]
            energieCourante = float(rows[0][1]) / 1000  # transformer en kwh
            intensite = float(rows[0][2])
            tension = float(rows[0][3])
            pApparente = float(rows[0][4])
            optionTarifaire = rows[0][5].strip(" ")
            versionTic = rows[0][6]
            numeroCompteur = rows[0][7]
            pApparenteSouscrite = rows[0][8]

            idOptionTar = updateOptionCompteurTable(cursor, numeroCompteur, versionTic, optionTarifaire,
                                                    pApparenteSouscrite)
            stge = rows[0][9]
            requetteAnomalie = getAnomalie(stge,dateCourante,numeroCompteur)
            if(requetteAnomalie != None) :
                cursor.execute(requetteAnomalie)
            if lastDate == 0:
                lastDate = dateCourante
            if "BASE" in optionTarifaire:
                hp = False
                hc = False
            if energieCourante != lastEnergieVar:
                if dateCourante != lastDate:
                    if pApparente != 0:
                        diffEnergie = energieCourante - lastEnergieVar
                        diffEnergie = diffEnergie *1000
                        diffDate =(dateCourante - lastDate).total_seconds() / 3600
                        pActive = diffEnergie / diffDate
                        cursor.execute(
                        "SELECT AVG(Papparente) FROM ProjetERDF_BDD.`Values` WHERE date < '"+dateCourante.strftime("%Y-%m-%d %H:%M:%S")+"' and date >= '"+lastDate.strftime("%Y-%m-%d %H:%M:%S")+"'")
                        data = cursor.fetchall()
                        pAppMoy = data[0][0]
                        if(pAppMoy > pActive):
                            pReactive = sqrt((pAppMoy * pAppMoy) - (pActive * pActive))
                        else :
                            pReactive = 0

                lastDate = dateCourante
                lastEnergieVar = energieCourante
            else:
                pActive = None
                pReactive = None
            if pApparente == 0:
                pActive = 0
                pReactive = 0
            dateCourante = dateCourante.strftime("%Y-%m-%d %H:%M:%S")

            # peuplement de la base
            cursor.execute("""INSERT INTO `ProjetERDF_BDD`.`Values`(Date, Intensite, Tension, Energie, Papparente, Pactive, Preactive, HeurePleine, HeureCreuse, IdOptCompteur)
					 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                dateCourante, intensite, tension, energieCourante, pApparente, pActive, pReactive, hp, hc, idOptionTar))
            # suppression de la tram traitee
            cursor.execute("DELETE FROM `ProjetERDF_BDD`.`BufferTrame` WHERE `DATE`='" + dateCourante + "'""")
        db.commit()
        db.rollback()
        # endWhile
    db.close()
