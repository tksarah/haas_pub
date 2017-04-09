#!/usr/bin/perl

require 'lib.pl';
use strict;

# From POST
my $form = CGI->new;
my $flag = $form->param('f');

# Get values
my $host = get_value('hostaddr');
my $pathname = get_value('pathname');
my $logfile = get_value('logfile');

### OUTPUT HTML ###
header("$host","$pathname");

out_log($host,$flag);

print <<LINKS;
<p>
<hr>
<a href="./$pathname/manage.cgi">[ Manage Top ]</a>
LINKS

footer("$pathname");

exit (0);

sub out_log {
	my $hostaddr = shift;
	my $flag = shift;
	my $num=5;
	my @readline;
	my @cols;
	my $i;


	if(!$flag){
		print "<h3>log</h3><br>\n";
		print "<a href=\"http://$hostaddr/$pathname/log_check.cgi?f=latest\">[ Latest 5 log ]</a> ";
		print "<a href=\"http://$hostaddr/$pathname/log_check.cgi?f=all\">[ All ]</a> ";
		print "<p>\n";

		# out at
		my $atl_out = `sudo at -l`;
		my $atq_out = `sudo atq`;
		print "<h3>at list</h3>";
		print "<h4>at -l</h4>";
		print "<pre style=\"padding-left: 20px\">$atl_out</pre>";
		print "<h4>atq</h4>";
		print "<pre style=\"padding-left: 20px\">$atq_out</pre>";

		# out docker
		my $docker_out = `docker ps -a`;
		print "<h3>container list</h3>";
		print "<pre style=\"padding-left: 20px\">$docker_out</pre>";
		
	}elsif($flag eq "latest"){
		print "<h3>Latest 5 log</h3><br>\n";
		print "<table>\n";
		print "<tr><th>ID</th><th>Type</th><th>Start</th><th>End</th>";
		print "<th>Blog</th><th>Htty</th><th>Ttty</th><th>Status</th>";
		print "<th>Finish</th><th>Duration(min)</th></tr>\n";

		my @readline = `tail -n $num $logfile`;
		foreach (reverse @readline) {
			print "<tr>";
			@cols = split(/,/,$_);
			foreach $i (@cols){ print "<td>$i</td>"; }
			print "</tr>\n";
		}
		close(R);
		print "</table>\n";
		print "</p>\n";
		print "<a href=\"http://$hostaddr/$pathname/log_check.cgi?f=all\">[ All ]</a> ";

	}elsif($flag eq "all"){
		print "<h3>All log</h3><br>\n";
		print "<table>\n";
		print "<tr><th>ID</th><th>Type</th><th>Start</th><th>End</th>";
		print "<th>Blog</th><th>Htty</th><th>Ttty</th><th>Status</th>";
		print "<th>Finish</th><th>Duration(min)</th></tr>\n";

		open(R,"<$logfile");
		while (<R>) {
			print "<tr>";
			@cols = split(/,/,$_);
			foreach $i (@cols){ print "<td>$i</td>"; }
			print "</tr>\n";
		}
		close(R);
		print "</table>\n";
		print "</p>\n";
		print "<a href=\"http://$hostaddr/$pathname/log_check.cgi?f=latest\">[ Latest 5 log ]</a> ";
	}

}
