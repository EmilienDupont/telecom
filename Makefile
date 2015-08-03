GENERATED_FILES = \
	capecod.json

all: $(GENERATED_FILES)
	./SimpleServer.py

test:
	./telecom.py

clean:
	-rm -rf -- $(GENERATED_FILES) build gurobi.log *.pyc *.lp


build/tracts.zip:
	mkdir build
	curl -o $@ 'http://wsgw.mass.gov/data/gispub/shape/census2010/CENSUS2010_BLK_BG_TRCT_SHP.zip'

build/CENSUS2010BLOCKGROUPS_POLY.shp: build/tracts.zip
	-rm -rf $@
	unzip -d build/ $<
	touch $@

build/tracts.shp: build/CENSUS2010BLOCKGROUPS_POLY.shp
	ogr2ogr -f "ESRI Shapefile" -where "COUNTYFP10 = '001'" -t_srs EPSG:4269 $@ $<

capecod.json: build/tracts.shp
	ogr2ogr -f GeoJSON $@ $<
