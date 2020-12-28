Type "Make all" to generate the Tamarin models from the edhocM4.spthy file and
verify them.

Type "Make genModels" to only generate the Tamarin models.

The generated models will appear in the current directory and their filenames
are prefixed with the string TMP_.  There is one model for each EDHOC method.

The proofs are written into the directory named proofs.

Type "Make check" after Tamarin completes the "Make all" target to print
a summary from the proofs.

After checking the results, the directory can be packed into a tar-ball by
typing "make pack".
