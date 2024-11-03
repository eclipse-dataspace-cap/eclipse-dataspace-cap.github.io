# Introduction

The ontology can be browsed at <https://eclipse-dataspace-cap.github.io/cap-ontology>

The full ontology can be downloaded in:

- [Turtle](https://eclipse-dataspace-cap.github.io/cap-ontology/ontology/ontology.owl.ttl)
- [RDF/XML](https://eclipse-dataspace-cap.github.io/cap-ontology/ontology/ontology.owl.xml)
- [LinkML](https://eclipse-dataspace-cap.github.io/cap-ontology/ontology/ontology.linkml.yml)

???info "Visualisation"

    A 3rd-party visualisation tool is available [here](https://service.tib.eu/webvowl/).

    ![Image webVOWL](figures/webVOWL-sample.png){ width="300" }

## For Developer

How to load the ontology

=== "Python + rdflib"

    Using [rdflib](https://rdflib.readthedocs.io/)

    ```python
    import rdflib  # rdflib==7.1.1
    g= rdflib.Graph()
    g.parse("ontology.owl.ttl")
    for s, p, o in g:
        print(s, p, o)
    ```

=== "Python + owlready2"

    Using [owlready2](https://owlready2.readthedocs.io/)

    ```python
    from owlready2 import get_ontology  # owlready2==0.47
    onto = get_ontology("file://ontology.owl.xml").load()
    for classe in onto.classes():
        print(classe, classe.iri)
    ```
