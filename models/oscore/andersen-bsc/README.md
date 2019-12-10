# OSCOREProverif
This is the ProVerif model developed in association with the formal verification of OSCORE.
CBOR
 -
  - OSCORE uses untagged COSE_Encrypt0 structure, with AEAD.
  - Plaintext denotes the data that is to be encrypted and integrity protected. 
  - AAD is integrity protection only
  - The COSE object (CBOR Object signing and Encryption)
    - ‘Protected’ field is empty
    - ‘Unprotected’ field includes:
      - “Partial IV” - Sender Sequence number. 
        - Present in requests
        - Only present in response to Observe Registrations
      - The “key identifier” - Sender ID
        - Present in requests
        - Not present in responses.
      - “kid context” contains an ID context.
        - Can be present in requests
        - MUST NOT be present in response
        - If present, recipient must use context with that ID context.
      - “Ciphertext” field:
        - Is computed from the secret key (recipient or sender)
          - AEAD nonce
            - AEAD nonce is computed from the partial IV, network byte order, sender ID of endpoint that generated partial IV, and common IV
            - When there is a single response to a request, the request and the response should typically use the same nonce.
          - Plaintext
            - An CoAP Message without header:
              - The Code of the original CoAP message
              - Class E option message fields
              - Payload of the original CoAP message.
          - and Additional Authenticated Data
              - OSCORE Version
              - Array of algorithms
              - KID
              - PIV
              - Class I options
  - Header Compression in OSCORE 
    - COSE is not optimized for usage in a stateful security protocol, which leads to larger than necessary message expansion. Therefore OSCORE simply removes redundant information from the COSE object, which significantly reduces the overhead. This is also known as the “compressed COSE object”
  - The COSE_Enncrypt0 object is transported in the option and in the Payload. The payload contains the ciphertext of the COSE object.

CoAP
 -
 CoAP is a web transfer protocol, designed for constrained nodes and networks.
 - CoAP uses proxies for scalability and efficency. DTLS for security. (important?)
 - Message ids:
    - Each message contains a message ID used for detecting duplicates and for optional reliability. 
    - Reliability is achieved by marking a message as Confirmable. 
    - A message with confirmable is resent until the endpoint sends an ACK message. 
    - The ACK message should therefore have the same message ID. 
    - If a message should not achieve reliablity, the message can be marked as non-confirmable. These are not confirmed, however they have a message id to detect duplicates.
 - Token:
    - Every request carries a client-generated token that the server MUST echo (without modification) in any resulting response. 
    - Binding to “DTLS” for security.
  - DTLS
      - CoAP request and response semantics are carried in CoAP messages, which include either a Method Code or Response Code. 
      - Security modes
    - PreSharedKeys: DTLS is enabled, there is a list of pre-shared keys [RFC4279], and each key includes a list of which nodes it can be used to communicate with as described in Section 9.1.3.1. 
      - Requires DTLS or TLS to be terminated at the proxy. 
      - Therefore proxy has access to the data required for performing the intended proxy functionality, but is also able to eavesdrop on, or manipulate any part of, the message payload and metadata in transit between the endpoints.-.
- Headers fields and payload. 
  - CoAP header fields are required to be read and or changed by CoAP proxies and cannot in general be protected end-to-end between endpoints. OSCORE only protects the CoAP request/response layer.So fields such as Type and Message ID are not protected.
  - The CoAP Header fields Code is protected by OSCORE. The Code is encrypted and integrity protected to prevent eavesdroping or manipulation.
  - In transit, dummy codes 0.02 (POST) for requests and (2.04) for responses (changed)
  - When a receiving endpoint receives an OSCORE message, it discards the outer code in the oscore message and writes the code of the cose object into the decrypted CoAP message. (The real not dummy code)

OSCORE
 -
 - Protocol translations from 'x' to CoAP requires DTLS to be terminated at the proxy. Therefore, the proxy can manipulate all data as a dolev yao. OSCORE changes that, as a security protocol
   - Protects CoAP and CoAP mappable HTTP requests and responses end-to-end across intermediary nodes such as CoAP forward proxies and cross-protocol translators, including HTTP-to-CoAP proxies.
   - OSCORE essentially protects the RESTful interactions; the request method, the requested resource, the message payload, etc.
   - It is designed to protect as much information as possible while still allowing CoAP proxy operations.
 - Protects requests across intermediary nodes. However, the messaging layer (T of a CoAP request) are unprotected, aswell as the token.
   - OSCORE does not protect the CoAP messaging layer nor the CoAP token which may change between the endpoints. 
 - OSCORE requires that the client and the server establish a shared security context, for processing of the COSE objects. This is done through an AEAD algorithm
    - May be used together with TLS or DTLS over one or more hops in the end to end path.
   - OSCORE ensures security through the following properties:
   - Transform a HTTP/CoAP message to an “OSCORE” message.
     - The original CoAP/HTTP message is translated to CoAP, and protected in a COSE object. 
     - The encrypted message fields of this COSE object are transported in the CoAP payload of the OSCORE message. 
     - The OSCORE option is included in the message, and it indicates that OSCORE processing has occured.
   - The shared security context:
     - A recipient uses an ID to get a recipient context.
       - The recipient context contains the necessary information to decrypt and verify a message
     - A sender uses an ID to get a sender context.
       - The sender context contains the necessary information to encrypt a message
     - This is used for the symmetric communication between the two endpoints.
 - Unique for OSCORE:
   - Both endpoints MUST keep the association (Token, Security Context, Partial IV of the request) in order to be able to find the security context and compute the AAD to protect or verify the response. The association MAY be forgotten after it has been used to successfully protect or verify the response. 
   - Works in very constrained nodes and networks, thanks to its small message size and the restricted code and memory requirements.
   - OSCORE can be applied to both reliable and unreliable transports.
   - The CoAP Header fields Code is protected by OSCORE. The Code is encrypted and integrity protected to prevent eavesdroping or manipulation.
   - When a receiving endpoint receives an OSCORE message, it discards the outer code in the oscore message and writes the code of the cose object into the decrypted CoAP message. (The real not dummy code)
   - Endpoints may operate as both a client and server
     - The endpoints are not allowed to change IDs when switching roles. The same security context should be used.
   - Input parameters need to be known and agreed on by both endpoints (For the security context)
     - **Master Secret**
     - **Sender ID**, which must be unique in the set of all security context where the same master secret and master salt is used.
       - May be derived from negotiating with a trusted third party or out of band (Interesting maybe?)
     - **Recipient ID**
   - There are also some optional prerequisites, which if not given, will default to a preset value.
     - **Master Salt**
     - **AEAD algorithm**
     - **HKDF** - “HKDF must be one of the HMAC based HKDF algorithms for COSE. SHA-256 is mandatory”
     - **Replay window**
   - OSCORE uses untagged COSE_Encrypt0 structure, with AEAD.
 - **The COSE object**
   - ‘Protected’ field is empty
   - ‘Unprotected’ field includes:
   - “Partial IV” - Sender Sequence number
 - The protocol uses pre-shared keys which may have been established out of band or with a key establishment protocol (EDHOC)
 - OSCORE supports the protection of **SIGNALING MESSAGES**
   - Signaling messages were introduced in CoAP running on TCP/TLS.
   - A signaling message will give information about
     - The maximum message size of the connection, for example
     - Shut down the connection in an orderly fashion
     - Provide diagnostic information when terminating a connection.
   - They are structured very much like the basic kinf od CoAP message, there are a code, a token, options and an optional payload.
 - The OSCORE message is related to the original CoAP message in the following way:
    - The CoAP message is protected in a COSE object. 
    - The encrypted message fields of this COSE object are transported in the CoAP payload of the OSCORE message
    - the OSCORE option is included in the message.
  - **Message binding:**
    - OSCORE binds responses to the requests by including the kid and Partial IV of the request in the AAD of the response.
    - The message binding does not guarantee that misbehaving server created the response before receiving the request. ie it does not verify server aliveness.
    - Sequence Numbers
      - An AEAD nonce MUST NOT be used more than once per AEAD key. The uniqueness particularly depends on a correct usage of Partial IV (which encode the Sender Sequence Numbers). If messages are processed concurrently the operation of reading and increasing  the sender sequence number MUST BE atomic.
    - Maximum Sequence Number
      - If the sender sequence number exceeds the maximum, the endpoiunt MUST NOT process and more messages with the given Sender Context. The endpoint SHOULD acquire a new security context.
    - Freshness
      - For requests, OSCORE provides only the guarantee that the request is not older than the security context.
      - Given an honest server, the message binding guarantees that a response is not older than its request. This gives absolout freshness unless the responses are notifications. For notifications the freshness gets weaker. 
    - Replay Windows
      - A server verify that the Partial IV (Sender Sequence Number) has not been received before. If this verification fails the server stops processing the message.
 - **OSCORE option**
   - The OSCORE option indicates that the CoAP message is an OSCORE message and that it contains a compressed COSE object.
   - An OSCORE option includes a sender sequence number, sender id, ID context.
   - If an endpoint receives a CoAP message without payload with an OSCORE option, it is malformed.
   - A successful response to a request with the OSCORE option shall contain the OSCORE option.
   - If the OSCORE option is empty, and the CoAP message contains no payload, the message is malformed and has to be rejected.
 - **The OSCORE option Value**
   - The value of the oscore option SHALL contain the OSCORE flag bits, the Partial IV, the kid context, and the kid parameter. The payload contains the ciphertext of the COSE object.
 - Message Fields:
   - There exists three ways of protecting CoAP Messages:
   - Class E: encrypted and integrity protected (inner)
   - Class I: Integrity protected (outer) (There are no class i defined options)
   - Class U: Unprotected (outer)
      - The sender puts Class E message fields in the ciphertext of the COSE object in the OSCORE message.
      - The sender also puts Class I message fields in the Additional Authenticated Data of the AEAD algorithm.
      - The sender does not protect Class U.
      - Class I and Class U are transferred in the header or options part of the OSCORE message, which is visible to proxies.
        - Inner option messages fields are used to communicate with the other endpoint, and should put the option message field in the original CoAP message into the plaintext of the COSE object.
        - Outer option message fields are used to support proxy operations. 
      - Note that some options require special processing, and for example, the Max-Age option may be both included as an inner and as an outer option. This is because proxies should not cache error response caused by OSCORE processing, so the server might set the Class U Max-Age message field with value zero. Sucessful OSCORE messages are non-cacheable so they dont have the need for that.
      - **The URI-Host and URI-Port**
        - The URI Host specifdies the internet host
          - The default value is the IP literal representing the destination IP address.
        - The URI port specifies the transport layer port number
          - The default value is the destination UDP port.
        - Each URI-Path option specifies one segment of the absolute path
        - Each URI-Query specifies one argument, parameterizing the resource
        - When these values are set to their default values, they are omitted from the message. However, to support forward proxy operations, these options need to be of class U. The manipulation of these unprotected message fields must not lead to an OSCORE message becoming verified by an unintended server. Different servers shall have different security contexts.
           - Explicit Uri-Host and Uri-Port Options are typically used when an endpoint hosts multiple virtual servers, and the default values are usually sufficient.

      - **Proxy URI and Proxy Scheme**
      - The Proxy URI option is used when making a request to a forward proxy. The forward proxy should then either serve a cached response or forward the request.
      - Firstly the Proxy-URI of the original CoAP message has to be decomposed into Proxy-Scheme, URI-host, URI-port URI-Path, and URI-Query.
        - URI Path and URI Query are class E options, and should be encrypted.
        - The Proxy-URI option of the OSCORE message shall be set to a composition of Proxy-Scheme, Uri-Host and Uri-Port, and procssed as Class U.
      - **Block Options**
        - OSCORE Supports block options which is used when a payloads size is above average.
        - ("Block1", "Size1") is used to refer to the transfer of the resource that pertains to the request
        - ("Block2", "Size2") is used to refer to the transfer of the resource that pertains to the RESPONSE.
        - Nothing more to add, will stay irrelevant.
      - **Observations**
        - CoAP Supports the publish-subscribe model through the addition of the Observation option.
        - The inner observe shall be used to protect the value of the observe option between endpoints
        - The outer observe is used to support forwarding by proxies.
        - The server includes a "new" partial iv **not sure what you mean here!** in responses to Observe registrations.
        - **Cancellations**
          - The Observation option allows a server to send "notifications" when a change in resource occur. The subscribers can cancel their subscription by sending a RST message. Another way to cancel is by eagerly sending a GET request that has the token field set to the token of the observation to be cancelled, and includes an Observe option with the value deregister (1). Everything else must be identical to the registration request.
        - When using Observe the Outer Code must be set to FETCH because POST is undefined for Observe.
        - **Registrations***
          - The inner and outer observe must contain the observe value of the original CoAP request. When a new observe request is issued, a new partial IV must be used, so the payload and OSCORE option is changed.
            - **Server**
              - Uses the Partial IV of the new request as the request_piv of all associated notifications
- In case of reliable and ordered transport from endpoint to endpoint, the server MAY just store the last received partial IV and recquire that newly receivedPartial IVs rquals the last received. However in case of mixed transports and messages such a replay mechanism may be too restrictive.

OSCORE Security
-
- Uses CBOR Object Signing and Encryption. A compressed version of COSE is used. 
  - The use of OSCORE is signaled in CoAP with a new option. The solution transforms a CoAP/HTTP message into an “OSCORE message”
- The security context
  - “The set of information elements necessary to carry out the cryptographic operations in OSCORE.”
  - For each endpoint the security context is composed of a “Common Context”, a “Sender Context”, and a “Recipient Context”
- OSCORE requires that client and server establish a shared security context used to process the COSE object. OSCORE uses AEAD (Authenticated Encryption Algorithm with Additional Data) for protecting data between a client and a server.
  - It is derived based on a shared secret and a key derivation function.
    - The endpoints protect messages to send using the Sender Context and verify messages received using the Recipient context. They are derived from the Common Context + other data.
    - The sender Context of one endpoint matches the recipient context of the other endpoint and vice versa.
  - Common Context:
    - AEAD Algorithm: The COSE AEAD algorithm to use for encryption
    - Key Function: derive the sender key, recipient key, and initialization vector.
    - Master Salt - used with key function
    - Master secret - used with key function.
    - ID context: sometimes used to identify the common context.
      - If an endpoint has the same recipient ID with different recipient contexts then the endpoint may need to try multiple times before verifying the right security context. The ID context is used to distinguish between security context.
    - An “common” initialization vector derived from master secret master salt and id context. Used for the nonce in AEAD algorithm.
  - Sender Context:
    - Sender ID: byte string used to identify the sender context. Can be used to derive AEAD keys and “Common IV”
    - Sender Key
    - Sender Sequence Number; used to enumerate requests.
      - The sender sequence number is initialized to 0.
  - Recipient Context:
    - Recipient ID
    - Recipient Key
    - Replay Window; (Verify requests received) 
      - The default is DTLS-type replay protection with a window size of 32 (Not sure what 32 means - bits? )
- Generating the security context:
  - Must have Master Secret, Sender ID, Recipient ID.
  - Optionally: AEAD algorithm (or it is default)
  - Optionally: Master Salt
  - Optionally: Key function
  - Optionally: Replay window
  - Key = kFunction(Master Secret, Sender ID, Recipient ID, type(key or vector), length) //I assume
- Requirements on security:
  - The tuple (Master Secret, Master Salt, ID context, Sender ID) must be unique.
  - (ID context, Sender ID) shall be unique in all security contexts with the same master salt and master key.
  - If an endpoint has the same RECIPIENT Id with different Recipient contexts then the endpoint may need to try multiple times before verifying the right security context.
  - ID’s can be assigned from a trusted third party. (and others, but this is what we will use)

The ProVerif Model
 -
 - Does NOT support signaling
 - Does NOT support observation
 - Does NOT support Block options
 - Does NOT support Proxy-URI/Host-URI
 - Does NOT support any other type of option except the OSCORE option


***CoAP***

In RFC 7252 A CoAP Message format is defined as the following:
```

      0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |Ver| T |  TKL  |      Code     |          Message ID           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Token (if any, TKL bytes) ...
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Options (if any) ...
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |1 1 1 1 1 1 1 1|    Payload (if any) ...
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

           Figure 3: CoAP Message Format as Defined in RFC 7252
```

In Proverif there exists no notion of byte ordering, and some aspect of the CoAP message only induces more overhead, so the message format used in the ProVerif model has been abstracted to only include parts necessary for OSCORE to work. Due to time constraints it has only been possible to include the OSCORE Option for now:
```

    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | T |    Dummy Code    |          Message ID                    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Token                                                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  OSCORE Option(Sender ID, Sender Sequence Number, ID Context) |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Encrypted Payload                                            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

           Figure 4: CoAP Message Format in OSCORE Proverif MODEL
```
***HKDF***
The HKDF is defined in the document as a function which will use some HKDF algorithm to derive keys that can be used to encrypt messages.

The HKDF function from the document defines the procedure as follows (assuming the use of HMAC-SHA-256 default function): 
  - PRK = HMAC-SHA-256(Master Salt, Master Secret)
  - output parameter = HMAC-SHA-256(PRK, info || 0x01)

The HKDF function in ProVerif is abstracted to become a function that returns a key given the parameters Master Secret, Master Salt, INFO, and length of key respectively.

For example, a sender key is derived from the following:
```
let senderInfo = (senderID, idcontext, AES_CCM, label_key) in let senderKey = HKDF(msecret, msalt, senderInfo, alg_key_length(AES_CCM, label_key))

Where HKDF is defined as follows:

fun HKDF(bitstring, bitstring, bitstring, bitstring): key.
```
Where the INFO object is defined as follows:

- The INFO object in ProVerif: 
```
A tuple of: (SenderID/RecipientID/EmptyID, IDContext, AES_CCM - Hardcoded, KEY/IV label)
```
- The INFO object from the Document: A CBOR representation:
```
      info = [
        id : bstr,
        id_context : bstr / nil,
        alg_aead : int / tstr,
        type : tstr,
        L : uint,
      ]
```
***Plaintext***
Plaintext is encoded as a CoAP message without header, e.g
```
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |     Code      |    Class E options (if any) ...
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |1 1 1 1 1 1 1 1|    Payload (if any) ...
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       (only if there
         is payload)
```
So, given it's basic structure we just call it a tuple, and give it a unique identifier for attacking:

```
    let plaintext = ((CoAP_GETCode, isLightBulbTurnedOn), msg1id) in
```

***AEAD***

Encryption of parts of the CoAP message is done through the COSE_Encrypt0 structure which is used when a recipient structure is not needed because the key to be
  used is known implicitly.
  
In the document, it is defined as follows: 
```
  COSE_Encrypt0 = [
       Headers,
       ciphertext : bstr / nil,
   ]
   ```
   Where the headers being set are: **Partial IV**, **KID**, and **KID Context**.
   The Ciphertext is computed from the **secret key** (Sender Key or Recipient Key), **AEAD Nonce**, **plaintext** and the **Additional Authenticated Data** (AAD).

Given that ProVerif does not have to contain to a specific structure to utilize functions, the notion of an Encrypt0 structure does not exist in the model. Instead, ciphertext is produced from the function:

```
let ciphertext = aeadEncrypt(senderKey, aead_nonce, plaintext, aad) 

Where AEADEncrypt is defined as:

fun aeadEncrypt(key, nonce, bitstring, bitstring): bitstring.
```
***Additional Authenticated Data***

The additional authenticated data is a collection of data which is necessary to integrity protect, e.g KID and Sender Sequence Number, where the OSCORE version and the AEAD Algorithm is included as to make sure that both endpoints are executing OSCORE on the same terms. As in the document, the bytestring is prepended by an "Encrypt0" string which indicates that the AAD is for the content encryption of a COSE_Encrypt0 data structure.

```
    let aad = (encrypt0, oscore_version_one, AES_CCM, recipientID, partial_iv) in
```

In the document, the AAD is composed quite differently. Firstly, an external aad is composed by wrapping a CBOR array in a bitstring. This array contains the oscore version, supported algorithms, KID, PIV and Class I options. This array is then populated into an Enc_structure where it will go in the external_aad parameter. It looks like this:

```
   Enc_structure = [
       context : "Encrypt" / "Encrypt0" / "Enc_Recipient" /
           "Mac_Recipient" / "Rec_Recipient",
       protected : empty_or_serialized_map,
       external_aad : bstr
   ]
```
***The AEAD Nonce***
In ProVerif, the AEAD nonce is a result of a cryptographic function where it is assumed that it is infeasible to reproduce without having the correct inputs, which looks like this:
```
let aead_nonce = aeadNonce(senderID, partial_iv, CommonIv)

Where aeadNonce() is defined as:

fun aeadNonce(id, bitstring, key) : nonce.
```

This differs from the document where the AEAD nonce is obtained through a series of binary operations:

1.  left-pad the Partial IV (PIV) with zeroes to exactly 5 bytes,

2.  left-pad the Sender ID of the endpoint that generated the Partial
    IV (ID_PIV) with zeroes to exactly nonce length minus 6 bytes,

3.  concatenate the size of the ID_PIV (a single byte S) with the
    padded ID_PIV and the padded PIV,

4.  and then XOR with the Common IV.

E.g:
```
          <- nonce length minus 6 B -> <-- 5 bytes -->
     +---+-------------------+--------+---------+-----+
     | S |      padding      | ID_PIV | padding | PIV |----+
     +---+-------------------+--------+---------+-----+    |
                                                           |
      <---------------- nonce length ---------------->     |
     +------------------------------------------------+    |
     |                   Common IV                    |->(XOR)
     +------------------------------------------------+    |
                                                           |
      <---------------- nonce length ---------------->     |
     +------------------------------------------------+    |
     |                     Nonce                      |<---+
     +------------------------------------------------+

```
**Replay Windows, Security Contexts, Request-Response bindings**
All of the above are implemented through a feature in ProVerif known as tables. A table is a collection of data like the ones you see in SQL Databases. Each process can look up in the table to find a Request to a respone from a token, or a security context from an Sender ID. The tables are defined as follows:

```
table security_context_lookup(host, host, id, id, bitstring, bitstring, bitstring).

```
The token to message lookup will for a given host, and a given token, identify the security context (the last parameter) for that token. 

```
table token_to_message_lookup(host, bitstring, bitstring).
```

The table is accessed as follows: 
```
get token_to_message_lookup(=identity, =token, security_context:bitstring) in

let (endpoint:host, senderID:id, recipientID:id, idcontext:bitstring, partial_iv:bitstring, aead_nonce:nonce) = security_context
```

However, as seen above, there is one modification to the security context, as it actually contains the AEAD Nonce from the request which the sender has to store during the lifetime of the request/response.

The replay window will contain the host identifier, and all Partial IV's seen. If a message is received and the PIV can be found in the lookup table it's a replay attack.
```
table replay_window(host, bitstring).
```

The Proverif Scennario
 -
 
 The model is largely motivated by section 8 of the document, and the example in appendix A.1. It relies on having two honest processes running OSCORE in a Dolev Yao environment. The model contains 5 processes which are defined below:
 - The oscore initiator - who sends a request to a server
 - The oscore receiver - who receives a request and generates a response
 - The oscore response receiver - who receives a response and matches it to a request
 - The init process - who inserts security contexts into the security context table. 
   - Note that the security context between the two honest processes can not be overriden by the attacker.
- The start process, which starts the model by generating a security context for the two honest hosts.
- 
**The server receives a OSCORE request**.
0. If the request is confirmable, an ACK is sent.
1. The Code of the OSCORE request is discarded.
2. Using the KID and KID Context from the OSCORE option, a Security Context is identified.
3. The Common IV and Recipient Key is derived.
4. The AAD is composed using, among others, the partial IV, and the KID.
5. The Nonce is composed from the KID, Partial IV, and the Common IV
6. Payload of the OSCORE request is decrypted using the recipient key, the aead nonce, and the AAD.
7. If the decryption is sucessful, the replay window is updated with the Partial IV, and if it is not, processing is stopped.
8. A response is generated

**The server generates a OSCORE response to the request**
After receiving and interpreting a request, a server responds with a CoAP response that is matched to the request by means of a client- generated token, e.g the server uses the same token in the response as in the request.

A response is identified by the Code field in the CoAP header being set to the CHANGEDCode.  
1. A new message ID is generated (responseId)
2. A message payload is generated based upon the context of the decrypted ciphertext from the original request
3. Using the AAD and the AEAD Nonce from the request, the sender key and the generated response, the response is encrypted.
4. Note: The OSCORE option is empty because the AEAD Nonce of the request is used.
5. The message is put together as a tuple of (non_confirmable, CoAP_CHANGEDCode, responseId, token, empty, ciphertext)

**A response is received in the oscore response receiver**
1. The response has to contain an empty OSCORE option since the process is not able to derive an AEAD nonce itself yet.
2. The token is matched to the security context (See tables for how this is done)
3. The security context is destructured and the master secret/master salt is identified.
4. The recipient key is derived using the master secret and master salt
5. The AAD is constructed from the senderID and sender sequence number
6. The AEAD Nonce is stored together with the security context, so the message can now be decrypted.

**A request is sent from the oscore initiator**
0. The attacker chooses the endpoint to send the request to. (The security context for this endpoint will be used)
1. The security context is looked up
2. The Common IV and Sender Key is derived
3. The AAD and the AEAD Nonce are composed
4. The plaintext is composed from the isLightBulbTurnedOn request, and in the future, we would like to confirm that the attacker can not see the difference between this and isLightBulbTurnedOff
5. The OSCORE option is composed from the Partial IV, Sender ID, and ID Context.
6. The message is composed
7. Before being sent, the security context used to create the message is stored together with the token of the request and the dervied aead nonce.

**Issues with the current model**
- The response receiver should be capable of receiving the same response multiple times as there are no checks as to whether the response has been received before! NB: The query gets stuck.
- Updating the replay window is not currently atomic, so replay attacks can occur. (Much like two processes running the same security context but not synchronized)
- Partial IV is not increased incrementally for each request.
- Unsure about the complexities regarding the Partial IV in observations
- The OSCORE option is relatively naive in that its just a tuple. Probably change


**Need help with**
- I need to understand the security context deriviation protocol, and i'm currently not sure how it works. Both Alessandro and the authors might be able to help with this.
- Why do the endpoints need 2 keys, instead of just using one?
