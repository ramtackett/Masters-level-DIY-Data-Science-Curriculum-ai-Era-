from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# === OUTPUT FILE NAME ===
pdf_path = "Win11_to_WSL2_Data_Science_Environment_Guide.pdf"

# === SET UP DOCUMENT & STYLES ===
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.75 * inch,
    bottomMargin=0.75 * inch,
)

styles = getSampleStyleSheet()
title_style = styles["Title"]
h1 = styles["Heading1"]
h2 = styles["Heading2"]
body = styles["BodyText"]

# slightly more readable line spacing for body text
body.leading = 14

code_style = ParagraphStyle(
    "Code",
    parent=body,
    fontName="Courier",
    fontSize=9,
    leading=11,
)

story = []

# === TITLE PAGE ===
story.append(Paragraph("Windows 11 → WSL2 Data-Science Environment", title_style))
story.append(Spacer(1, 12))
story.append(Paragraph("(DIY Master's in the AI Era)", h2))
story.append(Spacer(1, 18))

story.append(Paragraph(
    "A step-by-step, reproducible guide to rebuild your full setup from a clean Windows 11 install: "
    "WSL2 + Ubuntu, VS Code, Git/SSH, Conda (Python 3.13.5), Docker Desktop, GitHub Actions CI, and a "
    "project skeleton in <b>ds-zero-to-one</b>.",
    body,
))
story.append(Spacer(1, 12))

story.append(PageBreak())

# === 0) Overview & Assumptions ===
story.append(Paragraph("0) Overview & Assumptions", h1))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "This document rebuilds the exact environment you used for the curriculum:",
    body,
))
story.append(Spacer(1, 4))
story.append(Paragraph("• Windows 11 (administrator access), internet available.", body))
story.append(Paragraph("• GitHub account available.", body))
story.append(Paragraph(
    "• Final state uses: WSL2 (Ubuntu), VS Code + Remote-WSL, Docker Desktop "
    "(Linux containers via WSL2), Conda 25.5.1 with Python 3.13.5, and a GitHub Actions workflow "
    "that verifies the environment by printing “CI env OK”.",
    body,
))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Tip: Commands marked <b>(PowerShell)</b> are run in Windows; <b>(WSL)</b> are run inside the Ubuntu terminal.",
    body,
))
story.append(Spacer(1, 12))

# === 1) Install Core Windows Apps ===
story.append(Paragraph("1) Install Core Windows Apps (PowerShell / Windows UI)", h1))
story.append(Spacer(1, 6))
story.append(Paragraph("Install these in any order:", body))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "• Docker Desktop (Linux containers only). Enable “Use the WSL 2 based engine”; "
    "DO NOT enable Windows Containers.",
    body,
))
story.append(Paragraph("• Visual Studio Code.", body))
story.append(Paragraph("• Windows Terminal (bundled on Win11; install from Microsoft Store if missing).", body))
story.append(Paragraph("• Git for Windows (optional; you can use Git entirely in WSL).", body))
story.append(Spacer(1, 12))

# === 2) Enable WSL2 + Install Ubuntu ===
story.append(Paragraph("2) Enable WSL2 + Install Ubuntu (PowerShell as Administrator)", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    "wsl --install -d Ubuntu\n\n"
    "# Reboot when prompted.\n"
    "# On first Ubuntu launch, create your UNIX username and password.",
    code_style,
))
story.append(Spacer(1, 12))

# === 3) VS Code + WSL Integration ===
story.append(Paragraph("3) VS Code + WSL Integration (Windows UI)", h1))
story.append(Spacer(1, 6))
story.append(Paragraph("Open VS Code → Extensions → install:", body))
story.append(Spacer(1, 4))
story.append(Paragraph("• WSL (by Microsoft)", body))
story.append(Paragraph("• Python (by Microsoft)", body))
story.append(Paragraph("• Jupyter (by Microsoft)", body))
story.append(Paragraph("• Docker (by Microsoft)", body))
story.append(Paragraph("• YAML (by Red Hat)", body))
story.append(Paragraph("• Markdown All in One (Yzhang)", body))
story.append(Spacer(1, 12))

# === 4) Configure Docker Desktop ===
story.append(Paragraph("4) Configure Docker Desktop (Windows UI)", h1))
story.append(Spacer(1, 6))
story.append(Paragraph("Open Docker Desktop → Settings:", body))
story.append(Paragraph("• General: ✓ Use the WSL 2 based engine", body))
story.append(Paragraph("• Resources → WSL Integration: enable for Ubuntu", body))
story.append(Paragraph("• (Optional) Start Docker Desktop on login", body))
story.append(Spacer(1, 12))

# === 5) SSH Keys & Git Identity ===
story.append(Paragraph("5) SSH Keys & Git Identity", h1))
story.append(Spacer(1, 8))

story.append(Paragraph("5A) Reuse Windows SSH key in WSL (recommended):", h2))
story.append(Spacer(1, 4))
story.append(Preformatted(
    'mkdir -p ~/.ssh\n'
    'cp /mnt/c/Users/<YourWindowsUser>/.ssh/id_ed25519 ~/.ssh/\n'
    'cp /mnt/c/Users/<YourWindowsUser>/.ssh/id_ed25519.pub ~/.ssh/\n'
    'chmod 600 ~/.ssh/id_ed25519\n'
    'chmod 644 ~/.ssh/id_ed25519.pub\n'
    'eval "$(ssh-agent -s)"\n'
    'ssh-add ~/.ssh/id_ed25519\n'
    'ssh -T git@github.com   # success message expected\n',
    code_style,
))
story.append(Spacer(1, 8))

story.append(Paragraph("5B) Or generate a new key inside WSL:", h2))
story.append(Spacer(1, 4))
story.append(Preformatted(
    'ssh-keygen -t ed25519 -C "github-wsl"\n'
    'eval "$(ssh-agent -s)"\n'
    'ssh-add ~/.ssh/id_ed25519\n'
    'cat ~/.ssh/id_ed25519.pub   # add at GitHub → Settings → SSH and GPG Keys\n',
    code_style,
))
story.append(Spacer(1, 8))

story.append(Paragraph("5C) Configure Git identity (use GitHub noreply email):", h2))
story.append(Spacer(1, 4))
story.append(Preformatted(
    'git config --global user.name "Your Name"\n'
    'git config --global user.email "12345678+yourusername@users.noreply.github.com"\n'
    'git config --global init.defaultBranch main\n',
    'git remote set-url origin git@github.com:GIT_USERNAME/REPO_NAME.git\n',
    code_style,
))
story.append(PageBreak())

# === 6) Get Your Repository ===
story.append(Paragraph("6) Get Your Repository (WSL)", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    'mkdir -p ~/projects\n'
    'cd ~/projects\n'
    'git clone git@github.com:<your-username>/Masters-level-DIY-Data-Science-Curriculum-ai-Era-.git\n'
    'cd Masters-level-DIY-Data-Science-Curriculum-ai-Era-\n'
    'git remote -v   # should show SSH URLs\n',
    code_style,
))
story.append(Spacer(1, 12))

# === 7) Project Structure ===
story.append(Paragraph("7) Project Structure (inside ds-zero-to-one)", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    'cd ~/projects/Masters-level-DIY-Data-Science-Curriculum-ai-Era-\n'
    'mkdir -p ds-zero-to-one\n'
    'cd ds-zero-to-one\n\n'
    'mkdir -p data/raw data/processed notebooks reports src tests .github/workflows\n'
    'touch data/.gitkeep data/raw/.gitkeep data/processed/.gitkeep \\\n'
    '      notebooks/.gitkeep reports/.gitkeep src/.gitkeep tests/.gitkeep\n\n'
    "cat > .gitignore <<'EOF'\n"
    "data/**\n\n"
    "!data/.gitkeep\n"
    "!data/raw/.gitkeep\n"
    "!data/processed/.gitkeep\n"
    "**/.ipynb_checkpoints\n"
    "__pycache__/\n"
    "*.pyc\n"
    ".env\n"
    ".venv\n"
    "EOF\n\n"
    "cat > .gitattributes <<'EOF'\n"
    "* text=auto\n"
    "*.py      text eol=lf\n"
    "*.ipynb   text eol=lf\n"
    "*.yml     text eol=lf\n"
    "*.md      text eol=lf\n"
    "*.csv     text eol=lf\n"
    "*.ps1     text eol=crlf\n"
    "*.bat     text eol=crlf\n"
    "*.png     binary\n"
    "*.jpg     binary\n"
    "*.pdf     binary\n"
    "EOF\n\n"
    "git add .\n"
    'git commit -m "chore: scaffold project structure"\n'
    "git push --set-upstream origin main\n",
    code_style,
))
story.append(PageBreak())

# === 8) Install Miniconda & Create Env ===
story.append(Paragraph("8) Install Miniconda (WSL) & Create Env", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    "sudo apt update && sudo apt install -y wget curl\n"
    "wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh\n"
    "bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3\n"
    "~/miniconda3/bin/conda init bash\n"
    "exec bash\n\n"
    "conda --version\n"
    "conda config --add channels conda-forge\n"
    "conda config --set channel_priority strict\n\n"
    "# Create env (or use environment.yml in next step)\n"
    "conda create -n ds -c conda-forge python=3.13.5 numpy pandas scikit-learn \\\n"
    "             jupyterlab ipykernel matplotlib plotly duckdb -y\n"
    "conda activate ds\n"
    "pip install polars\n"
    'python -m ipykernel install --user --name ds --display-name "Python (ds)"\n',
    code_style,
))
story.append(Spacer(1, 12))

# === 9) Add environment.yml ===
story.append(Paragraph("9) Add environment.yml (preferred)", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    "cat > environment.yml <<'YML'\n"
    "name: ds\n"
    "channels:\n"
    "  - conda-forge\n"
    "channel_priority: strict\n"
    "dependencies:\n"
    "  - python=3.13.5\n"
    "  - numpy\n"
    "  - pandas\n"
    "  - matplotlib\n"
    "  - scikit-learn\n"
    "  - jupyterlab\n"
    "  - ipykernel\n"
    "  - duckdb\n"
    "  - plotly\n"
    "  - pip\n"
    "  - pip:\n"
    "      - polars\n"
    "YML\n\n"
    "git add environment.yml\n"
    'git commit -m "chore: add environment.yml"\n'
    "git push\n",
    code_style,
))
story.append(PageBreak())

# === 10) JupyterLab Smoke Test ===
story.append(Paragraph("10) JupyterLab Smoke Test", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    "cd ~/projects/Masters-level-DIY-Data-Science-Curriculum-ai-Era-/ds-zero-to-one\n"
    "conda activate ds\n"
    "jupyter lab --no-browser --ip=0.0.0.0\n\n"
    "# In a new notebook, run:\n"
    "# import pandas as pd, duckdb, polars as pl\n"
    '# print("Environment OK!", pd.__version__, duckdb.__version__, pl.__version__)\n',
    code_style,
))
story.append(Spacer(1, 12))

# === 11) GitHub Actions CI ===
story.append(Paragraph("11) GitHub Actions CI (repo root)", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    "cd ~/projects/Masters-level-DIY-Data-Science-Curriculum-ai-Era-\n"
    "mkdir -p .github/workflows\n"
    "cat > .github/workflows/ci.yml <<'CI'\n"
    "---\n"
    "name: CI\n"
    "'on':\n"
    "  - push\n"
    "  - pull_request\n\n"
    "jobs:\n"
    "  build:\n"
    "    runs-on: ubuntu-latest\n"
    "    defaults:\n"
    "      run:\n"
    "        working-directory: ds-zero-to-one\n"
    "        shell: bash -l {0}\n"
    "    steps:\n"
    "      - uses: actions/checkout@v4\n"
    "      - uses: conda-incubator/setup-miniconda@v3\n"
    "        with:\n"
    "          miniforge-version: latest\n"
    "          use-mamba: true\n"
    "          auto-activate-base: false\n"
    "          conda-remove-defaults: true\n"
    "          channels: conda-forge\n"
    "          channel-priority: strict\n"
    "          environment-file: ds-zero-to-one/environment.yml\n"
    "          activate-environment: ds\n"
    "      - name: Sanity check\n"
    '        run: python -c "import pandas, duckdb, polars as pl; print(\'CI env OK\')"\n'
    "CI\n\n"
    "git add .github/workflows/ci.yml\n"
    'git commit -m "ci: reproducible conda-forge workflow"\n'
    "git push\n",
    code_style,
))
story.append(PageBreak())

# === 12) Optional Docker Dev Image ===
story.append(Paragraph("12) Optional Docker Dev Image", h1))
story.append(Spacer(1, 6))
story.append(Preformatted(
    "cat > ds-zero-to-one/.dockerignore <<'DIGN'\n"
    "__pycache__/\n"
    "*.pyc\n"
    ".ipynb_checkpoints/\n"
    ".env\n"
    ".env.*\n"
    "data/\n"
    "models/\n"
    "mlruns/\n"
    "node_modules/\n"
    "DIGN\n\n"
    "cat > ds-zero-to-one/Dockerfile <<'DF'\n"
    "FROM mambaorg/micromamba:1.5.10\n"
    "WORKDIR /workspace\n"
    "COPY environment.yml /tmp/environment.yml\n"
    "ARG MAMBA_DOCKERFILE_ACTIVATE=1\n"
    "RUN micromamba create -y -n ds -f /tmp/environment.yml && micromamba clean --all --yes\n"
    'SHELL ["/bin/bash", "-lc"]\n'
    "ENV CONDA_DEFAULT_ENV=ds\n"
    "EXPOSE 8888\n"
    "COPY . /workspace\n"
    'CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token="" --NotebookApp.password=""\n'
    "DF\n\n"
    "cd ~/projects/Masters-level-DIY-Data-Science-Curriculum-ai-Era-/ds-zero-to-one\n"
    "docker build -t ds-env .\n"
    "docker run --rm -p 8888:8888 -v $(pwd):/workspace ds-env\n",
    code_style,
))
story.append(PageBreak())

# === 13) Validation Checklist ===
story.append(Paragraph("13) Validation Checklist", h1))
story.append(Spacer(1, 6))
story.append(Paragraph("Quick ways to sanity-check your setup:", body))
story.append(Spacer(1, 4))
story.append(Paragraph("• SSH: run <code>ssh -T git@github.com</code> → expect a success message.", body))
story.append(Paragraph("• Docker: <code>docker run hello-world</code> → see “Hello from Docker!”.", body))
story.append(Paragraph("• Conda: <code>conda --version</code> (25.5.x); <code>python --version</code> (3.13.5) in env.", body))
story.append(Paragraph(
    "• Jupyter: in a notebook, print versions for <code>pandas</code>, <code>duckdb</code>, <code>polars</code>.",
    body,
))
story.append(Paragraph(
    "• GitHub Actions: GitHub → Actions → <b>CI</b> → check latest run contains “CI env OK”.",
    body,
))
story.append(Spacer(1, 12))

# === 14) Troubleshooting (Quick Fixes) ===
story.append(Paragraph("14) Troubleshooting (Quick Fixes)", h1))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "<b>Polars conda solver conflicts</b>: Install <code>polars</code> via <code>pip</code> "
    "(keep conda-forge only).",
    body,
))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>CI can't import pandas</b>: Ensure <code>activate-environment: ds</code> and "
    "<code>defaults.run.shell: 'bash -l {0}'</code>, and that <code>environment-file</code> path "
    "is correct.",
    body,
))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>SSH passphrase prompts each push</b>: run <code>eval \"$(ssh-agent -s)\"</code>; "
    "<code>ssh-add ~/.ssh/id_ed25519</code>; add these to <code>~/.bashrc</code> to auto-load.",
    body,
))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>Docker not found in WSL</b>: Enable WSL integration in Docker Desktop; run "
    "<code>wsl --shutdown</code>, then reopen Ubuntu.",
    body,
))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "<b>No workflows listed</b>: Workflows must live at repo root <code>.github/workflows/</code>. "
    "Use <code>working-directory</code> in CI to target a subfolder.",
    body,
))
story.append(Spacer(1, 18))

story.append(Paragraph(
    "You can now rebuild this entire environment from scratch any time, on any Windows 11 machine, "
    "by walking through these steps in order.",
    body,
))

# === BUILD PDF ===
doc.build(story)

print(f"PDF written to: {pdf_path}")
