The steps for an offgrid build with the distribution recipes are as follows.
We will use the rhel7 build as an example, but any other recipe will be similarly used.

# Get the sources

    mkdir sources
    cd sources
    git clone https://github.com/baallan/distribution.git
    git clone https://github.com/ovis-hpc/ovis.git
    git clone https://github.com/ovis-hpc/sos.git
    wget https://github.com/LLNL/ldms-plugins-llnl/releases/download/1.5/ldms-plugins-llnl-1.5.tar.gz
    cd ..
    tar czf sources.tar.gz sources

Please note: Do NOT use the Github-offered zip files of the latest sources from these repositories.
The automatic zip files produced by github are broken because they do not
contain the git data our build assumes to exist.
Using the release tar or zip files from ovis-hpc/ovis is usually ok starting with version ovis-ldms-4.3.4-alpha.1.tar.gz, but anything earlier may have missing files depending on the release.

# Copy the sources.tar.gz file into your off-grid environment and extract it.

# Unpack the sources

    tar xzf sources.tar.gz
    cd sources

# Modify a build recipe for your site (e.g.)

    cd distribution
    cp -ar ovis-4.rhel7.base ovis-4.rhel7.base.myhacks
    cd ovis-4.rhel7.base.myhacks

# Modify ./firerpms and other scripts with your favorite editor
Change lines such as

    SOSREPO=https://github.com/ovis-hpc/sos.git
    OVISREPO=https://github.com/ovis-hpc/ovis.git


to


    SOSREPO=../../sos
    OVISREPO=../../ovis


then do the builds as directed by the README.md in your directory.

