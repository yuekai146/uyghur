for site in tianshan uycnr xinhua xjdaily xj_gov xjkunlun xj_people 
do
	cd ./finished/$site
	cp ../../clean.sh ./
	bash clean.sh ./texts.txt
	cd ../../
done
