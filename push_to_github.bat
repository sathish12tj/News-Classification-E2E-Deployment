@echo off
echo ========================================================
echo Pushing News Classification Platform to GitHub...
echo Repository: https://github.com/sathish12tj/News_Classification_E2E_Deployment
echo ========================================================
set "PATH=%PATH%;C:\Users\Karku\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd"

git status
echo.
echo Adding files...
git add .
git commit -m "feat: complete end-to-end news classification, live feed routing, docs and presentation"
echo.
echo Pushing to origin main...
git push -u origin main

echo.
echo ========================================================
echo Push command executed.
echo ========================================================
pause
