@echo off
echo Instalando dependencias de Node.js...
call npm install

echo Compilando Tailwind CSS...
call npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css

echo Proceso completado!
echo Para desarrollo en tiempo real, ejecuta: npm run build-css
pause