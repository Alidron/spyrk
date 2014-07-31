Contributions to Spyrk
======================

Thank you for wanting to contribute to this project. You are amazing :).

Spyrk is following the `C4.1 - Collective Code Construction Contract <http://rfc.zeromq.org/spec:22>`_ process. You should read through it, but here are the most important bits for you:

Licensing and Ownership
-----------------------

* Your contribution should use the same license than Spyrk: LGPLv3.
* All patches are owned by their authors. The copyrights of Spyrk are owned collectively by all its contributors.
* Add yourself in the project AUTHORS.rst file.

Patch Requirements
------------------

* A patch should be a minimal and accurate answer to exactly one identified problem.
* A patch must adhere to a typical code-style enforced with Flake8 for instance. It is tolerated to ignore W293 and E302 rules.
* A patch must pass the tests on at least principle target platforms.
* A patch commit message should consist of a single short (less than 50 character) line summarizing the change, optionally followed by a new line and then a more thorough description.

Development process
-------------------

* Please, use GitHub issue tracker to log an issue concerning a change or feature request, or propose ideas, suggestions or any solutions to problems.
* To log an issue, please, describe the problem you face or observe in a documented and provable way. You should then seek concensus on the accuracy and the value of solving the problem.
* To work on an issue, fork the project repository and then work on your forked repository. Once ready, submit your patch through a pull request, where it can be discussed and evaluated. A maintainer of the project can then decide to merge it, ask for improvements or reject it.
* If you have an opposing view on how a patch should be implemented, please, express it via a patch of your own.

Evolution of Public Contracts (APIs)
------------------------------------

* All public contracts should be documented.
* All public contracts should have space for extensibility and experimentation.
* A patch that modifies a stable public contract should not break existing applications unless there is overriding consensus on the value of doing this.

