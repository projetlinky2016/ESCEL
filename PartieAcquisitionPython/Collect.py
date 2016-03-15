# =========================================================================
# Dependances / Librairies
# =========================================================================
import multiprocessing
import GetData
import TreatWeft

# thread de traitement et insertion en base
treatWeftThread = multiprocessing.Process(target=TreatWeft.doIt)
treatWeftThread.start()
# recuperation de la tram
GetData.doIt()
