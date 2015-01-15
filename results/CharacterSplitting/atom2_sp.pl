#!/usr/bin/perl
# atom2_sp.pl
# Atomizes characters further

# This is part of the Perl script that was used to further atomize (split up) Flora of the Guianas volumes other than volume A24 (for which a different, less efficient, method was used). As usual, processing file line-by-line.

# What does the script do?

# 1) Firstly, using a if-then-loop, it selects only lines with (sub-)characters to modify.
# 2) For each of these lines, it tries to match certain specific words that belong to specific, concrete subcharacters (traits), as follows:
	# a) A regular expression is used to match the first instance of a keyword being used, and then insert the opening XML tags for that subcharacter/trait,
	# b) A second regular expression is used to match the last instance of a keyword being used, using the previously inserted XML as a starting point, and then insert the closing XML tags  for that subcharacter/trait.
		# The first and last keywords matched may be the same word, but not necessarily. All text between the first and last keyword is assumed to belong to the same subcharacter/trait. This method requires subsequent proofreading of the XML file to ensure correctness.
	# c) The Perl regex "g" flag ('global') is used to allow the regexes to always match the subcharacters sought, even if there's multiple cases of them within the same line (which is possible).
	
# NOTE: for use on a TSV-file, some modifications will be needed because you can't use the XML-tags as starting points (since they are absent).



use warnings;
use strict;
use utf8;
use open ':encoding(utf8)';

my $source = shift @ARGV;
my $destination = shift @ARGV;

open IN, $source or die "Can't read source file $source: $!\n";
open OUT, "> $destination" or die "can't write on file $destination: $!\n";

while (<IN>) {

	# Further atomisation, originally for pilot study (Hester), now for all remaining vols.:
	
	if (/^\t+<(?:subC|c)har/) {
		
		# Colors:
		# Finding first colour-related word in line:
		s/(har class="[a-z -]+">.+? )((?:bright(?:er|) |dark(?:er|) |dull(?:er|)|light(?:er|) |pale(?:r|) |pastel |waxy |)(?:aquamarine|azure|black(?:ish|)|blu(?:e|ish)|brown(?:ish|)|champagne|crimson|cyan|gold(?:en|ish|)|green(?:ish|)|grey(?:ish|)|indigo|lavender|lilac|magenta|maroon|orang(?:e|ish)|pink(?:ish|)|purpl(?:e|ish)|(?:brick |wine-|)red(?:dish|)|scarlet|silver(?:ish|)|transparent|turquoise|variously colored|vermillion|violet|whit(?:e|ish)|yellow(?:ish|))(?: |\.|,|;|:|-))/$1<subChar class="colour">$2/g;
		# Collecting remaining colour-related words in line:
		s/(<subChar class="colour">(?:.+|)(?:aquamarine|azure|black(?:ish|)|blu(?:e|ish)|brown(?:ish|)|champagne|crimson|cyan|gold(?:en|ish|)|green(?:ish|)|grey(?:ish|)|indigo|lavender|lilac|magenta|maroon|orang(?:e|ish)|pink(?:ish|)|purpl(?:e|ish)|(?:brick |wine-|)red(?:dish|)|scarlet|silver(?:ish|)|transparent|turquoise|variously colored|vermillion|violet|whit(?:e|ish)|yellow(?:ish|))(?: base|))(?!\n)/$1<\/subChar>/g;
		
		
		# Growth form:
		# Finding first growth form-related word in line:
		s/(har class="[a-z -]+">.+? )((?:more or less |occasionally |slightly |some(?:times|what) |)(?:clambering|creeping|erect|multi(?:-|)stemmed|parted|pendent|recurved|repent|scandent|spreading)(?!, smooth calyculus\.)(?! leaves)(?: |\.|,|;|:|-))/$1<subChar class="growth form">$2/g;
		# Collecting remaining growth form-related words in line:
		s/(<subChar class="growth form">(?:.+|)(?:clambering|creeping|erect|multi(?:-|)stemmed|parted|pendent|recurved(?: in upper 1\/2 or 1\/3 only|)|repent|scandent|spreading))(?!\n)/$1<\/subChar>/g;
		
		
		# Hairs:
		# Finding first hair-related word in line:
		s/(har class="[a-z -]+">.+? )((?:above |appressed(?: |-)|(?:outside |)densely |fairly |inside |minutely |more or less |nearly |often |outside |rather |short |softly |somewhat |(?:above |)sparsely |very |)(?:glabr(?:escent|ous)|hair(?:less|s)|hirsute|pilos(?:e|ulous)|(?:hirto-|)puberul(?:ent|ous)|(?:appressed |)pubescent|sericeous|strig(?:ill|)ose|toment(?:ellous|ose)|villo(?:se|us))(?: |\.|,|;|:|-))/$1<subChar class="hairs">$2/g;
		# Collecting remaining hair-related words in line:
		s/(<subChar class="hairs">(?:.+|)(?:glabr(?:escent|ous)|hair(?:less|s)|hirsute|pilos(?:e|ulous)|(?:hirto-|)puberul(?:ent|ous)|(?:appressed |)pubescent|sericeous|strig(?:ill|)ose|toment(?:ellous|ose)|villo(?:se|us))(?: on exterior|))(?!\n)/$1<\/subChar>/g;
		
		
		# Margin type:
		# Finding first margin type-related word in line:
		s/(har class="margins">.+? )((?:fairly |minutely |more or less |nearly |often |rather |short |softly |somewhat |sparsely |very |)(?:dentate|entire|serrate|serrulate|sinuate|spinose)(?: |\.|,|;|:|-))/$1<subChar class="margin type">$2/g;
		# Collecting remaining margin type-related words in line:
		s/(<subChar class="margin type">(?:.+|)(?:dentate|entire|serrate|serrulate|sinuate|spinose))(?!\n)/$1<\/subChar>/g;
		
		
		
		# Position:
		# Finding first position-related word in line:
		s/(har class="[a-z -]+">.+? )((?:both |former in |mostly |nearly |(?:in uppermost leaf axils, |)not (?:truly |)|)(?:(?:supra-|)axillary(?: only(?:\?|)|)|cauliflorous|lateral|pendulous|ramiflorous|terminal)(?! corky)(?! horn)(?: |\.|,|;|:|-))/$1<subChar class="position">$2/g;
		# Collecting remaining position-related words in line:
		s/(<subChar class="position">(?:.+|)(?:(?:supra-|)axillary(?: only(?:\?|)|)|cauliflorous|lateral|pendulous|ramiflorous|terminal)(?: and in nearby axils| and at older nodes|))(?!\n)/$1<\/subChar>/g;
		
		# Questionable cases, removal of character class:
		s/(<subChar class=")(position)(">.+?<\/subChar> (?:branch|flower|groups|inflorescence|leaves|ligule|raceme))/$1$3/;
		
		
		
		
		# Shape:
		# Finding first shape-related word in line:
		s/(har class="[a-z -]+">.+? )((?:broadly |irregularly |more or less |mostly |narrowly |obliquely |somewhat |varying from |)(?:acuminate|acute|(?:a|)symmetrical|(?:ob|)conic(?:al|)|cordate|cuneate|cylindric|deltoid|(?:ob|)ellip(?:soid|tic(?:al|))|(?:sub|)falcate|funnelform|fusiform|(?:sub|)globose|(?:(?:linear-|)ob|\(ob\)|wide-|)lance(?:olate|)|linear|oblong(?:oid|)|obtuse|(?:sub|)orbicula(?:r|te)|(?:(?:sub|)ob|\(ob\)|)ovate|ovoid|(?:sub|)rhombic|(?:sub|)reniform|rounded|(?:sub|)spat(?:h|)ulate|(?:sub|)spherical|subulate|(?:sub|)triangular|truncate|tubular)(?: |\.|,|;|:|-))/$1<subChar class="shape">$2/g;
		# Collecting remaining shape-related words in line:
		s/(<subChar class="shape">(?:.+|)(?:acuminate|acute|(?:a|)symmetrical|(?:ob|)conic(?:al|)|cordate|cuneate|cylindric|deltoid|(?:ob|)ellip(?:soid|tic(?:al|))|(?:sub|)falcate|funnelform|fusiform|(?:sub|)globose|(?:(?:linear-|)ob|\(ob\)|wide-|)lance(?:olate|)|linear|oblong(?:oid|)|obtuse|(?:sub|)orbicula(?:r|te)|(?:(?:sub|)ob|)ovate|ovoid|(?:sub|)rhombic|(?:sub|)reniform|rounded|(?:sub|)spathulate|(?:sub|)spherical|subulate|(?:sub|)triangular|truncate|tubular))(?!\n)/$1<\/subChar>/g;
		
		
		# Texture:
		# Finding first texture-related word in line:
		s/(har class="[a-z -]+">.+? )((?:fairly |more or less |often |rather |somewhat |very |)(?:bullate|chartaceous|(?:sub|)coriaceous|fleshy|leathery|membranous|papery|papyraceous|scabrous|stiff|thick(?!-walled)|thin)(?: |\.|,|;|:|-))/$1<subChar class="texture">$2/g;
		# Collecting remaining texture-related words in line:
		s/(<subChar class="texture">(?:.+|)(?:bullate|chartaceous|(?:sub|)coriaceous|fleshy|leathery|membranous|papery|papyraceous|scabrous|stiff|thick(?!ening)| thin))(?!\n)/$1<\/subChar>/g;
		
		
	}
	
	
	
	
	print OUT $_; 
}

close IN;
close OUT;