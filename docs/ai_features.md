# AI-Powered Project Generation

The ds-template includes revolutionary AI-powered features that allow you to generate projects based on natural language descriptions using Claude Code integration.

## Overview

Instead of manually selecting from predefined templates, you can describe your project in plain English and let AI:

1. **Understand your requirements** through intelligent follow-up questions
2. **Propose optimal project structure** with appropriate components
3. **Generate code** using proven templates from the `templates/` directory
4. **Customize and adapt** the project through interactive Claude sessions


## Requirements

To use AI-powered features, you need:

- **Claude Code** installed and configured
- **Editor** environment variable set (e.g., `export EDITOR=nano`)

## Step-by-Step Process

### Step 1: Project Description
Start by describing your project in natural language. The AI will analyze your description to determine:

You provide your project description by editing a file that opens in your configured editor (`$EDITOR`). Write a short, natural language summary of your intended project in this file. When ready to proceed, **save and exit the editor**.

The AI will analyze your description to understand:
- **Project goals** and objectives
- **Technical requirements** and constraints
- **Integration needs** and dependencies
- **Deployment considerations**

**Example descriptions:**
```
"I want to build a machine learning API that serves predictions for image classification with a monitoring dashboard"

"Create a data science project for analyzing customer behavior with real-time streaming and batch processing capabilities"

"Build a microservices architecture for real-time data processing with background workers and a web interface"
```

### Step 2: Intelligent Questions

Based on your description, Claude will ask you follow-up questions directly in the console to clarify requirements and make sure the generated structure matches your needs.

**Common question categories:**
- **Technical stack**: What frameworks, databases, or tools do you prefer?
- **Architecture**: Do you need microservices, monolith, or hybrid approach?
- **Data processing**: Real-time, batch, or both?
- **Deployment**: Cloud, on-premises, or hybrid?
- **Integration**: What external systems need to connect?

**Example questions:**
```
- What type of machine learning models will you be using?
- Do you need real-time predictions or batch processing?
- What data sources will you be working with?
- Do you need user authentication and authorization?
- What are your performance and scalability requirements?
```

### Step 3: Structure Proposal

After answering the console questions, the AI generates a structure proposal, which you can immediately review and edit in your preferred editor (set via `$EDITOR`). 

The proposed structure includes:
- **Package types** selected from available templates
- **Component functions** and responsibilities
- **Integration patterns** between components
- **Branding requirements** (for frontend components)

**Example structure proposal:**
```json
{
  "project_name": "ml-image-classifier",
  "packages": [
    {
      "type": "pkg_core",
      "name": "ml_image_classifier",
      "functions": ["configuration", "logging", "data models", "shared utilities"]
    },
    {
      "type": "pkg_api",
      "name": "ml_image_classifier_api",
      "functions": ["REST endpoints", "model serving", "authentication", "data validation"]
    },
    {
      "type": "pkg_frontend_streamlit",
      "name": "ml_image_classifier_dashboard",
      "functions": ["model monitoring", "prediction interface", "branding integration"]
    },
    {
      "type": "pkg_worker",
      "name": "ml_image_classifier_worker",
      "functions": ["batch processing", "model retraining", "data preprocessing"]
    }
  ]
}
```
_For details about each package type, see [Package Templates](template_content.md#package-templates) in the Template Content documentation._

You can review (and optionally edit) this structure in the opened file. To continue, **save and exit the editor**.

**Review and editing options:**
- **Modify package names** and types
- **Add or remove components**
- **Adjust functionality descriptions**
- **Fine-tune architecture**


### Step 4: Template-Based Generation
The initial structure is generated with proven templates from the `templates/` directory.

**Generation process:**

1. **Template selection** based on package types
2. **Code generation** using Jinja2 templating
3. **Workspace registration** for monorepo structure
4. **Dependency management** with uv workspace

**Generated components:**

- **Package structure** with proper Python packaging
- **Configuration files** (pyproject.toml, mise.toml, etc.)
- **Code quality setup** (Ruff, mypy, pytest)
- **Documentation** (MkDocs with Material theme)
- **CI/CD pipelines** (GitHub Actions or GitLab CI)

### Step 5: Claude Code Integration
After generation, an interactive Claude session is launch to customize the project based on provided instructions:

**Customization capabilities:**

- **Code modification** and enhancement
- **Feature addition** and implementation
- **Architecture refinement** and optimization
- **Integration assistance** with external systems


