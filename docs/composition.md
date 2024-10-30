# :material-bowl-mix-outline: Composition of conformity assessment scheme

!!! warning

    A conformity scheme can be composed as described below under the condition that the scopes of the object of conformity `#1` and `#2` are indisputable between the conformity scheme.

In the diagram below, the `Conformity Assessment System #1` is composed of the `Conformity Assessment System #2`.

The `Conformity Assessment System #2` has no impact on `Conformity Assessment System #1`.

!!! example

    The `Conformity Assessment Activities #1` could be fully automated while the `Conformity Assessment Activities #2` could be manual.


```mermaid
flowchart

    subgraph CASystem [Conformity Assessment System #1]
        direction TB
        CAScheme(Conformity Assessment Scheme #1)
        object(Objects of Conformity Assessment #1)
        criteria(Specified Requirements #1)
        CAB(Conformity Assessment Bodies #1)
        CAA(Conformity Assessment Activities #1)

        CAScheme -- identify --> criteria
        CAScheme -- provide the methodology to perform --> CAA
        CAA -- demonstrate fulfillment of --> criteria
        CAB -- perform --> CAA

        criteria -- might refers to 3rd party --> CAScheme2

        subgraph CASystem1 [Conformity Assessment System #2]

            CAScheme2(Conformity Assessment Scheme #2)
            criteria2(Specified Requirements #2)
            CAB2(Conformity Assessment Bodies #2)
            CAA2(Conformity Assessment Activities #2)
            object2(Objects of Conformity Assessment #2)

            CAB2 -- perform --> CAA2
            CAScheme2 -- identify --> criteria2
            CAScheme2 -- provide the methodology to perform --> CAA2
            CAA2 -- demonstrate fulfillment of --> criteria2
            criteria2 -- need or expectation applying to --> object2

        end
            object2 -- equivalent or part of --> object
    end
```

!!! example

    For a given ecosytem or domain specific qualification or label, the scheme owner can define a `Conformity Scheme #1` that mandates the acquisition of an ISO/IEC 27001 from a specific list of eligible `CAB #2`.
    Those CAB are a type of Trust Anchors and are listed in a Registry.
