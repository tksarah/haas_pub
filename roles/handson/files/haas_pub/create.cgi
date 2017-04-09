#!/usr/bin/perl

require 'lib.pl';
use strict;
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $id = $form->param('name');
my $type = $form->param('type');

# Get values
my $limit = get_value('limit');
my $host = get_value('hostaddr');
my $pathname = get_value('pathname');
my $playhome = get_value('playhome');
my $inventory = get_value('inventory');
my $inventoryfile = "$playhome/$inventory";
my $playbook = get_value('playbook');
my $playbookfile = "$playhome/$playbook";
my $dbfilename = get_value('dbfilename');
my @list;

my $back_url = $ENV{'HTTP_REFERER'};
if(!$back_url){
        $back_url = "http://$host/$pathname/";
}

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";
my $num = keys %h;

# Check name,type exists/name duplicated
if( $id eq "" || $id !~ /^[\w]+$/ ){
        error_page(1,$back_url);
        exit(0);
}elsif($type eq ""){
        error_page(2,$back_url);
        exit(0);
}elsif($h{$id}){
        error_page(3,$back_url);
        exit(0);
}

# Get time
my $dts = DateTime->now(time_zone => 'Asia/Tokyo');
my $dte = $dts->clone;
$dte->add(minutes => $limit);

# Create ports
my $blog = 8081 + $num;
my $htty = 3000 + $num + 1;
# Limit 50 users
my $ttty = $htty + 50;

# Check Open port
my $ret = system("ss -ltn | grep $blog");
if(!$ret){
	my $add = int(rand(99));
	$blog = $blog + $add;
	$htty = $htty + $add;
	$ttty = $ttty + $add;
}
	
# Generate portlist
my $port = "$blog,$htty,$ttty";

# Make string
my $string = "$type,$dts,$dte,$port";

# Run Playbook
create($id,$type,$blog,$htty,$ttty,$inventoryfile,$playbookfile);

# Set k/v
$h{"$id"} = $string;

untie %h;

### OUTPUT HTML ###
header("$host","$pathname");

howto();

handsref($host,$type,$blog,$htty,$ttty,$dte,$id);

print "完了したら以下の「 終了 」ボタンを押してください。実施が記録され、環境がクリアされます。<br>";
print "<center><form action=\"./$pathname/delete.cgi\" method=\"post\">\n";
print "<input type=\"hidden\" name=\"name\" value=\"$id\"><input id=\"button\" type=\"submit\" value=\"終了\">\n";
print "</form></center><br><br>\n";

footer("$pathname");

exit (0);
