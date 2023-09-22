# **Overall design**

Here is a short introduction to default project template to give you better understanding of _why_ and _what_.

It was created to propagate some good practices and provide sensible and flexible defaults and to quickly bootstrap new projects.

## Considerations
Let's start with understanding a design considerations. **There is not really a one, universally good way** and there are trade-offs involved. Below is a list of things we want to focus on.

1. **Harnessing experiences from different projects** (both DS and SE) - so they can propagate as sensible defaults.
1. **Adapting to software house project style** - more than a product or a single project needs.
1. **Adding tools and configuration that are useful** - usually they would take too much time to setup or read about. It is easier to edit existing file for specific project needs.
1. **Providing sensible defaults** - we mostly work with quite short living projects like PoC, where it is important to move fast and rarely we hit any production, but we should keep highest quality possible.
1. **Making onboarding as easy as possibleg** - similar structure, enforced code style and tools allow to faster onboard someone or switch between projects.
1. **Handing over ownership to ensure independence** - after the template is used, the team takes ownership and can adapt it quickly to specific needs of a project or client.
1. **Being PEP and other best practices complaint** - unless experience suggest otherwise or they would be impossible to provide in a satisfying way.
1. **Being cautious** - preference is given to battle-tested, stable with known drawbacks, issues and workarounds approaches, so it should work in more broad situations and be more flexible with different clients.

This templates does not:
- Provide perfect configuration for every project,
- Agree with all subjective personal opinions,
- Recommend the newest and shiny tools or approaches as they appear.

For example, there are many new projects that provide a better developer experience, however they can lead to difficult and new issues for the clients that might use older software stack or non standard workflow for which implementation might be lacking. Migration and fixing corner cases takes time, so when finally things start to be stable enough we will eventually migrate to them.
On the other hand team has a possibility to do that on their own if client do not have nothing against it.

## Inspiration

The inspiration for configuration is based on:

- lessons learned from interviews about different projects that happened during 2020-2022 in deepsense.ai,
- other cookiecutter projects and open source repositories,
- PEP documents, stack overflow posts, medium posts etc to identify other drawbacks and trade-offs,
- adapting to recent findings.

## Assumptions

- Python 3.9 is default on CI, 3.8 as minimum installable for package - due to recent projects (as of 01.2023), hopefully to update soon.
- GitLab is used in almost all projects so it's selected as the default CI / CD provider.
- The licences of used libraries are verified against the provided whitelist, which can be exceptionally modified to accept GPL-like licenses.
- No support multiple python version in the project - each project sticks to single python version and most dependencies are constant.
- No support for native code, pure python focus.
- Research quality code and faster development has priority.
- Good engineering practices like tests, security scanners are introduced to ensure quality and enforce good habits.
- Most projects have a single thing to focus on. Multi topic monorepo is not supported at the moment.
- All non-standard things are intended to be _opt-in_ based on `ds-tools` project.

## Stability - python, system and package versions

For all projects that follow semantic versions, we should update patch to incorporate all bug and security fixes.
Major and minor release are more troublesome due to additional risks and trade-offs.

Why older, stable versions as default are preferred:
- Ecosystem support:
  - libraries and their dependency take time to update and _test_. 
  - older versions have more compatible libraries to work with and known workarounds/google results for issues.
  - it is more likely that research open source code used older versions
- Ubuntu/Debian/CentOS LTS are targeted platforms:
  - they don't use newest versions
  - usually those versions which are shipped are the best well-supported in libraries as they are used in CI tests and docker images.
  - target LTS (Long Time Support) and usually it takes 2 years for libraries to catch up with releases.
- Python older code works on newer versions but backport of features is not always possible/harder.
  - your code will work in the future versions, won't work in previous versions
  - example: near the end of the project client might ask you to run inference on a nvidia container which uses older version of python and you would need to rewrite it...
  - default older version on CI allows you to use locally newer version - however it works if you have good suite of tests.
- Testing multiple python versions (and matrix testing) is costly so pick one version
  - each version multiplies required tests which costs time and money to support.
- Targeting older versions increases chances to re-use code in other projects due to higher compatibility.

This is why default version is older one, however it should be updated as soon as possible when:
- Python support cycle ends: https://devguide.python.org/versions/
- NVIDIA images are updated to newer versions
- Cloud providers such as AWS/GCP/Azure moved to newer versions
- most popular packages (numpy, pytorch etc) moved at least half a year ago (so other packages had time to migrate too).

THis ensures we reduce chances of having issues with client infrastructure or libraries we use are not yet updated.
That said, for internal project it is generally safer to use newer versions, especially if the project is for educational purposes.
It is also true for tools that are not critical e.g. linters.


## Future plans and ideas

Project is far from finished and it is planned to evolve over time. Below are _some_ ideas we can work on:

1. Multi-project monorepo - e.g. multiple packages in single repository
1. cibuildwheel/nox/tox - native code, mutliple python versions
1. GitHub pipelines

