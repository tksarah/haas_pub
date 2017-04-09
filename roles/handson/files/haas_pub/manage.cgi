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


statistics($this_month);

print <<LINKS;
<p>
<hr>
<a href="./$pathname/log_check.cgi"  target="_blank">[ Status Check ]</a>
LINKS

footer("$pathname");

exit (0);

### Log Page
## Statistics for month
sub statistics{

        my $month = shift;
        my $logfile = get_value('logfile');
        my $total=0;
        my $rec;
        my $ucnt;
        my $urec;
        my @ids;
        my @types;
	my @id_type;
	my %counts;
	my %over20_counts = (emp => 0, time => 0);
	my %under20_counts = (emp => 0, time => 0);;
	my $emp_m = 0;
	my $emp_m_o20 = 0;
	my $emp_m_u20 = 0;
	
        open(R,"<$logfile");
        while (<R>) {

                my $id = (split/,/,$_)[0];
                my $type = (split/,/,$_)[1];
		# date hands-on has been started
                my $date = (split/,/,$_)[2];
                my $status = (split/,/,$_)[7];
                my $time = (split/,/,$_)[9];

		if( $date =~ /$month/ ){
			$rec = "$id:$type";
			push(@ids,$id);
			push(@id_type,$rec);

			if($time >= 20){
				$over20_counts{"emp"}++;
				$over20_counts{"time"} = $over20_counts{"time"} + $time;
			}else{
				$under20_counts{"emp"}++;
				$under20_counts{"time"} = $under20_counts{"time"} + $time;
			}

			if($status == 1){
				$counts{"success"}++;;
				$counts{"stime"} = $counts{"stime"} + $time;
			}else{
				$counts{"ftime"} = $counts{"ftime"} + $time;
			}

			if($type eq "ansible-1" && $status == 1){
				$counts{"ansible-1-s"}++;
			}elsif($type eq "ansible-1" && $status == 0){
				$counts{"ansible-1-f"}++;
			}elsif($type eq "ansible-2" && $status == 1){
				$counts{"ansible-2-s"}++;
			}elsif($type eq "ansible-2" && $status == 0){
				$counts{"ansible-2-f"}++;
			}elsif($type eq "serverspec-1" && $status == 1){
				$counts{"serverspec-1-s"}++;
			}elsif($type eq "serverspec-1" && $status == 0){
				$counts{"serverspec-1-f"}++;
			}
			$total++;
        	}
	}
        close(R);

        $ucnt = uniq_func(@ids);
        $urec = uniq_func(@id_type);

	# /employee
	# $round=sprintf("%.2f",$val); 3.14
	if($ucnt != 0){
		$emp_m = sprintf("%.1f",($counts{'stime'} + $counts{'ftime'})/$ucnt);
	}
	if($over20_counts{'emp'} != 0){
		$emp_m_o20 = sprintf("%.1f",$over20_counts{'time'}/$over20_counts{'emp'});
	}
	
	if($under20_counts{'emp'} != 0){
		$emp_m_u20 = sprintf("%.1f",$under20_counts{'time'}/$under20_counts{'emp'});
	}

	# ajust for hours
	my $emp_h = sprintf("%.1f", ($counts{'stime'} + $counts{'ftime'})/60); 

# OUTPUT
print <<STATS;

<div onclick="obj=document.getElementById('sogo').style; obj.display=(obj.display=='none')?'block':'none';">
<a style="cursor:pointer;"><h3>▼ 総合集計（$month）</h3></a>
</div>
<br>
試験運用：2016/7/19～2016/7/31 <br>
サービス開始日：2016/8/1～
<div id="sogo" style="display:none;clear:both;">
<table class="simple">
<tr><th>項目</th><th>値</th></tr>
<tr><td>トータル施策適用工数（時）</td><td id="r"><font size="5pt"><b>$emp_h</b></font></td></tr>
<tr><td>トータルハンズオン実施数</td><td id="r">$total</td></tr>
<tr><td>トータルハンズオン完了数</td><td id="r">$counts{'success'}</td></tr>
<tr><td>トータルハンズオン完了時間（分）</td><td id="r"><font color="blue">$counts{'stime'}</font></td></tr>
<tr><td>トータルハンズオン未完了時間（分）</td><td id="r"><font color="red">$counts{'ftime'}</font></td></tr>
<tr><td>ユニークユーザ数</td><td id="r">$ucnt</td></tr>
<tr><td>ユニークハンズオン数（ID＋ハンズオンタイプ）</td><td id="r">$urec</td></tr>
<tr><td>ハンズオン時間/人（分）</td><td id="r">$emp_m</td></tr>
</table>
</div>
<p>

<div onclick="obj=document.getElementById('detail').style; obj.display=(obj.display=='none')?'block':'none';">
<a style="cursor:pointer;"><h3>▼ 詳細集計（$month）</h3></a>
</div>
<p>
各ハンズオンはインチキをしない限り、数分では完了できませんのでそのような実施は除外とするための情報
<p>
<div id="detail" style="display:none;clear:both;">
<table class="simple">
<tr><th>項目</th><th>サブ項目</th><th>値</th></tr>
<tr><td rowspan="2">20分以上で終了</td><td>ハンズオン数</td><td id="r">$over20_counts{'emp'}</td></tr>
<tr></td><td>時間/ハンズオン（分）</td><td id="r">$emp_m_o20</td></tr>
<tr><td rowspan="2">20分以下で終了</td><td>ハンズオン数</td><td id="r">$under20_counts{'emp'}</td></tr>
<tr></td><td>時間/ハンズオン（分）</td><td id="r">$emp_m_u20</td></tr>
</table>
</div>
<p>

<div onclick="obj=document.getElementById('handsons').style; obj.display=(obj.display=='none')?'block':'none';">
<a style="cursor:pointer;"><h3>▼ ハンズオン科目別（$month）</h3></a>
</div>
<br>
<div id="handsons" style="display:none;clear:both;">
<table class="simple">
<tr><th>項目</th><th>値</th></tr>
<tr><td>Ansible 初級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'ansible-1-s'}</font></td></tr>
<tr><td>Ansible 中級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'ansible-2-s'}</font></td></tr>
<tr><td>Serverspec 初級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'serverspec-1-s'}</font></td></tr>
<tr><td>Ansible 初級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'ansible-1-f'}</font></td></tr>
<tr><td>Ansible 中級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'ansible-2-f'}</font></td></tr>
<tr><td>Serverspec 初級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'serverspec-1-f'}</font></td></tr>
</table>
</div>
<p>

STATS

}

