MODEL=edhoc_model_draft20200301.pv
TEST=libTest.pv
LIB=edhoc_common.pvl


TSTPASS=grep --color=auto -E "verified|falsified|analysis incomplete"
SRC=edhocM4.spthy
TAMARIN=tamarin-prover --quit-on-warning --heuristic=O --oraclename=oracle.py

# Set this to PASSIVE for passive attacker; else the attacker is DY
#MATTACKER=-Dm4ATTACKER=PASSIVE
MATTACKER=-Dm4ATTACKER=ACTIVE

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
	m4 ${MATTACKER} ${MSIGSTAT} ${SRC} > ${TSIGSTAT}
	m4 ${MATTACKER} ${MSTATSIG} ${SRC} > ${TSTATSIG}
	m4 ${MATTACKER} ${MSTATSTAT} ${SRC} > ${TSTATSTAT}
	m4 ${MATTACKER} ${MSIGSIG} ${SRC} > ${TSIGSIG}
	m4 ${MATTACKER} ${MPSKPSK} ${SRC} > ${TPSKPSK}

# This target checks that all models parses correctly
sense: genModels
	tamarin-prover --parse-only ${TSTATSIG} |& awk "/summary/,/======/"
	tamarin-prover --parse-only ${TSIGSTAT} |& awk "/summary/,/======/"
	tamarin-prover --parse-only ${TSTATSTAT} |& awk "/summary/,/======/"
	tamarin-prover --parse-only ${TSIGSIG} |& awk "/summary/,/======/"
	tamarin-prover --parse-only ${TPSKPSK} |& awk "/summary/,/======/"

# This target verifies all lemmas beginning with "sanity" for all models
alotofsense: genModels
	${TAMARIN} --prove=sanity ${TSTATSIG} |& grep --color=always sanity | ${TSTPASS}
	${TAMARIN} --prove=sanity ${TSIGSTAT} |& grep --color=always sanity | ${TSTPASS}
	${TAMARIN} --prove=sanity ${TSTATSTAT} |& grep --color=always sanity | ${TSTPASS}
	${TAMARIN} --prove=sanity ${TSIGSIG} |& grep --color=always sanity | ${TSTPASS}
	${TAMARIN} --prove=sanity ${TPSKPSK} |& grep --color=always sanity | ${TSTPASS}

# This target is useful for viewing the GUI
interactive: genModels
	tamarin-prover interactive ./ -b=5 --quit-on-warning --heuristic=O --oraclename=oracle.py

auth: genModels
	d=$$(date +%s); tamarin-prover --prove=auth ${TPSKPSK} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/authPSKPSK.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/authPSKPSK.spthy
	d=$$(date +%s); tamarin-prover --prove=auth ${TSIGSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/authSIGSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/authSIGSTAT.spthy
	d=$$(date +%s); tamarin-prover --prove=auth ${TSIGSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/authSIGSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/authSIGSIG.spthy
	d=$$(date +%s); tamarin-prover --prove=auth ${TSTATSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/authSTATSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/authSTATSTAT.spthy
	d=$$(date +%s); tamarin-prover --prove=auth ${TSTATSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/authSTATSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/authSTATSIG.spthy

pfs: genModels
	d=$$(date +%s); tamarin-prover --prove=secrecyPFS ${TPSKPSK} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsImpPSKPSK.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsImpPSKPSK.spthy
	d=$$(date +%s); tamarin-prover --prove=secrecyPFSGIY ${TSIGSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsImpSIGSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsImpSIGSTAT.spthy
	d=$$(date +%s); tamarin-prover --prove=secrecyPFSGIY ${TSIGSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsImpSIGSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsImpSIGSIG.spthy
	d=$$(date +%s); tamarin-prover --prove=secrecyPFSGIY ${TSTATSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsImpSTATSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsImpSTATSTAT.spthy
	d=$$(date +%s); tamarin-prover --prove=secrecyPFSGIY ${TSTATSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsImpSTATSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsImpSTATSIG.spthy

# Appears not needed
#pfsexp: genModels
	#d=$$(date +%s); tamarin-prover --prove=secrecyExp ${TPSKPSK} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsExpPSKPSK.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsExpPSKPSK.spthy
	#d=$$(date +%s); tamarin-prover --prove=secrecyExp ${TSIGSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsExpSIGSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsExpSIGSTAT.spthy
	#d=$$(date +%s); tamarin-prover --prove=secrecyExp ${TSIGSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsExpSIGSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsExpSIGSIG.spthy
	#d=$$(date +%s); tamarin-prover --prove=secrecyExp ${TSTATSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsExpSTATSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsExpSTATSTAT.spthy
	#d=$$(date +%s); tamarin-prover --prove=secrecyExp ${TSTATSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/pfsExpSTATSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/pfsExpSTATSIG.spthy

# This target is for commandline usage but only see if properties hold
all: genModels
	tamarin-prover --prove ${TPSKPSK} --quit-on-warning --heuristic=O --oraclename=oracle.py |& | ${TSTPASS}
	tamarin-prover --prove ${TSIGSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& | ${TSTPASS}
	tamarin-prover --prove ${TSIGSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& | ${TSTPASS}
	tamarin-prover --prove ${TSTATSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& | ${TSTPASS}
	tamarin-prover --prove ${TSTATSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& | ${TSTPASS}

clean:
	rm TMP_*

proverifAll:
	proverif ${LOADLIB} ${MODEL}

proverifRes:
	proverif ${LOADLIB} ${MODEL} | grep RESULT

proverifTst:
	proverif ${LOADLIB} ${TEST}

