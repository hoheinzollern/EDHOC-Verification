MODEL=edhoc_model_draft20200301.pv
TEST=libTest.pv
LIB=edhoc_common.pvl

ERR=echo "SANITY FAILURE"
ORFAILPARSE=grep "All well-formedness checks were successful" || (${ERR}; exit)
ORFAILSANITY=grep "verified" || (${ERR}; exit)
SRC=edhocM4.spthy
TAMARIN=tamarin-prover --quit-on-warning --heuristic=O --oraclename=oracle.py
TAMARIN_SANITY=${TAMARIN} --prove=sanity

# Set this to PASSIVE for passive attacker; else the attacker is DY
MATTACKER=-Dm4ATTACKER=PASSIVE

MSIGSIG=-Dm4METHODI=SIG -Dm4METHODR=SIG
TSIGSIG=TMP_edhoc_SIG_SIG.spthy
MSIGSTAT=-Dm4METHODI=SIG -Dm4METHODR=STAT
TSIGSTAT=TMP_edhoc_SIG_STAT.spthy
MSTATSIG=-Dm4METHODI=STAT -Dm4METHODR=SIG
TSTATSIG=TMP_edhoc_STAT_SIG.spthy
MSTATSTAT=-Dm4METHODI=STAT -Dm4METHODR=STAT
TSTATSTAT=TMP_edhoc_STAT_STAT.spthy
MPSKPSK=-Dm4METHODI=PSK -Dm4METHODR=PSK
TPSKPSK=TMP_edhoc_PSK_PSK.spthy

genModels:
	m4 ${MATTACKER} ${MSIGSTAT} ${SRC} > ${ATT_A}${TSIGSTAT}
	m4 ${MATTACKER} ${MSTATSIG} ${SRC} > ${ATT_A}${TSTATSIG}
	m4 ${MATTACKER} ${MSTATSTAT} ${SRC} > ${ATT_A}${TSTATSTAT}
	m4 ${MATTACKER} ${MSIGSIG} ${SRC} > ${ATT_A}${TSIGSIG}
	m4 ${MATTACKER} ${MPSKPSK} ${SRC} > ${ATT_A}${TPSKPSK}

# This target checks that all models parses correctly
sense: genModels
	${TAMARIN} ${TSTATSIG} |& ${ORFAILPARSE}
	${TAMARIN} ${TSIGSTAT} |& ${ORFAILPARSE}
	${TAMARIN} ${TSTATSTAT} |& ${ORFAILPARSE}
	${TAMARIN} ${TSIGSIG} |& ${ORFAILPARSE}
	${TAMARIN} ${TPSKPSK} |& ${ORFAILPARSE}

# This target verifies all lemmas beginning with "sanity" for all models
alotofsense: genModels
	${TAMARIN_SANITY} ${TSTATSIG} |& ${ORFAILSANITY}
	${TAMARIN_SANITY} ${TSIGSTAT} |& ${ORFAILSANITY}
	${TAMARIN_SANITY} ${TSTATSTAT} |& ${ORFAILSANITY}
	${TAMARIN_SANITY} ${TSIGSIG} |& ${ORFAILSANITY}
	${TAMARIN_SANITY} ${TPSKPSK} |& ${ORFAILSANITY}

interactive: genModels
	tamarin-prover interactive ./ --quit-on-warning --heuristic=O --oraclename=oracle.py

alotofsense-psk: genModels
	${TAMARIN_SANITY} ${TPSKPSK}

clean:
	rm TMP_*

all:
	proverif ${LOADLIB} ${MODEL}

res:
	proverif ${LOADLIB} ${MODEL} | grep RESULT

tst:
	proverif ${LOADLIB} ${TEST}

