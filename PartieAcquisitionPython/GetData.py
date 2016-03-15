# ============================================================================
# Recuperation de la tram qui sera lancer par le processus "treatFrameThread"
# ============================================================================

import serial
import MySQLdb
import Utils
from Weft import Weft
import sys



# =========================================================================
# Fonction LireTeleinfo : lit la trame et renvoi celle qui est valide
# =========================================================================
def readWeft(ser):
    # Attendre le debut du message

    message = ""
    fin = False
    # tant qu'on a pas atteint la fin de la tram
    while not fin:
        # on recupere caractere par caractere la tram
        char = ser.read(1)
        if char != chr(2):
            message = message + char
        else:
            fin = True
    # decommenter pour afficher la tram
    # print(message)
    # decouper la tram on "etiquette" "horodate" " donnee"
    trames = [
        trame.split("\t")
        for trame in message.strip("\r\n\x03").split("\r\n")
        ]
    # recuperer la tram si elle est valide
    tramesValides = dict()
    for trame in trames:
        if len(trame) > 2 and Utils.checksum(trame):

            if len(trame) == 4:
                tramesValides[trame[0]] = trame[1] + "\t" + trame[2]
            if len(trame) == 3:
                tramesValides[trame[0]] = trame[1]
            sys.stdout.flush()
    return tramesValides


# =========================================================================
# Recuperation de la tram
# =========================================================================
def doIt():
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS)
    db = MySQLdb.connect("localhost", "root", "linky", "ProjetERDF_BDD")
    cursor = db.cursor()

    ser.write('A')
    ser.flushInput()
    while ser.read(1) != chr(2):
        pass

    lastDate = 0
    while 1:
        tramesOk = readWeft(ser)
        weft = Weft()
        insert = False
        diffDate = True
        for etiquette in tramesOk:
            if etiquette == 'ADSC':
                weft.adsc = tramesOk[etiquette]
                insert = True
            if etiquette == 'VTIC':
                weft.vtic = tramesOk[etiquette]
            if etiquette == 'DATE':
                date = tramesOk[etiquette]
                weft.date = Utils.parseDate(date)
                sys.stdout.flush()
                if lastDate == weft.date:
                    diffDate = False
                else:
                    lastDate = weft.date
            if etiquette == 'NGTF':
                weft.ngtf = tramesOk[etiquette]
            if etiquette == 'LTARF':
                weft.ltarf = tramesOk[etiquette]
            if etiquette == 'EAST':
                weft.east = tramesOk[etiquette]
            if etiquette == 'EASF01':
                weft.easf01 = tramesOk[etiquette]
            if etiquette == 'EASF02':
                weft.easf02 = tramesOk[etiquette]
            if etiquette == 'EASF03':
                weft.easf03 = tramesOk[etiquette]
            if etiquette == 'EASF04':
                weft.easf04 = tramesOk[etiquette]
            if etiquette == 'EASF05':
                weft.easf05 = tramesOk[etiquette]
            if etiquette == 'EASF06':
                weft.easf06 = tramesOk[etiquette]
            if etiquette == 'EASF07':
                weft.easf07 = tramesOk[etiquette]
            if etiquette == 'EASF08':
                weft.easf08 = tramesOk[etiquette]
            if etiquette == 'EASF09':
                weft.easf09 = tramesOk[etiquette]
            if etiquette == 'EASF10':
                weft.easf10 = tramesOk[etiquette]
            if etiquette == 'EASD01':
                weft.easd01 = tramesOk[etiquette]
            if etiquette == 'EASD02':
                weft.easd02 = tramesOk[etiquette]
            if etiquette == 'EASD03':
                weft.easd03 = tramesOk[etiquette]
            if etiquette == 'EASD04':
                weft.easd04 = tramesOk[etiquette]
            if etiquette == 'IRMS1':
                weft.irms1 = tramesOk[etiquette]
            if etiquette == 'URMS1':
                weft.urms1 = tramesOk[etiquette]
            if etiquette == 'PREF':
                weft.pref = tramesOk[etiquette]
            if etiquette == 'PCOUP':
                weft.pcoup = tramesOk[etiquette]
            if etiquette == 'SINST1':
                weft.sinst1 = tramesOk[etiquette]
            if etiquette == 'SMAXN':
                weft.smaxn = tramesOk[etiquette].split("\t")
                weft.smaxn[0] = Utils.parseDate(weft.smaxn[0])
            if etiquette == 'SMAXN-1':
                weft.smaxn1 = tramesOk[etiquette].split("\t")
                weft.smaxn1[0] = Utils.parseDate(weft.smaxn1[0])
            if etiquette == 'CCASN':
                weft.ccasn = tramesOk[etiquette].split("\t")
                weft.ccasn[0] = Utils.parseDate(weft.ccasn[0])
            if etiquette == 'CCASN-1':
                weft.ccasn1 = tramesOk[etiquette].split("\t")
                weft.ccasn1[0] = Utils.parseDate(weft.ccasn1[0])
            if etiquette == 'UMOY1':
                weft.umoy1 = tramesOk[etiquette].split("\t")
                weft.umoy1[0] = Utils.parseDate(weft.umoy1[0])
            if etiquette == 'STGE':
                weft.stge = tramesOk[etiquette]

        # endFor

        # =========================================================================
        # insertion dans la base
        # =========================================================================


        if insert and diffDate and len(tramesOk) == 31 :
            smaxnid = Utils.insertInto(cursor, 'ProjetERDF_BDD.SMAXN', weft.smaxn)
            smaxn1id = Utils.insertInto(cursor, 'ProjetERDF_BDD.SMAXN1', weft.smaxn1)
            ccasnid = Utils.insertInto(cursor, 'ProjetERDF_BDD.CCASN', weft.ccasn)
            ccasn1id = Utils.insertInto(cursor, 'ProjetERDF_BDD.CCASN1', weft.ccasn1)
            umoy1id = Utils.insertInto(cursor, 'ProjetERDF_BDD.UMOY1', weft.umoy1)

            cursor.execute("""INSERT INTO `ProjetERDF_BDD`.`BufferTrame`(DATE, ADSC, VTIC, NGTF, LTARF, EAST,EASF01,EASF02,EASF03,EASF04,EASF05,EASF06,EASF07, EASF08,EASF09,EASF10,EASD01,EASD02,EASD03,EASD04,IRMS1,URMS1,PREF,PCOUP,SINST1,SMAXNID,SMAXN1ID,CCASNID,CCASN1ID,UMOY1ID,STGE)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (weft.date, weft.adsc, weft.vtic, weft.ngtf, weft.ltarf, weft.east, weft.easf01,
                            weft.easf02,
                            weft.easf03, weft.easf04, weft.easf05, weft.easf06, weft.easf07, weft.easf08,
                            weft.easf09, weft.easf10, weft.easd01, weft.easd02, weft.easd03, weft.easd04, weft.irms1,
                            weft.urms1, weft.pref, weft.pcoup, weft.sinst1, smaxnid,
                            smaxn1id, ccasnid, ccasn1id, umoy1id, weft.stge))
            db.commit()
            db.rollback()
    # endWhile
    db.close()
    ser.close()
    # =========================================================================
