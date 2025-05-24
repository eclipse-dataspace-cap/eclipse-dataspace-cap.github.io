#!/usr/bin/env python3

## Import modules
import hashlib
import json
from datetime import datetime, timedelta

import requests
from dateutil.relativedelta import relativedelta
from jwcrypto import jwk, jwt
from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, Node
from rdflib.namespace import FOAF, RDF, SDO, XSD

## Pick Eclipse CAP version and defines the others ontologies
CAP_VERSION = "v2.2.1"

CRED = Namespace("https://www.w3.org/ns/credentials/v2/")
CAP = Namespace(f"https://w3id.org/eclipse-cap/{CAP_VERSION}/#")
GX = Namespace("https://w3id.org/gaia-x/development#")
EX = Namespace("http://example.com/#")

g = Graph(bind_namespaces="none")  # create an empty graph
# declare prefix to increase readability
g.bind("cap", CAP)
g.bind("cred", CRED)
g.bind("ex", EX)
g.bind("foaf", FOAF)
g.bind("gx", GX)
g.bind("schema", SDO)


## Generate an Eclipse `cap:Certification` object
def generate_cap_certification(g: Graph) -> tuple[Node, Node]:
    certification = EX.TrustedNotary_certification01
    g.add((certification, RDF.type, CAP.Certification))
    g.add((certification, CAP.object, EX.OutScaleSAS_IaaS))

    scheme = BNode()
    g.add((certification, CAP.conformity_assessment_scheme, scheme))
    g.add((scheme, RDF.type, CAP.ConformityAssessmentScheme))
    g.add((scheme, CAP.name, Literal("SecNumCloud")))
    g.add((scheme, CAP.version, Literal("3.2")))
    issuance_date = datetime(year=2023, month=11, day=30)
    valid_from = issuance_date
    valid_until = valid_from + relativedelta(years=3)
    g.add((certification, CAP.valid_from_datetime, Literal(valid_from.isoformat(), datatype=XSD.dateTime)))
    g.add((certification, CAP.valid_until_datetime, Literal(valid_until.isoformat(), datatype=XSD.dateTime)))
    g.add((certification, CAP.issuance_datetime, Literal(issuance_date.isoformat(), datatype=XSD.dateTime)))

    issuer = EX.LNE
    g.add((certification, CAP.issuer, issuer))
    g.add((issuer, RDF.type, CAP.ConformityAssessmentBody))
    g.add((issuer, RDF.type, GX.LegalPerson))
    g.add((issuer, FOAF.name, Literal("LABORATOIRE NATIONAL DE METROLOGIE ET D'ESSAIS", lang="fr")))
    g.add((issuer, SDO.vatID, Literal("FR313320244")))

    print(f"The cap:Certification object has the id {certification.n3()}")
    print(f"The cap:Certification issuer is {issuer.n3()}")
    return certification, issuer


certification, certification_issuer = generate_cap_certification(g)

## Generate the `cred:Evidence` for the Verifiable Credential


def compute_sri(url: str) -> str:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    sha256_hash = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def generate_cred_evidence(g: Graph, evidence_url: str) -> Node:
    evidence = BNode()
    g.add((evidence, RDF.type, CRED.Evidence))
    g.add((evidence, CRED.value, Literal(evidence_url)))
    evidence_sri = compute_sri(evidence_url)
    g.add((evidence, CRED.digest, Literal(f"sha256-{evidence_sri}")))
    return evidence


evidence = generate_cred_evidence(
    g, "https://cyber.gouv.fr/sites/default/files/decisions-qualifications/2023_2118_np.pdf"
)

## Create the Verifiable Credential
vc = EX.myvc
g.add((vc, RDF.type, CRED.VerifiableCredential))
g.add((vc, CRED.issuer, Literal("did:web:trusted-notary.eu")))
valid_from = datetime.now()
valid_until = valid_from + timedelta(days=90)
g.add((vc, CRED.validFrom, Literal(valid_from.isoformat(), datatype=XSD.dateTime)))
g.add((vc, CRED.validUntil, Literal(valid_until.isoformat(), datatype=XSD.dateTime)))

# attach the cap:Certificate to the VC
g.add((vc, CRED.credentialSubject, certification))

# attach the cred:Evidence to the VC
g.add((vc, CRED.evidence, evidence))


## Display RDF data in Turtle format
print(g.serialize(format="ttl"))

## Verify format with SHACL

# Load the Eclipse CAP SHACL graph
shacl_graph = Graph()
shacl_graph.parse(
    f"https://github.com/eclipse-dataspace-cap/cap-ontology/releases/download/{CAP_VERSION}/cap.shacl.ttl", format="ttl"
)

# Load the Eclipse Ontology graph
ont_graph = Graph()
ont_graph.parse(
    f"https://github.com/eclipse-dataspace-cap/cap-ontology/releases/download/{CAP_VERSION}/cap.owl.ttl", format="ttl"
)

# Run the SHACL validation (TCK)
r = validate(
    g,
    shacl_graph=shacl_graph,
    ont_graph=ont_graph,
    inference="rdfs",
    abort_on_first=False,
    allow_infos=False,
    allow_warnings=False,
    meta_shacl=False,
    advanced=False,
    js=False,
    debug=False,
)
conforms, results_graph, results_text = r
print("*" * 80)
print(conforms, results_graph, results_text)
assert conforms


## Issue signed Verifiable Credential
# Recursively resolve ids
def nest_inside(obj, object_ids: dict):
    if isinstance(obj, dict):
        if "@id" in obj and len(obj) == 1:  # it's a object with only on @id field
            if obj["@id"] in object_ids:  # it has not yet been visited
                obj.update(object_ids[obj["@id"]])  # update the reference only object with the real object
                del object_ids[obj["@id"]]  # delete it from the list of available objects to prevent looping
                if obj["@id"].startswith("_:"):  # if it's a blank node
                    del obj["@id"]  # remove the blank node id
        for key in obj.keys():  # go through all object's property
            obj[key] = nest_inside(obj[key], object_ids)  # nest the object
        return obj  # return the updated object
    elif isinstance(obj, list):
        return [nest_inside(item, object_ids) for item in obj]  # go through the list and nest the object
    return obj  # nothing to do, it's a literal (int, str, etc.)

def get_vcs(g: Graph):
    flat_json_doc = json.loads(g.serialize(format="json-ld", auto_compact=True))
    # Build an index of objects of the @graph by "@id"
    object_ids = {item["@id"]: item for item in flat_json_doc["@graph"]}
    vc_ids = g.subjects(predicate=RDF.type, object=CRED.VerifiableCredential)
    for vc_id in vc_ids:
        compact_vc_id = vc_id.n3(namespace_manager=g.namespace_manager)
        assert compact_vc_id in object_ids, object_ids.keys()
        vc_obj = object_ids[compact_vc_id]
        del object_ids[compact_vc_id]
        vc_obj = nest_inside(vc_obj, object_ids)
        vc_obj["@context"] = flat_json_doc["@context"]
        yield vc_obj

    return (get_vcs,)


private_key = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIPtUxyxlhjOWetjIYmc98dmB2GxpeaMPP64qBhZmG13r
-----END PRIVATE KEY-----"""

headers = {"cty": "vc", "typ": "vc+jwt", "alg": "EdDSA"}

key = jwk.JWK()
key.import_from_pem(private_key.encode())
print("Public Key in JWK format:", key.export(private_key=False))

for vc_obj in get_vcs(g):
    # print(json.dumps(vc_obj, indent=2))
    token = jwt.JWT(header=headers, claims=vc_obj)
    token.make_signed_token(key)
    print(token.serialize())
