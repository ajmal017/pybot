from HMA_strat import check_signal
#from backtest2 import backtest
from minervini import check_trend
from HMA_strat_backtest import backtest
from sl_rechner import get_sl

#check_trend('PYPL')
backtest("WDI.DE")
#get_sl("WDI.DE", "2019-04-23", 120.00)
#check_signal("WDI.DE")

#DAX
'''
#adidas
check_signal("ADS.DE")
#Allianz
check_signal("ALV.DE")
#BASF
check_signal("BAS.DE")
#Bayer
check_signal("BAYN.DE")
#Beiersdorf
check_signal("BEI.DE")
#BMW
check_signal("BMW.DE")
#Continental
check_signal("CON.DE")
#Covestro
check_signal("1COV.DE")
#Daimler
check_signal("DAI.DE")
#Deutsche Bank
check_signal("DBK.DE")
#Deutsche Börse
check_signal("DB1.DE")
#Detusche Post
check_signal("DPW.DE")
#Dt Telekom
check_signal("DTE.DE")
#eon
check_signal("EOAN.DE")
#Fresenius
check_signal("FRE.DE")
#Fresenius MC
check_signal("FME.DE")
#HeidelbergCement
check_signal("HEI.DE")
#Henkel
check_signal("HEN.DE")
#Infineon
check_signal("IFX.DE")
#Linde
check_signal("LIN.DE")
#Lufthansa
check_signal("LHA.DE")
#Merck
check_signal("MRK.DE")
#Münchner Rück
check_signal("MUV2.DE")
#rwe
check_signal("RWE.DE")
#sap
check_signal("SAP.DE")
#Siemens
check_signal("SIE.DE")
#Thyssenkrupp
check_signal("TKA.DE")
#VW
check_signal("VOW.DE")
#Vonovia
check_signal("VNA.DE")
#Wirecard
check_signal("WDI.DE")

#Nasdaq
check_signal("ATVI")
check_signal("ADBE")
check_signal("AMD")
check_signal("ALGN")
check_signal("ALXN")
check_signal("AMZN")
check_signal("AMGN")
check_signal("AAL")
check_signal("ADI")
check_signal("AAPL")
check_signal("AMAT")
check_signal("ASML")
check_signal("ADSK")
check_signal("ADP")
check_signal("AVGO")
check_signal("BIDU")
check_signal("BIIB")
check_signal("BMRN")
check_signal("CDNS")
check_signal("CELG")
check_signal("CERN")
check_signal("CHKP")
check_signal("CHTR")
check_signal("CTRP")
check_signal("CTAS")
check_signal("CSCO")
check_signal("CTXS")
check_signal("CMCSA")
check_signal("COST")
check_signal("CSX")
check_signal("CTSH")
check_signal("DLTR")
check_signal("EA")
check_signal("EBAY")
check_signal("EXPE")
check_signal("FAST")
check_signal("FB")
check_signal("FISV")
check_signal("FOX")
check_signal("FOXA")
check_signal("GILD")
check_signal("GOOG")
check_signal("GOOGL")
check_signal("HAS")
check_signal("HSIC")
check_signal("ILMN")
check_signal("INCY")
check_signal("INTC")
check_signal("INTU")
check_signal("ISRG")
check_signal("IDXX")
check_signal("JBHT")
check_signal("JD")
check_signal("KLAC")
check_signal("KHC")
check_signal("LRCX")
check_signal("LBTYA")
check_signal("LBTYK")
check_signal("LULU")
check_signal("MELI")
check_signal("MAR")
check_signal("MCHP")
check_signal("MDLZ")
check_signal("MNST")
check_signal("MSFT")
check_signal("MU")
check_signal("MXIM")
check_signal("MYL")
check_signal("NTAP")
check_signal("NFLX")
check_signal("NTES")
check_signal("NVDA")
check_signal("NXPI")
check_signal("ORLY")
check_signal("PAYX")
check_signal("PCAR")
check_signal("BKNG")
check_signal("PYPL")
check_signal("PEP")
check_signal("QCOM")
check_signal("REGN")
check_signal("ROST")
check_signal("SWKS")
check_signal("SIRI")
check_signal("SBUX")
check_signal("SYMC")
check_signal("SNPS")
check_signal("TTWO")
check_signal("TSLA")
check_signal("TXN")
check_signal("TMUS")
check_signal("ULTA")
check_signal("UAL")
check_signal("VRSN")
check_signal("VRSK")
check_signal("VRTX")
check_signal("WBA")
check_signal("WDC")
check_signal("WDAY")
check_signal("WLTW")
check_signal("WYNN")
check_signal("XEL")
check_signal("XLNX")

#WL

check_trend("ABCB")
check_trend("ADBE")
check_trend("AEZS")
check_trend("AGS")
check_trend("ALGN")
check_trend("AMAL")
check_trend("AMGP")
check_trend("AMOT")
check_trend("AMZN")
check_trend("APPF")
check_trend("APY")
check_trend("ASML")
check_trend("ATH")
check_trend("ATHM")
check_trend("ATI")
check_trend("ATNI")
check_trend("ATRS")
check_trend("ATTU")##############################öl
check_trend("AXAS")
check_trend("AYR")
check_trend("AYTU")
check_trend("AYX")
check_trend("AZRE")
check_trend("BIDU")
check_trend("BILI")
check_trend("BL")
check_trend("BLFS")
check_trend("BRKS")
check_trend("BSM")
check_trend("BZUN")
check_trend("CAMT")
check_trend("CARG")
check_trend("CCI")
check_trend("CCMP")
check_trend("CCS")
check_trend("CDNA")# vorzeitiger Ausbruch aus Keil, weiter beobachten https://invst.ly/a6ild
check_trend("CELG")
check_trend("CF")
check_trend("CFMS")
check_trend("CLAR")# chart sieht gut aus Volumen bei nächster Base beobachten
check_trend("CMTL")
check_trend("CODA")
check_trend("CORT")
check_trend("COUP")# geiles Teil, da geh ich rein
check_trend("CRK")
check_trend("CSBR")
check_trend("CSGP")
check_trend("CSSE")
check_trend("CUB")
check_trend("CXO")
check_trend("CYBR")# Cybersecurity, gutes Wachstum, auf Base warten
check_trend("CZR")
check_trend("CZZ")
check_trend("DATA")# Tableau
check_trend("DBX")
check_trend("DENN")#chart nicht überzeugend. foodkette
check_trend("DPZ")
check_trend("DRIO")
check_trend("DXPE")
check_trend("EDN")
check_trend("EDRY")
check_trend("EKSO")
check_trend("EMAN")
check_trend("ENV")
check_trend("EPAM")#IT-Consultant und SW Hersteller. Gutes langfristiges Wachstum +20% Boden notwendig
check_trend("EPRT")
check_trend("EQNR")
check_trend("ERF")
check_trend("ERII")
check_trend("EXAS")#chart sieht nicht soooo gut aus
check_trend("EXEL")
check_trend("FANG")
check_trend("FET")
check_trend("FIVE")
check_trend("FLDM")
check_trend("FLGT")
check_trend("FLY")
check_trend("FMC")
check_trend("FNHC")
check_trend("GHDX")# Cancer Score - inverse SKS
check_trend("GLOG")
check_trend("GNK")
check_trend("GOOGL")
check_trend("GPRK")
check_trend("GRUB")
check_trend("GVP")
check_trend("HAYN")
check_trend("HBIO")
check_trend("HCCI")
check_trend("HCLP")
check_trend("HDB")
check_trend("HLX")
check_trend("HMI")
check_trend("HP")
check_trend("HRTX")
check_trend("HTBX")
check_trend("HTGM")
check_trend("HTHT")
check_trend("HUYA")
check_trend("IDXG")
check_trend("IEC")
check_trend("IIN")
check_trend("INCY")
check_trend("INST")
check_trend("INVE")
check_trend("IQ")
check_trend("IRBT")
check_trend("IRS")
check_trend("IRT")
check_trend("JD")
check_trend("JYNT") #physio - schreiben noch schulden!
check_trend("KEG")
check_trend("KEX")
check_trend("LASR")
check_trend("LEAF")
check_trend("LIQT")
check_trend("LLEX")
check_trend("LNG")
check_trend("LRAD")
check_trend("LX")
check_trend("MCB")
check_trend("MDXG")
check_trend("MED")
check_trend("MEDP")
check_trend("MMSI")
check_trend("MPWR")
check_trend("MRAM")
check_trend("MRO")
check_trend("MTLS")
check_trend("MUR")
check_trend("MX")
check_trend("MYND")
check_trend("NBIX")
check_trend("NBR")
check_trend("NCOM")
check_trend("NEO")
check_trend("NEOS")
check_trend("NGVT")
check_trend("NIU")
check_trend("NM")
check_trend("NMIH")
check_trend("NOA")
check_trend("NOG")
check_trend("NOV")
check_trend("NOW")
check_trend("NR")
check_trend("NSP")
check_trend("NSSC")
check_trend("NTN")
check_trend("NVTA")
check_trend("NXTD")
check_trend("OLBK")
check_trend("OLLI")
check_trend("ONDK")
check_trend("ORRF")
check_trend("OTIV")
check_trend("PANW")
check_trend("PCTY")
check_trend("PDCE")
check_trend("PE")
check_trend("PLAB")
check_trend("POWL")
check_trend("PRIM")
check_trend("PRLB")
check_trend("PRPO")
check_trend("PRTA")
check_trend("PSX")
check_trend("QLYS")
check_trend("QNST")
check_trend("QTNA")
check_trend("QUIK")
check_trend("QUOT")
check_trend("RDFN")
check_trend("RDS-A")
check_trend("RDS-B")
check_trend("RIOT")
check_trend("RNET")
check_trend("RYAM")
check_trend("SAFE")
check_trend("SB")
check_trend("SCON")
check_trend("SECO")
check_trend("SEDG")
check_trend("SGYP")
check_trend("SITE")
check_trend("SM")
check_trend("SMTX")
check_trend("SNAP")
check_trend("SOI")
check_trend("SPKE")
check_trend("SPOT")
check_trend("SQ")
check_trend("SRCI")
check_trend("SU")
check_trend("SYX")
check_trend("TAL")
check_trend("TALO")
check_trend("TBBK")
check_trend("TCMD")
check_trend("TEUM")
check_trend("TLGT")
check_trend("TNDM")
check_trend("TOT")
check_trend("TPNL")
check_trend("TRGP")
check_trend("TRHC")
check_trend("TRUP")
check_trend("TS")
check_trend("TSC")
check_trend("TSLA")
check_trend("TTD")
check_trend("TWIN")
check_trend("ULTA")
check_trend("UNT")
check_trend("USAC")
check_trend("USAK")
check_trend("USAT")
check_trend("VCEL")
check_trend("VCYT")
check_trend("VLRX")
check_trend("VNDA")
check_trend("VRTU")
check_trend("VUZI")
check_trend("WPX")
check_trend("WSC")
check_trend("WTM")
check_trend("WUBA")
check_trend("WWE")
check_trend("WYY")
check_trend("XOG")
check_trend("XOM")
check_trend("YNDX")
check_signal("ZTO")'''