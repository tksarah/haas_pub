use lib qw(./lib);
use CGI;
use IO::Socket;
use DateTime;
use DateTime::Format::Strptime;
use File::Basename;
use Data::Dumper;
use YAML::Tiny;
use feature ':5.10';

### HEADER Output
sub header{
	$hostaddr = shift;
	$pathname = shift;

print <<HEADER;
Content-type: text/html
Pragma: no-cache
Cache-Control: no-cache
Cache-Control: post-check=0, pre-check=0
Expires: Thu, 01 Dec 1994 16:00:00 GMT


	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
	<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
	 <head>
	  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
	  <meta http-equiv="Pragma" content="no-cache">
	  <meta http-equiv="Expires" content="0">
	  <title>Hands-on as a Service</title>
	  <base href="http://$hostaddr/"/>
	  <link rel="stylesheet" type="text/css" href="default.css"/>
	 </head>

	<body>

	<div id="header">
	  <h2><a href="http://$hostaddr/$pathname/">Hands-on as a Service for PUBLIC</a></h2>
	</div>

	<div id="content">
HEADER
}

### FOOTER Output
sub footer{
	$pathname = shift;

print <<FOOTER;
	</div>

	<div id="footer">
	  <em>
	  <font size="2" color="#508090">
	  COPYRIGHT(C) 2016,2017 「Hands-on as a Service for PUBLIC」 version 1.0<BR>
	  ALL RIGHTS RESERVED<BR>
	  Author:<a href="./$pathname/manage.cgi"  target="_blank"><font color="#508090">TK</font></a><BR>
	  </FONT>
	  </em>
	</div>

	</body>
	</html>
FOOTER
}

### Usage Output
sub usage{

print <<USAGE;
	<h3>お知らせ</h3><p>
	<b>XXXX年X月X日</b>・・・お知らせ
	<h3>利用方法</h3>
	<p>
	<font color="red">こちらを良く読んでから実施してください。</font>
	<ol id="list">
	<li><b>ハンズオンの種類を選択</b>します</li>
	<li>「ハンズオンビルド」ボタンを押すと、ハンズオンの環境が作られます</li>
	<li>ハンズオンの環境の情報を元にブラウザでアクセスし実施します</li>
	</ol>

	<h4>前提および、保持スキル</h4>
	<ul id="list">
	<li>Ansible、Serverspecの基本的な知識を保持</li>
	<li>Unix/Linuxオペレーション1年以上の経験、またはLPIC Level 1 同等以上の知識を保持</li>
	<li>viによるファイル編集、基本的なUnix/Linuxオペレーションが可能</li>
	</ul>

	<h4>必要なもの</h4>
	<ul id="list">
	<li>WiFiでインターネットアクセスが可能なPC、タブレットなど</li>
	<li>ブラウザ（Internet Explorer or Chrome で動作確認済み）</li>
	</ul>

	<h4>注意と制限</h4>
	<ul id="list">
	<li>ハンズオンの環境は手動で「終了」しない場合、<font color=red><b>60分</b></font>で自動的に削除</li>
	<li><font color=red>10人</font>までが同時に本サービスを利用可能</li>
	</ul>
USAGE
}

### Howto&Help
sub howto{

print <<HOWTO;
	<p>
	<h3>ハンズオンコンソール のTips</h3>
	<ul id="list">
	<li>コンソールが表示されない場合、少し待ってみる</li>
	<li>ブラウザのページ単位が1つのSSHセッション</li>
	<li>Copy & Paste は、Ctrl+C , Ctrl+V で可能</li>
	<li>コンソールが出てこない（ブラウザが黒いまま）の時、ブラウザの「更新」を試みる</li>
	<li>コンソールが乱れた時、ブラウザの「更新」か、新たにページを開いてみる</li>
	</ul>
HOWTO
}

### Hands-on Ref Output
sub handsref{

	my $hostaddr = shift;
	my $type = shift;
	my $wport = shift;
	my $hport = shift;
	my $tport = shift;
	my $endtime = shift;
	my $name = shift;
	my $wp = "http://$hostaddr:$wport/wordpress";
	my $hurl = "http://$hostaddr:$hport/wetty/ssh/root/";
	my $turl = "http://$hostaddr:$tport/wetty/ssh/root/";
	my $str = get_value($type);

print <<START;
        <h3>Informations of "$name"</h3>
        <p>
        <ul id="list">
        <li><a href="http://$hostaddr/$str->{'file'}" target="_blank">Hands-on Text - $str->{'name'} </a></li>
        <p>
        <li><a href="$hurl" target="_blank"><b>[ Ansible Host Console ]</b></a></li>
        <li><a href="$turl" target="_blank"><b>[ Ansible Target Console ]</b></a></li>
        <li><a href="$wp" target="_blank"><b>[ Top of WordPress page ]</b></a></li>
        <p>
        <li>Ending time : $endtime </li>
        </ul>
        <p>
START
}

### Create
sub create{

	my $id = shift;
	my $type = shift;
	my $bport = shift;
	my $htty = shift;
	my $ttty = shift;
	my $inventory = shift;
	my $playbook = shift;
	
	# Run Playbook
	system("ansible-playbook -i $inventory -e \"lesson=$type userid=$id port=$bport htty=$htty ttty=$ttty\" $playbook >& /dev/null &");
}

### Destroy
sub destroy{

	my $id = shift;
	my $inventory = shift;
	my $playbook = shift;
	my $type = "destroy";
	
	system("ansible-playbook -i $inventory -e \"lesson=$type userid=$id\" $playbook >& /dev/null &");
}

### Start Input
sub input_form{
        print "<h3>管理者用マニュアル登録</h3>";
        print "<form action=\"./$pathname/create.cgi\" method=\"post\"><p>";
        print "<h4>ユーザ入力</h4>\n";
	print "<ol style=\"list-style:none;\">\n";
	print "<li><input type=\"text\" name=\"name\" size=\"10\"></li>\n";
	print "</ol>\n";
        print "<h4>ハンズオンの種類を選択</h4>";
	print "<ol style=\"list-style:none;\">\n";
        print "<li><input type=\"radio\" name=\"type\" value=\"ansible-1\" checked><b><font color=\"blue\"> Ansible 初級ハンズオン</font></b></li>\n";
        print "<li><input type=\"radio\" name=\"type\" value=\"ansible-2\"><b><font color=\"blue\"> Ansible 中級ハンズオン</font></b></li>\n";
        print "<li><input type=\"radio\" name=\"type\" value=\"serverspec-1\"><b><font color=\"blue\"> Serverspec 初級ハンズオン</font></b></li>\n";
	print "</ol>\n";
        print "<input id=\"button\" type=\"submit\" value=\"ハンズオンビルド\">\n";
        print "</form>\n";
        print "<br>\n";
}

### User Table
sub userlist{
	my %data = @_;
	my $k;
	my $v;
	my $max_emp = get_value('max_emp');
	my @list;
	my $name;

	print "<h3>現在の利用状況</h3><br>";

	if(keys %data == 0){
		print "利用者がいません・・・<p>\n";
	}elsif(keys %data == $max_emp){
		print "現在<font color=\"red\">フル稼働</font>です。空きがでるまで少し時間をおいてください。\n";
		print "<table>\n";
		print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th></tr>\n";

		while (($k, $v) = each %data) {
			@list = split(/,/,$v);
			print "<tr>";
			print "<td><a href=\"./$pathname/myhandson.cgi?name=$k\">$k</a></td>";
			print "<td>$list[0]</td>";
			print "<td>$list[1]</td>";
			print "<td>$list[2]</td>";
			print "</tr>\n";
		}
		print "</table>\n";
	}else{
		print "<table>\n";
		print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th></tr>\n";

		while (($k, $v) = each %data) {
			@list = split(/,/,$v);
			my $lesson_name = get_value($list[0]);
			print "<tr>";
			print "<td><a href=\"./$pathname/myhandson.cgi?name=$k\">$k</a></td>";
			print "<td>$lesson_name->{lesson}</td>";
			print "<td>$list[1]</td>";
			print "<td>$list[2]</td>";
			print "</tr>\n";
		}
		print "</table>\n";
		print "</p>\n";
	}		
}

### Logging
sub logging{
	my @list = @_;

        open(W,">>$list[-1]");
	for($i=0; $i <= $#list-1; $i++){
		if($i == $#list-1){
			print W "$list[$i]\n";
		}else{
			print W "$list[$i],";
		}
	}
        close(W);

}

### Error Page
sub error_page{
	
	my $flag = shift;
	my $back_url = shift;
	my $input_msg = shift;
	my $msg;

	# Login Fail
	if($flag == '1'){
		$msg="<b>\"正しくユーザ入力\"</b>をしてください。<p>\n";
	}elsif($flag == '2'){
		$msg="<b>\"ハンズオンタイプ\"</b>を選択してください。<p>\n";
	}elsif($flag == '3'){
		$msg="<b>そのユーザのハンズオンは既に実行されています。</b><p>\n";
	}elsif($flag == '4'){
		$msg="<b>$input_msg</b><p>\n";
	}

	# Out Page
	print "Content-type: text/html\n\n";
	print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
	print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n";
	print "<html xmlns=\"html://www.w3.org/1999/xhtml\" xml:lang=\"ja\" lang=\"ja\">\n";
	print "<head>\n";
	print "<meta http-equiv=\"Content-Type\" content=\"application/xhtml+xml; charset=UTF-8\"/>\n";
	print "<title>Error Page</title>\n";
	print "</head>\n";
	print "<body>\n";
	print "<center>\n";
	print "<font color=\"red\"><b>Error:</b></font><br>\n";
	print "$msg";
	print "<a href=\"$back_url\">[ Back ]</a>\n";
	print "</body></html>\n";
}


# Get values form yaml file
sub get_value{

        my $para = shift;
        my $data= YAML::Tiny->new;
        $data = YAML::Tiny->read( "./host_vars/localhost" );
        my $yaml = $data->[0];

        return $yaml->{$para};
}

# Socket & Connect
sub check_http{

        my $ip = shift;
        my $port = shift;
        $remote = IO::Socket::INET->new( Proto => "tcp",
        PeerAddr => "$ip",
        PeerPort => "$port"
        );

        unless($remote){
                return (0);
        }
        $remote->autoflush(1);

        #print $remote "GET /wordpress/wp-admin/install.php \n\n";
        print $remote "HEAD /wordpress/wp-admin/install.php \n\n";

        $f=<$remote>;
        close $remote;

        if($f =~ /DOCTYPE\sHTML/){
                #print "HTTP OK\n";
                return (1)

        }else{
                return (0)
        }

}

sub uniq_func{
	my @src = @_;
	my %hash;

	@hash{@src} = ();
	return keys %hash;
}



1;

