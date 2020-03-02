MODEL=edhoc_model_draft20200301.pv
LIB=edhoc_common.pvl
LOADLIB=-lib ${LIB}

all:
	proverif ${LOADLIB} ${MODEL}

res:
	proverif ${LOADLIB} ${MODEL} | grep RESULT

