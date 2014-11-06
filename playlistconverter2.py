import sys
import codecs
import os

def main():
    if len(sys.argv) < 2:
        print "Please supply a playlist in .m3u8 format."
    elif len(sys.argv) >= 3:
        print "Please supply only one argument, given: " + str(len(sys.argv))
    else:
        filename = sys.argv[1]
        new_file_name = os.path.splitext(filename)[0] + ".wpl"
        
        if (os.path.exists(new_file_name)):
            response = raw_input("File exists, overwrite? y/n\n")
            if response != "y":
                print "Aborted"
                sys.exit
            else:
                convert(new_file_name)
        else:
            convert(new_file_name)
        
def convert(new_file_name):
    filename = sys.argv[1]
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        # Get rid of the BOM if it is present
        if lines[0].startswith(codecs.BOM_UTF8):
            lines[0] = lines[0].replace(codecs.BOM_UTF8,'',1)
        
        with open(new_file_name, 'w') as new_file:
            new_file.write('<?wpl version="1.0"?>\n')
            new_file.write('<smil>\n')
            new_file.write('\t<head>\n')
            new_file.write('\t\t<meta name="Generator" content="Microsoft Windows Media Player -- 12.0.7601.18526"/>\n')
            new_file.write('\t\t<meta name="ItemCount" content="' + str(len(lines)) +'"/>\n')
            new_file.write('\t\t<author/>\n')
            new_file.write('\t\t<title>' + os.path.splitext(filename)[0] + '</title>\n')
            new_file.write('\t</head>\n')
            new_file.write('\t<body>\n')
            new_file.write('\t\t<seq>\n')
            
            for line in lines:
                line = line.rstrip('\n')
                line = line.replace("&", "&amp;")
                line = line.replace("'", "&apos;")
                
                new_file.write('\t\t\t<media src="' + line + '"/>\n')
                
            new_file.write('\t\t</seq>\n')
            new_file.write('\t</body>\n')
            new_file.write('</smil>\n')
            
        new_file.closed
                   
    f.closed

    print "Finished converting."

main()
