#!/usr/bin/perl

require 'lib.pl';
use strict;
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $bm = $form->param('bm');

# Get values
my $host = get_value('hostaddr');
my $pathname = get_value('pathname');
my $dbfilename = get_value('dbfilename');
my $max_emp = get_value('max_emp');

# Get Date
my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
my $year = $dt->year;
my $this_month = $dt->month;
$this_month =~ s/(^\d$)/$year-0$1/;

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

### OUTPUT HTML ###
header("$host","$pathname");

### Manual Input Form
input_form();

# Registration List
print "<h3>利用状況</h3><br>";

if(keys %h == 0){
        print "利用者がいません。<p>\n";
}elsif(keys %h == $max_emp){
        print "現在<font color=\"red\">フル稼働</font>です。1時間以上お待ち下さい。\n";
        print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

        while (($k, $v) = each %h) {
                my @list = split(/,/,$v);
                print "<tr>";
                print "<td><a href=\"./$pathname/myhandson.cgi?name=$k\">$k</a></td>";
                print "<td>$list[0]</td>";
                print "<td>$list[1]</td>";
                print "<td>$list[2]</td>";
		print "<td><form action=\"./$pathname/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
                print "</tr>\n";
                }
        print "</table>\n";
}else{
        print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

        while (($k, $v) = each %h) {
                my @list = split(/,/,$v);
                print "<tr>";
                print "<td><a href=\"./$pathname/myhandson.cgi?name=$k\">$k</a></td>";
                print "<td>$list[0]</td>";
                print "<td>$list[1]</td>";
                print "<td>$list[2]</td>";
		print "<td><form action=\"./$pathname/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
                print "</tr>\n";
                }
        print "</table>\n";
        print "</p>\n";
}

untie %h;

footer("$pathname");

exit (0);


