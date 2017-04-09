#!/usr/bin/perl

require 'lib.pl';
use strict;
use BerkeleyDB;
use vars qw( %h $k $v );

# Get values
my $host = get_value('hostaddr');
my $pathname = get_value('pathname');
my $max_emp = get_value('max_emp');
my $dbfilename = get_value('dbfilename');

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";


### OUTPUT HTML ###
header("$host","$pathname");

# Output usage
#usage();

# Registration List
userlist(%h);

# Output Registration Form
#if (keys %h < $max_emp){ input_form(); }

#untie %h;

footer("$pathname");

exit(0);
