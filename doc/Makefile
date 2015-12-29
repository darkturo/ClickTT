PLANTUML_FILES=$(wildcard plantuml/*.uml)
PNG_FILES=$(patsubst %.uml,%.png,$(PLANTUML_FILES))

all: plantuml.jar $(PNG_FILES)

%.png: %.uml
	mkdir -p images
	java -Djava.awt.headless=true -jar plantuml.jar -tpng -o ../images $<

clean:
	rm -rf images

plantuml.jar:
	wget -O plantuml.jar http://downloads.sourceforge.net/project/plantuml/plantuml.jar?r=http%3A%2F%2Fplantuml.com%2Fdownload.html

purge: clean
	rm -rf plantuml.jar
