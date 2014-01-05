#!/usr/bin/env python

import argparse, io, os, pprint, re

def splitvcf(filepath):
	dirpath = os.path.dirname(filepath)
	dirpath = os.path.join(dirpath, 'cards')
	if not os.path.exists(dirpath) :
		os.makedirs(dirpath)
	nbvcard = 0
	nbfullname = 0
	vcard = ''
	with open(filepath) as fullvcf:
		for vcfline in fullvcf:
			if re.search('BEGIN:VCARD', vcfline) :
				if len(vcard) > 0 :
					# Save the vcard
					savevcard(dirpath, nbvcard, vcard)
					# Ready for next vcard
					vcard = ''
				nbvcard = nbvcard + 1
			elif re.search('^FN:', vcfline) :
				fullname = vcfline[3:-1]
				nbfullname = nbfullname + 1
			vcard = vcard + vcfline
	
	if len(vcard) > 0 :
		# Save the vcard
		savevcard(dirpath, nbvcard, vcard)
	
	print 'Nb cards: %d' % nbvcard
	print 'Nb full names: %d' % nbfullname
	
def savevcard(dirpath, nb, content) :
	filename = os.path.join(dirpath, 'card%03d.vcf' % nb)
	with open(filename, 'w') as cardfile:
		cardfile.write(content)
			
def parseargs():
	parser = argparse.ArgumentParser(description='Parse large VCF file')
	parser.add_argument('VCFfile')
	args = parser.parse_args()
	return args.VCFfile
	
VCF_FILE = parseargs()

splitvcf(VCF_FILE)

