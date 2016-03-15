# =========================================================================
# Fonction de decodage de date (format dans la doc : SAAMMDDhhmmss
# =========================================================================


def parseDate(date):
    # recuperation de l annee (S[AA]MMDDhhmmss)
    year = "20" + date[1] + date[2]
    # recuperation du mois (SAA[MM]DDhhmmss)
    month = date[3] + date[4]
    # recuperation du jour (SAAMM[DD]hhmmss)
    day = date[5] + date[6]
    # recuperation des heures (SAAMMDD[hh]mmss)
    hour = date[7] + date[8]
    # recuperation recuperation des minutes (SAAMMDDhh[mm]ss)
    minutes = date[9] + date[10]
    # recuperation des secondes (SAAMMDDhhmm[ss])
    sec = date[11] + date[12]
    # renvoyer la date sous la forme "AAAA-MM-DD hh:mm:ss"
    return year + "-" + month + "-" + day + " " + hour + ":" + minutes + ":" + sec


# =========================================================================
# Verification de la coherence des donnees recus
# =========================================================================
def checksum(trame):
    sum = 0
    # etiquette du groupe
    etiquette = trame[0]
    # selon le cas contient la date ou la valeur
    valeur = trame[1]
    # si le groupe est horodatee contient la valeur de la donnee
    # si le groupe est horodatee
    if len(trame) == 4:
        valeur2 = trame[2]
        for c in valeur2:
            sum += ord(c)
    for c in etiquette:
        sum += ord(c)
    for c in valeur:
        sum += ord(c)
    # ajout des <HT> a la somme , CF doc
    sum += (len(trame) - 1) * 9
    # CF doc pour le calcul
    sum = (sum & 63) + 32
    return chr(sum) == trame[len(trame) - 1]


# ===============================================================================
# inserer dans la table "tableName" la valeur "valeur" si elle n exite pas deja
# ===============================================================================
def insertInto(cursor, tableName, valeur):
    # chercher la valeur dans la base
    cursor.execute("SELECT ID  FROM " + tableName + """ where DATE = %s  and VALEUR = %s""", (valeur[0], valeur[1]))
    # recuperer le resultat de la requette
    rows = cursor.fetchall()
    id = -1
    # recuperer le resultat de la requette
    for rec in rows:
        for item in rec:
            id = item
    # si la valeur n'existe pas dans la base , l inserer
    if id == -1:
        cursor.execute("INSERT INTO " + tableName + """ (DATE,VALEUR) VALUES (%s, %s)""", (valeur[0], valeur[1]))
        id = cursor.lastrowid
    # renvoyer l ID
    return id
