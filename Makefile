GENERATED_FILES = \
	capecod.json \
        ma.json

all: $(GENERATED_FILES)
	./SimpleServer.py

test:
	./telecom.py

clean:
	-rm -rf -- $(GENERATED_FILES) build gurobi.log *.pyc *.lp

# Data from http://www.mass.gov/anf/research-and-tech/it-serv-and-support/application-serv/office-of-geographic-information-massgis/datalayers/census2010.html
build/tracts.zip:
	mkdir build
	curl -o $@ 'http://wsgw.mass.gov/data/gispub/shape/census2010/CENSUS2010_BLK_BG_TRCT_SHP.zip'

build/CENSUS2010BLOCKGROUPS_POLY.shp: build/tracts.zip
	-rm -rf $@
	unzip -d build/ $<
	touch $@

build/tracts.shp: build/CENSUS2010BLOCKGROUPS_POLY.shp
	ogr2ogr -f "ESRI Shapefile" -where "COUNTYFP10 = '001'" -t_srs EPSG:4269 $@ $<

build/ma.shp: build/CENSUS2010BLOCKGROUPS_POLY.shp
	ogr2ogr -f "ESRI Shapefile" -where "COUNTYFP10 = '023' or COUNTYFP10 = '007'" -t_srs EPSG:4269 $@ $<

capecod.json: build/tracts.shp
	ogr2ogr -f GeoJSON $@ $<

build/maunmerged.json: build/ma.shp
	ogr2ogr -f GeoJSON $@ $<

build/maunmerged.topojson: build/maunmerged.json
	node_modules/topojson/bin/topojson -o $@ -- $<

ma.json: build/maunmerged.topojson
	cat $< | bin/topomesh maunmerged > $@
