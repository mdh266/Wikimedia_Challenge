# Copyright (c) Mike Harmon.
# Distributed under the terms of the Modified BSD License.

FROM jupyter/base-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    git \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    netcat \
    unzip \
    vim \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


USER $NB_UID

RUN mkdir /home/$NB_USER/Wikimedia && \
    fix-permissions /home/$NB_USER/Wikimedia/ 

COPY *.py                          /home/$NB_USER/Wikimedia/
COPY Wikimedia_Challenge.ipynb     /home/$NB_USER/Wikimedia/
COPY events_log.csv                /home/$NB_USER/Wikimedia/
COPY requirements.txt              /home/$NB_USER/Wikimedia/



RUN pip install -r /home/$NB_USER/Wikimedia/requirements.txt

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions /home/$NB_USER

USER $NB_UID

