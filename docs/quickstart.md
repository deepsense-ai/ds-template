# **Quickstart**

## Generate project template locally

Install **cookiecutter>=2.1.1** first and then point it to git repository / local directory / zip file containing the template data.

**Cookiecutter** will ask you set of questions so it can generate customized project.

``` bash
    $ cookiecutter ds-template/
    client_name [ds]: Client Name
    project_name [default]: Sunglass
    repo_name [client-name-sunglass]:
    ...
```

![Presentation of cookiecutter generator](_static/make_template.gif "How to use cookiecutter locally as on 01.2023.")

## How to initialize new repository with the template

Firstly, you need to create a git project. The suggested name convention is:

`<client_name>-<project_name>`

Where `client_name` is the name of the client can also be your own name or name of the company you work for. `project_name` is the name of the project.

GIT-SSH is the SSH link to the repository you want to initialize.

Execute the following steps then:

### Approach 1 (clone empty):

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

### Approach 2 (initialize git locally and push to remote):

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
