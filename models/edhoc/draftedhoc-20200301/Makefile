MODEL=edhoc_model_draft20200301.pv
TEST=libTest.pv
LIB=edhoc_common.pvl

TSTPASS=grep --color=auto -E "verified|falsified|analysis incomplete"
SRC=edhocM4.spthy
TAMARIN_CLEAN=tamarin-prover
TAMARIN=${TAMARIN_CLEAN} --quit-on-warning --heuristic=O --oraclename=oracle.py
PROOFS=proofs


# Set this to PASSIVE for passive attacker; else the attacker is DY
#MATTACKER=-Dm4ATTACKER=PASSIVE
MATTACKER=-Dm4ATTACKER=ACTIVE

# Set this switch to include AD_3 in the model
#MAD3=-Dm4AD3

# All flags that are required for all models
MFLAGS=${MATTACKER} ${MAD3}

# Flags and filenames used for each method-model
METHODPAIRS=PSK_PSK SIG_SIG SIG_STAT STAT_SIG STAT_STAT
METHODSINGLES=PSK SIG STAT

MSIGSIG=-Dm4METHODI=SIG -Dm4METHODR=SIG
SIGSIG=edhoc_SIG_SIG.spthy
TSIGSIG=TMP_${SIGSIG}
MSIGSTAT=-Dm4METHODI=SIG -Dm4METHODR=STAT
SIGSTAT=edhoc_SIG_STAT.spthy
TSIGSTAT=TMP_${SIGSTAT}
MSTATSIG=-Dm4METHODI=STAT -Dm4METHODR=SIG
STATSIG=edhoc_STAT_SIG.spthy
TSTATSIG=TMP_${STATSIG}
MSTATSTAT=-Dm4METHODI=STAT -Dm4METHODR=STAT
STATSTAT=edhoc_STAT_STAT.spthy
TSTATSTAT=TMP_${STATSTAT}
MPSKPSK=-Dm4METHODI=PSK -Dm4METHODR=PSK
PSKPSK=edhoc_PSK_PSK.spthy
TPSKPSK=TMP_${PSKPSK}

# Using GNU time we can get more useful information about memory and time
# consumption.
# We log in this format: "[hours:]:minutes:seconds MB-of-memory"
# Time is measured in real time, becasue we care about how long we actually
# have to wait for verification runs
TIMEFMT=%E
TIME=/usr/bin/time -f ${TIMEFMT}


# Don't change the METH string or the LEMMAPREFIX strings. They are used
# as variables in substitutions below
TIME_PROVE_AND_LOG=(time ${TAMARIN} --prove=LEMMAPREFIX TMP_METH) > ${PROOFS}/LEMMAPREFIX-METH 2>&1;

check:
	grep --color=auto -E "verified|falsified|(user.*m.*s)" ${PROOFS}/*

genModels:
	mkdir -p proofs
	m4 ${MFLAGS} ${MSIGSTAT} ${SRC} > ${TSIGSTAT}
	m4 ${MFLAGS} ${MSTATSIG} ${SRC} > ${TSTATSIG}
	m4 ${MFLAGS} ${MSTATSTAT} ${SRC} > ${TSTATSTAT}
	m4 ${MFLAGS} ${MSIGSIG} ${SRC} > ${TSIGSIG}
	m4 ${MFLAGS} ${MPSKPSK} ${SRC} > ${TPSKPSK}

# This target is useful for viewing the GUI
interactive: genModels
	${TAMARIN_CLEAN} interactive ./ -b=5 --quit-on-warning --heuristic=O --oraclename=oracle.py

# This target checks that all models parses correctly
sense: genModels
	$(foreach meth,${PSKPSK} ${SIGSIG} ${STATSIG} ${SIGSTAT} ${STATSTAT},\
		${TAMARIN_CLEAN} --parse-only TMP_$(meth) 2>&1\
			| grep --color=auto -E "analyzed|error|tamarin-prover:.*";\
	 )

# This target verifies all lemmas beginning with "sanity" for all models
alotofsense: genModels
	#$(foreach meth,${PSKPSK},)
	$(foreach meth,${PSKPSK} ${SIGSIG} ${STATSIG} ${SIGSTAT} ${STATSTAT},\
		$(subst METH,$(meth),\
			$(subst LEMMAPREFIX,sanity,${TIME_PROVE_AND_LOG})\
		 )\
	 )

# Injective agreement on session key except when G_IY is included for I.
# Inj-agreement for full session key for R.
auth: genModels
	#$(foreach meth,${PSKPSK},)
	$(foreach meth,${PSKPSK} ${SIGSIG} ${STATSIG} ${SIGSTAT} ${STATSTAT},\
		$(subst METH,$(meth),\
			$(subst LEMMAPREFIX,authInj,${TIME_PROVE_AND_LOG})\
		 )\
	 )

authimplicit: genModels
	#$(foreach meth,${PSKPSK},)
	$(foreach meth,${PSKPSK} ${SIGSIG} ${STATSIG} ${SIGSTAT} ${STATSTAT},\
		$(subst METH,$(meth),\
			$(subst LEMMAPREFIX,authGIYImplicit,${TIME_PROVE_AND_LOG})\
		 )\
	 )

pfs: genModels
	#$(foreach meth,${PSKPSK},)
	$(foreach meth,${PSKPSK} ${SIGSIG} ${STATSIG} ${SIGSTAT} ${STATSTAT},\
		$(subst METH,$(meth),\
			$(subst LEMMAPREFIX,secrecyPFS,${TIME_PROVE_AND_LOG})\
		 )\
	 )

all: sense alotofsense auth authimplicit pfs

clean:
	rm ./TMP_*

proverifAll:
	proverif ${LOADLIB} ${MODEL}

proverifRes:
	proverif ${LOADLIB} ${MODEL} | grep RESULT

proverifTst:
	proverif ${LOADLIB} ${TEST}

