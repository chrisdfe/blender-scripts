@echo off
cd ".\addons"
if exist ".\sweaterparrot_functions_zipped.zip" (
  del ".\sweaterparrot_functions_zipped.zip"
)

tar -a -c -f "sweaterparrot_functions_zipped.zip" "sweaterparrot_functions"
cd ".."