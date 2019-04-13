DIR_SUFFIX="broncode"

build_image() {
	cd $1
	echo "Building ${1:2}"
	./build.sh > /dev/null
	cd ..
}

for FILE in ./*
do
	if [ "${FILE:2:8}" == "$DIR_SUFFIX" ]
	then	
		build_image "$FILE"
	fi
done
exit 0
