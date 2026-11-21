@echo off
setlocal enabledelayedexpansion
echo ======================================================================
echo    News Classification Platform — Push to GitHub
echo ======================================================================
echo.
echo Target GitHub Profile: https://github.com/sathish12tj
echo Configured Remote:   https://github.com/sathish12tj/News_Classification_E2E_Deployment.git
echo.
echo NOTE: If you haven't created the repository on GitHub yet:
echo 1. Open your browser and go to: https://github.com/new
echo 2. Name the repository: News_Classification_E2E_Deployment
echo 3. Keep it Public or Private, DO NOT initialize with README/license
echo 4. Click 'Create repository'
echo.
echo ----------------------------------------------------------------------

set "PATH=%PATH%;C:\Users\Karku\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd"

echo Checking git status...
git status -s
echo.
echo Attempting to push to origin main...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Repository successfully pushed to GitHub!
    echo Check it out at: https://github.com/sathish12tj/News_Classification_E2E_Deployment
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo [NOTICE] Push encountered an issue. Common reasons:
    echo 1. The repository 'News_Classification_E2E_Deployment' has not been created on GitHub yet.
    echo    Please visit https://github.com/new to create it.
    echo 2. If you named your repository differently (e.g. 'News_Classification'),
    echo    run: git remote set-url origin https://github.com/sathish12tj/<your-repo-name>.git
    echo ======================================================================
)

echo.
pause
