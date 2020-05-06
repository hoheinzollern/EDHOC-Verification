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

# This target is for commandline usage
cl: genModels
	#d=$$(date +%s); tamarin-prover --prove ${TPSKPSK} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/PSKPSK.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/PSKPSK.spthy
	#d=$$(date +%s); tamarin-prover --prove ${TSIGSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/SIGSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/SIGSTAT.spthy
	d=$$(date +%s); tamarin-prover --prove ${TSIGSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/SIGSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/SIGSIG.spthy
	#d=$$(date +%s); tamarin-prover --prove ${TSTATSTAT} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/STATSTAT.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/STATSTAT.spthy
	#d=$$(date +%s); tamarin-prover --prove ${TSTATSIG} --quit-on-warning --heuristic=O --oraclename=oracle.py |& tee proofs/STATSIG.spthy; echo "Execution time: $$((($$(date +%s)-d)/60)) minutes" >> proofs/STATSIG.spthy

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

