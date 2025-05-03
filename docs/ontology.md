# Ontology

The ontology can be browsed at <https://eclipse-dataspace-cap.github.io/cap-ontology>

???info "Visualisation"
    A 3rd-party visualisation tool is available [here](https://service.tib.eu/webvowl/#iri=https://github.com/eclipse-dataspace-cap/cap-ontology/releases/download/v2.0.1/cap.owl.ttl).

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
