#!/bin/sh

USAGE="USAGE: ./createcondarepo.sh -s <anaconda-script> -d <installation-directory> [options]"

CHANNELS=()
YAMLS=()
while [[ "$#" -gt 0 ]]; do
	case $1 in
		-s) ANACONDA_SCRIPT="$2"; shift ;;
		-d) PREFIX="$2"; shift ;;
		-c) CHANNELS+=("$2"); shift ;;
		-p) PIN="$2"; shift ;;
		-y) YAMLS+=("$2"); shift ;;
		-l) LOCAL_DIR="$2"; shift ;;
		-o) REPOSITORY_FILE="$2"; shift ;;
		-h) HELP="true" ;;
	esac
	shift
done

if [ "$HELP" == "true" ]; then
	echo ""
	echo "$USAGE"
	echo ""
	echo "This script will install Anaconda or Miniconda locally to create a local conda repository."
	echo "Internet access is required."
	echo ""
	echo "-s	Anaconda or Miniconda script installation file. If the script does not exist locally, it will be downloaded."
	echo "-d	Directory to install Anaconda."
	echo "-c	Name of channels used when creating the environment. If multiple channels are needed, specify this parameter multiple times."
	echo "-p	Version of conda to pin."
	echo "-y	Conda environment yaml file containing additional packages to be included in the repository. If multiple environments, specify this parameter multiple times."
	echo "-l	Local channel directory. Default is local-conda-channel."
	echo "-o	Output file name. Default is local-conda-repository.tgz."
	echo "-h	Help"
	exit 0
fi

if [ -z "$PREFIX" ]; then
	echo "$USAGE"
	exit 1
fi

if [ -z "$ANACONDA_SCRIPT" ]; then
	if [ ! -d "$PREFIX" ]; then
		echo "$USAGE"
		exit 1
	fi
elif [ ! -d "$PREFIX" ]; then
	if [[ "$ANACONDA_SCRIPT" == "Anaconda"* ]]; then
		TYPE="Anaconda"
		DOWNLOAD_PATH="https://repo.continuum.io/archive/$ANACONDA_SCRIPT"
	elif [[ "$ANACONDA_SCRIPT" == "Miniconda"* ]]; then
		TYPE="Miniconda"
		DOWNLOAD_PATH="https://repo.anaconda.com/miniconda/$ANACONDA_SCRIPT"
	else
		echo "ERROR: The $ANACONDA_SCRIPT is not recognized. Specify an Anaconda or Miniconda script name."
		exit 1
	fi
fi

if [ -z "$LOCAL_DIR" ]; then
	LOCAL_DIR="local-conda-channel"
fi

if [ -e "$LOCAL_DIR" ]; then
	echo "ERROR: $LOCAL_DIR already exists. Specify a new path to create the local conda channel."
	exit 1
fi

if [ -z "$REPOSITORY_FILE" ]; then
	REPOSITORY_FILE="local-conda-repository.tgz"
fi

if [ ! -d "$PREFIX" ]; then

	if [ -f "$ANACONDA_SCRIPT" ]; then
		echo "INFO: Found script $ANACONDA_SCRIPT."
	else
		echo "INFO: The $ANACONDA_SCRIPT script is not found. Downloading $TYPE from $DOWNLOAD_PATH."
		wget $DOWNLOAD_PATH
		if [ ! -f "$ANACONDA_SCRIPT" ]; then
			echo "ERROR: Failed to download $ANACONDA_SCRIPT."
			exit 1
		else
			chmod +x "$ANACONDA_SCRIPT"
		fi
	fi

	echo "INFO: Installing $TYPE to $PREFIX."

	./$ANACONDA_SCRIPT -b -p $PREFIX
	rc="$?"
	if [ "$rc" -ne 0 ]; then
		echo "ERROR: Failed to install $TYPE."
		exit $rc
	fi
else
	echo "INFO: Using existing Anaconda installation in $PREFIX."
fi

$PREFIX/bin/conda config --system --set auto_update_conda false

for channel in "${CHANNELS[@]}"
do
	$PREFIX/bin/conda config --system --add channels $channel
done

if [ -z "$PIN" ]; then
	echo "conda=$PIN" >> $PREFIX/conda-meta/pinned
fi

. $PREFIX/etc/profile.d/conda.sh

for y in ${YAMLS[@]}
do
	echo "INFO: Loading additional packages from $y."
	env_name=`cat $y | grep "name: "`
	env_name=`echo ${env_name:6}`
	if [ -d "$PREFIX/envs/$env_name" ]; then
		echo "INFO: Updating the conda environment $env_name."
		$PREFIX/bin/conda env update -f $y
	else
		echo "INFO: Creating the conda environment $env_name."
		$PREFIX/bin/conda env create -f $y
	fi
	rc="$?"
	if [ "$rc" -ne 0 ]; then
		echo "ERROR: Failed to create the conda environment from $y."
		exit 1
	fi

done

#Install conda-build if it is not already there
$PREFIX/bin/conda list conda-build | grep conda-build > /dev/null
rc="$?"
if [ "$rc" -ne 0 ]; then
	$PREFIX/bin/conda install conda-build -y
	rc="$?"
	if [ "$rc" -ne 0 ]; then
		echo "ERROR: Failed to install the conda-build package."
		exit 1
	fi
fi

echo "INFO: Creating a local repository from all of the bz2 files."

mkdir -p $LOCAL_DIR
if [ "$rc" -ne 0 ]; then
	echo "ERROR: Failed to create $LOCAL_DIR."
	exit $rc
fi

mkdir -p $LOCAL_DIR/linux-64
mkdir -p $LOCAL_DIR/linux-ppc64le

if [ `uname -m` == "x86_64" ]; then
	ls $PREFIX/pkgs/*.bz2 && cp $PREFIX/pkgs/*.bz2 ./$LOCAL_DIR/linux-64
	ls $PREFIX/pkgs/*.conda && cp $PREFIX/pkgs/*.conda ./$LOCAL_DIR/linux-64
else
	ls $PREFIX/pkgs/*.bz2 && cp $PREFIX/pkgs/*.bz2 ./$LOCAL_DIR/linux-ppc64le
	ls $PREFIX/pkgs/*.conda && cp $PREFIX/pkgs/*.conda ./$LOCAL_DIR/linux-ppc64le
fi

$PREFIX/bin/conda index $LOCAL_DIR
rc="$?"
if [ "$rc" -ne 0 ]; then
	echo "ERROR: Failed to index $LOCAL_DIR."
	exit 1
fi

echo "INFO: Creating repository file $REPOSITORY_FILE."
tar czf $REPOSITORY_FILE $LOCAL_DIR
rc="$?"
if [ "$rc" -ne 0 ]; then
	echo "ERROR: Failed to create $REPOSITORY_FILE from $LOCAL_DIR."
	exit $rc
fi

echo "INFO: Local repository $REPOSITORY_FILE is ready."

