#!/usr/bin/env perl

##############################################################################
#                                                                            #
# CasjaysDev.com FormMail                Version 1.01                                     #
#                                                                            #
# Copyright 1998 Network Now       info@networknow.net                       #
# Network Now             http://www.networknow.net                          #
# Created 11/11/98                                                            #
#                                                                            #
# Modifications Copyright (c) 1998 Network Now, All Rights Reserved.         #
# This version of FormMail may be used and modified free of charge by anyone #
# so long as this copyright notice and the one below by Matthew Wright and   #
# Brian Sietz remain intact. By using this code you agree to indemnify       # 
# Network Now from any liability arising from it's use. You also agree that  #
# this code cannot be sold to any third party without prior written consent  #
# of both Network Now, Brian Sietz and Matthew M. Wright.		     #
#                                                                            #
##############################################################################
# BFormMail                        Version 1.3a                              #
#                                                                            #
# Copyright 1997 Brian Sietz       bsietz@infosheet.com                      #
# The InfoSheet Place              http://www.infosheet.com                  #
# Created 8/14/97                                                            #
#                                                                            #
# Modifications Copyright (c) 1997,1998 Brian S. Sietz, All Rights Reserved. #
# This version of FormMail may be used and modified free of charge by anyone #
# so long as this copyright notice and the one below by Matthew Wright remain#
# intact. By using this code you agree to indemnify Brian Sietz from any     #
# liability arising from it's use. You also agree that this code cannot be   #
# sold to any third party without prior written consent of both Brian Sietz  #
# and Matthew M. Wright.						     #
#                                                                            #
# BFormMail is a universal WWW form to E-mail gateway based on Matt Wright's #
# FormMail Version 1.6.                                                      #
#                                                                            #
##############################################################################
# FormMail                        Version 1.6                                #
# Copyright 1995-1997 Matt Wright mattw@worldwidemart.com                    #
# Created 06/09/95                Last Modified 05/02/97                     #
# Matt's Script Archive, Inc.:    http://www.worldwidemart.com/scripts/      #
##############################################################################
# COPYRIGHT NOTICE                                                           #
# Copyright 1995-1997 Matthew M. Wright  All Rights Reserved.                #
#                                                                            #
# FormMail may be used and modified free of charge by anyone so long as this #
# copyright notice and the comments above remain intact.  By using this      #
# code you agree to indemnify Matthew M. Wright from any liability that      #
# might arise from its use.                                                  #
#                                                                            #
# Selling the code for this program without prior written consent is         #
# expressly forbidden.  In other words, please ask first before you try and  #
# make money off of my program.                                              #
#                                                                            #
# Obtain permission before redistributing this software over the Internet or #
# in any other medium.	In all cases copyright and header must remain intact #
#                                                                            #
#                                                                            #
##############################################################################
#                                                                            #
#                                                                            #
# CasjaysDev.com FormMail                                                                 #
#                                                                            #
#      Took Brian's Script (who took Matt's script) and made modifications   #
# to it to suit my needs.  I am not a perl programmer but I know how to make #
# things work the way I want them to.  I liked what Brian had done the best  #
# of all the FormMail modifications so I started with his script.  In a nut  #
# shell I added the ability to use FormMail as a GoldMine web import script  #
# as well as a regular full featured form mail processor.                    #
#									     #
# Some of the things I've done with this script:                             #
#                                                                            #
#      1. Improved,in my opinion the generic html output.                    #
#      2. Fixed a bug in the print_missing_fields option so now that works.  #
#      3. Added an exclude option so that form fields can be excluded from   #
#         the courtesy email that is sent to user.                           #
#      4. Removed Brian's fax service stuff.                                 #
#      5. Added the GoldMine webimport option.                               #
#                                                                            #
#          The GoldMine option allows importing of:                          #
#                                                                            #
#          All primary contact information.                                  #
#          One secondary contact.                                            #
#          10 Userdefined fields                                             #
#          10 Custom defined fields                                          #
#          10 Profiles along with all secondary profile data                 #
#          Assignment of 3 Tracks                                            #
#          Email address profile                                             #
#          Internet address profile                                          #
#                                                                            #
#  Of course along with using the GoldMine import option you can send a      #
#  courtesy reply to the user and you can write the data to a database.      #
#                                                                            #
#                                                                            #


$cfh = select (STDOUT); 
          $| = 1; 
          select ($cfh); 

# Define Variables                                                           #
#	 Detailed Information Found In README File.                          #

# $mailprog defines the location of your sendmail program on your unix       #
# system.                                                                    #

$mailprog = '/usr/lib/sendmail';

# @referers allows forms to be located only on servers which are defined     #
# in this field.  This security fix from the last version which allowed      #
# anyone on any server to use your FormMail script on their web site.        #

#@referers = ('yourdomain.com','www.yourdomain.com');


##############################################################################


# Check Referring URL
#&check_url;

# Retrieve Date
&get_date;

# Parse Form Contents
&parse_form;

# Check Required Fields
&check_required;

# Send GoldMine Web Import Email
if ($Config{'goldmine'}) {
    &send_GMmail ;}
else {&send_mail;}

# Courtesy E-Mail to Visitor
&send_courtesy;

# Return HTML Page or Redirect User
&return_html;


# Main ends here - only subroutines follow                                   #
##############################################################################

sub check_url {
#
#    # Localize the check_referer flag which determines if user is valid.     #
#    local($check_referer) = 0;
#
#    # If a referring URL was specified, for each valid referer, make sure    #
#    # that a valid referring URL was passed to FormMail.                     #
#
#    if ($ENV{'HTTP_REFERER'}) {
#        foreach $referer (@referers) {
#            if ($ENV{'HTTP_REFERER'} =~ m|https?://([^/]*)$referer|i) {
#                $check_referer = 1;
#                last;
#            }
#        }
#    }
#    else {
#        $check_referer = 1;
#    }
#
#    # If the HTTP_REFERER was invalid, send back an error.                   #
#    if ($check_referer != 1) { &error('bad_referer') }
}

sub get_date {

    # Define arrays for the day of the week and month of the year.           #
    @days   = ('Sunday','Monday','Tuesday','Wednesday',
               'Thursday','Friday','Saturday');
    @months = ('January','February','March','April','May','June','July',
	         'August','September','October','November','December');

    # Get the current time and format the hour, minutes and seconds.  Add    #
    # 1900 to the year to get the full 4 digit year.                         #
    ($sec,$min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[0,1,2,3,4,5,6];
    $time = sprintf("%02d:%02d:%02d",$hour,$min,$sec);
    $year += 1900;

    # Format the date.                                                       
    $date = "$days[$wday], $months[$mon] $mday, $year at $time";
    $mon2 = $mon + 1;
    $date2 = "$mon2/$mday/$year";
}

sub parse_form {

    # Define the configuration associative array.                            
    %Config = ('recipient','',          'subject','',
               'sendboth','',           'exclude','',
               'redirect','',           'bgcolor','',
               'background','',         'link_color','',
               'vlink_color','',        'text_color','',
               'alink_color','',        'title','',
               'sort','',               'print_config','',
               'required','',           'env_report','',
               'return_link_title','',  'return_link_url','',
               'print_blank_fields','', 'missing_fields_redirect','',

               'cc','',	                'bcc','',
	       'courtesy_reply','',
	       'courtesy_our_url','',   'courtesy_our_email','',
	       'courtesy_reply_texta','',
	       'courtesy_reply_textb','',
	       'courtesy_who_we_are','','courtesy_who_we_are2','',

	       'append_db','',          'db_delimiter','',
	       'db_fields','',
	       
	        'goldmine','',
	        'DupNotify','',		'NewNotify','',
		'Track1','',		'Track2','',
		'Track3','',		'CustomFieldName01','',
		'CustomFieldName02','',	'CustomFieldName03','',
		'CustomFieldName04','',	'CustomFieldName05','',
		'CustomFieldName06','',	'CustomFieldName07','',
		'CustomFieldName08','',	'CustomFieldName09','',
		'CustomFieldName10','',	'ProfDesc01','',
		'ProfDesc02','',	'ProfDesc03','',
		'ProfDesc04','',	'ProfDesc05','',
		'ProfDesc06','',	'ProfDesc07','',
		'ProfDesc08','',	'ProfDesc09','',
		'ProfDesc10',''
	   );

    # Determine the form's REQUEST_METHOD (GET or POST) and split the form   #
    # fields up into their name-value pairs.  If the REQUEST_METHOD was      #
    # not GET or POST, send an error.                                        #
    if ($ENV{'REQUEST_METHOD'} eq 'GET') {
        # Split the name-value pairs
        @pairs = split(/&/, $ENV{'QUERY_STRING'});
    }
    elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
        # Get the input
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
 
        # Split the name-value pairs
        @pairs = split(/&/, $buffer);
    }
    else {
        &error('request_method');
    }

    # For each name-value pair:                                              #
    foreach $pair (@pairs) {

        # Split the pair up into individual variables.                       #
        ($name, $value) = split(/=/, $pair);
 
        # Decode the form encoding on the name and value variables.          #
        $name =~ tr/+/ /;
        $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        # If they try to include server side includes, erase them, so they
        # aren't a security risk if the html gets returned.  Another 
        # security hole plugged up.
        $value =~ s/<!--(.|\n)*-->//g;

        # If the field name has been specified in the %Config array, it will #
        # return a 1 for defined($Config{$name}}) and we should associate    #
        # this value with the appropriate configuration variable.  If this   #
        # is not a configuration form field, put it into the associative     #
        # array %Form, appending the value with a ', ' if there is already a #
        # value present.  We also save the order of the form fields in the   #
        # @Field_Order array so we can use this order for the generic sort.  #
        if (defined($Config{$name})) {
            $Config{$name} = $value;
        }
        else {
            if ($Form{$name} && ($value)) {
                $Form{$name} = "$Form{$name}, $value";
            }

##########Fix by JJ Steward,To print blank fields 8/25/98############
            else {
##########was:   elsif ($value) { ##############

                push(@Field_Order,$name);
                $Form{$name} = $value;
            }
        }
    }

    # The next six lines remove any extra spaces or new lines from the       #
    # configuration variables, which may have been caused if your editor     #
    # wraps lines after a certain length or if you used spaces between field #
    # names or environment variables.                                        #
    $Config{'exclude'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'exclude'} =~ s/(\s+)?\n+(\s+)?//g;
    $Config{'required'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'required'} =~ s/(\s+)?\n+(\s+)?//g;
    $Config{'env_report'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'env_report'} =~ s/(\s+)?\n+(\s+)?//g;
    $Config{'print_config'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'print_config'} =~ s/(\s+)?\n+(\s+)?//g;
    $Config{'db_fields'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'db_fields'} =~ s/(\s+)?\n+(\s+)?//g;

    # Split the configuration variables into individual field names.         #
    @Exclude = split(/,/,$Config{'exclude'});
    @Required = split(/,/,$Config{'required'});
    @Env_Report = split(/,/,$Config{'env_report'});
    @Print_Config = split(/,/,$Config{'print_config'});
    @Print_DB = split(/,/,"$Config{'db_fields'},$Form{'db_fields'}");

}

sub check_required {

    # Localize the variables used in this subroutine.                        #
    local($require, @error);

    if (!$Config{'recipient'}) {
        if (!defined(%Form)) { &error('bad_referer') }
        else                 { &error('no_recipient') }
    }

    # For each require field defined in the form:                            #
    foreach $require (@Required) {

        # If the required field is the email field, the syntax of the email  #
        # address if checked to make sure it passes a valid syntax.          #
        if ($require eq 'Email' && !&check_email($Form{$require})) {
            push(@error,$require);
        }

        # Otherwise, if the required field is a configuration field and it   #
        # has no value or has been filled in with a space, send an error.    #
        elsif (defined($Config{$require})) {
            if (!$Config{$require}) {
                push(@error,$require);
            }
        }

        # If it is a regular form field which has not been filled in or      #
        # filled in with a space, flag it as an error field.                 #
        elsif (!$Form{$require}) {
            push(@error,$require);
        }
    }

    # If any error fields have been found, send error message to the user.   #
    if (@error) { &error('missing_fields', @error) }
}




sub return_html {
    # Local variables used in this subroutine initialized.                   #
    local($key,$sort_order,$sorted_field);

    # If redirect option is used, print the redirectional location header.   #
    if ($Config{'redirect'}) {
        print "Location: $Config{'redirect'}\n\n";
    }

    # Otherwise, begin printing the response page.                           #
    else {

        # Print HTTP header and opening HTML tags.                           #
        print "Content-type: text/html\n\n";
        print "<html>\n <head>\n";

        # Print out title of page                                            #
        if ($Config{'title'}) { print "  <title>$Config{'title'}</title>\n" }
        else                  { print "  <title>Thank You</title>\n"        }

        print " </head>\n <body";

        # Get Body Tag Attributes                                            #
        &body_attributes;

        # Close Body Tag                                                     #
        print ">\n  <center>\n";

        # Print custom or generic title.
        
        
        print "<BR><table  border=1 cellpadding=0 cellspacing=0 width=650><tr><td>\n";
        print "<table   border=0 cellpadding=5 cellspacing=0 width=650>\n";
        print "<tr><td colspan=3  align=center bgcolor=#333366>\n";
        print "<font face=arial size=+2 color=#FFFFFF><b>\n";
        
        if ($Config{'title'}) { print "$Config{'title'}\n" }
        else { print "Thank You For Filling Out This Form\n" }
        
        print "</b></td></tr><tr>\n";
        print "<td colspan=3 align=center bgcolor=#D0D0D0><font face=arial>\n";                                   #
        print "$date\n";
        print "</td></tr><tr><td colspan=3 align=center><font face=arial></td></tr>\n";
        print "<tr><td colspan=3><BR></td></tr>\n";
        
        

         
        if ($Form{'Email'}) {
            print "<tr><td align=right><font face=arial><b>E-mail:</b></td>\n";
	    print "<td align=left><font face=arial>$Form{'Email'}</td><td width=100></td></tr>\n";
        }


        # Sort alphabetically if specified:                                  #
        if ($Config{'sort'} eq 'alphabetic') {
            foreach $field (sort keys %Form) {

                # If the field has a value or the print blank fields option  #
                # is turned on, print out the form field and value.          #
                if ($Config{'print_blank_fields'} || $Form{$field}) {
 
                    print "<tr><td align=right><font face=arial><b>$field:</b></td>\n";
		    print "<td align=left><font face=arial>$Form{$field}</td><td width=100></td></tr>\n";

                }
            }
        }

        # If a sort order is specified, sort the form fields based on that.  #
        elsif ($Config{'sort'} =~ /^order:.*,.*/) {

            # Set the temporary $sort_order variable to the sorting order,   #
            # remove extraneous line breaks and spaces, remove the order:    #
            # directive and split the sort fields into an array.             #
            $sort_order = $Config{'sort'};
            $sort_order =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
            $sort_order =~ s/(\s+)?\n+(\s+)?//g;
            $sort_order =~ s/order://;
            @sorted_fields = split(/,/, $sort_order);

            # For each sorted field, if it has a value or the print blank    #
            # fields option is turned on print the form field and value.     #
            foreach $sorted_field (@sorted_fields) {
                if ($Config{'print_blank_fields'} || $Form{$sorted_field}) {
 
                    print "<tr><td align=right><font face=arial><b>$sorted_field:</b></td>\n";
		    print "<td align=left><font face=arial>$Form{$sorted_field}</td><td width=100></td></tr>\n";

                }
            }
        }

        # Otherwise, default to the order in which the fields were sent.     #
        else {

            # For each form field, if it has a value or the print blank      #
            # fields option is turned on print the form field and value.     #
            foreach $field (@Field_Order) {
                if ($Config{'print_blank_fields'} || $Form{$field}) {

                    print "<tr><td align=right><font face=arial><b>$field:</b></td>\n";
		    print "<td align=left><font face=arial>$Form{$field}</td><td width=100></td></tr>\n";

                }
            }
        }

 print "<tr><td colspan=3><BR></td></tr><tr>\n";
 print "<td colspan=3 align=center bgcolor=#D0D0D0>
 <font face=arial>Please direct all inquiries to <a href=\"mailto:$Config{'recipient'}\">$Config{'recipient'}</a></td></tr>\n";
if ($Config{'return_link_url'} && $Config{'return_link_title'}) {
print "<td colspan=3 align=center bgcolor=#D0D0D0><font face=arial><a href=\"$Config{'return_link_url'}\">$Config{'return_link_title'}</a></td></tr>\n";
}
print "<td colspan=3 align=center bgcolor=#C0C0C0><font face=arial size=-2><a href=\"javascript: history.go(-1)\"></a></td></tr>\n";
print "<td colspan=3 align=center bgcolor=#C0C0C0><font face=arial size=-2><a href=\"http://casjaysdev.com/\">CasjaysDev</a></td></tr>\n";
 print "</table></td></tr></table>\n";
 print "<br clear=all></center>\n";


        # Print the page footer.                                             #
        print <<"(END HTML FOOTER)";
        </body>
       </html>
(END HTML FOOTER)
    }
}

sub send_mail {
    # Localize variables used in this subroutine.                            #



    local($print_config,$key,$sort_order,$sorted_field,$env_report,$print_db,$field);
   undef %is_exclude;
for (@Exclude) { $is_exclude{$_} = 1 }  
    # Open The Mail Program
    open(MAIL,"|$mailprog -t");

 
        print MAIL "To: $Config{'recipient'}\n";
        print MAIL "From: $Form{'Email'} ($Form{'Name'})\n";
	if ($Config{'cc'} && check_email($Config{'cc'}))
        	{ print MAIL "Cc: $Config{'cc'}\n" };
        if ($Config{'bcc'} && check_email($Config{'bcc'}))
		{ print MAIL "Bcc: $Config{'bcc'}\n" };


    # Check for Message Subject
    if ($Config{'subject'}) { print MAIL "Subject: $Config{'subject'}\n\n" }
    else                    { print MAIL "Subject: WWW Form Submission\n\n" }

    print MAIL "Form submitted by:\n";
    print MAIL "$Form{'Name'} ($Form{'Email'}) on $date\n";


    print MAIL "-" x 75 . "\n\n";

    
   


    # Sort alphabetically if specified:                                      #
    if ($Config{'sort'} eq 'alphabetic') {
        foreach $field (sort keys %Form) {

            # If the field has a value or the print blank fields option      #
            # is turned on, print out the form field and value.              #
            if ($Config{'print_blank_fields'} || $Form{$field} ||
                $Form{$field} eq '0') {
                print MAIL "$field: $Form{$field}\n"  unless $is_exclude{$field};
            }
        }
    }

    # If a sort order is specified, sort the form fields based on that.      #
    elsif ($Config{'sort'} =~ /^order:.*,.*/) {

        # Remove extraneous line breaks and spaces, remove the order:        #
        # directive and split the sort fields into an array.                 #
        $Config{'sort'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
        $Config{'sort'} =~ s/(\s+)?\n+(\s+)?//g;
        $Config{'sort'} =~ s/order://;
        @sorted_fields = split(/,/, $Config{'sort'});

        # For each sorted field, if it has a value or the print blank        #
        # fields option is turned on print the form field and value.         #
        foreach $sorted_field (@sorted_fields) {
            if ($Config{'print_blank_fields'} || $Form{$sorted_field} ||
                $Form{$sorted_field} eq '0') {
                print MAIL "$sorted_field: $Form{$sorted_field}\n"  unless $is_exclude{$field};
            }
        }
    }

    # Otherwise, default to the order in which the fields were sent.         #
    else {

        # For each form field, if it has a value or the print blank          #
        # fields option is turned on print the form field and value.         #
        foreach $field (@Field_Order) {
            if ($Config{'print_blank_fields'} || $Form{$field} ||
                $Form{$field} eq '0') {
                print MAIL "$field: $Form{$field}\n"  unless $is_exclude{$field};
            }
        }
    }

    print MAIL "-" x 75 . "\n\n";

    # Send any specified Environment Variables to recipient.                 #
    foreach $env_report (@Env_Report) {
        if ($ENV{$env_report}) {
            print MAIL "$env_report: $ENV{$env_report}\n";
        }
    }


  if ($Config{'append_db'})
  {
    if (-w $Config{'append_db'})
    {

        &lockit ("$Config{'append_db'}.lock");

	open (DATABASE, ">>$Config{'append_db'}");
	print DATABASE "$Config{'db_delimiter'}";
	print DATABASE "$date2$Config{'db_delimiter'}";
        print DATABASE "$time$Config{'db_delimiter'}";

        if ($Config{'db_fields'})
        {
        foreach $print_db (@Print_DB) {
            if ($Config{$print_db}) {
	        $field = $Config{$print_db};
		$field =~ s/\r\n/ /gs;
	        print DATABASE "$field";
	    }
	    if ($Form{$print_db}) {
	        $field = $Form{$print_db};
		$field =~ s/\r\n/ /gs;
	        print DATABASE "$field";
	    }
	   print DATABASE "$Config{'db_delimiter'}";
           }

          }

        else {

          foreach $field (@Field_Order) {
	        print DATABASE "$Form{$field}";
	        print DATABASE "$Config{'db_delimiter'}";
             }



        }

        print DATABASE "\n"; 
    close (DATABASE);

    &unlockit ("$Config{'append_db'}.lock");

   }
 }

    close (MAIL);
}


sub send_GMmail {
    # Localize variables used in this subroutine.                            #
    local($print_config,$key,$sort_order,$sorted_field,$env_report);

    # Open The Mail Program
    open(MAIL,"|$mailprog -t");

    print MAIL "To: $Config{'recipient'}\n";
    print MAIL "From: $Form{'Email'}\n";
    print MAIL "Content-Type: application/x-gm-impdata\n";


    # Check for Message Subject
    if ($Config{'subject'}) { print MAIL "Subject: $Config{'subject'}\n\n" }
    else                    { print MAIL "Subject: WWW Form Submission\n\n" }


    print MAIL "[Instructions]\n";
    print MAIL "SaveThis=$Config{'subject'}\n";
    print MAIL "DupCheck1=Contact\n";                                   
    print MAIL "DupCheck2=Phone1\n"; 
    if ($Config{'DupNotify'}) { print MAIL "OnDupSendEmail=$Config{'DupNotify'},DUP,$Form{'Contact'} Duplicate Web Contact!\n" }				 
    if ($Config{'NewNotify'}) { print MAIL "OnNewSendEmail=$Config{'NewNotify'},NEW,$Form{'Contact'} New Web Contact!\n" }				 
    if ($Config{'Track1'}) { print MAIL "OnNewAttachTrack1=$Config{'Track1'}\n" }				 
    if ($Config{'Track1'}) { print MAIL "OnDupAttachTrack1=$Config{'Track1'}\n" }				 
    if ($Config{'Track2'}) { print MAIL "OnNewAttachTrack2=$Config{'Track2'}\n" }				 
    if ($Config{'Track2'}) { print MAIL "OnDupAttachTrack2=$Config{'Track2'}\n" }				 
    if ($Config{'Track3'}) { print MAIL "OnNewAttachTrack3=$Config{'Track3'}\n" }				 
    if ($Config{'Track3'}) { print MAIL "OnDupAttachTrack3=$Config{'Track3'}\n" }				 
    print MAIL "\n";                                                    
    print MAIL "[Data]\n";
  
   if ($Form{'Company'}) { print MAIL "Company=$Form{'Company'}\n" }	
   if ($Form{'Name'}) { print MAIL "Contact=$Form{'Name'}\n" }
   if ($Form{'Address1'}) { print MAIL "Address1=$Form{'Address1'}\n" }
   if ($Form{'Address2'}) { print MAIL "Address2=$Form{'Address2'}\n" }
   if ($Form{'City'}) { print MAIL "City=$Form{'City'}\n" }
   if ($Form{'State'}) { print MAIL "State=$Form{'State'}\n" }
   if ($Form{'Zip'}) { print MAIL "Zip=$Form{'Zip'}\n" }
   if ($Form{'Country'}) { print MAIL "Country=$Form{'Country'}\n" }
   if ($Form{'Phone1'}) { print MAIL "Phone1=$Form{'Phone1'}\n" }
   if ($Form{'Phone2'}) { print MAIL "Phone2=$Form{'Phone2'}\n" }
   if ($Form{'Phone3'}) { print MAIL "Phone3=$Form{'Phone3'}\n" }
   if ($Form{'Fax'}) { print MAIL "Fax=$Form{'Fax'}\n" }
   if ($Form{'Ext1'}) { print MAIL "Ext1=$Form{'Ext1'}\n" }
   if ($Form{'Ext2'}) { print MAIL "Ext2=$Form{'Ext2'}\n" }
   if ($Form{'Ext3'}) { print MAIL "Ext3=$Form{'Ext3'}\n" }
   if ($Form{'Ext4'}) { print MAIL "Ext4=$Form{'Ext4'}\n" }
   if ($Form{'Dear'}) { print MAIL "Dear=$Form{'Dear'}\n" }
   if ($Form{'Title'}) { print MAIL "Title=$Form{'Title'}\n" }
   if ($Form{'Department'}) { print MAIL "Department=$Form{'Department'}\n" }
   if ($Form{'Source'}) { print MAIL "Source=$Form{'Source'}\n" }
   if ($Form{'Assistant'}) { print MAIL "Secr=$Form{'Assistant'}\n" }
   if ($Form{'Key1'}) { print MAIL "Key1=$Form{'Key1'}\n" }
   if ($Form{'Key2'}) { print MAIL "Key2=$Form{'Key2'}\n" }
   if ($Form{'Key3'}) { print MAIL "Key3=$Form{'Key3'}\n" }
   if ($Form{'Key4'}) { print MAIL "Key4=$Form{'Key4'}\n" }
   if ($Form{'Key5'}) { print MAIL "Key5=$Form{'Key5'}\n" }
   if ($Config{'USERDEF01'}) { print MAIL "USERDEF01=$Config{'USERDEF01'}\n" }
   if ($Config{'USERDEF02'}) { print MAIL "USERDEF02=$Config{'USERDEF02'}\n" }
   if ($Config{'USERDEF03'}) { print MAIL "USERDEF03=$Config{'USERDEF03'}\n" }
   if ($Config{'USERDEF04'}) { print MAIL "USERDEF04=$Config{'USERDEF04'}\n" }
   if ($Config{'USERDEF05'}) { print MAIL "USERDEF05=$Config{'USERDEF05'}\n" }
   if ($Config{'USERDEF06'}) { print MAIL "USERDEF06=$Config{'USERDEF06'}\n" }
   if ($Config{'USERDEF07'}) { print MAIL "USERDEF07=$Config{'USERDEF07'}\n" }
   if ($Config{'USERDEF08'}) { print MAIL "USERDEF08=$Config{'USERDEF08'}\n" }
   if ($Config{'USERDEF09'}) { print MAIL "USERDEF09=$Config{'USERDEF09'}\n" }
   if ($Config{'USERDEF10'}) { print MAIL "USERDEF10=$Config{'USERDEF10'}\n" }
   if ($Form{'Notes'}) { print MAIL "Notes=$Form{'Notes'}\n" }
   if ($Form{'CustomField01'}){ print MAIL "$Config{'CustomFieldName01'}=$Form{'CustomField01'}\n" }
   if ($Form{'CustomField02'}){ print MAIL "$Config{'CustomFieldName02'}=$Form{'CustomField02'}\n" }
   if ($Form{'CustomField03'}){ print MAIL "$Config{'CustomFieldName03'}=$Form{'CustomField03'}\n" }
   if ($Form{'CustomField04'}){ print MAIL "$Config{'CustomFieldName04'}=$Form{'CustomField04'}\n" }
   if ($Form{'CustomField05'}){ print MAIL "$Config{'CustomFieldName05'}=$Form{'CustomField05'}\n" }
   if ($Form{'CustomField06'}){ print MAIL "$Config{'CustomFieldName06'}=$Form{'CustomField06'}\n" }
   if ($Form{'CustomField07'}){ print MAIL "$Config{'CustomFieldName07'}=$Form{'CustomField07'}\n" }
   if ($Form{'CustomField08'}){ print MAIL "$Config{'CustomFieldName08'}=$Form{'CustomField08'}\n" }
   if ($Form{'CustomField09'}){ print MAIL "$Config{'CustomFieldName09'}=$Form{'CustomField09'}\n" }
   if ($Form{'CustomField10'}){ print MAIL "$Config{'CustomFieldName10'}=$Form{'CustomField10'}\n" }

    print MAIL "\n"; 
    print MAIL "[ContSupp]\n";

 if ($Form{'Email'}) { print MAIL "cs1_ContSupRef=$Form{'Email'}\n"; 
                       print MAIL "cs1_Contact=E-mail Address\n";
                       print MAIL "cs1_RecType=P\n" }

 if ($Form{'WebSite'}) { print MAIL "cs2_ContSupRef=$Form{'WebSite'}\n"; 
                         print MAIL "cs2_Contact=Web Site\n";
                         print MAIL "cs2_RecType=P\n" }

 if ($Form{'Contact2'}) { print MAIL "cs3_RecType=C\n"; 
                         print MAIL "cs3_Contact=$Form{'Contact2'}\n";
                         print MAIL "cs3_Title=$Form{'C2_Title'}\n";
                         print MAIL "cs3_Address1=$Form{'C2_Address1'}\n";
                         print MAIL "cs3_Address2=$Form{'C2_Address2'}\n";
                         print MAIL "cs3_City=$Form{'C2_City'}\n";
                         print MAIL "cs3_State=$Form{'C2_State'}\n";
                         print MAIL "cs3_Zip=$Form{'C2_Zip'}\n";
                         print MAIL "cs3_Country=$Form{'C2_Country'}\n";
                         print MAIL "cs3_Phone=$Form{'C2_Phone'}\n";
                         print MAIL "cs3_Ext=$Form{'C2_Ext'}\n";
                         print MAIL "cs3_Fax=$Form{'C2_Fax'}\n";
                         print MAIL "cs3_Dear=$Form{'C2_Dear'}\n";
                         print MAIL "cs3_Notes=$Form{'C2_Notes'}\n"}


if ($Config{'ProfDesc01'}) { print MAIL "cs4_ContSupRef=$Form{'Profile01'}\n"; 
                             print MAIL "cs4_Title=$Form{'P1Title'}\n";
                             print MAIL "cs4_LinkAcct=$Form{'P1LinkAcct'}\n";
                             print MAIL "cs4_Country=$Form{'P1Country'}\n";
                             print MAIL "cs4_Zip=$Form{'P1Zip'}\n";
                             print MAIL "cs4_Ext=$Form{'P1Ext'}\n";
                             print MAIL "cs4_State=$Form{'P1State'}\n";
                             print MAIL "cs4_Address1=$Form{'P1Address1'}\n";
                             print MAIL "cs4_Address2=$Form{'P1Address2'}\n";
                          print MAIL "cs4_Contact=$Config{'ProfDesc01'}\n";
                          print MAIL "cs4_RecType=P\n" }
if ($Config{'ProfDesc02'}) { print MAIL "cs5_ContSupRef=$Form{'Profile02'}\n"; 
                             print MAIL "cs5_Title=$Form{'P2Title'}\n";
                             print MAIL "cs5_LinkAcct=$Form{'P2LinkAcct'}\n";
                             print MAIL "cs5_Country=$Form{'P2Country'}\n";
                             print MAIL "cs5_Zip=$Form{'P2Zip'}\n";
                             print MAIL "cs5_Ext=$Form{'P2Ext'}\n";
                             print MAIL "cs5_State=$Form{'P2State'}\n";
                             print MAIL "cs5_Address1=$Form{'P2Address1'}\n";
                             print MAIL "cs5_Address2=$Form{'P2Address2'}\n";
                          print MAIL "cs5_Contact=$Config{'ProfDesc02'}\n";                         
                          print MAIL "cs5_RecType=P\n" }
if ($Config{'ProfDesc03'}) { print MAIL "cs6_ContSupRef=$Form{'Profile03'}\n"; 
                             print MAIL "cs6_Title=$Form{'P3Title'}\n";
                             print MAIL "cs6_LinkAcct=$Form{'P3LinkAcct'}\n";
                             print MAIL "cs6_Country=$Form{'P3Country'}\n";
                             print MAIL "cs6_Zip=$Form{'P3Zip'}\n";
                             print MAIL "cs6_Ext=$Form{'P3Ext'}\n";
                             print MAIL "cs6_State=$Form{'P3State'}\n";
                             print MAIL "cs6_Address1=$Form{'P3Address1'}\n";
                             print MAIL "cs6_Address2=$Form{'P3Address2'}\n";
                          print MAIL "cs6_Contact=$Config{'ProfDesc03'}\n";
                          print MAIL "cs6_RecType=P\n" }
if ($Config{'ProfDesc04'}) { print MAIL "cs7_ContSupRef=$Form{'Profile04'}\n"; 
                             print MAIL "cs7_Title=$Form{'P4Title'}\n";
                             print MAIL "cs7_LinkAcct=$Form{'P4LinkAcct'}\n";
                             print MAIL "cs7_Country=$Form{'P4Country'}\n";
                             print MAIL "cs7_Zip=$Form{'P4Zip'}\n";
                             print MAIL "cs7_Ext=$Form{'P4Ext'}\n";
                             print MAIL "cs7_State=$Form{'P4State'}\n";
                             print MAIL "cs7_Address1=$Form{'P4Address1'}\n";
                             print MAIL "cs7_Address2=$Form{'P4Address2'}\n";
                          print MAIL "cs7_Contact=$Config{'ProfDesc04'}\n";
                          print MAIL "cs7_RecType=P\n" }
if ($Config{'ProfDesc05'}) { print MAIL "cs8_ContSupRef=$Form{'Profile05'}\n"; 
                             print MAIL "cs8_Title=$Form{'P5Title'}\n";
                             print MAIL "cs8_LinkAcct=$Form{'P5LinkAcct'}\n";
                             print MAIL "cs8_Country=$Form{'P5Country'}\n";
                             print MAIL "cs8_Zip=$Form{'P5Zip'}\n";
                             print MAIL "cs8_Ext=$Form{'P5Ext'}\n";
                             print MAIL "cs8_State=$Form{'P5State'}\n";
                             print MAIL "cs8_Address1=$Form{'P5Address1'}\n";
                             print MAIL "cs8_Address2=$Form{'P5Address2'}\n";
                          print MAIL "cs8_Contact=$Config{'ProfDesc05'}\n";
                          print MAIL "cs8_RecType=P\n" }
if ($Config{'ProfDesc06'}) { print MAIL "cs9_ContSupRef=$Form{'Profile06'}\n"; 
                             print MAIL "cs9_Title=$Form{'P6Title'}\n";
                             print MAIL "cs9_LinkAcct=$Form{'P6LinkAcct'}\n";
                             print MAIL "cs9_Country=$Form{'P6Country'}\n";
                             print MAIL "cs9_Zip=$Form{'P6Zip'}\n";
                             print MAIL "cs9_Ext=$Form{'P6Ext'}\n";
                             print MAIL "cs9_State=$Form{'P6State'}\n";
                             print MAIL "cs9_Address1=$Form{'P6Address1'}\n";
                             print MAIL "cs9_Address2=$Form{'P6Address2'}\n";
                          print MAIL "cs9_Contact=$Config{'ProfDesc06'}\n";
                          print MAIL "cs9_RecType=P\n" }
if ($Config{'ProfDesc07'}) { print MAIL "cs10_ContSupRef=$Form{'Profile07'}\n"; 
                             print MAIL "cs10_Title=$Form{'P7Title'}\n";
                             print MAIL "cs10_LinkAcct=$Form{'P7LinkAcct'}\n";
                             print MAIL "cs10_Country=$Form{'P7Country'}\n";
                             print MAIL "cs10_Zip=$Form{'P7Zip'}\n";
                             print MAIL "cs10_Ext=$Form{'P7Ext'}\n";
                             print MAIL "cs10_State=$Form{'P7State'}\n";
                             print MAIL "cs10_Address1=$Form{'P7Address1'}\n";
                             print MAIL "cs10_Address2=$Form{'P7Address2'}\n";
                          print MAIL "cs10_Contact=$Config{'ProfDesc07'}\n";
                          print MAIL "cs10_RecType=P\n" }
if ($Config{'ProfDesc08'}) { print MAIL "cs11_ContSupRef=$Form{'Profile08'}\n"; 
                             print MAIL "cs11_Title=$Form{'P8Title'}\n";
                             print MAIL "cs11_LinkAcct=$Form{'P8LinkAcct'}\n";
                             print MAIL "cs11_Country=$Form{'P8Country'}\n";
                             print MAIL "cs11_Zip=$Form{'P8Zip'}\n";
                             print MAIL "cs11_Ext=$Form{'P8Ext'}\n";
                             print MAIL "cs11_State=$Form{'P8State'}\n";
                             print MAIL "cs11_Address1=$Form{'P8Address1'}\n";
                             print MAIL "cs11_Address2=$Form{'P8Address2'}\n";
                          print MAIL "cs11_Contact=$Config{'ProfDesc08'}\n";
                          print MAIL "cs11_RecType=P\n" }
if ($Config{'ProfDesc09'}) { print MAIL "cs12_ContSupRef=$Form{'Profile09'}\n"; 
                             print MAIL "cs12_Title=$Form{'P9Title'}\n";
                             print MAIL "cs12_LinkAcct=$Form{'P9LinkAcct'}\n";
                             print MAIL "cs12_Country=$Form{'P9Country'}\n";
                             print MAIL "cs12_Zip=$Form{'P9Zip'}\n";
                             print MAIL "cs12_Ext=$Form{'P9Ext'}\n";
                             print MAIL "cs12_State=$Form{'P9State'}\n";
                             print MAIL "cs12_Address1=$Form{'P9Address1'}\n";
                             print MAIL "cs12_Address2=$Form{'P9Address2'}\n";
                          print MAIL "cs12_Contact=$Config{'ProfDesc09'}\n";
                          print MAIL "cs12_RecType=P\n" }
if ($Config{'ProfDesc10'}) { print MAIL "cs13_ContSupRef=$Form{'Profile10'}\n"; 
                             print MAIL "cs13_Title=$Form{'P10Title'}\n";
                             print MAIL "cs13_LinkAcct=$Form{'P10LinkAcct'}\n";
                             print MAIL "cs13_Country=$Form{'P10Country'}\n";
                             print MAIL "cs13_Zip=$Form{'P10Zip'}\n";
                             print MAIL "cs13_Ext=$Form{'P10Ext'}\n";
                             print MAIL "cs13_State=$Form{'P10State'}\n";
                             print MAIL "cs13_Address1=$Form{'P10Address1'}\n";
                             print MAIL "cs13_Address2=$Form{'P10Address2'}\n";
                          print MAIL "cs13_Contact=$Config{'ProfDesc10'}\n";
                          print MAIL "cs13_RecType=P\n" }

    close (MAIL);
}



sub check_email {
    # Initialize local email variable with input to subroutine.              #
    $email = $_[0];

    # If the e-mail address contains:                                        #
    if ($email =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)/ ||

        # the e-mail address contains an invalid syntax.  Or, if the         #
        # syntax does not match the following regular expression pattern     #
        # it fails basic syntax verification.                                #

        $email !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$/) {

        # Basic syntax requires:  one or more characters before the @ sign,  #
        # followed by an optional '[', then any number of letters, numbers,  #
        # dashes or periods (valid domain/IP characters) ending in a period  #
        # and then 2 or 3 letters (for domain suffixes) or 1 to 3 numbers    #
        # (for IP addresses).  An ending bracket is also allowed as it is    #
        # valid syntax to have an email address like: user@[255.255.255.0]   #

        # Return a false value, since the e-mail address did not pass valid  #
        # syntax.                                                            #
        return 0;
    }

    else {

        # Return a true value, e-mail verification passed.                   #
        return 1;
    }
}

sub body_attributes {
    # Check for Background Color
    if ($Config{'bgcolor'}) { print " bgcolor=\"$Config{'bgcolor'}\"" }

    # Check for Background Image
    if ($Config{'background'}) { print " background=\"$Config{'background'}\"" }

    # Check for Link Color
    if ($Config{'link_color'}) { print " link=\"$Config{'link_color'}\"" }

    # Check for Visited Link Color
    if ($Config{'vlink_color'}) { print " vlink=\"$Config{'vlink_color'}\"" }

    # Check for Active Link Color
    if ($Config{'alink_color'}) { print " alink=\"$Config{'alink_color'}\"" }

    # Check for Body Text Color
    if ($Config{'text_color'}) { print " text=\"$Config{'text_color'}\"" }

}

#

sub send_courtesy {
  if ($Config{'courtesy_reply'} && $Form{'Email'})
 { 
   open (MAIL,"|$mailprog -t");
   print MAIL "To: $Form{'Email'} ($Form{'Name'})\n";
   print MAIL "From: $Config{'courtesy_our_email'}\n";

   if ($Config{'subject'}) {
      print MAIL "Subject: Thanks for your $Config{'subject'}\n\n";
      $subjflag = 1;
   }
   else {
      print MAIL "Subject: Thank you - $date\n\n";
      $subjflag = 0;
   }
   print MAIL "On $date you responded to ";
   if ( $subjflag ) {
      print MAIL "our\n`$Config{'subject'}` form.\n\n";
   }
   else {
      print MAIL "a WWW  form.\n\n";
   }

     print MAIL "-" x 75 . "\n\n";

  
   
    # Sort alphabetically if specified:  
    undef %is_exclude;
for (@Exclude) { $is_exclude{$_} = 1 }                                    #
    if ($Config{'sort'} eq 'alphabetic') {
        foreach $field (sort keys %Form) {

            # If the field has a value or the print blank fields option      #
            # is turned on, print out the form field and value.              #
            if ($Config{'print_blank_fields'} || $Form{$field} ||
                $Form{$field} eq '0') {
                print MAIL "$field: $Form{$field}\n"  unless $is_exclude{$field};
            }
        }
    }

    # If a sort order is specified, sort the form fields based on that.      #
    elsif ($Config{'sort'} =~ /^order:.*,.*/) {

        # Remove extraneous line breaks and spaces, remove the order:        #
        # directive and split the sort fields into an array.                 #
        $Config{'sort'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
        $Config{'sort'} =~ s/(\s+)?\n+(\s+)?//g;
        $Config{'sort'} =~ s/order://;
        @sorted_fields = split(/,/, $Config{'sort'});

        # For each sorted field, if it has a value or the print blank        #
        # fields option is turned on print the form field and value.         #
        foreach $sorted_field (@sorted_fields) {
            if ($Config{'print_blank_fields'} || $Form{$sorted_field} ||
                $Form{$sorted_field} eq '0') {
                print MAIL "$sorted_field: $Form{$sorted_field}\n"  unless $is_exclude{$sorted_field};
            }
        }
    }

    # Otherwise, default to the order in which the fields were sent.         #
    else {

        # For each form field, if it has a value or the print blank          #
        # fields option is turned on print the form field and value.         #
        foreach $field (@Field_Order) {
            if ($Config{'print_blank_fields'} || $Form{$field} ||
                $Form{$field} eq '0') {
                print MAIL "$field: $Form{$field}\n"   unless $is_exclude{$field};
            }
        }
    }

    print MAIL "-" x 75 . "\n\n";

   if ($Config{'courtesy_reply_texta'}) {
      print MAIL "$Config{'courtesy_reply_texta'}\n";
   }
   if ($Config{'courtesy_reply_textb'}) {
      print MAIL "$Config{'courtesy_reply_textb'}\n\n";
   }
   print MAIL "Regards,\n";

if ($Config{'courtesy_who_we_are'}) {
   print MAIL "$Config{'courtesy_who_we_are'}\n";
}
if ($Config{'courtesy_who_we_are2'}) {
   print MAIL "$Config{'courtesy_who_we_are2'}\n";
}
if ($Config{'courtesy_our_email'}) {
   print MAIL "$Config{'courtesy_our_email'}\n";
}
if ($Config{'courtesy_our_url'}) {
   print MAIL "$Config{'courtesy_our_url'}\n";
}
   close (MAIL);
}
}




sub lockit
{
  local ($endtime);                                   
  $endtime = 60;                                      
  $endtime = time + $endtime;                         
  while (-e $lock_file && time < $endtime) 
   {
    # Do Nothing                                    
   }                                                   
   open(LOCK_FILE, ">$lock_file");                     
}


 



#######################################################################

sub unlockit
{
  close($lock_file);
  unlink($lock_file);
}


#######################################################################
sub file_open_error
  {
  local ($bad_file, $script_section, $this_file, $line_number) = @_;
  print "Content-type: text/html\n\n";
  &CgiDie ("I am sorry, but I was not able to access $bad_file.")
  }     



sub error { 
    # Localize variables and assign subroutine input.                        #
    local($error,@error_fields) = @_;
    local($host,$missing_field,$missing_field_list);

    if ($error eq 'bad_referer') {
        if ($ENV{'HTTP_REFERER'} =~ m|^https?://([\w\.]+)|i) {
            $host = $1;
            print <<"(END ERROR HTML)";
Content-type: text/html

<html>
 <head>
  <title>Bad Referrer - Access Denied</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>
  <center>
  <BR>
  <BR>
  <table  border=1 cellpadding=0 cellspacing=0 width=650>
      <tr><td>
          <table   border=0 cellpadding=2 cellspacing=0 width=650>
               <tr>
               <td colspan=3 align=center bgcolor=#333366><font face=arial size=+2 color=#FFFFFF><b>
              Bad Referrer - Access Denied</b></td></tr>
                <tr>
                <td width=150>
               </td><td bgcolor=#FFFFFF><font face=arial> <BR>                                
                    The form attempting to use <br><a href="http://casjaysdev.com">CasjaysDev.com FormMail</a>
                     resides at <tt>$ENV{'HTTP_REFERER'}</tt>, which is not allowed to access
                     this cgi script.<p> If you are attempting to configure CasjaysDev.com FormMail to run with this form, you need
                      to add the following to \@referers, explained in detail in the README file.<p>
                      Add <tt>'$host'</tt> to your <tt><b>\@referers</b></tt> array.<br>
                </td>
                <td width=150>
                </td></tr><tr><td colspan=3><br></td></tr>
                <tr><td colspan=3 align=center bgcolor=#C0C0C0>
                <font face=arial size=-2>
                <a href="javascript: history.go(-1)">Go Back</a><br>
                <a href="http://casjaysdev.com">CasjaysDev.com</a>
                </td>
                </tr>
          </table>
       </td></tr>
   </table>
  </center>
 </body>
</html>
(END ERROR HTML)
        }
        else {
            print <<"(END ERROR HTML)";
Content-type: text/html

<html>
 <head>
  <title>CasjaysDev.com FormMail</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>
  <center>
  <BR>
  <BR>
  <table  border=1 cellpadding=0 cellspacing=0 width=650>
      <tr><td>
          <table   border=0 cellpadding=2 cellspacing=0 width=650>
               <tr>
               <td colspan=3 align=center bgcolor=#333366><font face=arial size=+2 color=#FFFFFF><b>
              CasjaysDev Formail
              </b></td></tr>
                <tr>
                <td width=150>
               </td>
                <td width=150>
                </td></tr><tr><td colspan=3><br></td></tr>
                <tr><td colspan=3 align=center bgcolor=#C0C0C0>
                <font face=arial size=-2>
                <a href="javascript: history.go(-1)">Go Back</a>
                <br><a href="http://casjaysdev.com">CasjaysDev.com</a>
                </td>
                </tr>
          </table>
       </td></tr>
   </table>
  </center>
 </body>
</html>
(END ERROR HTML)
        }
    }

    elsif ($error eq 'request_method') {
            print <<"(END ERROR HTML)";
Content-type: text/html

<html>
 <head>
  <title>Error: Request Method</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>
  <center>
  <BR>
  <BR>
  <table  border=1 cellpadding=0 cellspacing=0 width=650>
      <tr><td>
          <table   border=0 cellpadding=2 cellspacing=0 width=650>
               <tr>
               <td colspan=3 align=center bgcolor=#333366><font face=arial size=+2 color=#FFFFFF><b>
              Error: Request Method</b></td></tr>
                <tr>
                <td width=150>
               </td><td bgcolor=#FFFFFF><font face=arial> <BR>                                
                    The Request Method of the Form you submitted did not match
     either <tt>GET</tt> or <tt>POST</tt>.  Please check the form and make sure the
     <tt>method=</tt> statement is in upper case and matches <tt>GET</tt> or <tt>POST</tt>.<p>
                </td>
                <td width=150>
                </td></tr><tr><td colspan=3><br></td></tr>
                <tr><td colspan=3 align=center bgcolor=#C0C0C0>
                <font face=arial size=-2>
                <a href="javascript: history.go(-1)">Go Back</a><br>
                <a href="http://casjaysdev.com">CasjaysDev.com</a>
                </td>
                </tr>
          </table>
       </td></tr>
   </table>
  </center>
 </body>
</html>
(END ERROR HTML)
    }

    elsif ($error eq 'no_recipient') {
            print <<"(END ERROR HTML)";
Content-type: text/html

<html>
 <head>
  <title>No Recipient</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>
  <center>
  <BR>
  <BR>
  <table  border=1 cellpadding=0 cellspacing=0 width=650>
      <tr><td>
          <table   border=0 cellpadding=2 cellspacing=0 width=650>
               <tr>
               <td colspan=3 align=center bgcolor=#333366><font face=arial size=+2 color=#FFFFFF><b>
              Error: No Recipient</b></td></tr>
                <tr>
                <td width=150>
               </td><td bgcolor=#FFFFFF><font face=arial> <BR> No Recipient was specified in the data sent to CasjaysDev.com FormMail.  Please
     make sure you have filled in the 'recipient' form field with an e-mail
     address.  More information on filling in recipient form fields can be
     found in the README file.<p>
                </td>
                <td width=150>
                </td></tr><tr><td colspan=3><br></td></tr>
                <tr><td colspan=3 align=center bgcolor=#C0C0C0>
                <font face=arial size=-2>
                <a href="javascript: history.go(-1)">Go Back</a><br>
                <a href="http://casjaysdev.com">CasjaysDev.com</a>
                </td>
                </tr>
          </table>
       </td></tr>
   </table>
  </center>
 </body>
</html>
(END ERROR HTML)
    }

    elsif ($error eq 'missing_fields') {
        if ($Config{'missing_fields_redirect'}) {
            print "Location: $Config{'missing_fields_redirect'}\n\n";
        }
        else {
            foreach $missing_field (@error_fields) {
                $missing_field_list .= "      <li>$missing_field\n";
            }

            print <<"(END ERROR HTML)";
Content-type: text/html

<html>
 <head>
  <title>Error: Blank Fields</title>
 </head>
 <body bgcolor=#FFFFFF text=#000000>
  <center>
  <BR>
  <BR>
  <table  border=1 cellpadding=0 cellspacing=0 width=650>
      <tr><td>
          <table   border=0 cellpadding=2 cellspacing=0 width=650>
               <tr>
               <td colspan=3 align=center bgcolor=#333366><font face=arial size=+2 color=#FFFFFF><b>
              Error: Blank Fields</b></td></tr>
                <tr>
                <td width=150>
               </td><td bgcolor=#FFFFFF><font face=arial> <BR>                                
                    The following fields were left blank in your submission form:<p>
     <ul>
$missing_field_list
     </ul><br>

     These fields must be filled in before you can successfully submit the form.<p>
     Please use your browser's back button to return to the form and try again.
                </td>
                <td width=150>
                </td></tr><tr><td colspan=3><br></td></tr>
                <tr><td colspan=3 align=center bgcolor=#C0C0C0>
                <font face=arial size=-2>
                <a href="javascript: history.go(-1)">Go Back</a><br>
                <a href="http://casjaysdev.com">CasjaysDev.com</a>
                </td>
                </tr>
          </table>
       </td></tr>
   </table>
  </center>
 </body>
</html>
(END ERROR HTML)
        }
    }
    exit;
}
