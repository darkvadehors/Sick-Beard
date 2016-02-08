$(document).ready(function(){
    var loading = '<img src="'+sbRoot+'/images/loading16.gif" height="16" width="16" />';
    
	function toggle_torrent_title(){
		if ($('#use_torrents').prop('checked'))
			$('#no-torrents').show();
		else
			$('#no-torrents').hide();
	}
	
    $.fn.nzb_method_handler = function() {
        
        var selectedProvider = $('#nzb_method :selected').val();

        if (selectedProvider == "blackhole") {
            $('#blackhole_settings').show();
            $('#sabnzbd_settings').hide();
            $('#testSABnzbd').hide();
            $('#testSABnzbd-result').hide();
            $('#nzbget_settings').hide();
            $('#t_blackhole_submit').show();
            
        } else if (selectedProvider == "nzbget") {
            $('#blackhole_settings').hide();
            $('#sabnzbd_settings').hide();
            $('#testSABnzbd').hide();
            $('#testSABnzbd-result').hide();
            $('#nzbget_settings').show();
        } else {
            $('#blackhole_settings').hide();
            $('#sabnzbd_settings').show();
            $('#testSABnzbd').show();
            $('#testSABnzbd-result').show();
            $('#nzbget_settings').hide();
        }

    }

    $.fn.torrent_method_handler = function() {
        
        var selectedProvider = $('#torrent_method :selected').val();
		
        if (selectedProvider == "blackhole") {
            $('#t_blackhole_settings').show();
            $('#torrent_settings').hide();
            $('#ftp_blackhole_settings').hide();
            $('#desc_torrent_dir').text('Fichier .TORRENT');
        } else if (selectedProvider == "utorrent") {
            $('#t_blackhole_settings').hide();
            $('#torrent_settings').show();
            $('#Torrent_username').show()
            $('#Torrent_custom_url').hide();
            $('#Torrent_Path').hide();
            $('#Torrent_Ratio').hide();
            $('#Torrent_Label').show()
            $('#host_desc').text('Hôte de uTorrent');
            $('#username_desc').text("Nom d'utilisateur uTorrent");
            $('#password_desc').text('Mot de Passe uTorrent');
            $('#ftp_blackhole_settings').hide();
            $('#label_desc').text('Label pour uTorrent');
        } else if (selectedProvider == "transmission"){
            $('#t_blackhole_settings').hide();
            $('#torrent_settings').show();
            $('#Torrent_username').show();
            $('#Torrent_Path').show();
            $('#Torrent_custom_url').show();
            $('#Torrent_Ratio').show();
            $('#Torrent_Label').hide();
            $('#host_desc').html('Hôte de Transmission');
            $('#username_desc').text("Nom d'utilisateur Transmission");
            $('#password_desc').text('Mot de Passe Transmission');
            $('#directory_desc').text('Dossier de Sauvegarde de Transmission');
            $('#ftp_blackhole_settings').hide();
        } else if (selectedProvider == "deluge"){
            $('#t_blackhole_settings').hide();
            $('#torrent_settings').show();
            $('#Torrent_Label').show();            
            $('#Torrent_username').hide();
            $('#Torrent_custom_url').hide();
            $('#Torrent_Path').show();
            $('#Torrent_Ratio').show();
            $('#host_desc').text('Hôte de Deluge');
            $('#username_desc').text("Nom d'utilisateur Deluge");
            $('#password_desc').text('Mot de Passe de Deluge');
            $('#label_desc').text('Label pour Deluge');
            $('#directory_desc').text('Dossier de Sauvegarde de Deluge');
            $('#ftp_blackhole_settings').hide();
        } else if (selectedProvider == "download_station"){
            $('#t_blackhole_settings').hide();
            $('#torrent_settings').show();
            $('#Torrent_Label').hide();            
            $('#Torrent_username').show();
            $('#Torrent_custom_url').hide();
            $('#Torrent_Paused').hide();
            $('#Torrent_Path').hide();
            $('#Torrent_Ratio').hide();
            $('#Torrent_High_Bandwidth').hide();
            $('#host_desc').text('Hôte de Synology');
            $('#username_desc').text("Nom d'utilisateur Synology");
            $('#password_desc').text('Mot de Passe Synology');
            $('#label_desc').text('Label pour Synology');
            $('#directory_desc').text('Dossier de Sauvegarde de Synology');
            $('#ftp_blackhole_settings').hide();
        } else if (selectedProvider == "ftpblackhole"){
            $('#t_blackhole_settings').show();
            $('#torrent_settings').hide();
            $('#ftp_blackhole_settings').show();
            $('#desc_torrent_dir').text('Dossier de Sauvegarde FTP');
            $('#t_blackhole_submit').hide();
        }
    }

    $('#nzb_method').change($(this).nzb_method_handler);

    $(this).nzb_method_handler();

    $('#testSABnzbd').click(function(){
        $('#testSABnzbd-result').html(loading);
        var sab_host = $('#sab_host').val();
        var sab_username = $('#sab_username').val();
        var sab_password = $('#sab_password').val();
        var sab_apiKey = $('#sab_apikey').val();
        
        $.get(sbRoot+"/home/testSABnzbd", {'host': sab_host, 'username': sab_username, 'password': sab_password, 'apikey': sab_apiKey}, 
        function (data){ $('#testSABnzbd-result').html(data); });
    });
    

    $('#torrent_method').change($(this).torrent_method_handler);
	
	$(this).torrent_method_handler();
    
    $('#use_torrents').click(function(){
    	toggle_torrent_title();
    });

    $('#testTorrent').click(function(){
        $('#testTorrent-result').html(loading);
        var torrent_method = $('#torrent_method :selected').val();
        var torrent_host = $('#torrent_host').val();
        var torrent_username = $('#torrent_username').val();
        var torrent_password = $('#torrent_password').val();

        $.get(sbRoot+"/home/testTorrent", {'torrent_method': torrent_method, 'host': torrent_host, 'username': torrent_username, 'password': torrent_password},
        function (data){ $('#testTorrent-result').html(data); });
    });
    $('#prefered_method').change($(this).prefered_method_handler);
	
	$(this).prefered_method_handler();

});
