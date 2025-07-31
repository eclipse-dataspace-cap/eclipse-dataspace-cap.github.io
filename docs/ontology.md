# Ontology

The ontology can be browsed at <https://eclipse-dataspace-cap.github.io/cap-ontology>

???info "Visualisation"
    A 3rd-party visualisation tool is available [here](https://webvowl.lab.gronlier.fr/#iri=https://github.com/eclipse-dataspace-cap/cap-ontology/releases/download/v2.2.1/cap.owl.ttl).

    ![Image webVOWL](figures/webVOWL-sample.png){ width="300" }

## For Developer

An example of `cap:Certification` inside a W3C Verifiable Credential v2.0 is available in the file `certification_vc.py` in the [notebooks](https://github.com/eclipse-dataspace-cap/eclipse-dataspace-cap.github.io/tree/main/docs/notebooks) folder.

The code sample include a TCK validation using Eclipse CAP SHACL file.

### Turtle output example

```text linenums="1"
@prefix cap: <https://w3id.org/eclipse-cap/v2.2.1/#> .
@prefix cred: <https://www.w3.org/ns/credentials/v2/> .
@prefix ex: <http://example.com/#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix gx: <https://w3id.org/gaia-x/development#> .
@prefix schema: <https://schema.org/> .

ex:myvc a cred:VerifiableCredential ;
    cred:credentialSubject ex:TrustedNotary_certification01 ;
    cred:evidence [ a cred:Evidence ;
            cred:digest "sha256-9b860c2fe0bc4200cf2b94369c82f3806f6db093bd92c3f341fee5e676ff1a60" ;
            cred:value "https://cyber.gouv.fr/sites/default/files/decisions-qualifications/2023_2118_np.pdf" ] ;
    cred:issuer "did:web:trusted-notary.eu" ;
    cred:validFrom "2025-05-24T11:36:39.804251"^^<http://www.w3.org/2001/XMLSchema#dateTime> ;
    cred:validUntil "2025-08-22T11:36:39.804251"^^<http://www.w3.org/2001/XMLSchema#dateTime> .

ex:LNE a cap:ConformityAssessmentBody,
        gx:LegalPerson ;
    foaf:name "LABORATOIRE NATIONAL DE METROLOGIE ET D'ESSAIS"@fr ;
    schema:vatID "FR313320244" .

ex:TrustedNotary_certification01 a cap:Certification ;
    cap:conformity_assessment_scheme [ a cap:ConformityAssessmentScheme ;
            cap:name "SecNumCloud" ;
            cap:version "3.2" ] ;
    cap:issuance_datetime "2023-11-30T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> ;
    cap:issuer ex:LNE ;
    cap:object ex:OutScaleSAS_IaaS ;
    cap:valid_from_datetime "2023-11-30T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> ;
    cap:valid_until_datetime "2026-11-30T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
```

### The signed JWT

```text
eyJhbGciOiJFZERTQSIsImN0eSI6InZjIiwidHlwIjoidmMrand0In0.eyJAY29udGV4dCI6eyJjYXAiOiJodHRwczovL3czaWQub3JnL2VjbGlwc2UtY2FwL3YyLjIuMS8jIiwiY3JlZCI6Imh0dHBzOi8vd3d3LnczLm9yZy9ucy9jcmVkZW50aWFscy92Mi8iLCJleCI6Imh0dHA6Ly9leGFtcGxlLmNvbS8jIiwiZm9hZiI6Imh0dHA6Ly94bWxucy5jb20vZm9hZi8wLjEvIiwiZ3giOiJodHRwczovL3czaWQub3JnL2dhaWEteC9kZXZlbG9wbWVudCMiLCJzY2hlbWEiOiJodHRwczovL3NjaGVtYS5vcmcvIn0sIkBpZCI6ImV4Om15dmMiLCJAdHlwZSI6ImNyZWQ6VmVyaWZpYWJsZUNyZWRlbnRpYWwiLCJjcmVkOmNyZWRlbnRpYWxTdWJqZWN0Ijp7IkBpZCI6ImV4OlRydXN0ZWROb3RhcnlfY2VydGlmaWNhdGlvbjAxIiwiQHR5cGUiOiJjYXA6Q2VydGlmaWNhdGlvbiIsImNhcDpjb25mb3JtaXR5X2Fzc2Vzc21lbnRfc2NoZW1lIjp7IkB0eXBlIjoiY2FwOkNvbmZvcm1pdHlBc3Nlc3NtZW50U2NoZW1lIiwiY2FwOm5hbWUiOiJTZWNOdW1DbG91ZCIsImNhcDp2ZXJzaW9uIjoiMy4yIn0sImNhcDppc3N1YW5jZV9kYXRldGltZSI6eyJAdHlwZSI6Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hI2RhdGVUaW1lIiwiQHZhbHVlIjoiMjAyMy0xMS0zMFQwMDowMDowMCJ9LCJjYXA6aXNzdWVyIjp7IkBpZCI6ImV4OkxORSIsIkB0eXBlIjpbImNhcDpDb25mb3JtaXR5QXNzZXNzbWVudEJvZHkiLCJneDpMZWdhbFBlcnNvbiJdLCJmb2FmOm5hbWUiOnsiQGxhbmd1YWdlIjoiZnIiLCJAdmFsdWUiOiJMQUJPUkFUT0lSRSBOQVRJT05BTCBERSBNRVRST0xPR0lFIEVUIEQnRVNTQUlTIn0sInNjaGVtYTp2YXRJRCI6IkZSMzEzMzIwMjQ0In0sImNhcDpvYmplY3QiOnsiQGlkIjoiZXg6T3V0U2NhbGVTQVNfSWFhUyJ9LCJjYXA6dmFsaWRfZnJvbV9kYXRldGltZSI6eyJAdHlwZSI6Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hI2RhdGVUaW1lIiwiQHZhbHVlIjoiMjAyMy0xMS0zMFQwMDowMDowMCJ9LCJjYXA6dmFsaWRfdW50aWxfZGF0ZXRpbWUiOnsiQHR5cGUiOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSNkYXRlVGltZSIsIkB2YWx1ZSI6IjIwMjYtMTEtMzBUMDA6MDA6MDAifX0sImNyZWQ6ZXZpZGVuY2UiOnsiQHR5cGUiOiJjcmVkOkV2aWRlbmNlIiwiY3JlZDpkaWdlc3QiOiJzaGEyNTYtOWI4NjBjMmZlMGJjNDIwMGNmMmI5NDM2OWM4MmYzODA2ZjZkYjA5M2JkOTJjM2YzNDFmZWU1ZTY3NmZmMWE2MCIsImNyZWQ6dmFsdWUiOiJodHRwczovL2N5YmVyLmdvdXYuZnIvc2l0ZXMvZGVmYXVsdC9maWxlcy9kZWNpc2lvbnMtcXVhbGlmaWNhdGlvbnMvMjAyM18yMTE4X25wLnBkZiJ9LCJjcmVkOmlzc3VlciI6ImRpZDp3ZWI6dHJ1c3RlZC1ub3RhcnkuZXUiLCJjcmVkOnZhbGlkRnJvbSI6eyJAdHlwZSI6Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hI2RhdGVUaW1lIiwiQHZhbHVlIjoiMjAyNS0wNS0yNFQxMTozNjozOS44MDQyNTEifSwiY3JlZDp2YWxpZFVudGlsIjp7IkB0eXBlIjoiaHR0cDovL3d3dy53My5vcmcvMjAwMS9YTUxTY2hlbWEjZGF0ZVRpbWUiLCJAdmFsdWUiOiIyMDI1LTA4LTIyVDExOjM2OjM5LjgwNDI1MSJ9fQ.YI2gB2eOyEgFoxYB_NeeU1WIcScnIG7fHqiYl-JB06FwnTVEWNG2j9qZS50WbJwXpIIzVnllAqVZx5lBLWN5DQ
```

with the public key in JWK format

```json
{
  "crv": "Ed25519",
  "kid": "zD6Ku27DiffK3Eo53dEThwg7azhZfXYV0x8egjO42jA",
  "kty": "OKP",
  "x": "7p4c1IU6aA65FWn6YZ-Bya5dRbfd4P6d4a6H0u9-gCg"
}
```
