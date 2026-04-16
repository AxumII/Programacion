# Definimos la ruta de Eigen (asegúrate que sea esta exactamente)
$eigenPath = "C:\Librerias c++\eigen-5.0.0"

# Limpiamos la consola
Clear-Host

Write-Host "Iniciando compilación de C++ puro..." -ForegroundColor Cyan

# Compilamos: main + kinematic + ruta de librerías
# Usamos -I para incluir Eigen
C:\msys64\mingw64\bin\g++.exe -I "$eigenPath" main.cpp Kinematic.cpp -o sim_robot.exe
if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilación exitosa. Ejecutando simulador:`n" -ForegroundColor Green
    ./sim_robot.exe
} else {
    Write-Host "`nError: No se pudo compilar. Revisa los errores arriba." -ForegroundColor Red
}