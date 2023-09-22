# deepsense.ai Project Template

This is a basic template to bootstrap new data science project.

Its intended use is to generate basic, most common configuration - however each team and developer is encouraged to modify it for its special needs.

It is a result of our experiences with building data science projects and is a part of our internal best practices, however it is not a silver bullet and should be treated as a starting point for your project.
Especially some settings might be less/more restrictive than you needs  but we believe it is better to start with a good baseline and modify it later than to start from scratch.

## Getting started

### Generate project template locally:

Install **cookiecutter** (at least **>=2.1.1** version) first and then point it to this repository.

**Cookiecutter** will ask you set of questions so it can generate customized project.

``` bash
    $ cookiecutter ds-template/
    client_name [ds]: Client Name
    project_name [default]: Sunglass
    repo_name [client-name-sunglass]:
    ...
```

### How to initialize new repository with the template:

Firstly, you need to create a new project. The name should be of the following convention: 

`<client_name>-<project_name>`

Execute the following steps then:

Approach 1 (clone empty):

```bash
# clone empty repository to repo_name
$ git clone <GIT-SSH>
# install cookiecutter if not yet installed
$ pip install cookiecutter
# generate cookiecutter with --force and ensure the repo_name is set to the same name as directory you cloned git repository to.
$ cookiecutter -f git@github.com:deepsense-ai/ds-template.git
# finally, add all files, commit and push.
$ git add .
$ git commit -m "Initialize repository with default project template"
$ git push origin
```

Approach 2 (initalize git locally and push to remote):

```bash
# install cookiecutter if not yet installed
$ pip install cookiecutter
# generate project
$ cookiecutter git@github.com:deepsense-ai/ds-template.git
# enter created directory
$ cd <project-name>
# now we need to connect it to repository (assuming empty repository)
$ git init
$ git remote add origin <GIT-SSH>
$ git fetch
$ git checkout -t origin/main
# finally, add all files, commit and push.
$ git add .
$ git commit -m "Initialize repository with default project template"
$ git push --set-upstream origin main
$ git push origin
```
