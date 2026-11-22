# Práctica 1 — Git (120 minutos)

## 1. Preparación (0–15 min)
1. Descomprimir ZIP y abrir la carpeta `01_git_telco` en VS Code.
2. Abrir **Terminal > New Terminal**.
3. Comprobar `git --version` y `py --version`.
4. Ejecutar los comandos de README para entrenar `forest`.

## 2. Primer commit (15–35 min)
```powershell
git init -b main
git config user.name "Nombre Apellido"
git config user.email "correo@example.com"
git status
git add .
git commit -m "Inicio: proyecto de clasificacion modular"
git log --oneline
```
`git add .` prepara los cambios; `commit` registra una instantánea. Comprueba que `models/` y `.venv/` no aparecen en el commit gracias a `.gitignore`.

## 3. Dos ramas que divergen (35–60 min)
Primero crea una rama para mejorar documentación:
```powershell
git switch -c feature/documentacion
```
Agrega al final de README.md la frase `Modelo base: Random Forest.` y registra:
```powershell
git add README.md
git commit -m "docs: explicar modelo base"
```
**Sin fusionar aún**, regresa a main y haz un cambio independiente:
```powershell
git switch main
```
Agrega al final de GUIA_GIT.md la frase `La rama main también evoluciona.` y registra:
```powershell
git add GUIA_GIT.md
git commit -m "docs: ampliar guia en main"
```
Así `main` y `feature/documentacion` avanzaron por separado.

## 4. Merge no fast-forward (60–85 min)
```powershell
git merge --no-ff feature/documentacion -m "merge: incorporar documentacion"
git log --oneline --graph --decorate --all
```
Debes observar dos caminos que convergen en un commit de merge. El merge no es fast-forward.

## 5. Provocar y resolver conflicto (85–105 min)
En `main`, cambia en README.md la línea `# Telco Customer Churn — práctica de Git` por `# Telco — versión principal`:
```powershell
git add README.md
git commit -m "docs: titulo principal"
git switch -c feature/titulo-alternativo HEAD~1
```
En esta nueva rama cambia esa misma línea por `# Telco — versión alternativa`:
```powershell
git add README.md
git commit -m "docs: titulo alternativo"
git switch main
git merge --no-ff feature/titulo-alternativo
```
Git debe mostrar un conflicto en README.md. Abre el archivo, elimina los marcadores `<<<<<<<`, `=======`, `>>>>>>>` y deja un solo título. Después:
```powershell
git add README.md
git commit -m "merge: resolver conflicto de titulo"
git log --oneline --graph --decorate --all
```

## 6. Recuperar un archivo (105–120 min)
Modifica README.md sin registrar el cambio, luego:
```powershell
git diff
git restore README.md
git status
```
`git restore` descarta cambios **no confirmados** en el archivo; úsalo solo si no necesitas conservarlos.

## Evidencia a entregar
- Captura de `git log --oneline --graph --decorate --all` con dos merges.
- Captura de `git status` limpio.
- Breve explicación (3–5 líneas) de commit, branch, merge y conflicto.

## Nota para docente
Todos los cambios indicados son locales y no necesitan GitHub. El conflicto se provoca de forma controlada en la misma línea de README.md. Si un alumno se equivoca, puede volver a descomprimir el ZIP y comenzar desde cero.
