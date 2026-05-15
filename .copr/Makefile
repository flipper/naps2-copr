srpm:
	dnf -y install spectool
	spectool -g -R naps2.spec
	rpmbuild -bs naps2.spec --define "_srcrpmdir $(outdir)"
