@ECHO OFF

pushd %~dp0

REM Command file for MkDocs documentation

if "%1" == "" goto help
if "%1" == "help" (
	:help
	echo.MkDocs documentation build commands:
	echo.  serve    Start development server
	echo.  build    Build the documentation
	echo.  clean    Clean the build directory
	echo.  deploy   Deploy to GitHub Pages
	goto end
)

if "%1" == "serve" (
	mkdocs serve
	goto end
)

if "%1" == "build" (
	mkdocs build
	goto end
)

if "%1" == "clean" (
	rmdir /s /q site
	goto end
)

if "%1" == "deploy" (
	mkdocs gh-deploy
	goto end
)

:end
popd