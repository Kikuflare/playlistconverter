// Playlist Converter by Kiku

window.onload = function() {
    var fileInput = document.getElementById('fileInput');
    var fileDisplayArea = document.getElementById('fileDisplayArea');

    fileInput.addEventListener('change', function(e) {
		var file = fileInput.files[0];
		var textType = /text.*/;
		
		if (file.type.match()) {
			var reader = new FileReader();
			
			reader.onload = function(e) {
				fileDisplayArea.innerText = reader.result;
			}

			reader.readAsText(file);
		}
		else {
			fileDisplayArea.innerText = "File not supported!";
		}
    });
}

function convert(contents) {
	var fileInput = document.getElementById('fileInput');
	var fileDisplayArea = document.getElementById('fileDisplayArea');
	var playlistTitleInput = document.getElementById('playlistTitleInput');
	
	// Split on line break to get contents of file, but remove empty lines
	// Is there any way to ignore empty lines when reading the file?
	var contents = fileDisplayArea.innerText.split('\n');
	for (var index = contents.length; index--;) {
		if (contents[index] === "") {
			contents.splice(index, 1);
		}
	}
	
	var file = fileInput.files[0];
	
	if (file != null) {
		// Determine the new file name (can be changed by user when saving)
		var oldFileName = file.name;
		var newFileName = oldFileName;
		if (oldFileName.endsWith('.m3u8')) {
			newFileName = newFileName.substring(0, newFileName.length - 5);
		}
		newFileName = newFileName.concat('.wpl');
		
		// Determine the playlist title (displayed in WMP)
		var playlistTitle = playlistTitleInput.value;
		if (playlistTitle === "") {
			playlistTitle = newFileName.replace(/\.[^/.]+$/, "");
		}
		
		newFileContents = "";
		newFileContents = newFileContents + '<?wpl version="1.0"?>\n';
		newFileContents = newFileContents + '<smil>\n';
		newFileContents = newFileContents + '\t<head>\n';
		newFileContents = newFileContents + '\t\t<meta name="Generator" content="Microsoft Windows Media Player -- 12.0.7601.18840"/>\n';
		newFileContents = newFileContents + '\t\t<meta name="ItemCount" content="' + contents.length +'"/>\n';
		newFileContents = newFileContents + '\t\t<author/>\n';
		newFileContents = newFileContents + '\t\t<title>' + playlistTitle + '</title>\n';
		newFileContents = newFileContents + '\t</head>\n';
		newFileContents = newFileContents + '\t<body>\n';
		newFileContents = newFileContents + '\t\t<seq>\n';

		for (var i = 0; i < contents.length; i++) {
			var line = contents[i];
			line = line.trim();
			line = line.replace("&", "&amp;")
			line = line.replace("'", "&apos;")
			
			newFileContents = newFileContents + '\t\t\t<media src="' + line + '"/>\n';
		}
		
		newFileContents = newFileContents + '\t\t</seq>\n';
		newFileContents = newFileContents + '\t</body>\n';
		newFileContents = newFileContents + '</smil>\n';
		
		var element = document.createElement('a');
		element.setAttribute('href', 'data:text/plain;charset=utf-8-sig,' + encodeURIComponent(newFileContents));
		element.setAttribute('download', newFileName);

		element.style.display = 'none';
		document.body.appendChild(element);

		element.click();

		document.body.removeChild(element);
	}
	else {
		fileDisplayArea.innerText = "Please select a file!";
	}
}