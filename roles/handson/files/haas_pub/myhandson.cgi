#!/usr/bin/perl

use strict;
require 'lib.pl';
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $id = $form->param('name');

# Get values
my $host = get_value('hostaddr');
my $pathname = get_value('pathname');
my $dbfilename = get_value('dbfilename');
my @list;

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

@list = split(/,/,$h{$id});
untie %h;

### OUTPUT HTML ###
header("$host","$pathname");

howto();

handsref($host,$list[0],$list[3],$list[4],$list[5],$list[2],$id);

print "完了したら以下の「 終了 」ボタンを押してください。実施が記録され、環境がクリアされます。";
print "<center><form action=\"./$pathname/delete.cgi\" method=\"post\">\n";
print "<input type=\"hidden\" name=\"name\" value=\"$id\"><input id=\"button\" type=\"submit\" value=\"終了\">\n";
print "</form></center>\n";

footer("$pathname");

exit (0);
