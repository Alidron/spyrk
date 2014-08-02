Contributions to Spyrk
======================

Thank you for wanting to contribute to this project. You are amazing :).

Spyrk is following the `C4.1 - Collective Code Construction Contract <http://rfc.zeromq.org/spec:22>`_ process. You should read through it, but here are the most important bits for you:

Licensing and Ownership
-----------------------

* Your contribution must use the same license than Spyrk: LGPLv3.

  * This license was chosen to avoid a forker flies away with the sources and make modifications illegal to back-port in the original project. While allowing integration of Spyrk in applications licensed under any kind of licenses, incl. for commercial purpose, without resorting to double-licensing.

* All patches are owned by their authors. The copyrights of Spyrk are owned collectively by all its contributors.

  * This was chosen to clearly ensure contributors that Alidron will NOT fly away with your work by re-licensing it under a different, potentially proprietary license. It will remain free and open-source as it is today, no matter what.

* Add yourself in the project AUTHORS.rst file.

Patch Requirements
------------------

* A patch should be a minimal and accurate answer to exactly one identified problem.
* A patch must adhere to a typical code-style enforced with Flake8 for instance. It is tolerated to ignore W293 and E302 rules.
..  code:: bash

    $ pip install flake8
    $ flake8 --ignore=W293,E302 spyrk tests
    
* A patch must pass the tests on at least principle target platforms.
..  code:: bash
    
    $ pip install pytest
    $ py.test

    # Using tox to test on various Python versions
    $ pip install tox
    $ tox
    
* A patch commit message should consist of a single short (less than 50 character) line summarizing the change, optionally followed by a new line and then a more thorough description.

Development process
-------------------

* Please, use GitHub issue tracker to log an issue concerning a change or feature request, or propose ideas, suggestions or any solutions to problems.
* To log an issue, please, describe the problem you face or observe in a documented and provable way. You should then seek consensus on the accuracy and the value of solving the problem.
* To work on an issue, fork the project repository and then work on your forked repository. Once ready, submit your patch through a pull request, where it can be discussed and evaluated. A maintainer of the project can then decide to merge it, ask for improvements or reject it.
* If you have an opposing view on how a patch should be implemented, please, express it via a patch of your own.

Evolution of Public Contracts (APIs)
------------------------------------

* All public contracts should be documented.
* All public contracts should have space for extensibility and experimentation.
* A patch that modifies a stable public contract should not break existing applications unless there is overriding consensus on the value of doing this.

