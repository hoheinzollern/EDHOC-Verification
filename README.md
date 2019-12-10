# EDHOC-Verification
Verification models and documentation of the EDHOC/OSCORE protocols

## Documentation and models

All documentation is present in [doc](doc) and relative models in
[models](models).

## Current results

### EDHOC

[models/edhoc](models/edhoc) contains the verification efforts of [draft-selander-ace-cose-ecdhe](https://datatracker.ietf.org/doc/draft-selander-ace-cose-ecdhe/), in particular of versions 08 and 11 (here referred to as draft08 and draft11). We have verified/disproved the following properties:
1. secrecy of application data (APP_2 susceptible to active attacks, APP_3 is secure) and session keys
2. identity protection (of the initiator, active attacks to show the responder's identity)
3. injective agreement proving mutual authentication of session keys and application data
4. perfect forward secrecy
5. session independence (only draft11)


The thesis [[1](doc/PJ_Formal_Verification_of_EDHOC_SSR18.pdf)] present the initial verification of EDHOC,
which was later refined into [[2](doc/BJPS_Formal_Verification_of_EDHOC_SSR18.pdf)]. Finally, [[3](doc/slides-interim-2019-secdispatch-01-sessa-formal-analysis-of-edhoc-00.pdf)] is the presentation of our verification of draft11, including the session independence properties.

Remaining to be verified: algorithms for selecting ciphers against downgrade attacks like FREAK and Logjam. Composability with OSCORE and possibly other protocols

### OSCORE

This verification effort is described in the document [[4](doc/Andersen_Verification_of_OSCORE_BSc_Thesis.pdf)]. Briefly speaking, it models a typical flow of interaction between a client and a server who have already established a security context (i.e. a common *master secret* possibly derived using EDHOC, an *ID context*, sender and recepient *IDs*, *session keys* and *sequence numbers*) where the communication is controlled by a potentially malicious proxy.

The verified properties are:
1. Integrity, Request-response binding & Non-replayability
2. Confidentiality (modelled by checking that the attacker cannot obtain the payload of the exchanged messages between two honest hosts)

Here more work is needed to check that we cover all possible protocol flows (for example more thought should be given to how OSCORE can coexist with other RESTful APIs), and whether more advanced security properties should be considered, (for example regarding the interplay between Encrypted, Integrity protected and Unencrypted data).

## References

1. Petersen, Jørgensen - Formal verification of EDHOC (BSc Thesis)
2. Bruni, Jørgensen, Petersen, Schürmann - Formal Verification of EDHOC (SSR18)
3. Bruni - Formal verification of EDHOC draft11 (Slides, IETF Interim 2019 Secdispatch 01)
4. Andersen - Verification of OSCORE (BSc Thesis)
