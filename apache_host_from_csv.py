#!/usr/bin/python3

from csv import DictReader

servername = 'my_virtualhost_name.com'
originaldomain = 'original_domain.com'
finaldestination = 'final_rule_address.com'

# Input is a CSV file with columns 'doi' (original address), then three destination based on three variables of 'doi'
inputfile = DictReader(open('art-url-pubhelp-6032-2016-02-01.csv'))
resultsfile = open('backfile_rules.txt', 'w')

#two column CSV file with source and destination to provide users with a readable spreadsheet
readableoutput = open('backfile_list.csv', 'w')

#list of URLs with missing/empty fields to follow up on with the user
wonkylinks = open('wonky_links.csv', 'w')

# wrap up the rules in a complete Apache2 virtualhost file
firstline1 = '<VirtualHost *:80>\n'
firstline2 = '  ServerName     %s\n' % servername
firstline3 = '  RewriteEngine  on\n\n'

# End the rules with a catch-all
lastline1 = '\n  RewriteRule    ^/(.*) %s/?  [L,R=301]\n\n' % finaldestination
lastline2 = '  ErrorLog       /var/log/apache2/sj-prd-error.log\n'
lastline3 = '  CustomLog      /var/log/apache2/sj-prd-access.log combined\n'
lastline4 = '</VirtualHost>'

resultsfile.writelines([firstline1, firstline2, firstline3])

wonkylinks.write('These point to URLs containing "///"' + '\n' + '\n')

for line in inputfile:
    if '///' not in line['abstract-view']:
        # Create rules, drop query strings, permanent redirect, [L]ast rule to check
        resultsfile.write('  RewriteRule ' + '^/doi/abs/' + line['doi'] + ' ' + line['abstract-view'] + '?' +  ' [R=301,L]' + '\n')
        resultsfile.write('  RewriteRule ' + '^/doi/pdf/' + line['doi'] + ' ' + line['pdf-view'] + '?' +  ' [R=301,L]' + '\n')
        resultsfile.write('  RewriteRule ' + '^/doi/ref/' + line['doi'] + ' ' + line['references'] + '?' + ' [R=301,L]' + '\n')
        
        # User-readable list of rules by source, destination
        readableoutput.write(originaldomain + '/doi/abs/' + line['doi'] + ',' + line['abstract-view'] + '\n')
        readableoutput.write(originaldomain + '/doi/pdf/' + line['doi'] + ',' + line['pdf-view'] + '\n')
        readableoutput.write(originaldomain + '/doi/ref/' + line['doi'] + ',' + line['references'] + '\n')
    
    # Missing fields result in '///' in input file.  List these out by source, destination
    if '///' in line['abstract-view']:
        wonkylinks.write(line['doi'] + ',' + line['abstract-view'] + ',' + line['references'] + ',' + line['pdf-view'] + '\n')

# Append the final bit of the virtualhost
resultsfile.writelines([lastline1, lastline2, lastline3, lastline4])
        
resultsfile.close()
readableoutput.close()
wonkylinks.close()
