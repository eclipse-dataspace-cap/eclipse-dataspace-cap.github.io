#!/usr/bin/env python3

## Import modules
import hashlib
import json
from datetime import datetime, timedelta

import requests
from dateutil.relativedelta import relativedelta
from jwcrypto import jwk, jwt
from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, Node, URIRef
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

criteria512 = URIRef(
    "https://docs.gaia-x.eu/policy-rules-committee/compliance-document/25.03/criteria_cloud_services/#P5.1.2"
)
criteria514 = URIRef(
    "https://docs.gaia-x.eu/policy-rules-committee/compliance-document/25.03/criteria_cloud_services/#P5.1.4"
)


def generate_cap_scheme(g: Graph) -> Node:
    scheme = GX.LabelLevel3_2503
    g.add((scheme, RDF.type, CAP.ConformityAssessmentScheme))
    g.add((scheme, CAP.name, Literal("Gaia-X Label level 3")))
    g.add((scheme, CAP.version, Literal("25.03")))
    g.add((scheme, CAP.specified_requirement, criteria512))
    g.add((scheme, CAP.specified_requirement, criteria514))
    g.add((criteria512, RDF.type, CAP.SpecifiedRequirement))
    g.add((criteria514, RDF.type, CAP.SpecifiedRequirement))
    return scheme


def generate_cap_declaration(g: Graph) -> Node:
    declaration = EX.my_declaration
    g.add((declaration, RDF.type, CAP.Declaration))
    g.add((declaration, CAP.conformity_assessment_scheme, generate_cap_scheme(g)))

    issuance_date = datetime.now()
    valid_from = issuance_date
    valid_until = valid_from + timedelta(days=90)
    g.add((declaration, CAP.valid_from_datetime, Literal(valid_from.isoformat(), datatype=XSD.dateTime)))
    g.add((declaration, CAP.valid_until_datetime, Literal(valid_until.isoformat(), datatype=XSD.dateTime)))
    g.add((declaration, CAP.issuance_datetime, Literal(issuance_date.isoformat(), datatype=XSD.dateTime)))

    issuer = EX.SuperCSP
    g.add((declaration, CAP.issuer, issuer))
    g.add((issuer, RDF.type, GX.LegalPerson))
    g.add((issuer, FOAF.name, Literal("SuperCSP", lang="en")))

    return declaration


## Create the Verifiable Credential
vc = EX.myvc
g.add((vc, RDF.type, CRED.VerifiableCredential))
g.add((vc, CRED.issuer, Literal("did:web:super-cloud.eu")))
valid_from = datetime.now()
valid_until = valid_from + timedelta(days=90)
g.add((vc, CRED.validFrom, Literal(valid_from.isoformat(), datatype=XSD.dateTime)))
g.add((vc, CRED.validUntil, Literal(valid_until.isoformat(), datatype=XSD.dateTime)))

# attach the cap:Certificate to the VC
g.add((vc, CRED.credentialSubject, generate_cap_declaration(g)))


## Display RDF data in Turtle format
print(g.serialize(format="ttl"))


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
