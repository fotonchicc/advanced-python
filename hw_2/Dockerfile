FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

RUN pip install latex_generator_fotonchicc==0.0.1

WORKDIR /app

COPY latex_2_2/main.py .
COPY latex_2_2/image.png .

CMD sh -c "python main.py && pdflatex 2_2_latex_doc.tex && cp 2_2_latex_doc.pdf /output/docker_output.pdf"