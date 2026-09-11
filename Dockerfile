# Single dev/runtime image (charter §7): Python app + LuaLaTeX/luatexja toolchain.
# TeX Live is installed from Debian packages and is NOT redistributed by us.
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Minimal TeX set for Japanese via LuaLaTeX. Add texlive-latex-extra later if a
# doc-package needs packages outside "recommended".
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      texlive-luatex \
      texlive-lang-japanese \
      texlive-latex-recommended \
      texlive-fonts-recommended \
      latexmk \
      fonts-noto-cjk \
      make \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install the package first so source edits under a bind mount do not bust the layer.
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e ".[dev]"

COPY . .

EXPOSE 8000
CMD ["entex", "--help"]
