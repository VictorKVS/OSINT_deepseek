@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN OFFICIAL SOURCE PACK
echo Trusted A0/A1 acquisition first; GARANT is HOLD.
echo ============================================================
echo.
echo Opening trusted state-source pages for the four P0 documents...
echo.

rem 152-FZ: official federal agency collection page containing the document entry.
start "" "https://voda.gov.ru/otkrytoe-agentstvo/informatsiya-o-prokhozhdenii-gossluzhby/"

rem PP 1119: official Government of Russia document page with downloadable document.
start "" "https://government.ru/docs/6339/"

rem FSTEC Order 21: official Federal Water Resources Agency document card with Download action.
start "" "https://voda.gov.ru/otkrytoe-agentstvo/normativnye-dokumenty/559246/"

rem FSB Order 378: official Federal Water Resources Agency document card with Download action.
start "" "https://voda.gov.ru/otkrytoe-agentstvo/normativnye-dokumenty/559247/"

echo Pages opened.
echo.
echo Download the document from each official page into your normal Downloads folder.
echo Do not use GARANT for this P0 acquisition slice.
echo.
pause
