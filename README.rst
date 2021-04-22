e3-specification
================

A proof-of-concept specification for an e3 environment as well as associated tools to manage and use the specification(s).

The specification is primarily intended to define modules to be built for an environment.

Note that the example specifications starting with `test-` vary in their contents, and have primarily been used as sort of debugging tools during development.

Usage
-----

Build an environment:

.. code-block:: sh

    $ python3 build.py -s specifications/test-2021-q1-small.yml -l /epics

Pre-populate specification file using existing specification and sourced environment as basis:

.. code-block:: sh

    $ python3 generate_spec.py -i specifications/test-2021-q1-full.yml -o specifications/test-2022-q3-draft.tmp.yml

Create (unordered) specification file from sourced environment:

.. code-block:: sh

    $ python3 generate_spec.py -o 2021-q1.yaml

Compare specification files:

.. code-block:: sh

    $ python3 compare_spec.py specifications/test-t1.yml specifications/test-t2.yml
