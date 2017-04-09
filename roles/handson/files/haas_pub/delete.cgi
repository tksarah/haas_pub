#!/usr/bin/perl

require 'lib.pl';
use strict;
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $id = $form->param('name');

# Get values
my $host = get_value('hostaddr');
my $pathname = get_value('pathname');
my $playhome = get_value('playhome');
my $inventory = get_value('inventory');
my $inventoryfile = "$playhome/$inventory";
my $playbook = get_value('playbook');
my $playbookfile = "$playhome/$playbook";
my $dbfilename = get_value('dbfilename');
my $logfile = get_value('logfile');

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

my @list = split(/,/,$h{$id});

# Get Delete time
my $now = DateTime->now(time_zone => 'Asia/Tokyo');
# Get Start time from db
my $strp = DateTime::Format::Strptime->new( pattern => '%Y-%m-%dT%H:%M:%S' );
my $dts = $strp->parse_datetime($list[1]);
# Start time - Delete time
my $dur = $dts->delta_ms($now);

# K/V Delete 
delete $h{$id};

# Destroy id
destroy($id,$inventoryfile,$playbookfile);

untie %h;

### OUTPUT HTML ###
header("$host","$pathname");

print "お疲れ様でした。<br>\n";

footer("$pathname");

exit (0);
