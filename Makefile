all:
	./SimpleServer.py

test:
	./telecom.py

clean:
	-rm gurobi.log *.pyc *.lp
