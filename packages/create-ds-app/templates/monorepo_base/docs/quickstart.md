# **Quickstart**

## Generate project template locally

Use **uvx** to run the create-ds-app tool directly without installation. The tool will ask you a set of questions to generate a customized project.

``` bash
    $ uvx create-ds-app
    project_name [my-project]: My Data Science Project
    pkg_name [my_data_science_project]: my_ds_project
    python_version [3.13]: 3.13
    ...
```

![Presentation of create-ds-app generator](_static/make_template.gif "How to use create-ds-app locally.")

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
# generate project using create-ds-app
$ uvx create-ds-app
# follow the prompts and ensure the project_name matches your repository name
# finally, add all files, commit and push.
$ git add .
$ git commit -m "Initialize repository with default project template"
$ git push origin
```

### Approach 2 (initialize git locally and push to remote):

```bash
# generate project using create-ds-app
$ uvx create-ds-app
# follow the prompts to configure your project
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
