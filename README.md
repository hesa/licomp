# licomp - License Compatibility

Licomp provides an interface and code for miscallenous compatibility
resources making them accessible more easily.

Licomp also provides some basic functionality for such resources to
easily create a command line program.

Licomp is used be the following compatibility resources:
* [licomp-hermione](https://github.com/hesa/licomp-hermione) (`pip install licomp-hermione`)
* [licomp-osadl](https://github.com/hesa/licomp-osadl) (`pip install licomp-osadl`)
* [licomp-proprietary](https://github.com/hesa/licomp-proprietary) (`pip install licomp-proprietary`)
* [licomp-reclicense](https://github.com/hesa/licomp-reclicense) (`pip install licomp-reclicense`)
* [licomp-toolkit](https://github.com/hesa/licomp-toolkit)  (`pip install licomp-toolkit`)
* [licomp-dwheeler](https://github.com/hesa/licomp-dwheeler)  (`pip install licomp-dwheeler`)

<a name="licomp-concepts"></a>
# Licomp basic concepts

Answering whether one license is compatible with another needs some
context. This context is often missing in the quesion but sometimes
also in tooling. We have tried to organise this context and a way to
provide this to the tool.

<a name="licomp-concepts-usecase"></a>
## Usecase

The way you use a software determines what parts of the license kick in. Let's take [GCC](https://gcc.gnu.org/) which is licensed under "[GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0-standalone.html) WITH [GCC-exception-3.1](GCC-exception-3.1)". If you use GCC as a compiler then the output of the compiler, typically your program, is covered by the exception and you distribute your program (the GCC Runtime libraries that comes with GCC) under any license. But if you use a snippet from GCC, then the copyleft effect is triggered and you need to license your work under the same license (GPLv3).

The following usecases are (currently) supported:

* `library` - you use the licensed component as a library (creating a combined work, a derivative work)
* `compiler` - you use the licensed component as a compiler taking input and producing output (e.g. GCC, Autoconf)
* `snippet` - you use a part of the licensed component's source code from another project, book, web page
* `test` - you use the licensed component for testing your software (e.g. linter, cyclomatic analysis)

<a name="licomp-concepts-provisioning"></a>
## Provisioning

* `source-code-distribution` - you disitrbute the licensed component, in source code form
* `binary-distribution` - you disitrbute the licensed component, in binary (non source code) form
* `local-use` -  you used the licensed component locally (e.g. and editor you use to write software)
* `provide-service` - you provide a service over a REST api. No source is distributed.
* `provide-webui` - you provide a webui which is distributed to the user's browser.

<a name="licomp-concepts-modification"></a>
## Modification

* `modified` - you have made modifications to the licensed component
* `unmodified`- you have not made any modifications to the licensed component

# Licomp reply format

See [Licomp Reply Format](docs/reply-format.md)

