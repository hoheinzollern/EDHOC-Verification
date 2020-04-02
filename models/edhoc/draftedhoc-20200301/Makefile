MODEL=edhoc_model_draft20200301.pv
TEST=libTest.pv
LIB=edhoc_common.pvl

ERR=echo "SANITY FAILURE"
ORFAIL=grep "All well-formedness checks were successful" || (${ERR}; exit)
SRC=edhocM4.spthy
TAMARIN=tamarin-prover --quit-on-warning --heuristic=O --oraclename=oracle.py
TAMARIN_SANITY=${TAMARIN} --prove=sanity

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
	m4 ${MSIGSTAT} ${SRC} > ${TSIGSTAT}
	m4 ${MSTATSIG} ${SRC} > ${TSTATSIG}
	m4 ${MSTATSTAT} ${SRC} > ${TSTATSTAT}
	m4 ${MSIGSIG} ${SRC} > ${TSIGSIG}
	m4 ${MPSKPSK} ${SRC} > ${TPSKPSK}

sense: genModels
	${TAMARIN} ${TSTATSIG} |& ${ORFAIL}
	${TAMARIN} ${TSIGSTAT} |& ${ORFAIL}
	${TAMARIN} ${TSTATSTAT} |& ${ORFAIL}
	${TAMARIN} ${TSIGSIG} |& ${ORFAIL}
	${TAMARIN} ${TPSKPSK} |& ${ORFAIL}

alotofsense: genModels
	${TAMARIN_SANITY} ${TSTATSIG} |& ${ORFAIL}
	${TAMARIN_SANITY} ${TSIGSTAT} |& ${ORFAIL}
	${TAMARIN_SANITY} ${TSTATSTAT} |& ${ORFAIL}
	${TAMARIN_SANITY} ${TSIGSIG} |& ${ORFAIL}
	${TAMARIN_SANITY} ${TPSKPSK} |& ${ORFAIL}

all:
	proverif ${LOADLIB} ${MODEL}

res:
	proverif ${LOADLIB} ${MODEL} | grep RESULT

tst:
	proverif ${LOADLIB} ${TEST}

